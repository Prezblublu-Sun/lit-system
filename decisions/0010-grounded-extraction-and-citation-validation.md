# ADR-0010: Grounded Extraction with Citation Validation

Status: Proposed (Week 3 Day 2 设计, Week 4 实施)
Date: 2026-05-12
Context: 综述写作 / 课题设计需要 metadata 和 evidence package 可追溯到原文.
         LLM 幻觉无法完全消除, 但可以通过工程手段降到 10% 以下.
         本 ADR 定义 4 层防幻觉机制 + 引用位置标注规范.

---

## Decision

所有 SOP 抽取 + evidence package 生成必须满足:

1. 每个 claim 带 verbatim_quote (5-25 词原文)
2. 每个 quote 必须通过后处理验证 (字符串匹配 chunk_text)
3. 失败的 quote 标记 FABRICATED_QUOTE, 不进 metadata
4. 引用格式标准化: [P{n}, chunk_{x}, §{section_heading}, p.{page_hint}?]
5. page 信息标 confidence (high/low/none), LLM 不得自行生成 page number

---

## 4 层防幻觉机制 (按强度)

### Layer 1: Prompt-level Rules (所有 SOP 都用)

强制规则加在 SOP_v3 prompt 顶部:

  CRITICAL RULES (must obey):
  1. Only extract what is EXPLICITLY stated. No inference.
  2. For every claim, provide verbatim_quote (5-25 words from chunk).
  3. The verbatim_quote MUST match chunk text character-for-character.
  4. If no information present in chunk, output {"value": null, "reason": "not in chunk"}.
  5. Do NOT use external knowledge.
  6. Do NOT generate page numbers. Page is provided by Docling, not LLM.
  7. Do NOT combine information from different chunks in one extraction.

预计减少 30-50% 幻觉. 但单靠 prompt 不够, 必须配合 Layer 2-4.

### Layer 2: Inline Citation Enforcement

LLM 输出必须含 [P{n}, chunk_{x}] 引用. 后处理:

  def enforce_citations(llm_output, allowed_chunks):
      sentences = split_sentences(llm_output)
      valid = []
      for s in sentences:
          citations = re.findall(r'\[P\d+,\s*chunk_\d+\]', s)
          if not citations:
              continue  # 无引用, 丢弃
          for c in citations:
              if c not in allowed_chunks:
                  s = s.replace(c, '[INVALID CITATION]')
          valid.append(s)
      return valid

效果: 强制 LLM 学会引用, 留下的句子全可追溯.

### Layer 3: Verbatim Quote Validation (核心)

每个抽取必须输出 verbatim_quote + char_offset_in_chunk:

  GROUNDED EXTRACTION FORMAT (in SOP prompt):
    {
      "value": "<extracted content, your words OK>",
      "verbatim_quote": "<5-25 verbatim words from chunk>",
      "char_offset_in_chunk": <int, where quote starts>
    }

后处理 validator:

  def validate_extraction(extraction, chunk_text):
      quote = extraction['verbatim_quote']
      if quote not in chunk_text:
          extraction['status'] = 'FABRICATED_QUOTE'
          return False
      actual_offset = chunk_text.find(quote)
      if actual_offset != extraction['char_offset_in_chunk']:
          extraction['offset_corrected'] = True
          extraction['char_offset_in_chunk'] = actual_offset
      extraction['status'] = 'VALIDATED'
      return True

效果: 90%+ fabricated quotes 被逮到. LLM 编不出真不在原文里的句子.

### Layer 4: Chunk-level Grounding (高价值任务用)

不让 LLM 一次性看多 chunk 综合, 而是每 chunk 独立判断:

  for chunk in retrieved_chunks:
      prompt = f"""
      CHUNK: {chunk.text}
      QUESTION: Does this chunk support claim "{claim}"?
      Output ONLY JSON:
      {{
        "supports": true/false,
        "verbatim_quote": "<exact words or null>",
        "confidence": "high/medium/low"
      }}
      """
      result = llm_call(prompt)
      if result.supports and result.verbatim_quote in chunk.text:
          valid_evidence.append({chunk, result})

代价: LLM 调用次数 = chunks 数 (而非 1 次综合).
  - Claude Sonnet $3/M, 10 chunks 约 $0.10/查询
  - 完全可接受

用于:
- export_section_evidence.py (Week 4)
- citation_audit.py (Week 6+)
- 不用于: SOP 抽取 (一篇文章一个 chunk 即可)

---

## 引用格式规范

标准引用 (full form):

  [P5, chunk_007, §3.2 Methods, p.4?]

字段含义:
- P5            : paper_id (100% reliable, schema 字段)
- chunk_007     : chunk_id within P5 (100% reliable, Chroma 索引)
- §3.2 Methods  : section heading (best-effort, 来自 Docling H1/H2 抽取)
- p.4?          : page hint from Docling. "?" 表示 unreliable
                  (尤其 OCR 后 / 复杂 layout / multi-column 文档)

简化形式 (in-text):

  [P5, c7]   或   [P5:c7]

---

## Chunk Metadata Schema (Schema v2 强制)

