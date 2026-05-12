# ADR-0003: 文献资产 Schema v1 (混合架构: 本地数据 + 商业判断)

## 日期
2026-05-11

## 状态
Accepted (Week 4 重评)

## 背景

Week 1 Day 1 做了 3 件事:
1. 用户提出 5 层 30 字段文献处理 SOP (ADR-0002 输入)
2. 提供综述纲要 (corpus/outline/review_outline.md, 580 行)
3. SOP 实测 P5 论文得到分级 (results/sop_test_p5_analysis.md)

实测结论:
- 本地 14B 在事实抽取上 A 级 (可用)
- 在评分 / 章节定位上 C-D 级 (不可用)
- 用户做出新决策: 引入商业模型层补判断能力
- 库规模: 300+ 篇 (远超 project_brief 写的 50 篇)

## 决策

采用三层 schema + 混合产出。

Schema 顶层结构 (示意, 完整版见下文):

    metadata.json
        id_block            -- 论文标识 + 内容 hash (去重核心)
        source_block        -- 来源信息 (作者/期刊/DOI 等)
        factual             -- 本地 LLM 抽取 (A 级可信)
        interpretive        -- 本地 + 商业 LLM 协作
        personal_relevance  -- 本地候选 + 商业 / 人工确认
        assets              -- 资产路径 (figures/, tables/, chunks.jsonl)
        provenance          -- 每个字段的产生记录


## 字段产出策略

| 字段类 | 子字段 | 产出方 | 重跑代价 |
|---|---|---|---|
| id_block | doc_id, content_hash, filename | 自动 (sha256) | 一次终身 |
| source_block | title, authors, doi, journal, year | LLM 抽 + 人工 review | 低 |
| factual | background, concepts, pitfalls, objectives, metrics, motivation | 本地 LLM-auto | 低 |
| factual | core_problem, technical_difficulties, methods (实验/分析/验证) | 本地 LLM-auto | 低 |
| interpretive | claims_vs_evidence_gap | 本地 LLM + 人工抽检 | 中 |
| interpretive | writing_techniques | 本地 LLM | 低 |
| interpretive | scoring_10_dim | 商业模型 (Sonnet/GPT 候选) | 高 |
| interpretive | position_label | 商业模型 | 高 |
| interpretive | strengths_and_limitations | 商业模型 | 中 |
| personal_relevance | review_section_top3 | 本地 LLM 候选 | 低 |
| personal_relevance | review_section_final | 商业模型 + 人工确认 | 中 |
| personal_relevance | argument_support | 商业模型 + 人工 | 中 |
| personal_relevance | borrow_insight | 本地 LLM | 低 |

position_label 取值: intensive_read / supporting / supplementary / low

## 去重设计 (回应"避免重复"需求)

- doc_id = sha256(pdf_bytes)[:16], 同一 PDF 始终同一 id
- 文件名仅作展示, 不作主键
- 同一论文不同版本 (preprint vs published): 用 doi 字段作 group_id
- inbox/ 监听: 入库前 hash 比对, 已存在则跳过
- 同一 doc_id + 同一 prompt_version 不重复调用 LLM (cache)


## Provenance 字段 (强制必备)

每个非 id_block 字段都必须有 _meta 子对象, 包含:

- value           : 字段值本身
- produced_by     : qwen2.5-14b-8k / claude-sonnet-4.6 / human-wei / paperqa-agent
- prompt_version  : v1.0 (锁定 prompt 的版本, 改 prompt 必升号)
- produced_at     : ISO8601 timestamp
- reviewed_by     : null 或 human-wei
- reviewed_at     : null 或 timestamp
- cost_usd        : 仅商业 API 字段需记
- evidence        : 引文片段列表 (含页码)

JSON 形式示意 (用缩进表达):

    "background":
        "value": "..."
        "_meta":
            "produced_by": "qwen2.5-14b-8k"
            "prompt_version": "v1.0"
            "produced_at": "2026-05-11T20:00:00Z"
            "reviewed_by": null
            "evidence": ["pages 14-15", "abstract"]

## 商业模型层

- 接口: 通过 LiteLLM 统一封装 (paper-qa 已经依赖, 复用)
- 模型选择: 推迟到 ADR-0004 (本周内决定)
  候选: Claude Sonnet 4.6 ($3/$15) / GPT-5.4 ($1.75/$14) / DeepSeek (国产备选)
- 数据出境: 用户已授权; 只发送本地 factual 抽取结果, 不发送原始 PDF
- Cache 策略: 同一 doc_id + 同一 prompt_version 不重复调用
- 可关闭: 商业 API key 缺失时, 系统降级到纯本地 (失去 scoring 等高级字段, 核心可用)
- 成本预算: 300 篇全库一次商业判断 ~$15-30 (Sonnet 4.6), 不是瓶颈


## 备选方案 (留档)

- A: 全本地 (违反实测结论, 否决)
- B: 全商业 (违反 ADR-0001 全本地数据底座原则, 否决)
- C: 混合 (本采纳)
- D: 双套 schema 并行 (复杂度过高, 否决)

## 何时重新评估 (写 ADR-0005 触发条件)

满足任一即触发:
- Week 4 实测 50 篇后, 任一 A 级字段质量不达标
- 商业 API 成本超过 $100 / 月
- 商业模型选择改变 (DeepSeek 国产化等)
- 用户对 SOP 字段需求变化 (增删字段超 5 个)
- 库规模超过 1000 篇 (schema 需要适应大规模)

## 影响

- chunks.jsonl 设计 (Week 2 任务): 必须含 doc_id + page + bbox + chunk_type
- paper.md 设计: 必须含 doc_id 关联, 不能是孤立 markdown
- Week 2-3 工作量翻倍: schema 实现 + provenance 系统 + 商业 API 集成
- Week 5-6 综述写作辅助层: 必须能用 personal_relevance 字段定位章节
- 跨批次一致性: schema v1 锁定后, 即使 v2 更新也要保证 v1 数据可读
- ADR-0001 (Ollama-only) 局部修订: 允许商业 API 用于判断层

## Week 1 后续行动

- ADR-0004 (本周内): 选定商业模型 + 实测一两次 P5 评分对比
- Week 2 启动: 实现 schema v1 的 JSON 格式 + provenance 写入工具
- Week 2 启动: 实现 doc_id hash 与 inbox/ 监听
