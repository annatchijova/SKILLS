#!/usr/bin/env python3
"""
tristate_runner.py — Run checks with distinct PASS / WARN / FAIL outcomes.

A two-state PASS/FAIL runner has nowhere to record "this best-effort guarantee
was not confirmed in this environment", so it records PASS — and a real
weakness disappears into a green check. This runner keeps three states, counts
WARNs separately, surfaces them by name, and never lets a non-PASS hide in the
pass total. A WARN does not fail the suite; an unhandled exception is a FAIL.

A check is a zero-argument callable that returns "PASS" | "WARN" | "FAIL"
(or any truthy value, treated as PASS), or raises (treated as FAIL).

Generalized from a determinism-aware test suite.
"""
from __future__ import annotations

import traceback
from typing import Callable, List

Check = Callable[[], object]


def run_checks(checks: List[Check], *, title: str = "checks") -> bool:
    """Run all checks. Return True iff zero FAILs (WARNs are visible, not fatal)."""
    print("=" * 56)
    print(f"  {title}")
    print("=" * 56)

    passed = warned = failed = 0
    warns: List[str] = []
    fails: List[str] = []

    for check in checks:
        name = getattr(check, "__name__", repr(check))
        try:
            outcome = check()
        except Exception as exc:  # noqa: BLE001 — an exception is an explicit FAIL
            failed += 1
            fails.append(name)
            print(f"  FAIL {name}: {exc}")
            traceback.print_exc()
            continue

        if outcome == "WARN":
            warned += 1
            warns.append(name)
            print(f"  WARN {name}")
        elif outcome == "FAIL":
            failed += 1
            fails.append(name)
            print(f"  FAIL {name}")
        else:
            passed += 1
            print(f"  PASS {name}")

    print("=" * 56)
    print(f"  RESULT: {passed} PASS, {warned} WARN, {failed} FAIL")
    if warns:
        print(f"  WARNED: {', '.join(warns)}  (not confirmed — investigate, do not ignore)")
    if fails:
        print(f"  FAILED: {', '.join(fails)}")
    print("=" * 56)
    return failed == 0


if __name__ == "__main__":
    def check_core_invariant():
        return "PASS"

    def check_cross_environment():
        # Best-effort: this environment couldn't confirm it. WARN, not a false PASS.
        return "WARN"

    def check_regression():
        raise AssertionError("expected 3, got 4")  # becomes a FAIL

    ok = run_checks(
        [check_core_invariant, check_cross_environment, check_regression],
        title="demo suite",
    )
    print("suite passed (no FAILs):", ok)
