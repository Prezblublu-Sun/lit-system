# lit-system 使用手册

本文档讲怎么用这个系统做综述写作和学术研究。
对应 ADR-0004 Path C(本地数据底座 + 网页 LLM 合成)的实际工作流。

---

## 1. 系统的三层架构

  Layer 1: 你脑子里 —— 综述 outline 和写作意图
  Layer 2: lit-system —— 数据底座,提供素材
  Layer 3: Claude/GPT 网页 —— 合成层,负责"读素材 → 写段落"

lit-system 不替你写综述,它替你做"查找、比较、关联"这 70% 繁琐工作。
论点构造 / 批判评估 / 写作风格这 30% 仍然是你。

---

## 2. 综述写作完整流程

### 阶段 1: 写 outline(你自己 + 可借 Claude 网页讨论)

先有 outline 才有"我要找什么"。每节是一个主题坑位。
示例:

  1. Introduction
  2.1 Bioink design via ML
  2.2 Nozzle / printability prediction
  3.1 Process monitoring

### 阶段 2: 对每个小节,从系统找素材(三种方式)

**方式 A: 语义检索(找具体内容)**

    ~/lit-system/.venv/bin/python scripts/retrieve_test_v1.py \
      --query "ML prediction of cell viability extrusion bioprinting" --top 8

返回最相关的 chunks(原文段落 + paper_id + section + similarity)。
这是写一节综述最常用的入口。

**方式 B: Metadata 筛选(找特定类型的论文)**

    ~/lit-system/.venv/bin/python -c "
    import json
    from pathlib import Path
    hits = []
    for p in sorted(Path('metadata').glob('P*.json')):
        d = json.load(p.open())
        title = d['source_block']['title']['value']
        if 'review' in title.lower():
            hits.append((d['_paper_id'], title))
    print(f'{len(hits)} reviews:')
    for pid, t in hits:
        print(f'  {pid}: {t[:80]}')
    "

(Schema v2 落地后能按 article_type / status / domain / themes 过滤)

**方式 C: 跨论文比较**

    ~/lit-system/.venv/bin/python -c "
    import json
    for pid in ['P5', 'P11', 'P89']:
        d = json.load(open(f'metadata/{pid}.json'))
        print(f'=== {pid}: {d[\"source_block\"][\"title\"][\"value\"][:60]} ===')
        print('METHODS:', d['factual'].get('methods_raw', {}).get('value', '')[:300])
        print()
    "

### 阶段 3: 综述合成(走 Claude/GPT 网页 chat = Path C)

3a. 把检索到的 chunks 整理成"素材包",格式示例:

    我要写综述的小节 "4.1 Cell viability prediction in bioprinting"

    相关文献(从我本地 RAG 检索):

    【P5】Mass-customizable bioprinting (2024)
      方法: Gaussian process regression
      输入: wall shear stress, exposure time, nozzle geometry
      输出: as-extruded cell viability
      限制: 仅 hydrogel A/B 验证,跨 bioink 泛化未证明

    【P11】Real-time monitoring with DNN (2023)
      方法: CNN + LSTM
      训练数据: 5000 张过程图像
      准确率: R²=0.91
      限制: 仅 extrusion-based,inkjet 不适用

    请帮我写这一节(约 600 字),要求:
      - 按 method-by-method 组织
      - 标出每篇 unique contribution
      - 段落末引用我标的 paper_id
      - 段尾点出剩余的 open challenge

3b. 粘到 claude.ai(或 GPT/Gemini),拿合成段落
3c. 审稿 —— 必须对着检索到的 chunks 验证内容,避免幻觉
3d. 改写成你的语气,把 P5 替换成真 citation(从 metadata 的 doi/author 拿)
3e. 重复 3a-3d 每节,4 小时/节,整篇综述 1-3 周

---

## 3. 系统能帮你节省的具体时间

| 任务 | 以前 | 现在 |
|---|---|---|
| "库里有没有这个主题的文章" | 翻 EndNote/Excel,20 分钟 | retrieve_test_v1 30 秒 |
| 跨论文方法对比 | 开 5 PDF 来回找,1-2 小时 | 读 metadata.factual.methods,10 分钟 |
| 发现"忘记自己有的"论文 | 凭记忆,经常漏 | 语义检索不依赖记忆 |
| 网页快筛 50 篇新论文 | 8 小时 | 4 小时(Schema v2 后) |

---

## 4. 系统不能帮你做的事(诚实清单)

- 替你想综述论点(outline 必须你自己)
- 替你写 citation(DOI 在 metadata,你 copy 进 BibTeX)
- 保证 Claude/GPT 网页写的段落 100% 准确(你必须审稿)
- 替你填 Status / Priority / Review Use(策略字段,人工判断)
- 判断"这篇该不该纳入综述"(学术判断只能你做)

---

## 5. 典型场景手册

### 场景 5.1 接到一篇新 PDF

    cp ~/Downloads/new.pdf inbox/
    ~/lit-system/.venv/bin/python scripts/scan_library.py
    ~/lit-system/.venv/bin/python scripts/ingest.py inbox/<doc_id>.pdf
    # 8 分钟后 metadata/P{n}.json 落档,自动进 Chroma

