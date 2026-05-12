# ADR-0004: 商业 API 策略 -- 推迟接入, 优先网页工作流 (Path C)

## 日期
2026-05-11 (Week 1 Day 2 结尾)

## 状态
Accepted (Week 4 重评)

## 背景

ADR-0003 设计了"本地数据 + 商业判断"混合架构, 留了商业模型选型给本 ADR 决定。
原计划: 评估 Claude Sonnet 4.6 / GPT-5.4 / DeepSeek, 选一个接 API。

但 Day 2 实测出现一个未预料的事实:

1. 本地 Ollama (qwen2.5-14b-32k) 直读 PDF + 简单 SOP, 25/25 任务成功, 60 秒/任务
2. 把 5 篇论文的 SOP 结果 export 成 60KB markdown (literature_corpus_v1.md)
3. 把这份 markdown 粘到 Claude.ai / Gemini / ChatGPT 网页对话
4. 三家网页 chat 都给出了高质量综述写作辅助:
   - 准确指出 X.5.5 节核心引文应为 P4 + P2
   - 正确区分 P4 (system-level architecture) vs P5 (function-level application)
   - 起草了 200 字开头, 三家都可直接修改使用
   - 引用页码全部正确, 无幻觉

这意味着出现了一条新路径:

**Path C: 本地数据底座 (Ollama 自主) + 网页 chat 推理 (零 API 成本)**

## 决策

**双轨并行, 网页主力, API 备份。**

1. 优先用 literature_corpus_v1.md (及未来扩展版) + 网页 chat 工作流写综述
2. 推迟商业 API 接入到 Week 3 或更晚
3. 接入时, 用于 batch 自动化场景, 不取代网页 chat 工作流
4. 不锁定具体模型选型 (Sonnet / GPT / DeepSeek), 留到真正接入时实测决定

## 理由

### 为什么不立刻接 API

- 网页 chat 三家实测可用, 零增量成本
- Claude Pro 订阅已付, 边际成本为 0
- API 接入需要: 申请 key + 写客户端 + 错误处理 + cache + provenance --- 3-5 小时工作量
- single-user research workflow, 不需要 batch 自动化
- 钱不是瓶颈 (300 篇 ~$30) 但工时是瓶颈

### 为什么仍要保留 API 选项

- Week 5-6 综述写作冲刺时如果发现网页 chat 工作流卡 (反复粘贴疲劳 / 上下文管理混乱), 需要 fallback
- 300+ 篇全库的批量 metadata 升级 (例如对所有论文重跑 L2_interpretive_scoring) 必须 API
- 跨主题语料库比较需要程序化处理

### 为什么网页 chat 工作流"够用"

实测证据 (literature_corpus_v1.md 测试):

| 维度 | 网页 chat 表现 |
|---|---|
| 引用准确性 | 100% (无幻觉) |
| 章节定位精度 | 三家都正确指向 X.5.5 |
| 跨论文判断 | Claude 抓到 P4 / P5 嵌套关系 |
| 综述起草质量 | 三个 200 字版本都可用 |
| 批判性观察 | 三家都引用了本地 14B 提取的 claims-vs-evidence gap |

意味着: 本地 14B 抓事实, 网页 chat 抓判断, 工作流闭环。

## 修订 ADR-0003 (副作用)

ADR-0003 写的"interpretive.scoring 用商业模型"那条字段产出方式:

| 字段 | 原 ADR-0003 | 修订为 (本 ADR) |
|---|---|---|
| interpretive.scoring | 商业 API (Sonnet/GPT) | 网页 chat (Claude.ai), API 备份 |
| personal_relevance.section_final | 商业 API + 人工 | 网页 chat + 人工 |
| 商业 API key | Week 2 接入 | 推迟到至少 Week 3 |

provenance 字段含义不变, 只是 produced_by 现在可能写 "claude-web-chat-2026-05-11" 之类的标记。

## 备选方案 (留档)

- A: 按 ADR-0003 立即接 API --- 否决, 投入产出不划算
- B: 完全不用商业 (纯本地) --- 否决, 14B 评分 D 级是已知缺陷
- **C: 推迟 API, 网页主力 (本采纳)**
- D: 双路并行立即都做 --- 否决, 资源不允许

## 何时重评

任一触发即写 ADR-0005:

- 网页 chat 工作流出现明显瓶颈 (反复粘贴 / 上下文管理混乱 / 单次对话装不下)
- 批量任务需求出现 (例如想给 300 篇都跑一遍 L2_scoring)
- 网页 chat 服务出现政策性限制 (Claude Pro 配额 / 区域封锁)
- Week 5-6 综述写作进度卡住, 怀疑 chat 工作流是瓶颈

## 对 Week 2-6 计划的影响

Week 2:
- 不接 API (省 3-5 小时)
- 重点: schema v1 实现 + 单篇 pipeline (Docling)
- 验证 export_corpus.py 在更多论文上的可扩展性

Week 3-4:
- 主要工作: 用现有工作流 + 网页 chat 写综述初稿
- Week 4 决策: Path A vs Path B 现在变成"评估网页工作流是否够用 vs 是否需要 API"

Week 5-6:
- 综述冲刺
- 如果网页工作流卡, 此时再快速接 API