每个 chunk JSON 必须含:

  {
    "chunk_id": "P5_chunk_007",
    "paper_id": "P5",
    "char_start": 1842,          // 在 cleaned.md 的字符位置
    "char_end": 2438,
    "text": "...",
    "section_heading": "3.2 Bioink characterization",  // optional, from Docling
    "section_level": 2,           // H1=1, H2=2 (optional)
    "content_layer": "body",      // body | abstract | references | caption
    "page_hint": 4,               // optional int
    "page_confidence": "high"     // high | low | none
  }

不允许:
- chunk 无 chunk_id (违反 schema)
- page_hint 由 LLM 生成 (must be from Docling)
- char_offset 不可验证 (must point to actual location in cleaned.md)

---

## 4 类无法消除的"语义级"幻觉 (Known Limits)

| 类型                            | 能消除? | 处理              |
|--------------------------------|---------|------------------|
| 编造数字                        | ✅      | verbatim quote 验证 |
| 编造作者 / 年份                  | ✅      | 跟 metadata 字段交叉 |
| 编造 page number                | ✅      | 禁止 LLM, 用 Docling |
| 错误综合 2+ 篇 paper            | ⚠️      | Layer 4 chunk-grounding |
| 暗示因果但没明说的关系           | ❌      | 人审, 无工程解 |
| 过度概括 ("most studies...")    | ❌      | prompt 禁止 + 人审 |

后两类是 LLM 底层问题, 工程不能解决. 综述核心论点必须人审 + 多 LLM consensus.

---

## Implementation Phases

### Phase 1: Chunk Metadata Upgrade (Week 3 Day 2)
- 改 build_chunks (scripts/ingest/pipeline.py):
  - 计算 char_start / char_end
  - 从 Docling 抽 section_heading + page_hint
  - 写 page_confidence 字段
- Pydantic ChunkMetadata 模型, 强制 schema 验证
- 已有 124 篇 (P1-P56+) chunks 需要重生成 (--force)

### Phase 2: SOP_v3 Verbatim Quote (Week 3 Day 3-4)
- 改 SOP_v3 prompts (所有 5 任务):
  - 输出格式加 verbatim_quote + char_offset_in_chunk
- 写 scripts/validate_metadata.py:
  - 每个 extraction 跑 validate_extraction()
  - 失败标 FABRICATED_QUOTE, 不进 metadata
- 5 黄金集 benchmark 验证: validated rate 应 >85%

### Phase 3: Section Evidence Pipeline (Week 4)
- export_section_evidence.py 用 Layer 4 chunk-grounding:
  - 每 chunk 独立问 "supports claim X?"
  - 模板拼装段落, LLM 不做二次综合
- 输出 evidence package 含完整引用链:
  [P5, chunk_7, §3.2, p.4?] - quote: "..."

### Phase 4: Citation Audit (Week 6+)
- citation_audit.py:
  - 输入: 综述草稿 (.md)
  - 检查: 每个引用句的引用是否真支撑该 claim
  - 标记 无引用句 (你的观点) vs 有引用句 (文献支撑)
  - 报告 fabricated citation rate

---

## Multi-LLM Consensus (Reserve, 高价值场景)

综述核心论点 + 引用关键数据点, 用两个不同模型独立验证:

  claim = "Bioink viscosity >1 Pa·s ensures shape fidelity"
  source = (P5, chunk_7)
  
  v1 = verify_with_gemini_flash(claim, chunk_7)
  v2 = verify_with_deepseek_v3(claim, chunk_7)
  
  if v1.supports and v2.supports and v1.quote == v2.quote:
      ACCEPT
  elif v1.supports != v2.supports:
      FLAG_FOR_HUMAN_REVIEW
  else:
      FLAG_INCONSISTENT_QUOTES

不默认开启. 仅用于:
- 综述章节最终稿的关键 claim
- ADR 推翻 / 反驳类决策

成本: 翻倍. 但每篇综述只跑一次, 约 $5-10.

---

## Validation Metrics (Benchmark 指标)

5 黄金集 benchmark 中加 3 个新指标:

  fabricated_quote_rate    : 应 < 5%
  fake_page_rate           : 应 = 0% (Layer 1 强制)
  chunk_offset_accuracy    : 应 > 95%

跟 ADR-0007 已有指标合并:
  filler_rate              : 应 = 0%
  schema_validity          : 应 = 100%
  field_completeness       : 应 > 90% (per required fields)

---

## Consequences

- 优: metadata 100% 可追溯, 综述 citation audit 可自动化
- 优: 比 paper-qa 还严格 (paper-qa 不强制 verbatim quote)
- 优: 跟 ADR-0007 (clean output) + ADR-0009 (domain SOP) 兼容
- 劣: SOP prompt 变长 (加 verbatim_quote 字段, +200 tokens)
- 劣: 抽取吞吐降低 (validation 失败要 retry)
- 劣: 部分 claim 因 quote 验证失败被丢弃 (但这是好事)

---

## Related

- ADR-0007 (Clean SOP Output) - Layer 1 prompt rules 在此基础上
- ADR-0008 (Candidate Index) - candidate 不需要 grounding, ingested 才需要
- ADR-0009 (Domain-Specific SOPs) - 所有 per-domain SOP 都用本 ADR 规则
- decisions/roadmap/roadmap_v2.md 原则 5 (Evidence package)
- 引用 paper-qa 的 citation 设计哲学, 但更严格