### 场景 5.2 找"用 Bayesian 优化的股骨柄"那篇

    ~/lit-system/.venv/bin/python scripts/retrieve_test_v1.py \
      --query "Bayesian optimization femoral stem implant" --top 5

返回 paper_id 后,看 metadata 找文件名 / DOI / 原 PDF 路径。

### 场景 5.3 跑 5 个 query 评估"库里覆盖度"

如果想写一节但不确定库里素材够不够,跑 5-8 个不同 query,
看返回的 paper_id 集合 → 缺什么主题就该再下 / ingest 几篇。

### 场景 5.4 大于 100 篇的批量入库 (tmux 后台)

    tmux new-session -d -s ingest_batch \
      "cd ~/lit-system && \
       ~/lit-system/.venv/bin/python scripts/ingest.py \
         \$(cat results/my_todo.txt) 2>&1 | tee results/my.log"

    tmux ls
    tmux attach -t ingest_batch   # 看进度,Ctrl+B d 离开
    tail -50 results/my.log

doc_id 去重保证重启或中断后不重复 ingest。

### 场景 5.5 大批量入库时跳过 SOP_v2 (节省 5x 时间)

主题超出 SOP_v2 适用范围时(比如金属 AM 用 bioprinting 的 SOP 没意义):

    ~/lit-system/.venv/bin/python scripts/ingest.py --no-sop inbox/*.pdf

仍生成 chunks 和 Chroma 入库 (可被检索),只跳过 5 个 LLM 抽取任务。
Week 3 引入领域专属 SOP 后,可以 --force 重 ingest 补 metadata。

---

## 6. 跟你三个 Excel 数据库的对接

你在 light-responsive / 股骨柄 / bioprinting 三个 Excel 工作流的 schema 是
一致的: 网页快筛(Web_Screening, /49 分) + 全文入库(Main_DB) + 写作用途
(Suggested Section / Review Use / Author Line)。

对应 lit-system:

| Excel 流程 | lit-system 对应 |
|---|---|
| 在网上搜到一篇 | 下 PDF 到 inbox/ |
| 看 abstract + /49 评分 | ingest 跑 SOP_v2,interpretive.scoring 字段 |
| 决定 status / priority / review_use | 人工编辑 metadata.workflow 字段(Schema v2) |
| 填进 Main_Database | metadata/P{n}.json 自动 |
| 写综述按 Suggested Section 找 | 检索 + writing_use 字段过滤 |

Schema v2(Week 3 落地)后, metadata 包含人工策划字段, 系统成为你 Excel 的
自动化版本但同时支持向量检索。导出可一键变 Excel Main_DB 格式。

---

## 7. 命令速查

| 想做 | 命令 |
|---|---|
| 看库里有几篇 | `ls metadata/P*.json \| wc -l` |
| 找一篇的 DOI | `python -c "import json; d=json.load(open('metadata/P{n}.json')); print(d['source_block']['doi']['value'])"` |
| 语义检索 | `python scripts/retrieve_test_v1.py --query "..." --top N` |
| 加新 PDF | `cp X.pdf inbox/ && python scripts/scan_library.py && python scripts/ingest.py inbox/<doc_id>.pdf` |
| 后台批量 | `tmux new-session -d -s name "...ingest.py $(cat todo.txt)..."` |
| 看 tmux 任务 | `tmux ls` / `tmux attach -t name` / Ctrl+B d 离开 |
| 看 ingest 日志 | `tail -50 results/ingest_xxx.log` |
| 重 ingest 一篇 | `python scripts/ingest.py --force inbox/<doc_id>.pdf` |
| 轻量 ingest(跳 SOP) | `python scripts/ingest.py --no-sop inbox/*.pdf` |
| GPU 状态 | `nvidia-smi --query-gpu=utilization.gpu,memory.used,temperature.gpu --format=csv` |

---

## 8. 熟练后的速度参考

| 任务 | 时间 |
|---|---|
| 写一节 600 字综述(用系统配 Claude 网页) | 30-60 分钟 |
| 接到新 PDF → 入库 → 可检索 | 9 分钟(完整 ingest)/ 1 分钟(--no-sop) |
| 写整篇综述 6-8 节纯写作 | 3-6 小时 |
| 全综述含 outline / 审稿 / citation | 1-3 周 |

---

## 9. 注意事项

- ingest 用 GPU 满载,期间机器其他 GPU 任务会慢
- 关 ssh 不影响 tmux 后台 ingest
- Chroma 数据库不进 git, 但 metadata 进 git
- 已 ingest 的 paper(doc_id 去重)不会被重复跑除非 --force
- 中文 / 英文 query 都能用(bge-m3 跨语言)
- DOI 抽取用 LLM 抽 title 后查 CrossRef, P6 验证 sim=1.00 可信

---

## 10. 后续路线

- Week 3: Schema v2(吸收 Excel 字段) + domain filter 检索 + 细分多标签
- Week 5-6: 综述写作辅助层(目前手动复制粘贴, 未来可半自动)
- 长远: 通用学术知识库, 跨课题积累
