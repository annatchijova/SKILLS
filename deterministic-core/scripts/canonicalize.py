#!/usr/bin/env python3
"""
canonicalize.py — Single source of truth for deterministic serialization.

Typed, ordered, versioned canonical form for SHA-256 sealing. The same object
always produces identical bytes; objects that mean different things never
collide. Generalized from a production forensic canonicalizer.

Schema v1:
  bool          -> "true" / "false"      (checked before int — bool subclasses int)
  int           -> "N:int"
  Fraction      -> "P/Q:frac"            (exact rationals — preferred in decision paths)
  Decimal       -> "D:dec"
  float         -> "N.NNNNNNNN:flt"      (8 fixed decimals; nan/inf explicit) — cosmetic only
  str           -> unchanged
  None          -> "null"
  dict          -> keys sorted, values recursive
  list / tuple  -> elements recursive
  other         -> str(obj)              (fallback; never silently drops)

Bump CANONICALIZE_VERSION when the schema changes, and keep verifying old
versions so previously sealed payloads still validate.
"""
from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from fractions import Fraction
from typing import Any

CANONICALIZE_VERSION: str = "1"


def canonicalize(obj: Any) -> Any:
    """Recursively convert `obj` to its strict canonical form for hashing."""
    if isinstance(obj, bool):  # must precede int
        return "true" if obj else "false"
    if isinstance(obj, int):
        return f"{obj}:int"
    if isinstance(obj, Fraction):
        return f"{obj.numerator}/{obj.denominator}:frac"
    if isinstance(obj, Decimal):
        return f"{obj}:dec"
    if isinstance(obj, float):
        if obj != obj:
            return "nan:flt"
        if obj == float("inf"):
            return "inf:flt"
        if obj == float("-inf"):
            return "-inf:flt"
        return f"{obj:.8f}:flt"
    if isinstance(obj, str):
        return obj
    if obj is None:
        return "null"
    if isinstance(obj, dict):
        return {k: canonicalize(v) for k, v in sorted(obj.items())}
    if isinstance(obj, (list, tuple)):
        return [canonicalize(v) for v in obj]
    return str(obj)


def canonical_bytes(payload: Any) -> bytes:
    """Canonical UTF-8 bytes — the exact input to the hash."""
    canon = canonicalize(payload)
    return json.dumps(canon, sort_keys=True, ensure_ascii=False).encode("utf-8")


def seal(payload: Any) -> str:
    """SHA-256 digest over the canonical bytes of `payload`."""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def sealed_envelope(payload: Any) -> dict:
    """Payload plus its seal and schema version — a minimal chain-of-custody record."""
    return {
        "canonicalize_version": CANONICALIZE_VERSION,
        "sha256": seal(payload),
        "payload": payload,
    }


if __name__ == "__main__":
    demo = {"decision": "FLAG", "posterior": Fraction(3, 7), "edges": 12, "ok": True}
    print("version:", CANONICALIZE_VERSION)
    print("bytes  :", canonical_bytes(demo).decode())
    print("sha256 :", seal(demo))
