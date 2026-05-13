"""
cleaning_v2.py — Improved cleaning with section_header boundary detection.

Compared to cleaning_v1 (content_layer == 'body' filter only):
  - Detects body start: first 'Abstract' / 'Introduction' / '1.' section_header
  - Detects body end:   first 'References' / 'Acknowledgments' / 'Funding' /
                              'Conflict' / 'Data availability' / 'Author contributions'
  - Removes pre-body noise (title repeats, TOC, author affiliations, "You may also like")
  - Removes post-body noise (references, acknowledgments, ORCID, etc.)
  - Still uses content_layer == 'body' filter for furniture (page headers/footers)

Tested on 5 golden papers (P1, P5, P44, P77, P117): 17-35% additional reduction
over v1 cleaning, all references removed, all true body content preserved.
"""

import re
from collections import Counter

CLEANING_VERSION = "v2_section_boundary_body"

BODY_START_PATTERN = re.compile(
    r'^(abstract|introduction|1\.\s)',
    re.IGNORECASE
)

BODY_END_PATTERN = re.compile(
    r'^(references|bibliography|acknowledg(e?)ments?|funding|'
    r'conflict|data availability|author contributions|orcid)',
    re.IGNORECASE
)


def find_body_range(texts):
    """
    Find [start_idx, end_idx) covering true body content.
    
    Returns (start_idx, end_idx). If no markers found, returns (0, len(texts))
    as a fallback.
    """
    start_idx = 0
    end_idx = len(texts)
    
    # Find start: first 'Abstract' / 'Introduction' / '1.' section_header
    for i, t in enumerate(texts):
        if t.get('label') == 'section_header':
            txt = (t.get('text', '') or '').strip()
            if BODY_START_PATTERN.match(txt):
                start_idx = i
                break
    
    # Find end: first 'References' / 'Acknowledgments' / etc. after start
    for i in range(start_idx + 1, len(texts)):
        t = texts[i]
        if t.get('label') == 'section_header':
            txt = (t.get('text', '') or '').strip()
            if BODY_END_PATTERN.match(txt):
                end_idx = i
                break
    
    return start_idx, end_idx


def run_cleaning_v2(docling_json):
    """
    Apply section-boundary aware cleaning.
    
    Returns dict with same shape as v1, plus _cleaning provenance.
    """
    texts = docling_json.get('texts', [])
    start, end = find_body_range(texts)
    
    body_range = texts[start:end]
    
    # Still apply content_layer == 'body' filter for furniture rejection
    kept = [t for t in body_range if t.get('content_layer') == 'body']
    
    # Compute what was dropped for provenance
    pre_body  = texts[:start]
    post_body = texts[end:]
    furniture = [t for t in body_range if t.get('content_layer') != 'body']
    
    cleaned = {
        '_cleaning': {
            'version': CLEANING_VERSION,
            'body_range': [start, end],
            'total_input_blocks': len(texts),
            'kept_blocks': len(kept),
            'dropped_pre_body': len(pre_body),
            'dropped_post_body': len(post_body),
            'dropped_furniture_in_range': len(furniture),
            'dropped_label_distribution': dict(
                Counter(
                    t.get('label', '?') 
                    for t in (pre_body + post_body + furniture)
                )
            ),
        },
        'texts': kept,
    }
    
    return cleaned


def kept_as_markdown(cleaned):
    """Render kept texts as markdown for SOP input."""
    lines = []
    for t in cleaned['texts']:
        label = t.get('label', 'text')
        txt = (t.get('text', '') or '').strip()
        if not txt:
            continue
        if label == 'section_header':
            lines.append(f'\n## {txt}\n')
        else:
            lines.append(txt)
    return '\n\n'.join(lines)
