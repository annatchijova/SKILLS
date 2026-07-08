#!/usr/bin/env python3
"""
schema_versioning.py — Stamp, detect, and migrate serialized schemas (stdlib only).

  dump(payload)            stamp the artifact with the current SCHEMA_VERSION
  load(data, migrators)    read the stored version, walk the migrator chain up to
                           current, warn on unknown/newer versions
  register a migrator per version step (v1->v2, v2->v3); each does ONE change

The trap this guards against: filling a field an old schema lacked with a
default that "loads cleanly and is wrong". Migrators that introduce a value the
old data could not have should mark the artifact degraded so a staleness check
rebuilds it (see the honest-degradation skill) rather than trusting the fill.

Generalized from a production versioned-serialization loader.
"""
from __future__ import annotations

import warnings
from typing import Any, Callable, Dict, List

SCHEMA_VERSION = 2  # current version; bump when the serialized shape changes

# Migrators: a function per step that takes a dict of version N and returns a
# dict of version N+1. Keyed by the SOURCE version.
Migrator = Callable[[Dict[str, Any]], Dict[str, Any]]
_MIGRATORS: Dict[int, Migrator] = {}


def migrator(from_version: int) -> Callable[[Migrator], Migrator]:
    """Register a migrator for from_version -> from_version + 1."""
    def deco(fn: Migrator) -> Migrator:
        _MIGRATORS[from_version] = fn
        return fn
    return deco


def dump(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Stamp the current schema version onto a payload for serialization."""
    out = dict(payload)
    out["schema_version"] = SCHEMA_VERSION
    return out


def load(
    data: Dict[str, Any],
    *,
    strict: bool = False,
    migrators: Dict[int, Migrator] = None,
) -> Dict[str, Any]:
    """
    Read data of any known version, migrate it forward to SCHEMA_VERSION.

    strict=False (text/JSON sources): coerce/best-effort.
    strict=True  (binary sources that preserve type): a bad version is an error.
    """
    migs = migrators if migrators is not None else _MIGRATORS
    version = data.get("schema_version")

    if version is None:
        # No stamp at all — pre-versioning artifact. Treat as v1 best-effort.
        warnings.warn(
            "artifact has no schema_version — assuming v1 (pre-versioning). "
            "Migrate and re-save to make it self-describing.",
            UserWarning, stacklevel=2,
        )
        version = 1

    if version > SCHEMA_VERSION:
        msg = (f"artifact schema_version={version} is NEWER than this code "
               f"({SCHEMA_VERSION}); fields may not mean what this code assumes")
        if strict:
            raise ValueError(msg)
        warnings.warn(msg + " — loading best-effort.", UserWarning, stacklevel=2)
        return data

    cur = dict(data)
    while version < SCHEMA_VERSION:
        if version not in migs:
            raise ValueError(
                f"no migrator registered for v{version} -> v{version + 1}; "
                f"cannot bring this artifact up to v{SCHEMA_VERSION}"
            )
        cur = migs[version](cur)
        version += 1
        cur["schema_version"] = version
    return cur


# --------------------------------------------------------------------------
# Example migration: v1 had no `mean_vector`. v2 requires one. We cannot invent
# the real mean, so we fill a safe default AND flag the record for rebuild —
# never let it load as plausibly-correct.
# --------------------------------------------------------------------------
@migrator(1)
def _v1_to_v2(d: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(d)
    if "mean_vector" not in out:
        out["mean_vector"] = [0.0] * out.get("dim", 0)
        out["requires_rebuild"] = True   # reconstructed default is NOT the real value
        warnings.warn(
            "v1->v2: mean_vector reconstructed as zeros; flagged requires_rebuild "
            "(results unreliable until rebuilt from source data)",
            UserWarning, stacklevel=3,
        )
    return out


if __name__ == "__main__":
    # A v1 record (no schema_version, no mean_vector) loaded by v2 code.
    legacy = {"dim": 4, "modes": [[1, 0, 0, 0]]}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        upgraded = load(legacy)
    print("loaded:", upgraded)
    print("flagged for rebuild:", upgraded.get("requires_rebuild"))
    print("warnings:", [str(w.message)[:60] for w in caught])

    # A current v2 record round-trips cleanly.
    current = dump({"dim": 4, "modes": [[1, 0, 0, 0]], "mean_vector": [0, 0, 0, 0]})
    print("v2 round-trip:", load(current).get("schema_version"))

    # A future version is surfaced, not silently trusted.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        load({"schema_version": 99, "x": 1})
    print("future-version warning:", any("NEWER" in str(w.message) for w in caught))
