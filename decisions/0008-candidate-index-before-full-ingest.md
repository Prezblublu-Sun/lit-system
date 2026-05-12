# ADR-0008: Candidate Index Before Full Ingest

Status: Proposed (Week 3 Day 3 实施)
Date: 2026-05-12
Context: lit-system 从 PDF 解析实验进入长期科研基础设施阶段, 需要从 "能跑" 转向 "可控".

---

## Decision

任何新领域 / 新搜索的文献, 先进入 candidate index (轻量记录),
经主题、优先级、用途筛选后, 再 selective ingest (full Docling + SOP + Chroma).

不再有 "直接全量 ingest" 的默认路径.

Candidate Index 数据格式 (CSV):
  paper_id          CAND-{n} (placeholder, 不是 P{n})
  title
  authors
  year
  doi
  abstract          (if available from search)
  domain            bioprinting / fea / metal_am / orthopaedic / ai_ml / standards / ...
  theme             细分主题, 自由文本 (e.g. "stress shielding", "CutFEM")
  priority          A / B / C
  why_relevant      一句话: 为什么进 candidate
  pdf_status        have / need_download / no_access
  ingest_status     candidate / ingested / rejected
  source            搜索来源 (Google Scholar / Scopus / 已下 / 推荐 / ...)
  added_at          ISO 8601 timestamp
  notes             自由文本

---

## Rationale

- 防止低相关文献污染 RAG (Chroma 检索结果质量下降)
- 避免 SOP 不匹配 (bioprinting SOP 抽 metal AM 论文 = 浪费)
- 节省计算资源 (full ingest 8-12 min/篇, candidate 记录 < 1 min)
- 保证每篇入库文献有明确用途 (why_relevant 强制填)
- 让 "文献搜索" 成为系统化 stage, 而非临时人工活动

---

## Implementation

Week 3 Day 3 立刻执行:

  1. 创建目录:
     results/candidates/

  2. 创建三个初始 CSV:
     results/candidates/metal_am_candidate_index.csv  (515 篇 from current classification)
     results/candidates/other_candidate_index.csv     (281 篇 from current classification)
     results/candidates/fea_candidate_index.csv       (空, Week 4 开始填)

  3. 写脚本 scripts/candidate_index_from_classification.py:
     从 library_classification.json 转 CSV
     metal_am 515 篇全部 priority=B (默认中等, 待人工细化)
     other 281 篇全部 priority=C (默认低, 待人工细化)
     ingest_status=candidate

  4. 写辅助脚本:
     scripts/add_candidate.py        (从 DOI/title 加新条目)
     scripts/list_candidates.py      (按 domain/priority/status 过滤)
     scripts/promote_candidate.py    (candidate -> 准备 ingest, 移到 inbox)

文献搜索标准流程:

  Search query
    -> Candidate record (进 candidate_index, ingest_status=candidate)
    -> DOI / metadata check
    -> Theme + priority assigned
    -> PDF download decision (only A and selected B)
    -> promote_candidate.py 移到 inbox + ingest_status=promoting
    -> ingest.py 跑 full pipeline
    -> ingest_status=ingested + paper_id 更新为 P{n}

---

## Consequences

- 优: 文献搜索 / 入库 / ingest 三件事解耦
- 优: 可低成本积累 (光记不 ingest)
- 优: 可追溯 (每篇 ingest 前的 why_relevant 永久保留)
- 优: 不同领域 candidate 池独立, 不互相污染
- 劣: 新增一层抽象, 工作流变长 (但每步明确)
- 劣: candidate_index.csv 要维护 (但 ~1000 行 CSV 不是负担)

---

## Migration of Existing Data

当前 920 unique PDFs 已分类为:
  bioprinting 124   -> 已/正在 ingest, 进 candidate_index 时 ingest_status=ingested
  metal_am    515   -> 进 candidate_index, ingest_status=candidate (不 ingest)
  other       281   -> 进 candidate_index, ingest_status=candidate (不 ingest, 主要是教材/学位/低相关)

这把 ADR-0005 (通用知识库) 的含义精化为:
  - 任何课题文献都能进 lit-system (candidate_index)
  - 但 candidate != ingested
  - selective ingest 是后续独立决策
  - Chroma 检索只看 ingested

---

## Related

- ADR-0005 (通用知识库 + domain filter) 由此精化
- ADR-0009 (domain-specific SOPs) 是 ingest 决策的下一步
- decisions/roadmap/roadmap_v2.md Stage 2
