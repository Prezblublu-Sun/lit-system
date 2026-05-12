"""
Embed all chunks with bge-m3 via Ollama, store in Chroma.
- Ollama /api/embed (batch supported)
- Chroma persistent client at assets/chroma_db/
- One collection: lit_chunks_v1
- All chunk metadata flattened into Chroma metadata fields (Chroma supports
  scalar metadata only; nested objects like provenance are JSON-stringified.)
"""
import json
import time
import requests
from pathlib import Path
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR   = PROJECT_ROOT / "assets" / "chunks"
CHROMA_DIR   = PROJECT_ROOT / "assets" / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"
COLLECTION  = "lit_chunks_v1"
BATCH_SIZE  = 16  # bge-m3 batch via Ollama

PAPERS = ["P1", "P2", "P3", "P4", "P5"]


def embed_batch(texts):
    """Call Ollama batch embed. Returns list of vectors."""
    r = requests.post(OLLAMA_URL, json={"model": EMBED_MODEL, "input": texts}, timeout=300)
    r.raise_for_status()
    return r.json()["embeddings"]


# Load all chunks
all_chunks = []
for pid in PAPERS:
    path = CHUNKS_DIR / f"{pid}_chunks.jsonl"
    if not path.exists():
        print(f"[skip] {pid}: no chunks file")
        continue
    for line in open(path):
        all_chunks.append(json.loads(line))
print(f"[setup] loaded {len(all_chunks)} chunks from {len(PAPERS)} papers")

# Init Chroma
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
# Reset collection if exists (idempotent runs)
try:
    client.delete_collection(COLLECTION)
    print(f"[setup] deleted existing collection {COLLECTION!r}")
except Exception:
    pass
coll = client.create_collection(
    name=COLLECTION,
    metadata={
        "embedding_model": EMBED_MODEL,
        "dim": 1024,
        "chunker_version": "token_window_chunker_v2",
        "cleaning_version": "v1_content_layer_body",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    },
)

# Embed + upsert in batches
t0 = time.time()
for i in range(0, len(all_chunks), BATCH_SIZE):
    batch = all_chunks[i:i+BATCH_SIZE]
    texts = [c["text"] for c in batch]
    t_start = time.time()
    vecs = embed_batch(texts)
    t_embed = time.time() - t_start

    # Build Chroma payloads (metadata must be scalar)
    ids = [c["chunk_id"] for c in batch]
    metas = []
    for c in batch:
        metas.append({
            "doc_id":          c["doc_id"],
            "paper_id":        c["paper_id"],
            "chunk_index":     c["chunk_index"],
            "chunk_type":      c["chunk_type"],
            "token_count":     c["token_count"],
            "block_count":     c["block_count"],
            "block_start":     c["block_index_range"][0],
            "block_end":       c["block_index_range"][1],
            "section_headers": " | ".join(c.get("section_headers_seen") or []),
            "provenance_json": json.dumps(c.get("provenance", []), ensure_ascii=False),
            "chunker_version": c["_meta"]["chunker_version"],
        })

    coll.upsert(ids=ids, documents=texts, embeddings=vecs, metadatas=metas)
    print(f"  batch {i//BATCH_SIZE + 1}/{(len(all_chunks)+BATCH_SIZE-1)//BATCH_SIZE}: "
          f"{len(batch)} chunks, embed {t_embed:.1f}s")

elapsed = time.time() - t0
print(f"\n[done] {coll.count()} chunks in collection {COLLECTION!r}")
print(f"       total {elapsed:.1f}s, avg {elapsed/len(all_chunks)*1000:.0f}ms/chunk")
print(f"       persisted to {CHROMA_DIR}")
