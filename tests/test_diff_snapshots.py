"""Unit tests for scripts/diff_snapshots.py.

Run with:
    pytest tests/test_diff_snapshots.py
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import diff_snapshots as ds  # noqa: E402


SNAPSHOT_A = textwrap.dedent("""\
    === Overnight 124 status @ Thu 14 May 00:03:27 BST 2026 ===

    tmux:
    overnight_124: 1 windows (created Wed May 13 16:23:32 2026)

    Last 20 lines from tmux:
      [P40] L2_interpretive_scoring ...
        OK in 179.1s, 297 tok

    Stats:
      SOP tasks completed: 200
      Papers completed (-> metadata):  40
      DOI dedup warns: 4
      Ollama restarts: 8

    Ollama:
    qwen2.5-14b-32k:latest 18 GB 54%/46% CPU/GPU 32768 3 minutes from now

    GPU:
    12825 MiB, 0 %, 45

    Disk space:
    /dev/sda2       457G  192G  242G  45% /
""")

SNAPSHOT_B = textwrap.dedent("""\
    === Overnight 124 status @ Thu 14 May 06:03:27 BST 2026 ===

    tmux:
    overnight_124: 1 windows (created Wed May 13 16:23:32 2026)

    Stats:
      SOP tasks completed: 400
      Papers completed (-> metadata):  80
      DOI dedup warns: 6
      Ollama restarts: 10

    GPU:
    12000 MiB, 50 %, 60

    Disk space:
    /dev/sda2       457G  195G  239G  45% /
""")


def test_parse_timestamp_normal():
    dt = ds.parse_timestamp("Thu 14 May 00:03:27 BST 2026")
    assert dt is not None
    assert (dt.year, dt.month, dt.day) == (2026, 5, 14)
    assert (dt.hour, dt.minute, dt.second) == (0, 3, 27)


def test_parse_timestamp_malformed_returns_none():
    assert ds.parse_timestamp("") is None
    assert ds.parse_timestamp("not a timestamp") is None
    assert ds.parse_timestamp("Thu 14 BadMonth 00:03:27 BST 2026") is None
    assert ds.parse_timestamp("14 May 00:03:27 BST 2026") is None


def test_parse_snapshot_normal(tmp_path: Path):
    p = tmp_path / "snap.log"
    p.write_text(SNAPSHOT_A)
    snap = ds.parse_snapshot(p)
    assert snap.timestamp is not None
    assert snap.stats["sop_tasks"] == 200
    assert snap.stats["papers"] == 40
    assert snap.stats["doi_warns"] == 4
    assert snap.stats["ollama_restarts"] == 8


def test_parse_snapshot_missing_fields(tmp_path: Path):
    text = textwrap.dedent("""\
        === Overnight 124 status @ Thu 14 May 00:03:27 BST 2026 ===

        Stats:
          SOP tasks completed: 200
          Papers completed (-> metadata):  40

        GPU:
        12000 MiB, 50 %, 60
    """)
    p = tmp_path / "snap.log"
    p.write_text(text)
    snap = ds.parse_snapshot(p)
    assert snap.stats["sop_tasks"] == 200
    assert snap.stats["papers"] == 40
    assert snap.stats["doi_warns"] is None
    assert snap.stats["ollama_restarts"] is None


def test_parse_snapshot_malformed_timestamp(tmp_path: Path):
    text = textwrap.dedent("""\
        === Overnight 124 status @ BROKEN HEADER ===

        Stats:
          Papers completed (-> metadata):  40
    """)
    p = tmp_path / "snap.log"
    p.write_text(text)
    snap = ds.parse_snapshot(p)
    assert snap.timestamp is None
    assert snap.stats["papers"] == 40


def test_render_markdown_normal_diff(tmp_path: Path):
    pa = tmp_path / "a.log"
    pb = tmp_path / "b.log"
    pa.write_text(SNAPSHOT_A)
    pb.write_text(SNAPSHOT_B)
    out = ds.render_markdown(ds.parse_snapshot(pa), ds.parse_snapshot(pb))

    assert "| Papers completed | 40 | 80 | +40 |" in out
    assert "| SOP tasks completed | 200 | 400 | +200 |" in out
    assert "| DOI dedup warns | 4 | 6 | +2 |" in out
    assert "| Ollama restarts | 8 | 10 | +2 |" in out
    assert "6h 00m 00s" in out
    assert "6.67" in out  # papers/hour = 40 / 6
    assert "5.00" in out  # sop/paper = 200 / 40
    assert "20.00" in out  # papers per restart = 40 / 2


def test_render_markdown_missing_field_graceful(tmp_path: Path):
    pa = tmp_path / "a.log"
    pb = tmp_path / "b.log"
    pa.write_text(SNAPSHOT_A)
    pb.write_text(textwrap.dedent("""\
        === Overnight 124 status @ Thu 14 May 06:03:27 BST 2026 ===

        Stats:
          Papers completed (-> metadata):  80

    """))
    out = ds.render_markdown(ds.parse_snapshot(pa), ds.parse_snapshot(pb))

    assert "| Papers completed | 40 | 80 | +40 |" in out
    assert "| SOP tasks completed | 200 | N/A | N/A |" in out
    assert "| DOI dedup warns | 4 | N/A | N/A |" in out
    assert "N/A" in out  # derived metrics depending on missing fields


def test_render_markdown_malformed_timestamp_graceful(tmp_path: Path):
    pa = tmp_path / "a.log"
    pb = tmp_path / "b.log"
    pa.write_text(textwrap.dedent("""\
        === Overnight 124 status @ NOT A DATE ===

        Stats:
          SOP tasks completed: 200
          Papers completed (-> metadata):  40
          DOI dedup warns: 4
          Ollama restarts: 8
    """))
    pb.write_text(SNAPSHOT_B)
    out = ds.render_markdown(ds.parse_snapshot(pa), ds.parse_snapshot(pb))

    # Timing rows should fall back to N/A; stats deltas should still be computed.
    assert "| Before timestamp | N/A |" in out
    assert "| Elapsed          | N/A |" in out
    assert "+40" in out  # papers delta still computed
    assert "Papers per hour          | N/A" in out  # derived needs elapsed


def test_zero_delta_renders_without_plus_sign(tmp_path: Path):
    text = textwrap.dedent("""\
        === Overnight 124 status @ Thu 14 May 00:03:27 BST 2026 ===

        Stats:
          SOP tasks completed: 200
          Papers completed (-> metadata):  40
          DOI dedup warns: 4
          Ollama restarts: 8
    """)
    pa = tmp_path / "a.log"
    pb = tmp_path / "b.log"
    pa.write_text(text)
    pb.write_text(text.replace("00:03:27", "06:03:27"))
    out = ds.render_markdown(ds.parse_snapshot(pa), ds.parse_snapshot(pb))
    # All deltas are 0, no '+' sign for zero
    assert "| Papers completed | 40 | 40 | 0 |" in out
