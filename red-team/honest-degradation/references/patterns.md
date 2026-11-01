# Honest-degradation patterns

Concrete code shapes for each principle, with the failure each one prevents.
Read this when wiring a loader, a best-effort guarantee, or an optional feature.

## 1. Flag a reconstructed value; honor the flag downstream

```python
if data.get("mean_vector"):
    self.mean_vector = validate(data["mean_vector"])
else:
    # Legacy schema had no mean_vector. A zero mean is NOT the original centre —
    # anything computed over it is silently wrong.
    self.mean_vector = np.zeros(dim, dtype=DTYPE)
    self.requires_rebuild = True            # the flag is the whole point
    warnings.warn("legacy field without mean_vector; reconstructed as zeros — "
                  "results unreliable until rebuilt", UserWarning, stacklevel=2)

def is_stale(self, current_count) -> bool:
    if self.requires_rebuild:               # downstream honors it
        return True
    ...
```

Prevents: a result computed over a wrong basis that looks completely normal —
no exception, no NaN, just quietly incorrect numbers.

## 2. Tri-state outcome, WARNs counted separately

```python
def run_checks(checks):
    passed = warned = failed = 0
    for check in checks:
        outcome = check()                   # returns "PASS" | "WARN" | "FAIL"
        if   outcome == "WARN": warned += 1
        elif outcome == "FAIL": failed += 1
        else:                   passed += 1
    print(f"{passed} PASS, {warned} WARN, {failed} FAIL")
    return failed == 0                      # WARN does not fail the suite, but is visible
```

```python
# A child process that failed must NOT be reported as PASS:
result = subprocess.run([...], capture_output=True, text=True)
if result.returncode != 0:
    return "WARN"      # distinct, surfaced — not silently treated as success
return "PASS"
```

Prevents: an unverified best-effort guarantee, or a crashed child, recorded as a
green PASS — a real weakness vanishing into a healthy-looking summary.

## 3. Name the guarantee level in the serialized schema

```python
def to_dict(self):
    return {
        "engine_version": ENGINE_VERSION,
        "determinism_level": "best_effort",   # honest claim, readable by other code
        ...
    }
```

And in the module header / class docstring, state both regimes explicitly:
"intra-process: STRONG; cross-process: BEST-EFFORT (BLAS backend chosen at
install time)". Prevents: a blanket "deterministic" claim that holds on your
machine and fails on someone else's, with no way to discover the caveat.

## 4. Warn at the boundary, let the caller decide

```python
def coerce_dtype(arr, expected, strict=False):
    if arr.dtype == expected:
        return arr
    if strict:
        raise TypeError(f"expected {expected}, got {arr.dtype}")
    warnings.warn(f"dtype coercion {arr.dtype} -> {expected}; precision may be lost",
                  UserWarning, stacklevel=3)
    return arr.astype(expected)
```

Prevents: a silent precision loss (or a silent legacy path) that the caller
would have rejected had they known.

## 5. Optional component: degrade the feature, disclose, protect the core

```python
try:
    from spectral import SpectralField
    _SPECTRAL_AVAILABLE = True
except ImportError:
    _SPECTRAL_AVAILABLE = False
    logger.debug("spectral module not found — resonance metadata disabled")

# In the hot path, the optional feature can never break the core:
if self._spectral is not None and self._spectral.is_built:
    try:
        meta = self._spectral.resonance(q, m)
    except Exception:
        pass   # genuinely optional, and absence/failure already logged once
```

Prevents: an optional enrichment taking down the core operation it was only
meant to annotate.

## 6. Don't destroy valid work over a persistence failure

```python
field = build_field(...)            # expensive, correct, in memory
if field and field.is_built:
    try:
        store.save(field)
    except Exception as exc:
        warnings.warn(f"save failed ({exc}); returning in-memory field "
                      f"without persistence", RuntimeWarning, stacklevel=2)
return field                        # caller still gets the valid result
```

Prevents: discarding a correctly computed result because a locked DB or full
disk made the *write* fail — conflating "couldn't save" with "couldn't compute".
