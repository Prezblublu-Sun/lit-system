# Schema 设计要点 (临时笔记, Week 1 Day 1)

## 关键原则: provenance 是必备字段, 不是可选

根据用户反馈, 综述纲要的某些段落是 LLM 辅助产生的草稿
(例: X.3.1 AI 历史段)。
这意味着文献库的每个字段都需要追溯:
- author: 谁说的 (qwen14b / claude-opus / human-wei / paperqa-agent)
- generated_at: 什么时候说的
- prompt_version: 用什么 prompt 产出的
- reviewed_by: 谁人工 review 过

## 综述纲要与 5 篇黄金论文的对应关系

X.3.1 AI as a tool          <- P5 (Robazzi 2025, Synergy)
X.3.2 Pre-printing          <- P2 (Zhang 2025, AI-driven for regen med)
                            <- P5
X.3.3 In-printing           <- P5
X.3.4 Post-printing         <- P2, P5
X.4 Cross-cutting (Zhang)   <- P2
X.5 System-level (Tian)     <- P3 (Dong 2022, robotic in situ)
                            <- P4 (Liu 2026, self-driving)
                            <- P1 (Zhou 2024, AI biofabrication)
X.5.1 Robotic in situ       <- P3
X.5.5 Self-driving future   <- P4, P1

观察: 5 篇论文恰好覆盖纲要的 5 个主要节
含义: 类 3 "personal_relevance" 字段需要标"这篇放到哪个节"
含义: SOP 实测应该让 LLM 直接判断"这篇属于纲要哪一节"

## SOP 30 字段的初步分类 (待 ADR-0003 锁定)

### 类 1: factual (LLM 自动抽取)
- background_context, core_concepts, common_pitfalls, design_objectives
- evaluation_metrics, research_motivation
- core_problem, technical_difficulties, proposed_methods
- figures, experimental_methods, analytical_methods (only 主题+目的)
- method_inventory (实验/分析/验证 三类)

### 类 2: interpretive (LLM 判断 + 人工 review)
- writing_techniques, technique_purpose
- method_strengths_limitations, evidence_vs_claims
- 10_dim_scoring + reasoning
- paper_position (重点精读/正文支撑/补充参考/价值较弱)
- top_3_takeaways, biggest_strength, biggest_limitation
- innovation_type (substantive vs presentational)
- conclusion_confidence_tier

### 类 3: personal_relevance (依赖综述纲要作为上下文)
- review_section_placement (X.3.2.1 等)
- argument_support (这篇支持哪个论点)
- inspiration_for_my_research
- writing_techniques_to_borrow

## 字段间依赖图 (草)

factual --(LLM 二次推理)--> interpretive --(+纲要)--> personal_relevance

每一层都要 provenance 字段。
不能跳过 factual 直接产 interpretive (会幻觉)。
不能跳过 interpretive 直接产 personal_relevance (没基础)。

## 用户在 Week 1 Day 1 的新输入 (2026-05-11)

### 库规模升级
- 原 project_brief.md 写的是 50 篇
- 用户当前论文库 = 300+ 篇
- 含义: Week 2-3 实际工作量是 6x,
        ADR-0003 schema 必须在 v1 就内置:
        - 去重机制 (doc_id 由文件内容 hash 而非文件名生成)
        - 增量更新 (inbox/ 监听, 不重跑全库)
        - 跨批次一致性 (前 50 篇和后 250 篇结构必须一样)

### 用户对"多模态资产库"的核心关切
原话: "我只是想知道如何建立多模态资产库, 而且其应该做到避免重复"
解读:
- 不是 operational 问题 (怎么导入)
- 是 architecture 问题 (结构怎么设计)
- "避免重复" = 同一篇论文不应有多份资产
        = doc_id 必须可重现 (basename 不可靠, 用内容 hash)
        = 同一篇多版本 (preprint vs published) 需要明确策略

---

## 待办: GitHub 备份 (本周后期)

### 现状
所有 commit 只在 Linux 本机 ~/lit-system/.git/, 无任何远程备份。
机器坏 = 全失。

### 计划做的时间
本周后期 (Day 3-5)

### 做之前的决策点
- GitHub 个人账号 vs UCL 学术账号
- 私有 vs 公开 repo
- SSH key vs PAT 认证
- 是否需要补充 .gitignore (corpus/ 已忽略 *.pdf, 但要复审是否漏了什么敏感数据)
- 是否同时备份到 OneDrive (作为冷备份)

### 简版命令草稿 (本周做时参考)
- git remote add origin git@github.com:user/lit-system.git
- git branch -M main
- git push -u origin main

### 临时风险
机器一周内挂掉的概率低, 但不为零。如果担心, 可以今晚做最简单的本地冷备份:
  tar czf ~/lit-system-backup-$(date +%Y%m%d).tar.gz ~/lit-system/.git ~/lit-system/decisions ~/lit-system/results ~/lit-system/scripts ~/lit-system/corpus/questions.md ~/lit-system/corpus/outline/review_outline.md
然后把这个 tar.gz scp 到 Windows 上, 2 分钟搞定。
