# ADR-0002: 文献资产 schema 重新设计(决策延期)

## 日期
2026-05-10

## 状态
Deferred to Week 1 Day 1

## 背景
Week 0 末尾,用户提出了一个完整的"文献处理 SOP"(见 decisions/inputs/literature_processing_sop.md),
要求每篇论文产出 5 层 ~30 字段的结构化分析:
1. 基础背景提取
2. 核心问题/难题/解决办法
3. 10 维标准化评分
4. 知识资产沉淀
5. 综述写作落点

这个需求显著超出原 architecture.md 中 metadata.json 的字段范围。

## 决策
今晚不动,推迟到 Week 1 Day 1 处理。

## 理由
- Week 0 累计已 8.5 小时,精力不足以做大决策
- 改动会传导到 chunks.jsonl / paper.md / PaperQA2 替代方案 等多个层
- 应该和原 architecture.md 一起重审

## Week 1 Day 1 要做的事
1. 把 SOP 的 30 字段映射到 metadata.json schema 草稿
2. 评估哪些字段可被 LLM 自动产出,哪些需人工
3. 评估这对 Week 4 决策(Path A vs B)的影响
4. 写 ADR-0003 锁定新 schema
