#!/usr/bin/env python3
"""diff_snapshots.py — compute delta between two overnight-ingest status snapshots.

Reads two plain-text snapshot files of the format produced by the overnight
status generator (see results/overnight_snapshots/snapshot_*.log) and prints a
markdown table showing Before / After / Delta for the Stats section plus
derived throughput metrics.

Read-only: makes no live system calls (no nvidia-smi, no tmux capture-pane).

Usage:
    python scripts/diff_snapshots.py snapshot_A.log snapshot_B.log
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


STAT_KEYS: list[tuple[str, str]] = [
    ("sop_tasks", "SOP tasks completed"),
    ("papers", "Papers completed"),
    ("doi_warns", "DOI dedup warns"),
    ("ollama_restarts", "Ollama restarts"),
]


HEADER_RE = re.compile(r"===\s+.*?\s+@\s+(.+?)\s+===")
TIMESTAMP_RE = re.compile(
    r"^\w{3}\s+(?P<day>\d{1,2})\s+(?P<month>\w{3})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+\w+\s+(?P<year>\d{4})$"
)


@dataclass
class Snapshot:
    path: Path
    timestamp: Optional[datetime] = None
    stats: dict[str, Optional[int]] = field(default_factory=dict)


def parse_timestamp(raw: str) -> Optional[datetime]:
    """Parse 'Thu 14 May 00:03:27 BST 2026' style timestamps.

    Returns None on any failure. Timezone name is stripped (treated as naive),
    which is correct as long as both snapshots come from the same host.
    """
    m = TIMESTAMP_RE.match(raw.strip())
    if not m:
        return None
    try:
        return datetime.strptime(
            f"{m['day']} {m['month']} {m['year']} {m['time']}",
            "%d %b %Y %H:%M:%S",
        )
    except ValueError:
        return None


def parse_snapshot(path: Path) -> Snapshot:
    text = path.read_text(encoding="utf-8", errors="replace")

    snap = Snapshot(path=path, stats={key: None for key, _ in STAT_KEYS})

    for line in text.splitlines():
        m = HEADER_RE.search(line)
        if m:
            snap.timestamp = parse_timestamp(m.group(1))
            break

    in_stats = False
    for line in text.splitlines():
        if line.startswith("Stats:"):
            in_stats = True
            continue
        if not in_stats:
            continue
        stripped = line.strip()
        if not stripped:
            break
        for key, label in STAT_KEYS:
            if stripped.startswith(label):
                nums = re.findall(r"-?\d+", stripped)
                if nums:
                    snap.stats[key] = int(nums[-1])
                break

    return snap


def _fmt(v: Optional[int]) -> str:
    return "N/A" if v is None else str(v)


def _fmt_delta(a: Optional[int], b: Optional[int]) -> str:
    if a is None or b is None:
        return "N/A"
    d = b - a
    return f"+{d}" if d > 0 else str(d)


def _fmt_ratio(num: Optional[float], denom: Optional[float], suffix: str = "") -> str:
    if num is None or denom is None or denom == 0:
        return "N/A"
    return f"{num / denom:.2f}{suffix}"


def _fmt_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return "N/A"
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{sign}{h}h {m:02d}m {s:02d}s"


def render_markdown(a: Snapshot, b: Snapshot) -> str:
    lines: list[str] = []
    lines.append(f"# Snapshot diff: `{a.path.name}` -> `{b.path.name}`")
    lines.append("")

    t_a = a.timestamp.isoformat(sep=" ") if a.timestamp else "N/A"
    t_b = b.timestamp.isoformat(sep=" ") if b.timestamp else "N/A"
    elapsed = (
        (b.timestamp - a.timestamp).total_seconds()
        if a.timestamp and b.timestamp
        else None
    )

    lines.append("## Timing")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Before timestamp | {t_a} |")
    lines.append(f"| After timestamp  | {t_b} |")
    lines.append(f"| Elapsed          | {_fmt_duration(elapsed)} |")
    lines.append("")

    lines.append("## Stats")
    lines.append("")
    lines.append("| Metric | Before | After | Delta |")
    lines.append("|---|---|---|---|")
    for key, label in STAT_KEYS:
        a_v = a.stats.get(key)
        b_v = b.stats.get(key)
        lines.append(
            f"| {label} | {_fmt(a_v)} | {_fmt(b_v)} | {_fmt_delta(a_v, b_v)} |"
        )
    lines.append("")

    def _delta(key: str) -> Optional[int]:
        a_v = a.stats.get(key)
        b_v = b.stats.get(key)
        if a_v is None or b_v is None:
            return None
        return b_v - a_v

    d_papers = _delta("papers")
    d_sop = _delta("sop_tasks")
    d_restarts = _delta("ollama_restarts")
    hours = elapsed / 3600 if elapsed else None

    lines.append("## Derived metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Papers per hour          | {_fmt_ratio(d_papers, hours)} |")
    lines.append(f"| SOP tasks per paper      | {_fmt_ratio(d_sop, d_papers)} |")
    lines.append(f"| Papers per Ollama restart | {_fmt_ratio(d_papers, d_restarts)} |")
    lines.append("")

    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Diff two overnight-ingest status snapshots."
    )
    parser.add_argument("before", type=Path, help="Earlier snapshot file")
    parser.add_argument("after", type=Path, help="Later snapshot file")
    args = parser.parse_args(argv)

    a = parse_snapshot(args.before)
    b = parse_snapshot(args.after)
    print(render_markdown(a, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
