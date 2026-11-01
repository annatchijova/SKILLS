#!/usr/bin/env python3
"""
audit_chain.py — Append-only, tamper-evident hash chain (stdlib only).

Each entry seals the previous one:
    audit_hash = sha256( canonical(payload) + prev_hash )

Verification checks two independent properties:
    linkage   — entry[i].prev_hash == entry[i+1].audit_hash   (reorder/insert/delete)
    integrity — each audit_hash recomputes from its stored columns (in-place edits)

Design choices that make the chain actually protective:
  - the payload carries content_hashes (content, not just IDs)
  - the timestamp is captured ONCE and stored, so the chain is recomputable
  - a new producer continues the chain; it never restarts from genesis
  - append() verifies the tail and warns loudly on a pre-existing break
  - the verifier is stdlib-only and independent of any producer

Generalized from a production forensic audit log.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import warnings
from typing import Any, Dict, List, Optional

GENESIS = "0" * 64
_TAIL_CHECK = 25  # entries to re-link before appending


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=5.0)
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS audit_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts REAL NOT NULL,
            op TEXT NOT NULL,
            body TEXT NOT NULL,             -- canonical JSON of the event body
            content_hashes TEXT NOT NULL,   -- JSON list of referenced content hashes
            audit_hash TEXT NOT NULL,
            prev_hash TEXT NOT NULL
        )"""
    )
    conn.commit()
    return conn


def _canonical(ts: float, op: str, body: Any, content_hashes: List[str]) -> str:
    """Deterministic bytes for hashing: sorted keys, fixed separators, rounded ts."""
    return json.dumps(
        {
            "ts": round(float(ts), 6),     # capture-once value; recomputable from the row
            "op": op,
            "body": body,
            "content_hashes": sorted(content_hashes),  # content, not just IDs
        },
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def compute_hash(
    ts: float, op: str, body: Any, content_hashes: List[str], prev_hash: str
) -> str:
    payload = _canonical(ts, op, body, content_hashes)
    return hashlib.sha256((payload + prev_hash).encode("utf-8")).hexdigest()


def last_hash(conn: sqlite3.Connection) -> str:
    row = conn.execute(
        "SELECT audit_hash FROM audit_chain ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return row[0] if (row and row[0]) else GENESIS


def _tail_is_linked(conn: sqlite3.Connection, n: int = _TAIL_CHECK) -> bool:
    rows = conn.execute(
        "SELECT audit_hash, prev_hash FROM audit_chain ORDER BY id DESC LIMIT ?", (n,)
    ).fetchall()
    for i in range(len(rows) - 1):
        if rows[i][1] != rows[i + 1][0]:   # prev_hash[i] != audit_hash[i+1]
            return False
    return True


def append(
    conn: sqlite3.Connection,
    op: str,
    body: Any,
    content_hashes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Append one entry, continuing the existing chain.

    Captures the timestamp once, computes the hash over that exact value, and
    stores both. Warns loudly (without refusing) if the tail is already broken,
    so the operation is still recorded but the break stays discoverable.
    """
    content_hashes = content_hashes or []
    if conn.execute("SELECT 1 FROM audit_chain LIMIT 1").fetchone() and not _tail_is_linked(conn):
        warnings.warn(
            "Audit chain tail is already broken BEFORE this append. Appending "
            "anyway (the operation must be logged), but run verify_chain() and "
            "investigate — chaining over a break buries the tamper point.",
            RuntimeWarning,
            stacklevel=2,
        )

    prev = last_hash(conn)
    ts = time.time()  # captured once; this exact value is hashed and stored
    h = compute_hash(ts, op, body, content_hashes, prev)
    conn.execute(
        "INSERT INTO audit_chain (ts, op, body, content_hashes, audit_hash, prev_hash) "
        "VALUES (?,?,?,?,?,?)",
        (ts, op, json.dumps(body, sort_keys=True, ensure_ascii=False),
         json.dumps(sorted(content_hashes)), h, prev),
    )
    conn.commit()
    return {"ts": ts, "op": op, "audit_hash": h, "prev_hash": prev}


def fetch_all_desc(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    return [dict(r) for r in conn.execute(
        "SELECT * FROM audit_chain ORDER BY id DESC"
    ).fetchall()]


def verify_chain(entries_desc: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verify linkage and integrity over rows ordered id DESC.
    Returns {linkage_ok, integrity_ok, issues:[...]}. Never raises on bad data —
    a verify error becomes a reported issue, not a crash.
    """
    issues: List[Dict[str, Any]] = []
    linkage_ok = integrity_ok = True

    for i in range(len(entries_desc) - 1):
        if entries_desc[i]["prev_hash"] != entries_desc[i + 1]["audit_hash"]:
            linkage_ok = False
            issues.append({"type": "linkage_broken", "at_id": entries_desc[i].get("id")})

    for e in entries_desc:
        try:
            body = e["body"]
            if isinstance(body, str):
                body = json.loads(body)
            chashes = e["content_hashes"]
            if isinstance(chashes, str):
                chashes = json.loads(chashes)
            recomputed = compute_hash(e["ts"], e["op"], body, chashes, e["prev_hash"])
            if recomputed != e["audit_hash"]:
                integrity_ok = False
                issues.append({
                    "type": "hash_mismatch",
                    "at_id": e.get("id"),
                    "note": "stored columns do not reproduce audit_hash (tampered row)",
                })
        except Exception as exc:  # noqa: BLE001 — surfaced as an issue, never swallowed silently
            integrity_ok = False
            issues.append({"type": "verify_error", "at_id": e.get("id"), "error": str(exc)})

    return {"linkage_ok": linkage_ok, "integrity_ok": integrity_ok, "issues": issues}


if __name__ == "__main__":
    import tempfile, os

    path = tempfile.mktemp(suffix=".db")
    conn = connect(path)
    for i in range(5):
        append(conn, op="event", body={"i": i, "msg": f"entry {i}"},
               content_hashes=[hashlib.sha256(str(i).encode()).hexdigest()])

    clean = verify_chain(fetch_all_desc(conn))
    print("after honest build:", clean)

    # Tamper one row in place; integrity must catch it, linkage stays intact.
    conn.execute("UPDATE audit_chain SET body=? WHERE id=3",
                 (json.dumps({"i": 2, "msg": "EDITED"}),))
    conn.commit()
    tampered = verify_chain(fetch_all_desc(conn))
    print("after in-place edit:", tampered)

    os.unlink(path)
