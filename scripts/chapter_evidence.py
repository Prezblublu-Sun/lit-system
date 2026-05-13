"""
chapter_evidence.py — Generate per-section evidence packages from chapter outline.

For each section in the outline YAML, runs:
  1. Semantic search in Chroma using section's `query` string (top N chunks)
  2. Direct lookup of `cited_dois` -> paper_id in the library
  3. Combines retrieved + cited papers, deduplicating
  4. Outputs a markdown file with title, DOI, top chunks, and metadata excerpts

Output: one file per section in results/chapter_evidence/

Usage:
  python scripts/chapter_evidence.py
  python scripts/chapter_evidence.py --top 10 --outline custom.yaml
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import chromadb
import requests
import yaml

ROOT = Path('/home/prezblublu/lit-system')
CHROMA_DIR = ROOT / 'assets' / 'chroma_db'
METADATA_DIR = ROOT / 'metadata'
RESULTS_DIR = ROOT / 'results' / 'chapter_evidence'
DEFAULT_OUTLINE = ROOT / 'decisions' / 'inputs' / 'chapter_outline.yaml'

OLLAMA_URL = 'http://localhost:11434/api/embed'
EMBED_MODEL = 'bge-m3'


def embed_query(text):
    r = requests.post(OLLAMA_URL, json={'model': EMBED_MODEL, 'input': [text]}, timeout=60)
    r.raise_for_status()
    return r.json()['embeddings'][0]


def build_doi_to_paper_index():
    """Build {doi: paper_id} mapping from all 124 metadata files."""
    index = {}
    for f in METADATA_DIR.glob('P*.json'):
        d = json.loads(f.read_text())
        pid = d['_paper_id']
        doi_field = d.get('source_block', {}).get('doi')
        if isinstance(doi_field, dict):
            doi = doi_field.get('value')
        else:
            doi = doi_field
        if doi:
            # Normalize: lowercase, strip "https://doi.org/" prefix if any
            doi_norm = doi.lower().replace('https://doi.org/', '').strip()
            index[doi_norm] = pid
    return index


def query_chroma(query_text, top_n=10):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    coll = client.get_collection('lit_chunks_v1')
    vec = embed_query(query_text)
    results = coll.query(
        query_embeddings=[vec],
        n_results=top_n,
        include=['documents', 'metadatas', 'distances'],
    )
    chunks = []
    for i in range(len(results['ids'][0])):
        chunks.append({
            'chunk_id': results['ids'][0][i],
            'paper_id': results['metadatas'][0][i].get('paper_id'),
            'text': results['documents'][0][i],
            'distance': results['distances'][0][i],
            'section_headers': results['metadatas'][0][i].get('section_headers', ''),
            'chunk_index': results['metadatas'][0][i].get('chunk_index'),
        })
    return chunks


def load_paper_metadata(paper_id):
    f = METADATA_DIR / f'{paper_id}.json'
    if not f.exists():
        return None
    return json.loads(f.read_text())


def render_section_package(section, retrieved_chunks, cited_papers, doi_to_paper):
    """Produce the markdown for one section."""
    out = []
    out.append(f"# Section {section['id']}: {section['title']}")
    out.append('')
    if 'target_words' in section:
        out.append(f"**Target words**: {section['target_words']}")
    out.append(f"**Query**: `{section.get('query', '(none)')}`")
    out.append(f"**Generated**: {datetime.now().isoformat()}")
    out.append('')
    if section.get('description'):
        out.append(f"_{section['description']}_")
        out.append('')
    out.append('---')
    out.append('')

    # === Part A: Explicitly cited DOIs (with content) ===
    out.append('## Part A: Explicitly cited references in outline (with content)')
    out.append('')
    cited_dois = section.get('cited_dois', [])
    if not cited_dois:
        out.append('_No explicitly cited DOIs in outline._')
        out.append('')
    else:
        # First, a quick summary list
        out.append('### Quick index')
        out.append('')
        for doi in cited_dois:
            doi_norm = doi.lower().replace('https://doi.org/', '').strip()
            pid = doi_to_paper.get(doi_norm)
            if pid:
                out.append(f"- ✅ **{pid}** — `{doi}` (in library)")
            else:
                out.append(f"- ❌ `{doi}` (NOT in library — need to ingest separately)")
        out.append('')
        
        # Then: for each in-library cited paper, retrieve its top chunks for this section query
        # using the section's query as relevance ranking
        section_query = section.get('query', section['title'])
        
        client_a = chromadb.PersistentClient(path=str(CHROMA_DIR))
        coll_a = client_a.get_collection('lit_chunks_v1')
        
        out.append('### Detailed content per cited paper')
        out.append('')
        
        for doi in cited_dois:
            doi_norm = doi.lower().replace('https://doi.org/', '').strip()
            pid = doi_to_paper.get(doi_norm)
            if not pid:
                continue  # Already noted as missing
            
            meta = load_paper_metadata(pid)
            if not meta:
                continue
            
            title = meta['source_block']['title']['value']
            
            out.append(f"#### 🎯 {pid}: {title[:80]}")
            out.append('')
            out.append(f"**DOI**: {doi}")
            out.append('')
            
            # Query Chroma for top 3 chunks from THIS paper, ranked by relevance to section query
            try:
                vec = embed_query(section_query)
                results_for_paper = coll_a.query(
                    query_embeddings=[vec],
                    n_results=5,
                    where={'paper_id': pid},
                    include=['documents', 'metadatas', 'distances'],
                )
                if results_for_paper['ids'] and results_for_paper['ids'][0]:
                    out.append('**Top 3 chunks from this paper (ranked by relevance to section query):**')
                    out.append('')
                    for i in range(len(results_for_paper['ids'][0])):
                        ci = results_for_paper['metadatas'][0][i].get('chunk_index')
                        d = results_for_paper['distances'][0][i]
                        text = results_for_paper['documents'][0][i]
                        if len(text) > 1200:
                            text = text[:1200] + '...'
                        out.append(f"_[{pid} chunk_{ci}, d={d:.3f}]_")
                        out.append('')
                        out.append(text)
                        out.append('')
                else:
                    out.append('_(no chunks found in Chroma for this paper)_')
                    out.append('')
            except Exception as e:
                out.append(f'_(error retrieving chunks: {e})_')
                out.append('')
            
            # Metadata excerpts (None-safe)
            def safe_get(d, *keys):
                for k in keys:
                    if not isinstance(d, dict):
                        return None
                    d = d.get(k)
                    if d is None:
                        return None
                return d
            
            bg = safe_get(meta, 'factual', 'sop_l1_background_raw', 'value') or '(missing)'
            problem = safe_get(meta, 'interpretive', 'core_problem_raw', 'value') or '(missing)'
            
            out.append('**Background:**')
            out.append(bg[:600] + ('...' if len(bg) > 600 else ''))
            out.append('')
            out.append('**Core problem:**')
            out.append(problem[:600] + ('...' if len(problem) > 600 else ''))
            out.append('')
            out.append('---')
            out.append('')

    # === Part B: Semantic search results ===
    out.append('## Part B: Semantic search results (Chroma top N)')
    out.append('')
    
    # Group chunks by paper, take best distance per paper
    by_paper = defaultdict(list)
    for c in retrieved_chunks:
        by_paper[c['paper_id']].append(c)
    
    # Mark which are also explicitly cited
    cited_pids = set()
    for doi in cited_dois:
        doi_norm = doi.lower().replace('https://doi.org/', '').strip()
        pid = doi_to_paper.get(doi_norm)
        if pid:
            cited_pids.add(pid)
    
    # Order papers by best distance
    papers_sorted = sorted(by_paper.items(), key=lambda kv: min(c['distance'] for c in kv[1]))
    
    for pid, chunks in papers_sorted:
        meta = load_paper_metadata(pid)
        if not meta:
            continue
        title = meta['source_block']['title']['value']
        doi_field = meta.get('source_block', {}).get('doi', {})
        doi = doi_field.get('value') if isinstance(doi_field, dict) else doi_field
        
        cited_mark = ' 🎯 (also cited in outline)' if pid in cited_pids else ''
        out.append(f"### {pid}: {title[:80]}{cited_mark}")
        out.append('')
        out.append(f"**DOI**: {doi or '_missing_'}")
        out.append(f"**Best distance**: {min(c['distance'] for c in chunks):.3f}")
        out.append(f"**Chunks retrieved**: {len(chunks)}")
        out.append('')
        
        out.append('**Retrieved chunks:**')
        out.append('')
        for c in sorted(chunks, key=lambda x: x['distance']):
            out.append(f"_[{pid} chunk_{c['chunk_index']}, d={c['distance']:.3f}]_")
            out.append('')
            text = c['text']
            if len(text) > 1200:
                text = text[:1200] + '...'
            out.append(text)
            out.append('')
        
        # Brief metadata excerpts (SOP_v2 has pollution, SOP_v3 is clean)
        def safe_get(d, *keys):
            for k in keys:
                if not isinstance(d, dict):
                    return None
                d = d.get(k)
                if d is None:
                    return None
            return d
        
        bg = safe_get(meta, 'factual', 'sop_l1_background_raw', 'value') or '(missing)'
        out.append('**Background (from SOP metadata):**')
        out.append(bg[:600] + ('...' if len(bg) > 600 else ''))
        out.append('')
        
        problem = safe_get(meta, 'interpretive', 'core_problem_raw', 'value') or '(missing)'
        out.append('**Core problem & critique:**')
        out.append(problem[:600] + ('...' if len(problem) > 600 else ''))
        out.append('')
        out.append('---')
        out.append('')
    
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outline', default=str(DEFAULT_OUTLINE), help='Path to YAML outline')
    parser.add_argument('--top', type=int, default=12, help='Top N chunks per section (semantic search)')
    parser.add_argument('--sections', default=None, help='Comma-separated section IDs (default: all)')
    parser.add_argument('--merge', action='store_true', help='After generating sections, write a single master document combining all sections')
    parser.add_argument('--merge-only', action='store_true', help='Skip generation; just merge existing section files into master')
    args = parser.parse_args()
    
    outline = yaml.safe_load(Path(args.outline).read_text())
    sections = outline['sections']
    
    if args.sections:
        wanted = set(s.strip() for s in args.sections.split(','))
        sections = [s for s in sections if s['id'] in wanted]
    
    print(f"Loading outline: {args.outline}")
    print(f"Sections to process: {len(sections)}")
    print(f"Top N chunks per section: {args.top}")
    print()
    
    print("Building DOI -> paper_id index...")
    doi_to_paper = build_doi_to_paper_index()
    print(f"Indexed {len(doi_to_paper)} papers with DOI")
    print()
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Manifest
    manifest = []
    
    for i, section in enumerate(sections, 1):
        sec_id = section['id']
        query = section.get('query', section['title'])
        print(f"[{i}/{len(sections)}] {sec_id}: {section['title'][:50]}")
        print(f"    query: {query[:60]}")
        
        try:
            chunks = query_chroma(query, top_n=args.top)
        except Exception as e:
            print(f"    ERROR querying Chroma: {e}")
            continue
        
        # Resolve cited DOIs to paper IDs (for reporting only - rendering done in render)
        cited_papers = []
        for doi in section.get('cited_dois', []):
            doi_norm = doi.lower().replace('https://doi.org/', '').strip()
            pid = doi_to_paper.get(doi_norm)
            if pid:
                cited_papers.append({'doi': doi, 'paper_id': pid, 'in_library': True})
            else:
                cited_papers.append({'doi': doi, 'paper_id': None, 'in_library': False})
        
        n_in_lib = sum(1 for c in cited_papers if c['in_library'])
        n_total_cited = len(cited_papers)
        n_unique_papers_retrieved = len(set(c['paper_id'] for c in chunks))
        
        print(f"    cited in outline: {n_total_cited} ({n_in_lib} in library)")
        print(f"    retrieved: {len(chunks)} chunks from {n_unique_papers_retrieved} papers")
        
        package = render_section_package(section, chunks, cited_papers, doi_to_paper)
        
        # Safe filename
        safe_id = sec_id.replace('.', '_')
        out_file = RESULTS_DIR / f"section_{safe_id}.md"
        out_file.write_text(package)
        print(f"    wrote: {out_file.name} ({len(package):,} chars)")
        
        manifest.append({
            'section_id': sec_id,
            'title': section['title'],
            'target_words': section.get('target_words'),
            'file': str(out_file.name),
            'chars': len(package),
            'n_chunks_retrieved': len(chunks),
            'n_unique_papers_retrieved': n_unique_papers_retrieved,
            'n_cited_total': n_total_cited,
            'n_cited_in_library': n_in_lib,
        })
        print()
    
    # Write manifest
    manifest_path = RESULTS_DIR / '_manifest.json'
    manifest_path.write_text(json.dumps({
        'chapter': outline.get('chapter', {}),
        'generated': datetime.now().isoformat(),
        'top_n_per_section': args.top,
        'sections': manifest,
    }, indent=2))
    print(f"Manifest: {manifest_path}")
    
    # Master document: concatenate all section files
    if args.merge or args.merge_only:
        master_lines = [
            f"# {outline.get('chapter', {}).get('title', 'Chapter')} — Master Evidence Document",
            "",
            f"**Source**: lit-system v0.1.0",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Sections**: {len(outline['sections'])}",
            f"**Authors**: {outline.get('chapter', {}).get('authors', '(unknown)')}",
            "",
            "## How to use this document",
            "",
            "This is a comprehensive evidence package for ALL sections of the chapter.",
            "Each section has: (a) outline-cited papers with their chunks + metadata,",
            "(b) semantic-search results from the 124-paper bioprinting library.",
            "",
            "Use this for:",
            "- Cross-section consistency check before writing",
            "- Identifying papers that span multiple sections",
            "- Finding gaps in citation coverage",
            "",
            "For writing a SINGLE section, use the corresponding section_X_X.md file instead.",
            "",
            "## Table of contents",
            "",
        ]
        
        # TOC
        for s in outline['sections']:
            sec_id = s['id']
            safe_id = sec_id.replace('.', '_')
            master_lines.append(f"- [{sec_id} {s['title'][:80]}](#section-{safe_id.lower()})")
        master_lines.append("")
        master_lines.append("---")
        master_lines.append("")
        
        # Concatenate each section file (with anchor)
        total_chars = 0
        for s in outline['sections']:
            sec_id = s['id']
            safe_id = sec_id.replace('.', '_')
            section_file = RESULTS_DIR / f"section_{safe_id}.md"
            if not section_file.exists():
                master_lines.append(f"_(missing: {section_file.name})_")
                continue
            content_str = section_file.read_text()
            # Add anchor
            master_lines.append(f'<a id="section-{safe_id.lower()}"></a>')
            master_lines.append(content_str)
            master_lines.append("")
            master_lines.append("---")
            master_lines.append("")
            total_chars += len(content_str)
        
        master_text = chr(10).join(master_lines)
        master_path = RESULTS_DIR / '_chapter_master.md'
        master_path.write_text(master_text)
        print()
        print(f"Master document: {master_path}")
        print(f"Size: {len(master_text):,} chars (~{len(master_text)//4:,} tokens)")
        print(f"  - merged from {len(outline['sections'])} section files")
        print(f"  - sections subtotal: {total_chars:,} chars")


if __name__ == '__main__':
    main()
