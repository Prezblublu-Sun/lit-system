# Day 2 行动卡 · v7 受控修复

## 启动语
"Day 2 开始,跑 Path A,先 v7"

## 目标
让 PaperQA2 在本地小模型栈下出至少一个完整 ANSWER,为 Week 4 决策留对照数据。

## 受控修复(v7 配置)
- Embedding: nomic-embed-text(替 bge-m3,避 NaN)
- LLM: qwen2.5-14b-8k(Modelfile 锁定 num_ctx=8192,温度 0.1)
- PaperQA2:
  - use_doc_details=False
  - multimodal=False
  - recurse_subdirectories=False
  - paper_directory 绝对路径

## v7 成功标准
- [ ] 5 篇 PDF 入库
- [ ] 至少 3/5 问题返回 ANSWER
- [ ] 回答带引用片段
- [ ] 日志无 NaN
- [ ] 4096 截断消失或显著减少

## v8 备案
如 v7 失败,只允许换一处:
- qwen2.5-14b-8k → qwen2.5:7b 或 qwen3:8b(更小更稳)
其他不动。

## 止损线
v7 + v8 都失败 → 停止调 PaperQA2,记录"本地化改造成本超预期",
直接走 Week 1-2 自建最小 RAG。PaperQA2 留作 Week 4 后期 benchmark。

## 执行命令(逐条贴 Claude 让带跑)

cd ~/lit-system
source .venv/bin/activate

# 1. 拉稳定 embedding
ollama pull nomic-embed-text

# 2. Modelfile 锁定上下文
cat > Modelfile.qwen14b-8k <<'MODELFILE_EOF'
FROM qwen2.5:14b
PARAMETER num_ctx 8192
PARAMETER temperature 0.1
MODELFILE_EOF

ollama create qwen2.5-14b-8k -f Modelfile.qwen14b-8k

# 3. 基础连通测试(必须两条都过再继续)
curl -s http://localhost:11434/api/embed -d '{
  "model": "nomic-embed-text",
  "input": "Scientific literature on biomaterials and 3D bioprinting."
}' | head -c 300

curl -s http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-14b-8k",
  "prompt": "What is RAG in one sentence?",
  "stream": false
}' | head -c 300

# 4. 改脚本:LLM 改 ollama/qwen2.5-14b-8k,EMBED 改 ollama/nomic-embed-text
# 5. 清旧索引:rm -rf ~/lit-system/index/paperqa_week0
# 6. 重跑:python scripts/week0_paperqa_test.py 2>&1 | tee results/week0_smoke_v7.log

## 重要提醒
- 换 embedding 模型必须重建索引(bge-m3 是 1024 维,nomic-embed-text 是 768 维,不兼容)
- 不要再让 Claude 替你做决定该往哪走;明天先看 5 个研究问题再启动
