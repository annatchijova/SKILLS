#!/usr/bin/env python3
"""
sql_aggregation.py — Aggregate in the database, batch instead of N+1, cap exports.

Runnable SQLite demo of three patterns:
  count_stats_*   SQL GROUP BY vs materializing every row to tally in Python
                  (identical numbers; only the bad one reads the rows + blobs)
  load_by_ids     one batched IN(...) query, chunked under SQLite's 999-param cap
  capped_export   top-N by ranking + a `truncated` flag, never an unbounded dump

Generalized from a production memory store.
"""
from __future__ import annotations

import sqlite3
from typing import Dict, List

_SQLITE_MAX_PARAMS = 999


def make_db(n_rows: int = 5000) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE items (id TEXT PRIMARY KEY, state TEXT, recalls INTEGER, blob BLOB)"
    )
    states = ["REINFORCED", "NEUTRAL", "FORGOTTEN"]
    rows = [
        (f"id_{i}", states[i % 3], i % 7, bytes(256))  # 256-byte blob per row
        for i in range(n_rows)
    ]
    conn.executemany("INSERT INTO items VALUES (?,?,?,?)", rows)
    conn.commit()
    return conn


def count_stats_bad(conn: sqlite3.Connection) -> Dict:
    """Anti-pattern: load EVERY row (including the unused blob) to tally in Python."""
    dist = {"REINFORCED": 0, "NEUTRAL": 0, "FORGOTTEN": 0}
    total_recalls = 0
    rows_materialized = 0
    for _id, state, recalls, _blob in conn.execute("SELECT * FROM items"):
        rows_materialized += 1          # every row crosses into Python memory
        dist[state] += 1
        total_recalls += recalls
    return {"dist": dist, "total_recalls": total_recalls, "rows_materialized": rows_materialized}


def count_stats_good(conn: sqlite3.Connection) -> Dict:
    """Aggregate in SQL — constant application memory, no blob deserialization."""
    dist = {"REINFORCED": 0, "NEUTRAL": 0, "FORGOTTEN": 0}
    for state, c in conn.execute("SELECT state, COUNT(*) FROM items GROUP BY state"):
        dist[state] = c
    total_recalls = conn.execute("SELECT COALESCE(SUM(recalls), 0) FROM items").fetchone()[0]
    return {"dist": dist, "total_recalls": total_recalls, "rows_materialized": 0}


def load_by_ids(conn: sqlite3.Connection, ids: List[str]) -> List[tuple]:
    """One batched query, chunked under the 999 bound-parameter cap."""
    if not ids:
        return []
    out: List[tuple] = []
    for i in range(0, len(ids), _SQLITE_MAX_PARAMS):
        chunk = ids[i:i + _SQLITE_MAX_PARAMS]
        ph = ",".join("?" * len(chunk))
        out.extend(conn.execute(
            f"SELECT id, state, recalls FROM items WHERE id IN ({ph})", chunk
        ).fetchall())
    return out


def capped_export(conn: sqlite3.Connection, max_nodes: int = 1000) -> Dict:
    """Top-N by recalls + a truncated flag and the true total — never an unbounded dump."""
    total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    rows = conn.execute(
        "SELECT id, recalls FROM items ORDER BY recalls DESC LIMIT ?", (max_nodes,)
    ).fetchall()
    return {
        "nodes": [{"id": r[0], "recalls": r[1]} for r in rows],
        "returned": len(rows),
        "total": total,
        "truncated": total > max_nodes,
    }


if __name__ == "__main__":
    conn = make_db(5000)

    bad = count_stats_bad(conn)
    good = count_stats_good(conn)
    print("bad  (materialized rows):", bad["rows_materialized"], bad["dist"], bad["total_recalls"])
    print("good (materialized rows):", good["rows_materialized"], good["dist"], good["total_recalls"])
    assert bad["dist"] == good["dist"] and bad["total_recalls"] == good["total_recalls"]
    print("=> identical numbers; SQL version read 0 rows into Python\n")

    big_ids = [f"id_{i}" for i in range(2500)]  # > 999 -> exercises chunking
    fetched = load_by_ids(conn, big_ids)
    print(f"batched load of {len(big_ids)} ids -> {len(fetched)} rows (chunked under 999)\n")

    exp = capped_export(conn, max_nodes=100)
    print(f"capped export: returned={exp['returned']} total={exp['total']} "
          f"truncated={exp['truncated']}")
