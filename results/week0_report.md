# Week 0 现实校准报告

**日期**: 2026-05-10 (Day 1-2)
**位置**: Phase 0 终点
**Author**: Weikang Sun
**状态**: 完成

---

## 1. Week 0 目的

Week 0 不是"建系统",是"摸清状况"——回答三个问题:

1. PaperQA2 + 本地 LLM 够不够用?
2. 我的真实论文都长什么样?
3. 我每周能投入多少时间?

输出决定 Week 1 怎么走,Week 4 怎么决策 Path A vs Path B。

---

## 2. 完成的硬指标

| 项 | 状态 |
|---|---|
| 装 PaperQA2 | OK paper-qa 2026.3.18, uv venv 隔离 |
| 喂 5 篇代表论文 | OK 都是 AI + 生物打印综述, 原生 PDF |
| 准备 5 个真实研究问题 | OK 事实确认型, 覆盖 bioink/realtime/biological/robotic/clinical 五维 |
| PaperQA2 5 问跑通 | OK Mode B 跨文档 5/5 + Mode A 逐篇 25/25 (其中 9 真答案) |
| Khoj 对照 | 未跑, 推迟到 Week 1 后期 |
| 30 篇版面分布统计 | 未做, 推迟到 Week 3 (用真实批处理数据反推) |

未完成的两项不影响主线决策, 推后处理。

---

## 3. 关键发现

### 3.1 PaperQA2 + 本地小模型可以工作

经过 v1 到 v7 七版调优后, 达成的可工作配置:

    LLM        : ollama/qwen2.5-14b-8k (Modelfile 锁定 num_ctx=8192)
    Embedding  : ollama/nomic-embed-text
    PaperQA    : use_doc_details=False, multimodal=False
                 recurse_subdirectories=False
                 rebuild_index=False, sync_with_paper_directory=False
                 paper_directory = 绝对路径
    Index      : paper-qa 内置 Tantivy, 7.5 MB

性能 (5 篇论文, 30 题):
- Mode B 跨文档: 平均 59.5 秒/题
- Mode A 逐篇: 平均 47.5 秒/题
- 0 重试, 0 失败
- 答案带页码引用, 可点跳原文

### 3.2 PaperQA2 在逐篇事实核查场景下能力有限

Mode A 25 题里 16 题 (64%) 返回 "I cannot answer due to no papers"。

按论文统计:

| 论文 | 被找到次数/5 |
|---|---|
| P5 The Synergy of AI and 3D Bioprinting | 5/5 |
| P2 AI-driven 3D bioprinting for regenerative medicine | 2/5 |
| P3 Robotic-assisted automated in situ bioprinting | 1/5 |
| P4 Self-driving bioprinting laboratories | 1/5 |
| P1 AI for biofabrication | 0/5 |

根因猜测: PaperQA2 的 agent 用论文标题做内部检索, 标题里包含 "AI"+"bioprinting" 同时出现的论文被反复命中, 语义稍偏的 (如 P1 的 "biofabrication") 被错过。

### 3.3 PaperQA2 在跨文档综合场景下表现优秀

Mode B 5/5 全过, 每题答案都包含:
- 多个具体来源 (精确到 authorYYYYkeyword pages X-Y)
- 跨论文综合 (不只是某一篇)
- 完整 reference 列表带 DOI / 期刊 / 引用数

可直接用作综述素材。

### 3.4 隐含数据点: PaperQA2 偷偷拉了 metadata

即使设了 use_doc_details=False, 引用里仍出现 "57 citations from a peer-reviewed journal" 这类信息。说明 paper-qa 内部还有一条 metadata 抓取路径没被开关挡住。

含义: 严格"全本地零外网"目标下, paper-qa 需要再 patch。

---

## 4. 本地 LLM 栈遇到的坑 (给 Week 1 做参考)

