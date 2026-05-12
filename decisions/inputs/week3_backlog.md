
## Schema v2: 通用文献提取信息类(基于用户 Excel 表格经验)

**背景**:
用户(Wei)有三个长期维护的 Excel 文献数据库,字段在三主题(bioprinting / 股骨柄 / 光响应涂层)间高度一致,表明已收敛出可复用 schema. 41 个 unique 字段归为 8 类.

**两层评估架构**(从 Excel 抽取):
- Layer 1: 网页级快筛(accessibility A/B/C + /49 分 + recommendation),不读全文
- Layer 2: 全文深度入库(summary/contribution/limitation/review_use),读完后填

**Schema v2 字段类别**:
A. Identity / B. Bibliographic / C. Discovery & Access / D. Classification (multi-label) / E. Content Extraction / F. Critical Assessment / G. Workflow / H. Writing Use / I. Provenance

**跟 Schema v1 的关系**:
- v1 = LLM 自动抽取 raw text 块(给检索 + LLM 合成用)
- v2 = v1 + 人工策划的决策字段(给综述写作用)
- v1 是 v2 的 subset

**实施**: Week 3 Day 3-4 处理. 不破坏 v1, 用 schema_v2 builder 把 v1 metadata 包成 v2 + 留人工字段空位.

**导出**: 可一键导出 Excel(对应你现有 Main_DB 格式)+ JSON + Markdown report.

## Pipeline 稳定性:Docling 内存泄漏修复

**问题**:Week 2 Day 4 bioprinting batch ingest 跑 12 小时后,Python 进程 VRAM 从
1.3 GB 涨到 6.85 GB(每篇泄漏 ~130 MB),挤占 ollama 导致 qwen 17/49 层 CPU
offload,SOP_v2 单任务从 90s 退化到 200-400s.

P42 已经出现 SOP L1_factual_background 超时失败(只缺一个字段,其他 stage 都成).

**根因**:每篇调 docling.DocumentConverter() 时加载 RapidOCR 模型,用完未
显式释放. Python GC 不知道这是 GPU-allocated.

**修复方案**(Week 3 Day 1 优先做):
1. ingest_one() 加 try/finally,每篇结束显式:
   - converter = None
   - import gc; gc.collect()
   - import torch; torch.cuda.empty_cache() (如果用 torch)
2. 或者:在 ingest.py 主循环里, 每篇 ingest 跑成 subprocess(隔离内存)
   - 优点: 完全杜绝泄漏
   - 缺点: 每篇启动 Python 解释器 + Docling 初始化 ~5s 开销

**临时缓解**(Week 2 Day 4 已用):
- 每跑 40-50 篇手动重启 tmux ingest + ollama(本次 10:23 已执行)

**P42 修复**: `ingest.py --force inbox/<P42_doc_id>.pdf` 重跑该篇
(等 bioprinting 全跑完后批量补).

## 紧急: SOP_v2 输出污染清理(Week 3 Day 1)

**问题**: 抽样审 P7/P11/P25/P40/P43 metadata 发现所有字段都带 LLM
conversational filler 前缀,污染严重:

- "Based on the provided research paper, here are the extracted sections:"
- "Certainly! Here are the extracted sections..."
- 各篇 markdown 格式不一致 (### vs ** vs 1. )
- LLM 编造 "Page 2:" 这种它根本不知道的页码

**影响**: 综述写作 / 检索 / Excel 导出都被污染.
P43 等 metadata 实际有用内容只占 70-80%.

**修复(Week 3 Day 1)**:
1. 改 SOP_v2 prompt,加 CRITICAL FORMAT RULES:
   - NO preamble, NO greeting
   - NO markdown headers (###, **)
   - NO fabricated page numbers
   - Plain prose only
2. 在 5 篇黄金集 force re-ingest 对比新旧输出质量
3. 如果改善明显, --force 重跑所有 P1-P{当前最后} 篇 (~14 小时机器时)
4. 写 ADR-0007: SOP_v2 prompt hardening

**优先级**: 极高. Schema v2 落地的前置条件.

## 知识库 token 加权分配(Tier A/B/C)

**核心思想**: 200K context 内, 不平均分配每篇 paper 的 tokens,
而是按"对当前综述的价值"分档:
- Tier A (top 15%, ~15-20 篇): 完整 metadata + 3-5 chunks, ~5500 tokens/篇
- Tier B (next 25%, ~30 篇): 完整 metadata + 1 chunk, ~1800 tokens/篇
- Tier C (其余 ~80 篇): 一行摘要, ~250 tokens/篇

总预算 ~160K tokens, 留 40K 给对话和输出.

**评分维度**:
- SOP 自动评分 (interpretive.scoring_10_dim_local, 平均 0-10)
- 人工评分 (Schema v2 assessment.human_score, 0-10)
- 关联度评分 (向量检索 per-section query 的 max sim, 转 0-10)

**综合分**: w1 * sop + w2 * human + w3 * relevance
初始 w 推荐: 0.3 / 0.4 / 0.3 (可调)

**关键特性**:
- 分档是 **per-综述** 重算的, query 变就重排
- Tier C 不丢弃, 压缩成一行摘要让 Claude 知道存在
- Tier A 内容可继续细分 A1/A2 (5-8 篇核心证据 vs 8-12 篇支持例子, Week 5+)

**新脚本**: export_library_tiered.py
- 输入: list of section queries + tier budgets + target_tokens
- 输出: results/{review_name}/library_tiered.txt + scoring_report.json

**前置依赖**:
- SOP_v2 prompt 清洗 (Week 3 Day 1)
- Schema v2 human_score 字段 (Week 3 Day 3-5)
- Chroma 检索 API 改造为支持 query-many-papers (返回 124 个 paper 的 max sim)


## Week 3 执行顺序(已确认)

**Day 1**: SOP_v2 prompt 清洗(阻塞所有下游)
- 改 prompt: 加 CRITICAL FORMAT RULES
- 5 黄金集 force re-ingest 对比
- 通过后 --force 重跑全部 124 (~14 小时机器时)

**Day 2**: export_library_tiered.py (Tier A/B/C 分档导出)
- 接受 outline queries 作为输入
- 评分: 0.3 * SOP + 0.4 * human + 0.3 * relevance
- 输出 results/{review}/library_tiered.txt + scoring_report.json
- 用清洗后的 metadata 测试, 看分档跟直觉是否对齐
- 调权重 / query, 收敛

**Day 3-5**: Schema v2 (整合用户研究模板)
- schema_v2_builder.py: 自动层 (SOP_v2) + 人工层 (why_included, writing_use 等)
- Day 4: 用户用模板手填 5 篇黄金集 P1-P5
- Day 5: export_to_excel.py + writing_use 字段进 library_tiered Tier A 段

**Day 6-7**: 综述写作流程 dry run
- 用 5 篇黄金集 + tier 化知识库
- Session 1-6 走一遍, 验证整个工作流
- 记录哪里不顺, 后续修

