# ADR-0009: Domain-Specific SOPs under Common Schema

Status: Proposed (Week 3 Day 2 设计, Week 4-5 实施)
Date: 2026-05-12
Context: bioprinting 和 FEA 文献的信息结构完全不同, 统一 SOP 抽取质量低.

---

## Decision

使用 schema_v2_common 作为共享 metadata 骨架, 但每个 domain 用独立 SOP prompt
抽取该领域的核心字段.

结构:

  schema_v2_common
    id_block (doc_id, paper_id, content_hash, filename, schema_version)
    source_block (title, doi, authors, year, journal, abstract)
    classification (domain, primary_tags, secondary_tags, evidence_level)
    workflow (status, priority, why_included, ingest_status)
    _meta (produced_by, prompt_version, produced_at)

  sop_v3_bioprinting (per-domain block)
    bioink_composition
    cell_source
    printing_modality (extrusion / DLP / inkjet / laser)
    ai_role (pre / in / post / closed-loop)
    biological_validation
    process_parameters
    print_fidelity_metrics

  sop_v3_fea (per-domain block)
    research_object (femoral_stem / tibial / acetabular / patient_specific / abstract)
    model_type (linear / nonlinear / contact / bonded / press-fit)
    implant_type (cemented / cementless)
    geometry_source (CT / standard / patient_specific / parametric)
    material_model (isotropic_linear / anisotropic / hyperelastic / plastic / ...)
    interface_condition
    loading_condition
    boundary_condition
    mesh (element_type, size, validation)
    software (Abaqus / ANSYS / COMSOL / FEBio / custom)
    outputs (stress / strain / SED / micromotion / contact_pressure / safety_factor)
    validation (mesh_convergence / experiment / literature_comparison / clinical_data)
    limitations

  sop_v3_metal_am (per-domain block, Week 8+)
    process (LPBF / LDED / EBM / WAAM / binder_jetting / ...)
    material_system
    laser_parameters
    scan_strategy
    atmosphere
    build_orientation
    porosity / microstructure / mechanical_props / surface_roughness / residual_stress

  sop_v3_implant_clinical (per-domain block, future)
    cohort_size
    follow_up_duration
    implant_type
    surgical_approach
    failure_rate / patient_outcomes / radiographic_findings

所有 per-domain SOP 都遵守 ADR-0007 (clean output rules).

---

## Rationale

- bioprinting 和 FEA 关心的字段完全不同 (e.g. bioink vs mesh)
- 统一 SOP 让 LLM 抽不准 (e.g. 抽 FEA 论文的 "bioink" -> N/A)
- 共享 schema_v2_common 保证跨 domain 检索可用 (title/DOI/year/tags 通用)
- per-domain SOP 保证抽取准确性

---

## Implementation

Week 3 Day 2: 设计 schema_v2_common

Week 4-5: 设计 sop_v3_bioprinting (重构现有 SOP_v2)
  - 保持现有 5 任务结构 (background / methods / problem / scoring / personal_relevance)
  - 加 bioprinting 专属字段
  - 应用 ADR-0007 rules
  - 5 黄金集 P1-P5 + P44 验证

Week 5-6: 设计 sop_v3_fea
  - 用户提供的 9 节研究模板作为字段蓝本
  - 10 篇 FEA 黄金集人工筛选
  - prompt 设计 + 测试 + 修

Week 8+: sop_v3_metal_am, sop_v3_implant_clinical (按需启用)

Chroma metadata 必须更新:
  现有: paper_id, doc_id, section
  新增: domain, primary_tags, secondary_tags, schema_version, evidence_level

检索接口加 filter:
  retrieve_test_v1.py --domain bioprinting --tag-any "viability,shear"

---

## Consequences

- 优: 每个 domain 抽取质量大幅提升
- 优: 跨 domain 检索可用 (common schema), domain 内检索精准 (per-domain field)
- 优: 系统可扩展 (新 domain 只需加一个 sop_v3_X)
- 劣: SOP prompt 维护工作量翻倍 (一套变 4-5 套)
- 劣: ingest pipeline 需要 router (按 domain 选 SOP), 增加代码复杂度
- 劣: schema 演化时, 4-5 个 SOP 都要同步改

---

## Decision Pending

Domain 怎么决定?

选项 A: ingest 时手动指定 (--domain bioprinting)
  优: 明确, 简单
  劣: 每次手填

选项 B: candidate_index 提供 (从 candidate -> ingest 时带 domain 字段)
  优: domain 在 Layer 0 (Acquisition) 就定了, 入库自动用
  劣: 依赖 candidate_index 准确

选项 C: 入库时 LLM 自动判断
  优: 全自动
  劣: 增加一次 LLM 调用, 可能错判

倾向选项 B (跟 ADR-0008 candidate index 流程绑定).

---

## Related

- ADR-0005 (通用知识库) - common schema 是它的具体实现
- ADR-0007 (clean SOP output) - 所有 per-domain SOP 都必须遵守
- ADR-0008 (candidate index) - domain 字段在 candidate index 就要定
- decisions/roadmap/roadmap_v2.md Stage 3
