---
name: llm-out-of-the-loop
description: Architect any system that produces a consequential output so that the LLM stays entirely out of the decision path and only narrates an already-sealed result. Use this whenever an LLM is anywhere near a verdict, score, classification, ranking, risk number, approval, or any output that triggers an action or becomes evidence; when designing where the model "sits" in a pipeline; when someone proposes letting the model "decide", "judge", "classify", or "score"; and when you need the model to explain or write up a result without being able to change it. Push to use this whenever an LLM and a consequential output appear in the same system, even if the user hasn't framed it as an architecture question.
---

# LLM Out Of The Loop

A language model can read the evidence correctly and still reach the wrong conclusion. It is not that the model fails to *see*; it is that under narrative pressure — a persuasive framing, a leading prompt, the pull to agree, the urge to tell a coherent story — its judgment drifts even when its perception is right. The documented failure that anchors this skill: a model correctly flagged fabricated logs as fabricated, and then still returned the wrong verdict, because the surrounding narrative captured it. Correct perception does not imply correct judgment.

The architectural consequence is simple and absolute: **the LLM never touches the decision path.** A deterministic engine produces and seals the result. Only then does the LLM see it, and only to put it into words. The model can change the prose; it can never change the verdict.

## The layering

```
  inputs ──▶ [ deterministic engine ]  ──▶ result ──▶ [ SEAL: sha256 ]
                                                          │
                                          (sealed result + compressed summary)
                                                          ▼
                                                  [ LLM: narrate only ]  ──▶ prose
                                                          │
                                          stored alongside the seal, never inside it
```

Four properties make this hold:

1. **Seal before the model is ever called.** The SHA-256 seal is computed over the deterministic result *before* any LLM invocation. The model literally cannot influence a value that was already fixed. If you call the model first and seal after, you have rebuilt the failure.

2. **The model receives a compressed summary, not the full state.** Hand it the decision, the headline numbers, and the few contributions worth explaining — not the entire internal state. The less raw material it has, the less it can "reinterpret". The summary is a read-only view.

3. **The prompt forbids changing the numbers.** State explicitly that the figures are fixed, produced by a deterministic system, and must not be altered — the model's only job is to express them in domain language. See `references/architecture.md` for a generalized narrative-prompt template.

4. **The narrative is stored beside the seal, never within it.** The prose is an attachment. Recomputing the seal must not depend on the narrative, so a verifier can confirm the result without trusting the words wrapped around it. Optionally run a narrative auditor that checks the prose didn't smuggle in a different verdict than the sealed one.

## The backend is interchangeable — that's the point

Because the LLM touches nothing load-bearing, the backend is a swappable detail: a local model via Ollama, a hosted API, whatever. Switching from one to another changes the wording and nothing else — the verdict, the seal, and the chain of custody are identical. If swapping the narrator could change the outcome, the narrator is in the decision path and the architecture is wrong. Use that as a test.

## What belongs where

| Belongs in the deterministic engine | Belongs in the LLM layer |
|---|---|
| The decision / verdict / score | Explaining the decision in plain or domain language |
| Thresholds, weights, arithmetic | Translating jargon for a specific audience |
| Anything sealed or hashed | Drafting a human-readable report from the summary |
| Anything that triggers an action | Localizing or restyling the prose |

If you find yourself wanting the model to "just decide the edge case" or "pick when it's ambiguous", stop: that is the decision path. Encode the rule deterministically, even if the rule is "abstain / escalate to a human". An explicit ABSTAIN is a valid deterministic verdict; a model quietly deciding is not.

## Quick start

`scripts/seal_then_narrate.py` is the skeleton: compute result → seal → build a compressed summary → call a pluggable narrator (Ollama / API) under a numbers-are-fixed prompt → return the prose attached to, but unable to mutate, the sealed envelope. Adapt the engine and the narrator; keep the ordering.
