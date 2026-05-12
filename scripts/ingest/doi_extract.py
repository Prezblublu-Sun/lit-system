"""
DOI extraction with two strategies:
  1. regex over Docling markdown (fast, ~60-80% recall)
  2. CrossRef API fallback (title + author lookup, ~95% recall)
Returns (doi: str | None, method: str, score: float | None)
"""
import re
import requests
import difflib

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)

CROSSREF_API   = "https://api.crossref.org/works"
USER_AGENT     = "lit-system/0.1 (research; mailto:noreply@lit-system.local)"
MIN_SCORE      = 20.0
MIN_TITLE_SIM  = 0.60
REQUEST_TIMEOUT = 15


def _title_similarity(a: str, b: str) -> float:
    """Char-level ratio 0-1, case-insensitive."""
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def extract_doi_from_text(text: str, char_limit: int = 20000):
    """
    Scan early portion of text for DOI pattern. Return first reasonable match.
    Skips DOIs found in reference-list contexts (after 'References' header).
    """
    head = text[:char_limit]
    # Cut at references header if present (defensive; should already be cleaned)
    ref_match = re.search(r"\n##\s+(references|bibliography)\s*\n", head, re.IGNORECASE)
    if ref_match:
        head = head[:ref_match.start()]
    matches = DOI_RE.findall(head)
    seen = []
    for m in matches:
        m = m.rstrip(").,;]")
        if m not in seen:
            seen.append(m)
    return seen[0] if seen else None


def lookup_doi_via_crossref(title: str, author_lastname: str = "", year: int = None):
    """
    Query CrossRef. Returns (doi, score) if confident match, else (None, None).
    """
    params = {
        "query.title": title,
        "rows": 5,
        "select": "DOI,title,author,issued,score",
    }
    if author_lastname:
        params["query.author"] = author_lastname

    try:
        r = requests.get(
            CROSSREF_API,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
    except Exception as e:
        return None, None, f"crossref_error:{e}"

    items = r.json().get("message", {}).get("items", [])
    if not items:
        return None, None, "no_results"

    top = items[0]
    doi   = top.get("DOI")
    score = top.get("score", 0)
    titles = top.get("title", []) or [""]
    top_title = titles[0]
    sim = _title_similarity(title, top_title) if top_title else 0.0

    if score < MIN_SCORE:
        return None, None, f"low_score:{score:.1f}"
    if sim < MIN_TITLE_SIM:
        return None, None, f"low_title_sim:{sim:.2f}"
    return doi, score, f"matched:sim={sim:.2f}"


def get_doi(text: str, title: str = "", author_lastname: str = "", year: int = None):
    """
    Two-stage DOI extraction.
    Returns dict: {"doi": str|None, "method": str, "details": str}
    """
    # Stage 1: regex
    doi = extract_doi_from_text(text)
    if doi:
        return {"doi": doi, "method": "regex", "details": "first_match_in_head"}

    # Stage 2: CrossRef
    if not title:
        return {"doi": None, "method": "regex_failed", "details": "no_title_for_fallback"}
    doi, score, details = lookup_doi_via_crossref(title, author_lastname, year)
    if doi:
        return {"doi": doi, "method": "crossref", "details": details}
    return {"doi": None, "method": "all_failed", "details": details}
