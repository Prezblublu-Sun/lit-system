# SOP 实测分析 · P5 论文 (Robazzi 2025)

日期: 2026-05-11
配置: qwen2.5-14b-8k + nomic-embed-text via PaperQA2
论文: P5 "The Synergy of AI and 3D Bioprinting"
任务数: 5 (覆盖 SOP 三类: factual / interpretive / personal_relevance)
总耗时: 311 秒 (5 任务平均 62 秒/任务)
全部成功: 5/5

---

## 逐项质量分级

### L1 factual_background --- A 级 --- 可用

64 秒。给出 5 个字段, 每个带页码引用 (页码合理, 与 P5 47 页篇幅一致)。

优点:
- 引用真实, 不是幻觉
- 字段覆盖完整

缺点:
- "common_pitfalls" 写"insufficient training data" 这类通用化套话
- 缺乏 verbatim 原文引用

schema 决策: LLM-auto, 但 prompt 需要求"quote a specific sentence verbatim"

### L1 factual_methods --- A 级 --- 最佳一项

58 秒。清晰分 A/B/C 三类, 列出 4 个具体 ML 算法:
- Bayesian Optimization + Gaussian Process Modeling
- Fuzzy Logic Systems
- Random Forest, XGBoost
- Supervised / Unsupervised Learning

每个算法带页码 + 1 句目的。

schema 决策: method_inventory 是高质量 LLM-auto 字段。这是 Path A 自建路线的核心战力之一。

### L2 interpretive_problem --- B 级 --- 勉强可用

55 秒。第 3 部分有真正批判性判断:
"Claims 主要支持理论框架而非实证结果, Random Forest 和 XGBoost 的提及没有充分实证数据"

但第 4 部分"intellectual contribution"流于套话。

schema 决策: claims_vs_evidence 字段值得设, 需 prompt 工程优化。
LLM-auto + 人工 spot-check.

### L2 interpretive_scoring --- D 级 --- 不可用

63 秒。10 维评分 = 46/50, 全 4-5 分, 几乎没有 3 以下。

致命问题:
1. LLM 默认给好评, 没有真实区分度
2. "writing quality 5" --- 它看不到完整论文, 只看 chunks
3. "limitation acknowledgment 5" 与上一题自己说的 "claims 没有实证支持" 自相矛盾
4. 没输出 position label (跑题了)

schema 决策:
- 10 维评分字段必须保留
- 产出方式不能是本地 14B
- 选项 A: 用 Claude/GPT-4 等更强模型跑评分
- 选项 B: 人工填写 (从模板)
- 选项 C: 不打数字分, 只打 high/medium/low 三级
- 优先选 C, 因为本地化目标下不依赖外部 API

### L3 personal_relevance --- C 级 --- 方向对精度错

69 秒。

错误: 推荐放 X.1 Introduction
正确: 应该是 X.3.1 (AI as a tool) / X.3.2-X.3.4 (Pre/In/Post-printing) / X.4 (Cross-cutting)

原因诊断: 14B 把纲要看作大段文本, 关键词匹配 ("workflow-spanning intelligence" 在 X.1 出现), 但没理解层级。

但 writing_insight 那部分有价值:
"借鉴 P5 的结构化方法 + 不同 ML 算法对应不同打印模态" --- 这是真有用的建议

schema 决策:
- review_section_placement: LLM 给 top-3 候选 + 人工确认
- writing_insight: LLM-auto, 直接收

---

## 给 ADR-0003 的输入

### Schema 三层结构验证: 通过

factual / interpretive / personal_relevance 三层划分得到实测支持。
但每层的自动化策略需要细分。

### 关键设计要求

1. provenance 必备 (LLM model + prompt version + timestamp + reviewed_by)
2. 评分类字段不用数字, 用三级 high/medium/low
3. 章节定位字段产出 top-3 候选, 不强制单选
4. 所有字段必带 evidence (引文 + 页码), 不允许无依据断言
5. 字段间依赖: factual --> interpretive --> personal_relevance, 不允许跳层

### 字段自动化等级

| 字段类 | 等级 | 处理 |
|---|---|---|
| factual.* | A (auto) | LLM 单次产出 |
| interpretive.claims_vs_evidence | B (auto + check) | LLM 产, 人工抽检 |
| interpretive.scoring | C (degraded) | 三级标签, 不打分 |
| personal_relevance.section | D (candidate) | top-3 候选 + 人工确认 |
| personal_relevance.insight | B (auto + check) | LLM 产, 人工抽检 |

### 性能数据

- 1 篇论文跑 5 类任务: 311 秒 (5 分钟)
- 推算 300 篇全库: 1555 分钟 = 26 小时 (单线程)
- 推算如果 SOP 扩到 10 类任务: 50+ 小时
- 含义: 必须支持并发 / 增量 / 跳过已处理
- Week 2-3 必须有"已处理则跳过"机制, 不能全库重跑

---

## 后续决策更新 (2026-05-11 晚)

### 新决策: 引入商业模型层

基于上面的实测分级 (尤其 L2 scoring D 级 + L3 section C 级),
用户做出新架构决策:

> "可以把资料库整理再分为两大块, 一块本地准备,
>  一块基于本地提取的内容使用商业大模型总结对比"

含义:
- 本地层负责 factual 字段 + 数据存储 + 向量索引
- 商业层负责 interpretive.scoring + personal_relevance.section + 综述起草
- 商业模型只看本地层产出的结构化资产, 不发送原始 PDF

### 候选商业模型

| 模型 | Input | Output | 300 篇估算 | 备注 |
|---|---|---|---|---|
| Claude Sonnet 4.6 | $3/MTok | $15/MTok | ~$16 | 推荐: 批判判断强 |
| Claude Opus 4.7 | $5/MTok | $25/MTok | ~$26 | 过度配置 |
| GPT-5.4 | $1.75/MTok | $14/MTok | ~$12 | 略便宜, 上下文短 |
| Claude Haiku 4.5 | $1/MTok | $5/MTok | ~$5 | 太弱, 可能跟本地 14B 没拉开差距 |

300 篇全库的判断层总成本估算: $10-30, 不是钱的问题。

### 字段自动化等级 (更新)

| 字段类 | 等级 | 处理 |
|---|---|---|
| factual.* | A (auto) | 本地 LLM 单次产出 |
| interpretive.claims_vs_evidence | B (auto + check) | 本地 LLM 产, 人工抽检 |
| interpretive.scoring | **改为商业层** | 商业模型 (Claude Sonnet 4.6 候选) |
| personal_relevance.section | **改为混合** | 本地 top-3 候选 + 商业模型 / 人工最终确认 |
| personal_relevance.insight | B (auto + check) | 本地 LLM 产, 人工抽检 |

### 数据出境策略

- 数据底座 (PDF/chunks/paper.md/figures) 全本地, 不出境
- 商业 API 只看 factual 字段 + 章节摘要 + 评分 prompt
- 论文已发表 -> 不含商业机密
- 用户授权: 可出境

### 商业模型具体选哪家 -> 延期到 ADR-0004

今晚 ADR-0003 schema 设计先把"commercial_llm"做成可配置字段, 不锁定具体模型。
具体选 Sonnet / GPT / DeepSeek 留到 ADR-0004, 本周内决定 (需要实测一两次再定)。
