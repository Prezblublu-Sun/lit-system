"""
Retrieval smoke test: 5 queries on lit_chunks_v1 (bge-m3 + Chroma).
Prints top-k chunks per query: paper_id, distance, section, text preview.
"""
import json
import requests
from pathlib import Path
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR   = PROJECT_ROOT / "assets" / "chroma_db"

OLLAMA_URL  = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"
COLLECTION  = "lit_chunks_v1"
TOP_K       = 5
PREVIEW_LEN = 250

QUERIES = [
    "machine learning models for predicting bioink printability",
    "computer vision for real-time monitoring of 3D bioprinting process",
    "AI optimization of bioprinting process parameters",
    "self-driving laboratories and automated bioprinting workflows",
    "deep learning for cell viability prediction after bioprinting",
]


def embed_query(text):
    r = requests.post(OLLAMA_URL, json={"model": EMBED_MODEL, "input": text}, timeout=60)
    r.raise_for_status()
    return r.json()["embeddings"][0]


client = chromadb.PersistentClient(path=str(CHROMA_DIR))
coll = client.get_collection(COLLECTION)
print(f"[setup] collection {COLLECTION!r}: {coll.count()} chunks")
print(f"[setup] embed model: {EMBED_MODEL}, top-k: {TOP_K}\n")

for qi, q in enumerate(QUERIES, 1):
    print(f"=== Q{qi}: {q} ===")
    qvec = embed_query(q)
    res = coll.query(
        query_embeddings=[qvec],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )
    docs  = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]
    ids   = res["ids"][0]
    for rank, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), 1):
        headers = meta.get("section_headers", "")
        # First non-header line, trimmed
        first_text = " ".join(doc.split())[:PREVIEW_LEN]
        print(f"  #{rank} {meta['paper_id']} c{meta['chunk_index']:04d}  dist={dist:.3f}  tok={meta['token_count']}")
        if headers:
            print(f"      sections: {headers[:120]}")
        print(f"      text: {first_text}...")
    print()

# Distribution sanity: how many distinct papers across top-5 of all queries?
print("=== distribution check ===")
for qi, q in enumerate(QUERIES, 1):
    qvec = embed_query(q)
    res = coll.query(query_embeddings=[qvec], n_results=TOP_K, include=["metadatas"])
    papers = [m["paper_id"] for m in res["metadatas"][0]]
    from collections import Counter
    c = Counter(papers)
    print(f"  Q{qi}: {dict(c)}")
