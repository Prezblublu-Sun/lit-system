
---

## 用户进一步明确 (第三次)

### 原话
"这个大文件应该是在独立处理过每一个论文单篇之后整理出来的新文件, 
 不需要一开始就生成"

### 含义 (架构原则定型)
**单篇 metadata.json 是主资产, export 是派生视图**

不是: PDF -> 直接生成大文件
是  : PDF -> metadata.json (持久化) -> export 拼成大文件 (按需重跑)

### 这条原则的好处
- 单篇只跑一次, 聚合多次 (省 GPU 时间)
- 增量更新自然: 新论文只跑那一篇, 不重跑全库
- 一致性: 跑两次 export 结果完全一致
- 调试: 单篇 metadata 可独立 review
- 完美对齐 ADR-0003 (metadata.json 是 schema 主体)

### 数据流定型

[阶段 1 单篇处理, 一次性]:
  PDF -> Docling 解析
       -> chunks.jsonl (持久)
       -> paper.md (持久)
       -> metadata.json (持久, 含 factual / interpretive / personal_relevance)

[阶段 2 单篇 review, 人工介入]:
  metadata.json 的 interpretive / personal_relevance 字段
  -> 人工 review 或商业 LLM 复审
  -> _meta.reviewed_by 字段更新

[阶段 3 聚合导出, 按需多次]:
  N 份 metadata.json + review_outline.md
  -> export_corpus.py --topic <section>
  -> literature_corpus_{topic}.md (轻量, 派生)

### Week 2 实现优先级修订

不是一开始就写 export_corpus.py
是先把单篇 pipeline 做完, 再做 export

Week 2 顺序:
1. Docling 跑通 P1 一篇 -> 产 metadata.json (符合 schema v1)
2. 跑通 5 篇黄金集 -> 5 份 metadata.json
3. 然后再写 export_corpus.py, 把 5 份 JSON 聚合成 1 份 md

这样 export 一上来就有真实数据测试, 不是空跑。

### 含义对 schema 的反向要求

ADR-0003 schema 必须保证:
1. metadata.json 是完全自包含的 (不需要读 PDF 就能聚合)
2. 引文片段 (key_quotes) 要存在 metadata.json 里, 不能让 export 时再从 chunks.jsonl 捞
3. 每个字段的 evidence 字段要含原文片段, 不只是 page 引用

这条要写进 ADR-0003 v1.1 修订记录。

---

## 容量与按主题分组(补遗,第一次追加丢失了重写)

### 网页 chat 上下文窗口 (2026)
- ChatGPT (GPT-5.4): 128K
- Claude.ai (Sonnet/Opus): 200K 默认, 1M beta
- Gemini: 1M

### 每篇精炼资产 ~2000 token
- 元数据 + factual + 5 条引文 + interpretive + personal_relevance

### 单文件容纳
- 50 篇 ≈ 100K (Claude 安全)
- 100 篇 ≈ 200K (Claude 上限)
- 300 篇 ≈ 600K (需要 1M beta 或 Gemini)

### 实际方案: 按主题分组
不是单一巨型文件, 而是多个主题文件:
- literature_corpus_AI_bioink.md
- literature_corpus_robotic_in_situ.md
- literature_corpus_realtime_control.md
每个对应纲要某一章节, 在那章节深度 chat。

### export_corpus.py 参数 (Week 2 实现)
- --topic <section_id>   按纲要章节过滤
- --max-tokens <N>       上限默认 150K
- --include-quotes <N>   每篇引文数默认 5
- --output <path>        输出路径
