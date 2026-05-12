"""
schema v1: MetadataBuilder + sop_v2 + Docling -> metadata/P*.json
Implements ADR-0003 hybrid schema (id_block / source_block / factual /
interpretive / personal_relevance / assets) with inline _meta provenance.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR   = PROJECT_ROOT / "corpus" / "golden"
SOP_FILE     = PROJECT_ROOT / "results" / "sop_v2.json"
DOCLING_DIR  = PROJECT_ROOT / "assets" / "docling_test"
CLEAN_DIR    = PROJECT_ROOT / "assets" / "docling_clean"
METADATA_DIR = PROJECT_ROOT / "metadata"
METADATA_DIR.mkdir(exist_ok=True)

PROMPT_VERSION = "sop_v2_qwen14b_32k"  # commit 3f4b77e


# ============ MetadataBuilder ============

class MetadataBuilder:
    SCHEMA_VERSION = "v1"
    NON_ID_BLOCKS  = ["source_block", "factual", "interpretive", "personal_relevance"]
    REQUIRED_META  = {"produced_by", "prompt_version", "produced_at"}

    def __init__(self, doc_id, paper_id, produced_at=None):
        now = datetime.now(timezone.utc).isoformat()
        self.data = {
            "_schema_version": self.SCHEMA_VERSION,
            "_paper_id": paper_id,
            "_ingested_at": now,
            "_schema_notes": [
                "v1: factual/interpretive fields may contain raw markdown blocks (atomization deferred to v2)",
                "v1: core_problem_raw kept under interpretive per sop_v2 naming; ADR-0003 lists under factual (resolve in v2)",
            ],
            "id_block": {"doc_id": doc_id},
            "source_block": {},
            "factual": {},
            "interpretive": {},
            "personal_relevance": {},
            "assets": {},
        }
        self._default_produced_at = produced_at or now

    def set_id_block(self, filename, content_hash):
        self.data["id_block"]["filename"] = filename
        self.data["id_block"]["content_hash"] = content_hash

    def add_field(self, block, field_name, value, produced_by, prompt_version,
                  produced_at=None, evidence=None, reviewed_by=None,
                  reviewed_at=None, cost_usd=None, note=None):
        if block not in self.NON_ID_BLOCKS:
            raise ValueError(f"unknown block: {block}")
        entry = {
            "value": value,
            "_meta": {
                "produced_by": produced_by,
                "prompt_version": prompt_version,
                "produced_at": produced_at or self._default_produced_at,
                "reviewed_by": reviewed_by,
                "reviewed_at": reviewed_at,
                "evidence": evidence or [],
            }
        }
        if cost_usd is not None:
            entry["_meta"]["cost_usd"] = cost_usd
        if note:
            entry["_meta"]["note"] = note
        self.data[block][field_name] = entry

    def attach_asset(self, name, path):
        self.data["assets"][name] = str(path)

    def validate(self):
        errors = []
        for k in ["doc_id", "filename", "content_hash"]:
            if k not in self.data["id_block"]:
                errors.append(f"id_block.{k} missing")
        for block in self.NON_ID_BLOCKS:
            for fname, field in self.data[block].items():
                if not isinstance(field, dict):
                    errors.append(f"{block}.{fname} not a dict")
                    continue
                if "value" not in field:
                    errors.append(f"{block}.{fname} missing value")
                if "_meta" not in field:
                    errors.append(f"{block}.{fname} missing _meta")
                    continue
                missing = self.REQUIRED_META - set(field["_meta"].keys())
                if missing:
                    errors.append(f"{block}.{fname}._meta missing: {missing}")
        if errors:
            raise ValueError("Schema validation failed:\n  " + "\n  ".join(errors))

    def save(self, path):
        self.validate()
        Path(path).write_text(json.dumps(self.data, indent=2, ensure_ascii=False))
        return path


# ============ Helpers ============

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def rel(path):
    return str(path.relative_to(PROJECT_ROOT))


# ============ sop_v2 -> schema v1 mapping ============

MAPPING = [
    ("L1_factual_background",  "factual",            "sop_l1_background_raw", None),
    ("L1_factual_methods",     "factual",            "methods_raw",           None),
    ("L2_interpretive_problem","interpretive",       "core_problem_raw",
        "kept under interpretive per sop_v2 naming; ADR-0003 lists under factual"),
    ("L2_interpretive_scoring","interpretive",       "scoring_10_dim_local",
        "D-grade local LLM output; pending Path C web chat review"),
    ("L3_personal_relevance",  "personal_relevance", "sop_l3_raw",            None),
]


# ============ Orchestrator ============

sop = json.load(open(SOP_FILE))
sop_started = sop["config"]["started_at"]
papers = sop["papers"]

print(f"[setup] sop_v2 produced_at: {sop_started}")
print(f"[setup] prompt_version:     {PROMPT_VERSION}")
print()

for pid in ["P1", "P2", "P3", "P4", "P5"]:
    if pid not in papers:
        print(f"[skip] {pid}: not in sop_v2.json")
        continue
    p = papers[pid]
    filename = p["_filename"]
    title    = p["_title"]
    pdf_path = PAPERS_DIR / filename

    if not pdf_path.exists():
        print(f"[skip] {pid}: PDF not found at {pdf_path}")
        continue

    content_hash = sha256_file(pdf_path)
    doc_id = content_hash[:16]

    mb = MetadataBuilder(doc_id=doc_id, paper_id=pid, produced_at=sop_started)
    mb.set_id_block(filename=filename, content_hash=content_hash)

    mb.add_field("source_block", "title", value=title,
                 produced_by="human-wei",
                 prompt_version="manual_v1",
                 evidence=[])

    for sop_key, block, schema_field, note in MAPPING:
        entry = p.get(sop_key)
        if not entry or not entry.get("ok"):
            print(f"  [{pid}] missing or failed sop_v2 entry: {sop_key}")
            continue
        mb.add_field(block, schema_field,
                     value=entry["answer"],
                     produced_by="qwen2.5-14b-32k",
                     prompt_version=PROMPT_VERSION,
                     evidence=[],
                     note=note)

    mb.attach_asset("pdf_source", rel(pdf_path))
    for name, p_obj in [
        ("docling_json", DOCLING_DIR / f"{pid}_docling.json"),
        ("docling_md",   DOCLING_DIR / f"{pid}_docling.md"),
        ("cleaned_json", CLEAN_DIR   / f"{pid}_clean.json"),
        ("cleaned_md",   CLEAN_DIR   / f"{pid}_clean.md"),
    ]:
        if p_obj.exists():
            mb.attach_asset(name, rel(p_obj))

    out_path = METADATA_DIR / f"{pid}.json"
    mb.save(out_path)
    size_kb = out_path.stat().st_size / 1024
    print(f"[{pid}] doc_id={doc_id} -> {rel(out_path)} ({size_kb:.1f} KB)")

# Sanity print
print("\n[sample] metadata/P1.json structure:")
sample = json.load(open(METADATA_DIR / "P1.json"))
print(f"  top-level:      {list(sample.keys())}")
print(f"  id_block:       {list(sample['id_block'].keys())}")
print(f"  source_block:   {list(sample['source_block'].keys())}")
print(f"  factual:        {list(sample['factual'].keys())}")
print(f"  interpretive:   {list(sample['interpretive'].keys())}")
print(f"  personal_rel:   {list(sample['personal_relevance'].keys())}")
print(f"  assets:         {list(sample['assets'].keys())}")
