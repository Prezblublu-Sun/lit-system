"""
Incremental Chroma upsert: embed only new chunks, upsert into existing collection.
Idempotent: re-running over the same chunks just re-upserts (same ids).
"""
import json
import time
import requests
from pathlib import Path

OLLAMA_URL  = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"
EMBED_DIM   = 1024
COLLECTION  = "lit_chunks_v1"
BATCH_SIZE  = 16


def get_or_create_collection(chroma_dir: Path):
    import chromadb
    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    try:
        coll = client.get_collection(COLLECTION)
        return client, coll, False
    except Exception:
        coll = client.create_collection(
            name=COLLECTION,
            metadata={
                "embedding_model": EMBED_MODEL,
                "dim": EMBED_DIM,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
        )
        return client, coll, True


def embed_batch(texts):
    r = requests.post(OLLAMA_URL,
                      json={"model": EMBED_MODEL, "input": texts},
                      timeout=300)
    r.raise_for_status()
    return r.json()["embeddings"]


def chunks_to_payload(chunks):
    """Flatten chunk dicts -> (ids, docs, metas) for Chroma."""
    ids, docs, metas = [], [], []
    for c in chunks:
        ids.append(c["chunk_id"])
        docs.append(c["text"])
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
    return ids, docs, metas


def upsert_chunks(coll, chunks):
    """Embed (in batches) + upsert. Returns elapsed seconds."""
    t0 = time.time()
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i+BATCH_SIZE]
        ids, docs, metas = chunks_to_payload(batch)
        vecs = embed_batch(docs)
        coll.upsert(ids=ids, documents=docs, embeddings=vecs, metadatas=metas)
    return round(time.time() - t0, 1)


def remove_paper(coll, paper_id):
    """Remove all chunks of a given paper_id (for --force re-ingest)."""
    try:
        coll.delete(where={"paper_id": paper_id})
        return True
    except Exception as e:
        print(f"  [chroma] warn: delete paper_id={paper_id} failed: {e}")
        return False


def chunks_for_paper(coll, paper_id):
    """Count existing chunks for paper_id."""
    try:
        result = coll.get(where={"paper_id": paper_id}, include=[])
        return len(result.get("ids", []))
    except Exception:
        return 0


def load_chunks_jsonl(path: Path):
    chunks = []
    for line in open(path):
        chunks.append(json.loads(line))
    return chunks
