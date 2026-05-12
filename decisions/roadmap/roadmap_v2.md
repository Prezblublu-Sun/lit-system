# lit-system Roadmap v2

Status: Active (replaces ad-hoc planning notes from Week 2)
Created: 2026-05-12
Context: Re-framing after Week 2 Day 4 实战暴露的设计问题

---

## 1. 项目根本目标

lit-system 是一个本地化、可追溯、可扩展的科研知识底座, 把大量 PDF 文献转化为
结构化证据, 服务于:

- 综述写作 (短期: RSC AI for 3D bioprinting)
- 博士课题设计 (中期: femoral stem + FEA + surrogate model)
- 长期跨领域知识积累

不是简单的 PDF 管理工具, 也不是单纯 RAG. 是 research evidence operating system.

---

## 2. 解决的核心问题

1. 文献太多, 人工难以系统阅读
2. GPT/Claude context 有限, 不能长期记住所有文献
3. Zotero 只管理文献, 不理解文献
4. 综述写作需要可追溯证据, 而非模型凭空总结
5. 跨课题 (bioprinting / metal AM / orthopaedic implant / FEA / AI) 需要长期积累

---

## 3. 三层目标

近期: RSC bioprinting 综述
  - 124 篇 bioprinting -> 干净 metadata -> tiered library -> 章节写作
  - 当前进度: ingest 中 (54/124)

中期: 博士主线
  - femoral stem / hip implant / FEA / surrogate model / fixed background mesh
  - 建立 candidate index, 不立即 full ingest
  - 之后设计 sop_v3_fea, 小规模 ingest

远期: 通用学术知识库
  - bioprinting / metal AM / NiTi/SMA / orthopaedic implants / FEA / surrogate / clinical / standards / AI
  - 不同 domain 不同 schema
  - 检索可按 domain/tag/evidence_level 过滤
  - 写作时可导出 evidence package

---

## 4. 四层架构

Layer 0: Literature Acquisition Layer
  文献搜索 / DOI 查找 / 候选记录 / 下载决策 / 去重
  当前: 缺位, 这是关键空白

Layer 1: Local Knowledge Base Layer
  PDF 解析 / 清洗 / metadata / chunks / embedding / Chroma
  当前: 已跑通端到端, 但需要稳定 + 清洗

Layer 2: Evidence Synthesis Layer
  检索 / 分级 / evidence package / tiered export / 主题汇总
  当前: 设计中

Layer 3: Writing & Thinking Layer
  你 + GPT/Claude 做 outline / 论证 / 段落 / 课题设计
  当前: 依赖网页 LLM + 你的判断

---

## 5. 五条系统设计原则

原则 1: 先完成真实闭环, 再扩张
  当前必须先完成 bioprinting 闭环 (124 篇 -> 写作), 而非同时铺开多个领域.

原则 2: 新领域先 candidate index, 后 full ingest
  任何新搜索/新领域文献先进 candidate index, 经主题/优先级筛选后再 selective ingest.

原则 3: 通用知识库 != 无结构知识库
  通用库必须有 domain / tag / evidence_level / writing_use / schema_version / ingest_status.

原则 4: 自动层 + 人工层分开
  自动: title / DOI / methods / outputs / limitations / chunks / embedding (LLM 抽)
  人工: why_included / relevance_score / what_I_can_reuse / writing_use / my_critique (你填)
  关键决策 (why_included, what_I_can_reuse) 不能完全交给 LLM.

原则 5: RAG 最终产物是 evidence package, 不是 chunks
  不是 "这篇论文说了什么", 而是 "为某章节/某问题导出可写入综述的证据包".

---

## 6. Stage 路线图

Stage 1: bioprinting 闭环 (Week 3-4)
  目标: 证明系统能真实服务综述写作.
  完成标志:
    [ ] 124 篇 ingest 完成
    [ ] SOP 输出干净 (ADR-0007)
    [ ] metadata 无 filler
    [ ] DOI/title 基本正确
    [ ] chunks 可检索
    [ ] tiered library 可导出
    [ ] 支持一个 RSC 小节写作

Stage 2: candidate index 层 (Week 3+, parallel)
  目标: 把文献搜索纳入系统.
  新增:
    results/candidates/fea_candidate_index.csv
    results/candidates/metal_am_candidate_index.csv  (from 515 currently classified)
    results/candidates/other_candidate_index.csv     (from 281)
    results/candidates/seed_papers/{domain}.md
    results/candidates/search_logs/
  候选文献字段:
    paper_id (placeholder, e.g. CAND-{n})
    title / year / doi / abstract (if available)
    domain / theme / priority
    why_relevant
    pdf_status (have / need_download / no_access)
    ingest_status (candidate / ingested / rejected)
  完成标志:
    [ ] FEA/femoral stem 50 篇候选
    [ ] 每篇有 theme + why_relevant
    [ ] A/B/C 分级完成
    [ ] A 类 PDF 下载

