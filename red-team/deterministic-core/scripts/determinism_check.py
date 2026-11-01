#!/usr/bin/env python3
"""
determinism_check.py — Prove a producer is reproducible, or find where it isn't.

Runs a zero-argument producer callable N times, seals each output with the
canonical encoder, and asserts every seal is identical. On divergence it does
not just fail — it locates the first field that differs, so a nondeterminism
bug points you at the offending value instead of a bare assertion.

    from determinism_check import assert_deterministic
    assert_deterministic(lambda: build_result(x), n=5)
"""
from __future__ import annotations

from typing import Any, Callable

from canonicalize import canonicalize, seal


class NondeterminismError(AssertionError):
    """Raised when a producer yields different sealed outputs across runs."""


def _first_divergence(a: Any, b: Any, path: str = "$") -> str | None:
    """Return a human-readable path to the first structural difference, or None."""
    ca, cb = canonicalize(a), canonicalize(b)
    if isinstance(ca, dict) and isinstance(cb, dict):
        for key in sorted(set(ca) | set(cb)):
            if key not in ca:
                return f"{path}.{key} — present in run 2 only"
            if key not in cb:
                return f"{path}.{key} — present in run 1 only"
            deeper = _first_divergence(a[key], b[key], f"{path}.{key}")
            if deeper:
                return deeper
        return None
    if isinstance(ca, list) and isinstance(cb, list):
        if len(ca) != len(cb):
            return f"{path} — length {len(ca)} vs {len(cb)}"
        for i, (x, y) in enumerate(zip(a, b)):
            deeper = _first_divergence(x, y, f"{path}[{i}]")
            if deeper:
                return deeper
        return None
    if ca != cb:
        return f"{path} — {ca!r} vs {cb!r}"
    return None


def assert_deterministic(producer: Callable[[], Any], n: int = 3) -> str:
    """
    Call `producer` `n` times; require all sealed outputs to match.

    Returns the shared SHA-256 digest on success. Raises NondeterminismError
    with the path to the first diverging field on failure.
    """
    if n < 2:
        raise ValueError("n must be >= 2 to compare runs")

    first = producer()
    first_seal = seal(first)
    for run in range(2, n + 1):
        current = producer()
        if seal(current) != first_seal:
            where = _first_divergence(first, current) or "(structure identical, bytes differ)"
            raise NondeterminismError(
                f"Producer is nondeterministic between run 1 and run {run}.\n"
                f"  first divergence: {where}\n"
                f"  common leaks: float in path, set/dict ordering, unpinned "
                f"timestamp/RNG inside payload, PYTHONHASHSEED."
            )
    return first_seal


if __name__ == "__main__":
    import random

    # Demo: a deterministic producer passes; an RNG-tainted one is located.
    print("deterministic:", assert_deterministic(lambda: {"x": 1, "y": [1, 2, 3]}, n=4))
    try:
        assert_deterministic(lambda: {"x": random.random()}, n=4)
    except NondeterminismError as exc:
        print("caught as expected:\n", exc)