| 坑 | 触发点 | 修法 |
|---|---|---|
| bge-m3 在某些技术文本上返回 NaN | embedding API 500 | 改 nomic-embed-text (Ollama 已知 issue #13572) |
| qwen2.5:14b 默认 4096 上下文 | 论文 chunk 被截断 | Modelfile 锁 num_ctx=8192 |
| paper-qa 默认 multimodal=True 偷调 gpt-4o | AuthError | ParsingSettings(multimodal=False) |
| paper-qa 默认 rebuild_index=True | 每次 ask 重建索引 | AgentSettings(rebuild_index=False) |
| paper-qa 默认 sync_with_paper_directory=True | 同上 | IndexSettings(sync_with_paper_directory=False) |
| 相对路径让 paper-qa 索引整个 venv | 误索引几千个 .txt | 绝对路径 + recurse_subdirectories=False |
| Semantic Scholar 429 限流 | metadata 抓取 | use_doc_details=False |

这些坑都和 Week 1 的 Windows BGE-M3 fastapi 计划无关 —— Week 1 用原生 PyTorch, 绕开 Ollama 层。

---

## 5. 时间投入校准

| 项 | 实际花费 |
|---|---|
| Day 1 (硬件+网络+Ollama+5 篇 PDF+paper-qa 装机+6 版脚本失败) | 约 5 小时 |
| Day 2 (修 embedding + 锁上下文 + v7 通过 + Mode B/A 30 题) | 约 3.5 小时 |
| Week 0 合计 | 约 8.5 小时 (分两天) |

每周可投入小时数: ____(待填)

按 8.5 小时 / Week 0 推算, Week 1-6 工作量预估:
- Week 1 环境骨架: 8-15 小时 (vLLM 上 Blackwell 可能踩坑)
- Week 2-3 单篇 + 50 篇: 15-25 小时
- Week 4 决策: 2 小时 (本周已部分预备)
- Week 5-6 生产冲刺: 25-40 小时
- 6 周总计: 60-100 小时

---

## 6. 够用清单 vs 不够用清单

### 够用
- 跨文档综合问答 (直接可用)
- 引用追溯到页码 (综述写作刚需)
- 本地 LLM 端到端跑通 (全本地目标可行)
- Modelfile 上下文调优 (num_ctx 可控)

### 不够用
- 逐篇精确检索 (64% 失败, 综述筛选场景不可用)
- 图表 RAG (用 multimodal=False 直接关了, 本是核心需求)
- 严格"零外网" (metadata 抓取还有暗路)
- 增量更新 / inbox/ 自动入库 (没测)
- Open WebUI / Obsidian 集成 (没测)
- 5 层 30 字段文献分析 SOP (ADR-0002, Week 1 处理)

### 推迟
- Khoj 对照
- 30 篇版面分布 (用 Week 3 真实批处理数据反推更准)

---

## 7. 给 Week 4 决策的初步信号

基于 Week 0 数据, Path B (PaperQA2 + patch) 需要 patch agent 检索行为 + patch 多模态 + patch metadata 抓取 + 实现 5 层 SOP。Path A (自建) 需要从零写检索 + RAG 链 + UI + SOP 流水线。

哪条工作量更小, 取决于:
1. "图表 RAG" 在 Path B 上的可 patch 程度 (Week 3 回答)
2. "5 层 SOP" schema 的产出方式 (ADR-0003, Week 1 回答)

当前倾向: Path B 不再是默认假设。PaperQA2 适合作为基准对照, 不适合作为核心数据底座。

---

## 8. Week 1 启动条件

已就绪:
- [x] Ollama-only 决策 (ADR-0001)
- [x] 本地 LLM 栈跑通 (qwen2.5-14b-8k + nomic-embed-text)
- [x] paper-qa 评估数据 (evaluation.json, 30 题)
- [x] 坑位清单 (本报告第 4 节)
- [x] SOP 留档 (ADR-0002, decisions/inputs/literature_processing_sop.md)

待办:
- [ ] vLLM 是否上 (Blackwell 兼容性, Week 1 第一道关)
- [ ] BGE-M3 fastapi on Windows (Week 1 主目标)
- [ ] Qdrant 容器 (Week 1 主目标)
- [ ] 文献资产 schema 重审 (ADR-0003, Week 1 Day 1)

---

## 9. 不变项 vs 调整项

不变:
- 总目标 (写更好的综述)
- 六周框架
- 数据驱动 + 决策留痕
- "能借不建" 原则

调整:
- Week 0 输出 30 题对照, Week 4 决策依据从"模糊评估"变成"具体数据"
- PaperQA2 从"默认底层"降级为"基准对照"
- Week 5-6 准备分配更多时间给"逐篇精确检索"自建模块
- 引入 5 层文献处理 SOP, Week 1 重审 metadata schema

---

## 10. 下一步只有一步

Week 1 Day 1: 通读 SOP, 写 ADR-0003 锁定 metadata schema 或维持原设计。
启动语: "Week 1 Day 1 开始, 先做 schema 决策"
