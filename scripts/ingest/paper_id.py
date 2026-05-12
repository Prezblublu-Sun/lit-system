"""
Allocate the next available P{n} paper_id by scanning metadata/.
Also: load existing doc_id -> paper_id index for dedup.
"""
import json
import re
from pathlib import Path

PAPER_ID_RE = re.compile(r"^P(\d+)\.json$")


def load_existing_index(metadata_dir: Path):
    """
    Returns:
      doc_id_to_paper_id: dict[str, str]  e.g. {"5f23b783...": "P1"}
      doi_to_paper_id:    dict[str, str]  doi -> paper_id (skips null doi)
      used_nums:          set[int]        all P{n} numbers in use
    """
    doc_id_to_paper_id = {}
    doi_to_paper_id    = {}
    used_nums          = set()

    for f in sorted(metadata_dir.glob("P*.json")):
        m = PAPER_ID_RE.match(f.name)
        if not m:
            continue
        n = int(m.group(1))
        used_nums.add(n)
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        paper_id = d.get("_paper_id") or f.stem
        doc_id = d.get("id_block", {}).get("doc_id")
        if doc_id:
            doc_id_to_paper_id[doc_id] = paper_id
        doi_field = d.get("source_block", {}).get("doi")
        if isinstance(doi_field, dict):
            doi_val = doi_field.get("value")
        else:
            doi_val = doi_field
        if doi_val:
            doi_to_paper_id[doi_val.lower()] = paper_id
    return doc_id_to_paper_id, doi_to_paper_id, used_nums


def next_paper_id(used_nums: set):
    """Smallest non-used positive integer, e.g. P6 if 1-5 used."""
    n = 1
    while n in used_nums:
        n += 1
    return f"P{n}", n
