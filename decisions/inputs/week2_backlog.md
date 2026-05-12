# Week 2 Backlog (deferred to Week 3 or beyond)

记 Day 1/Day 2 期间有意推迟的事项,避免遗忘。
触发任一条件升级到 ADR-0005 的话,把对应条目挪过去。

## 1. Path C 复评 scoring (D 级 -> 可用)

**背景**: ADR-0004 锁定 Path C (本地数据 + 网页 chat 推理). Week 1 Day 2 实测
qwen2.5-14b-32k 在 L2_interpretive_scoring 任务上是 D 级.

**当前状态**: metadata/P*.json 里 interpretive.scoring_10_dim_local 标注
"D-grade local LLM output; pending Path C web chat review", reviewed_by/at 字段
保留 null 等填.

**何时做**: Week 2 末 或 Week 3 初. 触发: 综述写作辅助阶段需要 position_label
做章节定位时.

**怎么做**: 用 assets/export/literature_corpus_v1.md 作为输入, 走 Claude/GPT/Gemini
网页 chat, 把评分结果手工填回 metadata, 同时填 reviewed_by="human-wei via
claude_web/gpt_web/..." 和 reviewed_at.

## 2. Cleaning 升级 / 广告检测

**背景**: cleaning_v1 (content_layer=body) 只去 furniture (page_header/footer
共 86 个 in P1). BreathSpec 类广告本体仍在 cleaned 数据里, 当前靠 chunk 起点
跳到 Abstract 才把广告排除 -- 是侥幸不是设计.

**风险**: 如果某篇广告插在正文中间 (出版社可能这么做), chunks 会受污染.

**何时做**: Week 3 评估 30+ 篇时一起处理. 候选触发 ADR-0005 (cleaning 策略升级).

**候选方案**:
- B. 章节孤岛检测 (短 section 后接 < N block 又换 section)
- C. Page-level 整页过滤 (要求广告是整页, P1 不满足)
- D. LLM 二次过滤 (qwen2.5-14b 判断每个 section 是不是广告)

## 3. chunk tok_max 超过 WINDOW

**背景**: WINDOW_TOKENS=800 但 chunks tok_max 实测 844-901.

**原因**: 边界 block 加入时用 <= 判断, 单 block 自身大可能溢出.

**影响**: embedding 模型上限通常 8K+, 完全无影响. 不堵路.

**何时做**: 如果未来换 embedding 模型 (比如 BGE 等本地小模型上下文 512), 再处理.

## 4. .venv pip --break-system-packages

**背景**: 在 (.venv) 里 pip install 触发 PEP 668 拒绝, 怀疑 venv 是 system-site-packages
模式建的. 但 import 现有包 (tiktoken/docling) 都正常.

**何时做**: 下次真缺包要装时再处理.
