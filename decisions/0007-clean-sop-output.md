# ADR-0007: Clean SOP Output

Status: Proposed (Week 3 Day 1 实施)
Date: 2026-05-12
Context: Week 2 Day 4 抽样审 P7/P11/P25/P40/P43/P44 metadata 发现严重输出污染.

---

## Decision

所有 SOP (v2 现有, v3 per-domain) 的 LLM 输出必须满足:
- 不含 conversational filler (e.g. "Based on...", "Certainly!", "Here are...")
- 不含 fake page numbers (e.g. "Page 2:"), 除非上游有真实 page metadata
- 不含 markdown 噪音 (无 ###, **, 编号列表, 表格), plain prose only
- 直接以实质内容开头, 不前言

具体做法 (Prompt 改造):

加在每个 SOP prompt 顶部的 CRITICAL FORMAT RULES:

  CRITICAL FORMAT RULES (must obey):
  1. Output ONLY substantive content. NO preamble, NO greeting, NO acknowledgment.
  2. DO NOT include phrases like "Based on the provided text" or "Here are the sections".
  3. NO markdown headers (###, **, bullets, numbered lists).
  4. NO page numbers (you do NOT have page info in the input).
  5. NO bold/italic emphasis.
  6. Plain prose paragraphs, separated by single newlines.
  7. Start immediately with the first substantive sentence.

---

## Rationale

- metadata 70-80% 字符是有用内容, 其余被 filler 占, 浪费 token
- tiered library export 时 filler 进 Tier A 段, 挤占核心信息空间
- RAG 检索召回时 filler 文本进 embedding, 稀释语义相关性
- 综述写作时 Claude 读到 "Based on..." 会被前缀干扰
- fake page 引用不真实, 综述 citation audit 困难
- markdown 格式不一致, 下游 parser 难写稳定规则

---

## Implementation

Week 3 Day 1:
  1. 改 scripts/ingest/pipeline.py 里 SOP_PROMPTS (5 个 prompt)
  2. 5 黄金集 (P1, P3, P5, P7, P44) --force re-ingest 对比
  3. 人工审 5 篇新 metadata, 确认无 filler / no fake page / no markdown
  4. 通过后 --force 重跑 bioprinting 124 篇 (~14 小时机器时)

Validation:
  写 scripts/validate_metadata.py, 自动检查:
    - 每字段开头是否符合 plain prose pattern
    - 是否含 "Based on" / "Certainly" / "Here are" 等 filler 关键词
    - 是否含 "Page \d+" pattern
    - 是否含 ###/** markdown
  通过 = 合格

---

## Consequences

- 优: metadata 字符密度提升 20-30%, evidence quality 上升
- 优: tiered export 同样 token 预算装更多有效信息
- 优: 写作时 Claude 输出更准确 (无 prefix 干扰)
- 劣: 已 ingest 的 124 篇需要 --force 重跑 (~14h 机器时, 一次性成本)
- 劣: SOP prompt 变长 (加 100 tokens RULES), 但 qwen 32k 上下文充足

---

## Related

- ADR-0009 (domain-specific SOPs) 也必须遵守这套 RULES
- decisions/roadmap/roadmap_v2.md 原则 5 (RAG 产物是 evidence package)