Stage 3: 多领域 schema (Week 4-5)
  目标: 不同领域不同 SOP, 共用 common schema.
  结构:
    schema_v2_common
    sop_v3_bioprinting
    sop_v3_fea
    sop_v3_metal_am
    sop_v3_implant_clinical
  FEA SOP 重点字段:
    research_object / model_type (linear/nonlinear/contact/bonded/press-fit)
    implant_type (cemented/cementless)
    geometry / material_model / interface / loading / boundary / mesh / software
    outputs / validation / limitations
    reusable_method / reusable_metric / writing_use
  完成标志:
    [ ] 10 篇 FEA 黄金集抽取合格
    [ ] interface / loading / outputs 准确识别
    [ ] 无 fake page / 无 conversational filler

Stage 4: 多领域 RAG 子库 (Week 5-6)
  目标: 按 domain 检索.
  Chroma metadata 加: domain / paper_id / year / title / tags / priority / schema_version / chunk_type / content_layer
  完成标志:
    [ ] bioprinting / FEA / metal_am 都可检索
    [ ] 不被 references 污染
    [ ] 可按 domain/tag 过滤

Stage 5: 写作支持层 (Week 6+)
  目标: 从 RAG 输出 evidence package, 不只 chunks.
  核心导出类型:
    1. section evidence package
    2. tiered library package
    3. metrics comparison table
    4. citation audit report
    5. paper-by-paper summary pack
  完成标志:
    [ ] 能为某 RSC 小节导出 10-20 篇核心证据
    [ ] 能按 Tier A/B/C 分配 token
    [ ] 能检查草稿 claims 是否有文献支持
    [ ] 能输出可写入综述的观点句

---

## 7. 两条并行主线

Main A: RSC bioprinting 生产线 (近期)
  A1. 等 bioprinting ingest 跑完 (进行中, 54/124)
  A2. 检查 metadata 完整性
  A3. 修 SOP_v2 prompt (ADR-0007)
  A4. P1-P5 + P44 黄金集回归测试
  A5. --force 重跑 124 篇
  A6. 生成 tiered library
  A7. 小节写作 dry run
  A8. 反推 schema / export 脚本问题

  这阶段不要做: 切 LLM 模型 / 大规模 ingest metal_am / 立刻 ingest FEA / 重构所有代码

Main B: FEA / femoral stem 预研线 (中期)
  B1. 建 fea_candidate_index.csv
  B2. 写入用户 14 篇 seed paper
  B3. 扩展到 50 篇候选
  B4. 每篇标 priority + why_relevant
  B5. 下载 A 类 PDF
  B6. 选 10 篇 FEA 黄金集
  B7. 设计 SOP_v3_fea
  B8. 小规模 ingest 10 篇测试
  B9. 修 SOP_v3_fea
  B10. ingest 30-50 篇

  这阶段不要做: 把 FEA 混进 bioprinting SOP / 凑数量下几百篇 / 没设计 schema 就 full ingest

---

## 8. 当前优先级排序

1. 完成 bioprinting 124 篇 ingest (进行中)
2. 修 SOP_v2 输出污染 (ADR-0007, Week 3 Day 1)
3. 立刻: 创建 candidate index (metal_am 515 + other 281 都进去)
4. 生成 bioprinting tiered library
5. 用 RSC 小节做 dry run
6. 建 FEA candidate index
7. 扩展 FEA seed papers 到 50 篇
8. 设计 SOP_v3_fea
9. 小规模 ingest FEA 黄金集
10. 建 FEA RAG 子库
11. 再考虑 metal_am 全量扩展和多模型对比

---

## 9. 文献搜索标准流程

  Search query
    -> Candidate record (进 candidate_index)
    -> DOI / metadata check
    -> Theme classification
    -> Priority scoring (A/B/C)
    -> PDF download decision
    -> Selected PDF (only A and selected B)
    -> Domain-specific SOP ingest
    -> RAG chunks + embedding
    -> Evidence package

搜到一篇新文献时, 必须回答 6 个问题:
  1. 它属于哪个 domain?
  2. 它解决什么研究问题?
  3. 它提供什么方法 / 指标 / 证据?
  4. 它是 A/B/C 哪个优先级?
  5. 它值不值得下 PDF?
  6. 它值不值得 full ingest?

答不上, 就先不下载, 不入库.

---

## 10. 一句话规划

先用 bioprinting 综述完成 lit-system 的第一个真实闭环;
同时用 candidate index 低成本积累 FEA/femoral stem 文献;
之后通过 domain-specific SOP 把 FEA 文献正式纳入 RAG,
最终让系统服务于 fixed-background-mesh + Abaqus automation + surrogate model 的博士课题设计.

---

## 11. 系统转折点判断

lit-system 已经从 "PDF 解析实验" 进入 "长期科研基础设施" 阶段.

接下来从 "能跑" 转向 "可控":
  可控的文献进入机制 (candidate index)
  可控的 schema (schema v2 common + per-domain)
  可控的 SOP 输出 (clean prose, no filler)
  可控的 domain filter (Chroma metadata)
  可控的 evidence package (export pipelines)
  可控的写作工作流 (Stage 5)

核心秩序:
  candidate index -> selective ingest -> domain-specific schema -> evidence package -> writing/research decision
