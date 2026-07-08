#!/usr/bin/env python3
"""
boundary_validators.py — Validate untrusted inputs at the edge, with clear,
named errors raised BEFORE the value reaches an operation that can't explain
its own failure.

  validate_array()  two-phase: structural (shape, finiteness, non-empty) then
                    dtype contract (raise for binary sources, coerce+warn for text)
  validate_finite() reject NaN/Inf before arithmetic spreads them silently
  sanitize_path()   resolve-then-compare; reject non-regular/symlink/traversal,
                    enforce a size cap

Everything raises explicit ValueError/RuntimeError (never assert — that vanishes
under python -O) with a message that names the offending value.

numpy is optional: the array/finite helpers need it; sanitize_path() does not.
Generalized from production tensor- and path-validation code.
"""
from __future__ import annotations

import os
import stat
import warnings
from pathlib import Path
from typing import Optional, Sequence, Tuple

try:
    import numpy as np
    _HAVE_NUMPY = True
except ImportError:
    _HAVE_NUMPY = False


class BoundaryError(ValueError):
    """Raised when an input fails validation at the system boundary."""


# --------------------------------------------------------------------------
# Arrays / tensors
# --------------------------------------------------------------------------
def validate_finite(arr) -> None:
    """Raise unless every element is finite. NaN/Inf spread silently — stop them here."""
    if not np.isfinite(arr).all():
        raise BoundaryError("array contains NaN or Inf")


def validate_array(
    data,
    expected_shape: Tuple[int, ...],
    *,
    expected_dtype=None,
    strict: bool = False,
):
    """
    Two-phase boundary validation for array-like input.

    Phase 1 (structure): coerce to ndarray, require exact shape, finiteness,
    and non-empty. Phase 2 (dtype): if expected_dtype is set, raise on mismatch
    when strict (binary source that should preserve dtype), else coerce with a
    UserWarning (text/JSON source that structurally can't).
    """
    if not _HAVE_NUMPY:
        raise RuntimeError("numpy is required for validate_array()")

    arr = np.asarray(data)
    if arr.size == 0:
        raise BoundaryError("array is empty")
    if arr.shape != expected_shape:
        raise BoundaryError(f"shape mismatch: expected {expected_shape}, got {arr.shape}")
    validate_finite(arr)

    if expected_dtype is not None and arr.dtype != expected_dtype:
        if strict:
            raise BoundaryError(
                f"dtype mismatch: expected {expected_dtype}, got {arr.dtype} "
                f"(use strict=False for JSON sources, which always yield float64)"
            )
        warnings.warn(
            f"dtype coercion {arr.dtype} -> {expected_dtype}; precision may be lost",
            UserWarning,
            stacklevel=2,
        )
        arr = arr.astype(expected_dtype)
    return arr


def validate_each(items: Sequence, expected_shape: Tuple[int, ...]) -> None:
    """
    Validate every element BEFORE a bulk op (e.g. vstack). One bad element
    detonates inside the library with an opaque error; this names which one.
    """
    if not _HAVE_NUMPY:
        raise RuntimeError("numpy is required for validate_each()")
    for i, e in enumerate(items):
        arr = np.asarray(e)
        if arr.shape != expected_shape:
            raise BoundaryError(f"element {i} has shape {arr.shape}, expected {expected_shape}")
        if not np.isfinite(arr).all():
            raise BoundaryError(f"element {i} contains NaN or Inf")


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


def sanitize_path(
    raw_path,
    base_dir: Optional[Path] = None,
    max_size: int = _MAX_FILE_SIZE,
) -> Path:
    """
    Validate a caller-supplied path before it touches the filesystem.

    Resolve first (collapses `..` and links), then require: exists, is a regular
    file (not symlink/device/pipe/socket), within base_dir if given (or
    VIGIA_EVIDENCE_BASE_DIR-style env override), and under the size cap.
    """
    p = Path(raw_path).resolve()  # resolve BEFORE any comparison

    if not p.exists():
        raise BoundaryError(f"path not found: {raw_path}")
    if p.is_symlink():
        raise BoundaryError(f"symlink rejected: {raw_path}")

    st = p.stat()
    if not stat.S_ISREG(st.st_mode):
        raise BoundaryError(f"not a regular file: {raw_path} (mode={oct(st.st_mode)})")
    if st.st_size > max_size:
        raise BoundaryError(f"file too large: {st.st_size} bytes > {max_size}: {raw_path}")

    if base_dir is None:
        env_base = os.environ.get("EVIDENCE_BASE_DIR")
        if env_base:
            base_dir = Path(env_base)
    if base_dir is not None:
        base = base_dir.resolve()
        if not str(p).startswith(str(base) + os.sep) and p != base:
            raise BoundaryError(f"path traversal: {raw_path!r} is outside {base}")

    return p


if __name__ == "__main__":
    import tempfile

    # Path checks
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        good = base / "ok.txt"
        good.write_text("hi")
        print("good path:", sanitize_path(good, base_dir=base).name)
        try:
            sanitize_path(base / "missing.txt", base_dir=base)
        except BoundaryError as e:
            print("rejected missing:", e)
        link = base / "link.txt"
        link.symlink_to(good)
        try:
            sanitize_path(link, base_dir=base)
        except BoundaryError as e:
            print("rejected symlink:", e)

    # Array checks
    if _HAVE_NUMPY:
        validate_array([[1.0, 2.0], [3.0, 4.0]], (2, 2), expected_dtype=np.float32)
        print("good array OK (with coercion warning)")
        for bad, why in [
            (([1.0, 2.0],), "wrong shape"),
            ([[1.0, float("nan")], [3.0, 4.0]], "NaN"),
        ]:
            try:
                validate_array(bad, (2, 2))
            except BoundaryError as e:
                print(f"rejected {why}:", e)
        try:
            validate_each([np.zeros(384), np.zeros(383)], (384,))
        except BoundaryError as e:
            print("rejected bad element pre-vstack:", e)
