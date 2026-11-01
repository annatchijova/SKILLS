# Architecture reference: LLM as narrator, not decider

This file expands the SKILL.md with a concrete template you can adapt. Read it
when you are wiring an LLM into a system that already (or should) produce a
deterministic, sealed result.

## Invocation order (non-negotiable)

1. `result = engine.decide(inputs)` — deterministic, exact arithmetic, no LLM.
2. `envelope = seal(result)` — SHA-256 over canonical bytes. Fixed from here on.
3. `summary = compress(result)` — small, read-only view for the model.
4. `prose = narrator(summary)` — LLM call, narration only.
5. `attach(envelope, prose)` — prose stored beside the seal, outside the hashed payload.
6. (optional) `audit(prose, result)` — confirm the prose's stated verdict matches the sealed one.

Reordering 2 and 4 reintroduces the failure this whole pattern exists to prevent.

## The compressed summary

Give the model the minimum it needs to explain the result, not the machinery
that produced it. A good summary contains: the decision/verdict, the few
headline numbers, and the named contributions worth mentioning. It does NOT
contain raw evidence the model could "re-judge", thresholds it could
second-guess, or anything not already reflected in the sealed result.

## Generalized narrative-prompt template

Adapt the domain, audience, and house style; keep the constraints. The key
clause is that the numbers are fixed and the model's only job is wording.

```
You are a domain expert writing a concise report for {audience}.
The analysis below was produced by a deterministic system. The figures are
fixed and authoritative: do NOT modify, re-rank, recompute, or contradict any
number, the decision, or its direction. Your only task is to express this
result in clear {domain} language.

Constraints:
- Do not introduce a conclusion the result does not state.
- Do not soften or strengthen the decision; report it as given.
- {house style: tone, length, vocabulary, no emojis, etc.}

RESULT (authoritative, do not alter):
{json summary, sorted keys}

Write the report:
```

## Narrator backends are swappable by design

A local model (Ollama) and a hosted API must be interchangeable behind one
`narrator(summary) -> str` interface. Because the narrator touches nothing
load-bearing, switching backends changes wording only. Treat "would swapping
the narrator change the outcome?" as a design test: if yes, something
load-bearing leaked into the narration layer — pull it back into the engine.

## Optional: narrative auditor

A cheap defense-in-depth check: after narration, verify the prose's stated
verdict/direction matches the sealed result (a keyword or structured check is
enough for many domains). If they disagree, the narration is discarded or
flagged — never the sealed result. The seal is ground truth; the prose is not.
