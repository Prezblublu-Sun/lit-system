"""
Scan library_raw/, sha256 each PDF, dedupe, create inbox/ symlinks.
Idempotent: re-running is safe (existing symlinks kept).

Outputs:
- inbox/{doc_id_16hex}.pdf  -> library_raw/<original-path>.pdf
- library_index.json        -> map doc_id -> source_path, sha256, size, page_count
- Console report: duplicates, corrupted, oversized/undersized, name issues
"""
import sys
import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "library_raw"
INBOX   = ROOT / "inbox"
INDEX   = ROOT / "library_index.json"

INBOX.mkdir(exist_ok=True)

if not RAW_DIR.exists() or not any(RAW_DIR.iterdir()):
    print(f"[error] {RAW_DIR} empty or missing.")
    sys.exit(1)


def sha256_of(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def try_open_pdf(path: Path):
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path))
        return True, len(r.pages)
    except Exception as e:
        return False, str(e)[:80]


pdfs = list(RAW_DIR.rglob("*.pdf")) + list(RAW_DIR.rglob("*.PDF"))
print(f"[scan] found {len(pdfs)} PDFs under {RAW_DIR}")
print(f"[scan] computing sha256 + opening each (this takes a few minutes)\n")

by_hash = {}
records  = []
problems = {"corrupted": [], "tiny": [], "huge": [], "weird_name": []}

# Allow ASCII printable + CJK + common punctuation
NAME_OK = re.compile(
    r"^[\x20-\x7e"          # ASCII printable
    r"\u3000-\u303f"         # CJK symbols/punctuation
    r"\u4e00-\u9fff"         # CJK Unified Ideographs
    r"\u3400-\u4dbf"         # CJK Extension A
    r"\uff00-\uffef"         # Halfwidth/Fullwidth Forms
    r"\u2010-\u2027"         # Hyphens / dashes
    r"\u2030-\u205e"         # Punctuation
    r"]+$"
)

for i, p in enumerate(sorted(pdfs), 1):
    rel = p.relative_to(RAW_DIR)
    try:
        size = p.stat().st_size
    except Exception:
        problems["corrupted"].append((str(rel), "stat failed"))
        continue

    if i % 50 == 0 or i == len(pdfs):
        print(f"  ...{i}/{len(pdfs)} processed")

    if size < 50_000:
        problems["tiny"].append((str(rel), size))
    if size > 100_000_000:
        problems["huge"].append((str(rel), size))
    if not NAME_OK.match(p.name):
        problems["weird_name"].append(str(rel))

    h = sha256_of(p)
    doc_id = h[:16]

    if h in by_hash:
        by_hash[h].append(rel)
        continue

    ok, pages = try_open_pdf(p)
    if not ok:
        problems["corrupted"].append((str(rel), pages))
        continue

    by_hash[h] = [rel]
    records.append({
        "doc_id":      doc_id,
        "sha256":      h,
        "source_path": str(rel),
        "size":        size,
        "page_count":  pages,
        "filename":    p.name,
    })

# Create symlinks
created = 0
existed = 0
for r in records:
    link = INBOX / f"{r['doc_id']}.pdf"
    target = (RAW_DIR / r["source_path"]).resolve()
    if link.is_symlink() or link.exists():
        try:
            if link.is_symlink() and Path(link.readlink()).resolve() == target:
                existed += 1
                continue
        except Exception:
            pass
        link.unlink()
    link.symlink_to(target)
    created += 1

INDEX.write_text(json.dumps(records, ensure_ascii=False, indent=2))

# Report
print(f"\n{'='*60}\nSCAN REPORT")
print(f"  total PDFs found:    {len(pdfs)}")
print(f"  unique by sha256:    {len(records)}")
print(f"  duplicates skipped:  {sum(len(v)-1 for v in by_hash.values() if len(v) > 1)}")
print(f"  symlinks created:    {created}")
print(f"  symlinks existed:    {existed}")
print(f"  index:               {INDEX.relative_to(ROOT)}")
print(f"  inbox:               {INBOX.relative_to(ROOT)} ({len(list(INBOX.glob('*.pdf')))} files)")

dup_groups = [(h, paths) for h, paths in by_hash.items() if len(paths) > 1]
if dup_groups:
    print(f"\n  DUPLICATE files (same sha256, multiple paths) - first 10:")
    for h, paths in dup_groups[:10]:
        print(f"    doc_id={h[:16]}:")
        for pth in paths:
            print(f"      {pth}")
    if len(dup_groups) > 10:
        print(f"    ... and {len(dup_groups)-10} more duplicate groups")

for label, items in problems.items():
    if items:
        print(f"\n  {label}: {len(items)}")
        for it in items[:5]:
            print(f"    {it}")
        if len(items) > 5:
            print(f"    ... and {len(items)-5} more")

# Folder distribution
from collections import Counter
folder_counter = Counter()
for r in records:
    parts = Path(r["source_path"]).parts
    if len(parts) >= 2:
        folder_counter[parts[0]] += 1
    else:
        folder_counter["<root>"] += 1
print(f"\n  PDFs per top-level source folder:")
for src, n in folder_counter.most_common():
    print(f"    {src}: {n}")
