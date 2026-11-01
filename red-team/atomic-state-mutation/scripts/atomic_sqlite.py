#!/usr/bin/env python3
"""
atomic_sqlite.py — All-or-nothing multi-write operations in SQLite.

connect()      sets a busy timeout (contenders wait instead of failing) and WAL
               (readers don't block on a writer). WAL is persistent — set once.
atomic(conn)   a context manager that takes the write lock UP FRONT
               (BEGIN IMMEDIATE), commits on clean exit, and rolls back on any
               exception. The unit of atomicity is the whole logical operation.

The failure this prevents: committing an insert and a delete separately, so a
crash between them leaves both the merged record and its sources alive —
duplicated data and any index rebuilt over the corrupted set.

Generalized from a production merge-and-cascade operation.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator


def connect(db_path: str, *, timeout: float = 5.0) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=timeout)
    conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    conn.execute("PRAGMA journal_mode=WAL")      # persistent; concurrent readers
    conn.execute("PRAGMA synchronous=NORMAL")    # recommended pairing with WAL
    return conn


@contextmanager
def atomic(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """
    Run a block as one all-or-nothing transaction with the write lock held
    from the first statement. Commits on success; rolls back on any exception.
    """
    conn.execute("BEGIN IMMEDIATE")              # write lock up front — no interleaving
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()                          # half-mutated state never persists
        raise


def merge_and_cascade(conn: sqlite3.Connection, new_row, source_ids, child_ids) -> None:
    """
    Example: insert a merged row, delete its sources, and cascade-clean their
    children — all in ONE transaction. Either the whole merge lands or nothing
    does; a concurrent writer cannot interleave.
    """
    with atomic(conn):
        conn.execute("INSERT INTO items (id, content) VALUES (?, ?)", new_row)
        ph = ",".join("?" * len(source_ids))
        conn.execute(f"DELETE FROM items WHERE id IN ({ph})", source_ids)
        if child_ids:
            cph = ",".join("?" * len(child_ids))
            conn.execute(f"DELETE FROM links WHERE owner_id IN ({cph})", child_ids)


if __name__ == "__main__":
    import tempfile, os

    path = tempfile.mktemp(suffix=".db")
    conn = connect(path)
    conn.executescript(
        "CREATE TABLE items (id TEXT PRIMARY KEY, content TEXT);"
        "CREATE TABLE links (owner_id TEXT);"
        "INSERT INTO items VALUES ('a','one'),('b','two');"
        "INSERT INTO links VALUES ('a'),('b');"
    )
    conn.commit()

    def count():
        return (conn.execute("SELECT COUNT(*) FROM items").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM links").fetchone()[0])

    print("before:", count())  # (2, 2)

    # A mid-operation failure must leave the store exactly as it was.
    try:
        with atomic(conn):
            conn.execute("INSERT INTO items VALUES ('merged','m')")
            conn.execute("DELETE FROM items WHERE id IN ('a','b')")
            raise RuntimeError("crash between writes")
    except RuntimeError as exc:
        print("rolled back on:", exc)

    print("after rollback:", count())  # still (2, 2) — atomic

    # A clean run commits everything together.
    merge_and_cascade(conn, ("merged", "m"), ["a", "b"], ["a", "b"])
    print("after clean merge:", count())  # (1, 0)

    os.unlink(path)
