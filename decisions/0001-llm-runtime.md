# ADR-0001: LLM 推理引擎选择 Ollama-only

## 日期
2026-05-10

## 状态
Accepted(可在 Week 4 重评)

## 背景
原 architecture 计划 Week 1 同时部署 Ollama + vLLM。
Week 0 体检后新发现:
- GPU 为 RTX 5060 Ti(Blackwell sm_120,16GB VRAM)
- vLLM 预编译 wheel 在 sm_120 上不可用,需 FlashInfer 后端 + 特殊配置
- Week 0/1 实际只需要单流推理验证流程,不需要高吞吐

## 决策
Week 0-3 只部署 Ollama。
vLLM 推迟,触发条件见下。

## 备选方案
- A: 立即上 vLLM(否决:Blackwell 兼容成本高,Week 0 不需要)
- B: 双引擎并行(否决:违反"小步交付",增加 Week 1 复杂度)
- C: 永远只用 Ollama(待定:取决于 Week 3 实测数据)

## 何时重新评估
满足任一即触发:
- Week 3 批处理 50 篇耗时 > 6 小时
- Week 5 RAG 单次问答 > 15 秒且无法优化
- 引入并发场景(多人/多 tab/Web UI)出现明显排队

## 影响
- Week 1 checklist 中 vLLM 相关条目暂缓
- BGE-M3 / BGE-Reranker 仍按原计划在 Windows 上 fastapi 部署(不变)
- ARCHITECTURE.md 标记"LLM 推理引擎"模块当前实现 = Ollama
