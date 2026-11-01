#!/usr/bin/env python3
"""
seal_then_narrate.py — Skeleton for "LLM narrates, never decides".

Enforces the invocation order: the deterministic result is sealed BEFORE any
LLM is called, the model receives only a compressed read-only summary under a
numbers-are-fixed prompt, and the prose is attached beside the seal — never
inside the hashed payload, and never able to mutate it.

The narrator is a pluggable `Callable[[dict], str]`. A local (Ollama) and a
hosted backend must be interchangeable behind this interface; swapping them
changes wording only. Replace `decide()` and the narrator with your own.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from typing import Any, Callable


# --------------------------------------------------------------------------
# 1. Deterministic engine (replace with yours; no LLM, exact arithmetic).
# --------------------------------------------------------------------------
def decide(inputs: dict) -> dict:
    """Produce the load-bearing result deterministically. Stub."""
    raise NotImplementedError("Plug in your deterministic decision engine.")


# --------------------------------------------------------------------------
# 2. Seal (compute BEFORE any LLM call).
# --------------------------------------------------------------------------
def seal(payload: Any) -> str:
    canon = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canon).hexdigest()


# --------------------------------------------------------------------------
# 3. Compress: a small read-only view for the model.
# --------------------------------------------------------------------------
def compress(result: dict) -> dict:
    """Headline numbers + decision only — never the raw machinery."""
    return {
        "decision": result.get("decision"),
        "score": result.get("score"),
        "contributions": result.get("contributions", []),
    }


# --------------------------------------------------------------------------
# 4. Narrator (pluggable; narration only — must not change numbers).
# --------------------------------------------------------------------------
NARRATIVE_PROMPT = (
    "You are a domain expert writing a concise report.\n"
    "The analysis below was produced by a deterministic system. The figures "
    "are fixed and authoritative: do NOT modify, re-rank, recompute, or "
    "contradict any number, the decision, or its direction. Express the result "
    "in clear language only. No emojis.\n\n"
    "RESULT (authoritative, do not alter):\n{summary}\n\nWrite the report:"
)


def ollama_narrator(summary: dict, model: str = "gemma3:27b") -> str:
    """Local narration via Ollama. Interchangeable with any hosted backend."""
    prompt = NARRATIVE_PROMPT.format(
        summary=json.dumps(summary, sort_keys=True, ensure_ascii=False, indent=2)
    )
    proc = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Ollama narration failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


# --------------------------------------------------------------------------
# 5. Orchestration: order is the contract.
# --------------------------------------------------------------------------
def analyze(
    inputs: dict,
    narrator: Callable[[dict], str] = ollama_narrator,
) -> dict:
    """
    Sealed result first, narration second. The returned prose is attached to
    the envelope but lives outside the hashed payload and cannot mutate it.
    """
    result = decide(inputs)            # 1. deterministic
    digest = seal(result)              # 2. fixed from here on
    summary = compress(result)         # 3. read-only view
    try:
        prose = narrator(summary)      # 4. narration only
    except Exception as exc:           # narration is optional; the seal is not
        prose = None
        prose_error = str(exc)
    else:
        prose_error = None

    return {
        "sha256": digest,              # ground truth
        "result": result,              # the sealed payload
        "narrative": prose,            # attached beside the seal, never within
        "narrative_error": prose_error,
    }


if __name__ == "__main__":
    print(__doc__)
    print("PYTHONHASHSEED:", os.environ.get("PYTHONHASHSEED", "(unset)"))
