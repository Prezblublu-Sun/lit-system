"""
topic_evidence.py — Generate evidence package for a given topic.

Given a topic query (e.g. "in-printing monitoring"), retrieves top N chunks 
from Chroma, then for each unique paper, assembles:
  - Title + DOI
  - Top chunks (with their text)
  - Full metadata (background, methods, problem, scoring summary)
  - Personal relevance hint

Output: a markdown file ready to upload to Web Claude / GPT for synthesis.

Usage:
  python scripts/topic_evidence.py "in-printing monitoring" --top 10
  python scripts/topic_evidence.py "bioink rheology" --top 8 --output bioink_rheology.md
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import chromadb
import requests

ROOT = Path('/home/prezblublu/lit-system')
CHROMA_DIR = ROOT / 'assets' / 'chroma_db'
METADATA_DIR = ROOT / 'metadata'
RESULTS_DIR = ROOT / 'results'
OLLAMA_URL  = 'http://localhost:11434/api/embed'
EMBED_MODEL = 'bge-m3'


def embed_query(text):
    """Embed query text using same bge-m3 model as the index."""
    r = requests.post(OLLAMA_URL, json={'model': EMBED_MODEL, 'input': [text]}, timeout=60)
    r.raise_for_status()
    return r.json()['embeddings'][0]


def query_chroma(topic, top_n=15):
    """Retrieve top N chunks for topic using bge-m3 embedding."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection('lit_chunks_v1')
    
    query_vec = embed_query(topic)
    
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_n,
        include=['documents', 'metadatas', 'distances'],
    )
    
    chunks = []
    for i in range(len(results['ids'][0])):
        chunks.append({
            'chunk_id':  results['ids'][0][i],
            'paper_id':  results['metadatas'][0][i].get('paper_id'),
            'text':      results['documents'][0][i],
            'distance':  results['distances'][0][i],
            'section_headers': results['metadatas'][0][i].get('section_headers', ''),
            'chunk_index':     results['metadatas'][0][i].get('chunk_index'),
        })
    return chunks


def load_paper_metadata(paper_id):
    """Load metadata for one paper."""
    f = METADATA_DIR / f'{paper_id}.json'
    if not f.exists():
        return None
    return json.loads(f.read_text())


def assemble_package(topic, chunks, output_path):
    """Write the topic evidence package."""
    # Group chunks by paper
    chunks_by_paper = defaultdict(list)
    for c in chunks:
        chunks_by_paper[c['paper_id']].append(c)
    
    out = [
        f'# Topic Evidence Package: "{topic}"',
        '',
        f'**Source**: lit-system v0.1.0 — Chroma `lit_chunks_v1`',
        f'**Generated**: {datetime.now().isoformat()}',
        f'**Total chunks retrieved**: {len(chunks)}',
        f'**Unique papers**: {len(chunks_by_paper)}',
        '',
        '**Note**: This is SOP_v2 metadata (has known pollution: some fake page',
        'references and markdown artifacts). Use chunks for quotes; use metadata',
        'fields for context but verify all specific claims against original PDFs.',
        '',
        '---',
        '',
    ]
    
    # Order papers by best (lowest) distance
    papers_ordered = sorted(
        chunks_by_paper.items(),
        key=lambda kv: min(c['distance'] for c in kv[1])
    )
    
    for paper_id, paper_chunks in papers_ordered:
        meta = load_paper_metadata(paper_id)
        if not meta:
            continue
        
        title = meta['source_block']['title']['value']
        doi_field = meta.get('source_block', {}).get('doi')
        if isinstance(doi_field, dict):
            doi = doi_field.get('value')
        else:
            doi = doi_field
        
        # Aggregate chunks for this paper
        out.append(f'## {paper_id}: {title}')
        out.append('')
        out.append(f'**DOI**: {doi or "(missing)"}')
        out.append(f'**Best distance**: {min(c["distance"] for c in paper_chunks):.3f}')
        out.append(f'**Chunks retrieved**: {len(paper_chunks)}')
        out.append('')
        
        # Show each chunk
        out.append('### Retrieved chunks (in order of relevance)')
        out.append('')
        for c in sorted(paper_chunks, key=lambda x: x['distance']):
            out.append(f'**[{paper_id} chunk_{c["chunk_index"]}]** _(d={c["distance"]:.3f})_')
            out.append('')
            # Trim text to ~600 chars to keep package compact
            text = c['text']
            if len(text) > 1000:
                text = text[:1000] + '...'
            out.append(text)
            out.append('')
        
        # Metadata excerpts
        out.append('### Paper context (from metadata, SOP_v2)')
        out.append('')
        
        bg = meta['factual']['sop_l1_background_raw']['value']
        out.append('**Background:**')
        out.append(bg[:600] + ('...' if len(bg) > 600 else ''))
        out.append('')
        
        methods = meta['factual']['methods_raw']['value']
        out.append('**Methods:**')
        out.append(methods[:600] + ('...' if len(methods) > 600 else ''))
        out.append('')
        
        problem = meta['interpretive']['core_problem_raw']['value']
        out.append('**Core problem & critique:**')
        out.append(problem[:600] + ('...' if len(problem) > 600 else ''))
        out.append('')
        
        out.append('---')
        out.append('')
    
    Path(output_path).write_text('\n'.join(out))
    return len('\n'.join(out))


def main():
    parser = argparse.ArgumentParser(description='Build topic evidence package')
    parser.add_argument('topic', help='Topic query (e.g. "in-printing monitoring")')
    parser.add_argument('--top', type=int, default=12, help='Number of chunks to retrieve (default 12)')
    parser.add_argument('--output', default=None, help='Output filename (default: results/topic_evidence_<slug>.md)')
    args = parser.parse_args()
    
    if not args.output:
        slug = re.sub(r'[^a-z0-9]+', '_', args.topic.lower()).strip('_')[:50]
        args.output = str(RESULTS_DIR / f'topic_evidence_{slug}.md')
    
    print(f'Topic: "{args.topic}"')
    print(f'Retrieving top {args.top} chunks from Chroma...')
    chunks = query_chroma(args.topic, top_n=args.top)
    
    papers = set(c['paper_id'] for c in chunks)
    print(f'Retrieved {len(chunks)} chunks from {len(papers)} unique papers')
    print(f'Top 5 chunks:')
    for c in chunks[:5]:
        print(f'  [{c["paper_id"]} c{c["chunk_index"]}] d={c["distance"]:.3f}')
    
    print(f'\nAssembling package...')
    size = assemble_package(args.topic, chunks, args.output)
    print(f'Wrote: {args.output}')
    print(f'Size: {size:,} chars (~{size//4:,} tokens)')


if __name__ == '__main__':
    main()
