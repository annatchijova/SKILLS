---
name: rt-ai-security
description: "Red-team assessment of LLM / AI-application boundaries (OWASP LLM Top 10): direct and indirect prompt injection, jailbreak/guardrail robustness, sensitive-information disclosure, tool/agent abuse and excessive agency, insecure output handling, training-data and MLOps-platform exposure, and model extraction. Re-expressed as scoped experiments against an owned AI system with an inert objective and guardrail-robustness scoring instead of a jailbreak cookbook."
---

# LLM / AI-Application Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's AI-pentest craft as scoped experiments against an owned AI system: it names the injection, agency and disclosure classes, scoring guardrail robustness against an inert objective rather than shipping a jailbreak cookbook. Compose with `model-evaluation-discipline`, `agent-trust-boundaries`, `llm-out-of-the-loop`.

## Scope and prerequisites

Test an owned/authorized AI application. Prove impact with an inert objective — a benign canary action or a planted secret the model should refuse to reveal — not real harm. For agentic systems, confirm the tool boundary with a reversible, owned action.

Declare the system (model, tools, data sources, guardrails), attempt budget, stop condition. Spec-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes (OWASP LLM Top 10)

- **Prompt injection** — direct (user input overrides instructions) and indirect (poisoned retrieved/linked content carries instructions).
- **Jailbreak / guardrail robustness** — getting the model past its policy (measured as robustness, not catalogued as recipes).
- **Sensitive-information disclosure** — system-prompt/secret/PII leakage.
- **Excessive agency / insecure tool use** — the agent takes an unauthorized tool action from injected instructions.
- **Insecure output handling** — model output flows unsanitized into a sink (XSS/SQLi/command — route to the web skills).
- **Training-data / MLOps** — poisoning, model/registry exposure, pipeline access.
- **Model extraction / inversion** — stealing weights/behavior or memorized data.

## Mechanism and observation

Trace untrusted content (user or retrieved) into the model's instruction-following, and the model's output into any downstream tool/sink.

**Firstness:** Record whether the inert objective was achieved (the model performed the canary action / revealed the planted secret / an agent called a tool it should not). **Secondness:** State the intended boundary (instructions outrank data; secrets never disclosed; tools gated by authorization) and the deviation. **Thirdness:** Infer the class only after a controlled attempt confirms it on the owned system.

## Abduction and refutation

**Hypothesis:** Untrusted content can override the model's instructions, extract protected data, or drive an unauthorized tool action.

**Competing benign explanation:** The guardrail refused; the "secret" was never in context; the tool call required an authorization check the model cannot bypass (the decision path is deterministic, not the LLM — see `llm-out-of-the-loop`); the output sink sanitizes; the extraction attempt returns only public behavior.

## Deduction and controls

A benign prompt behaves safely (positive control). A confirmed finding achieves the inert objective where a correctly-guarded system refuses. Predeclare the objective signal. Guardrail refusal / secret-not-in-context / deterministic tool authorization / output sanitization are PASS controls. Guardrail robustness is scored as a rate across trials, not a single success.

## Induction: bounded laboratory procedure

Owned AI system; inert objective.

1. **Baseline.** Issue benign prompts; capture normal behavior and guardrail responses.
2. **Direct injection.** Attempt instruction override toward the inert objective; measure success rate across trials (robustness).
3. **Indirect injection.** Plant instructions in a document/URL the system retrieves; see if the model follows them.
4. **Disclosure.** Probe for system-prompt/planted-secret leakage.
5. **Agency/tool.** For agents, attempt to induce an unauthorized but reversible owned tool action; confirm whether a deterministic check gates it.
6. **Output handling.** Check whether model output reaches a sink unsanitized (route to `rt-xss`/`rt-sqli`/`rt-rce`).
7. **Control.** Confirm guardrails/authorization hold on the benign baseline and score robustness.

Record results including refutations. Keep finding status separate from guardrail-robustness scoring (a rate with trials).

## Craft notes (leads)

Indirect injection via retrieved/linked content is the highest-impact class for RAG/agent systems — the attacker never talks to the model directly. Jailbreak families (persona, encoding, multi-turn, policy-puppetry, image-embedded) are robustness probes; report a success rate, not a "the jailbreak". The architectural fix for agency is keeping the LLM out of the decision path (deterministic authorization gates tool calls) — see `llm-out-of-the-loop` and `agent-trust-boundaries`. Model extraction is a query-budget/behavior-cloning concern.

## Domain-specific failure modes

One jailbreak success is a robustness data point, not a universal bypass — report the rate. A "leaked" secret that was never in context is not disclosure. If a deterministic check (not the model) authorizes tool calls, injection cannot cross it — a PASS. Prompt-injection impact is realized only at the sink/tool; a model saying something is not yet harm. Non-determinism means re-run; a single transcript is weak evidence.

## Evidence and deliverable

Provide the class, the inert objective, the success/robustness rate across trials, the downstream sink/tool reached (if any), and the control that held. Use inert objectives and planted secrets. Attach minimal replay, expected/observed, rival explanation, falsifier, classes not tested.

## Versions and tool limitations

Pin the model, version, system prompt, tools and guardrail stack — behavior is model- and version-specific and non-deterministic. No system behavior was verified by this content; confirm on the owned system and run multiple trials.

## Remediation and detection

Treat all model input (including retrieved content) as untrusted; keep the LLM out of the decision path with deterministic authorization gates; separate data from instructions; sanitize model output at every sink; minimize secrets in context; rate-limit to blunt extraction; and monitor for injection patterns. Add a regression asserting the inert objective is refused. Score and track guardrail robustness over releases.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The inert objective is achieved (unauthorized tool action / secret disclosure / instruction override) at a meaningful rate where a guarded system refuses: CONFIRMED; FAIL (report the rate). |
| Benign refutation | Guardrails refuse / deterministic gate blocks the tool / secret not in context: REFUTED; PASS for the control. |
| Insufficient evidence | A single non-reproducing success: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/ai/offensive-ai-security/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's prompt-injection, agency, disclosure, MLOps and extraction craft, re-expressed as owned-system experiments with inert objectives and guardrail-robustness scoring, replacing a jailbreak cookbook with bounded, rate-based boundary assessment. Composes with `model-evaluation-discipline`, `agent-trust-boundaries`, `llm-out-of-the-loop`, `training-run-provenance`.
