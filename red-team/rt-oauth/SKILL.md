---
name: rt-oauth
description: "Red-team assessment of OAuth 2.0/2.1 and OIDC trust boundaries: authorization-code and implicit flows, redirect_uri validation, state/PKCE/nonce handling, token leakage and mix-up, and escalation to account takeover or lateral movement. Covers FAPI considerations, re-expressed as owned-client experiments that prove a flow weakness against a negative control instead of taking over real accounts."
---

# OAuth / OIDC Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's OAuth craft as scoped experiments on owned clients/accounts: it names the flow weaknesses, confirming a leak/bypass against a control rather than taking over a real user's account.

## Scope and prerequisites

Map the flow (authorization server, client, resource server) and its type (auth-code + PKCE, implicit, client-credentials). Use owned client registrations and owned accounts; redirect only to owned endpoints. Confirm a leak by receiving an owned code/token at your endpoint, not by compromising a victim.

Declare target, flow, attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED. Account takeover is an impact class to reason about, not to execute against real users.

## Attack surface and classes

- **redirect_uri** — loose matching (prefix/suffix/subdomain/open-redirect on the client) leaks the code/token.
- **state / CSRF** — missing/unchecked `state` enables login CSRF / code injection.
- **PKCE** — missing or downgradeable `code_challenge` on public clients.
- **nonce** (OIDC) — missing nonce enables ID-token replay.
- **Implicit flow** — token in URL fragment, leak via referrer/history.
- **Token/code leakage** — via redirect, logs, `Referer`; code replay (not one-time), code substitution.
- **Mix-up** — client confused about which AS issued a code.
- **Scope/consent** — scope upgrade, consent bypass.

## Mechanism and observation

Trace the code/token from issuance to redemption and the validation at each hop.

**Firstness:** Record an owned code/token arriving at an endpoint it should not, or a flow completing without a required check (no `state`, no PKCE). **Secondness:** State the spec-correct behavior (exact redirect match, `state` verified, PKCE enforced, code one-time) and the deviation. **Thirdness:** Infer the class only after a controlled flow confirms the leak/bypass.

## Abduction and refutation

**Mechanism hypothesis:** The AS or client validates a flow parameter loosely (redirect_uri match, `state`, PKCE, code reuse), so a code/token can be redirected, replayed or injected.

**Competing benign explanation:** redirect_uri is matched exactly; `state` is bound and verified; PKCE is enforced; codes are one-time and short-lived; the ID-token nonce is checked; the leak endpoint is actually same-origin and safe.

## Deduction and controls

The legitimate flow completes correctly (positive control). A confirmed finding delivers an owned code/token to an owned unintended endpoint, or completes a flow missing a required check, where a correct configuration refuses. Predeclare the confirming artifact. Exact redirect match / `state` / PKCE / one-time code are PASS controls.

## Induction: bounded laboratory procedure

Owned client and accounts; owned endpoints only.

1. **Baseline.** Complete the legitimate flow; capture redirect_uri matching, `state`, PKCE, code lifetime.
2. **redirect_uri.** Test suffix/subdomain/path variants and client-side open redirect, pointing at an owned domain; see if the code/token follows (compose with `rt-open-redirect`).
3. **state/PKCE/nonce.** Drop/alter `state`; omit/downgrade PKCE on a public client; omit nonce and replay the ID token.
4. **Code handling.** Replay a used code; attempt code injection into another owned session; test mix-up with a second owned AS.
5. **Implicit.** Observe token exposure in the fragment and referrer leakage.
6. **Control.** Confirm a correct configuration refuses each.

Record results including refutations. Keep finding and control status separate. Only ever handle owned codes/tokens.

## Craft notes (leads)

The highest-impact variant is a `redirect_uri` loophole that leaks the authorization code (→ account takeover) — often via suffix/subdomain matching or an open redirect on an allowlisted client host. OAuth 2.1 mandates PKCE and drops implicit; FAPI adds stronger binding (PAR, JARM, DPoP). Mix-up attacks target multi-AS clients. Token-in-URL (implicit) leaks via history/referrer.

## Domain-specific failure modes

Exact redirect matching defeats most code-leak variants — a refutation. A bound, verified `state` defeats CSRF/injection. PKCE enforcement neutralizes code interception on public clients. A same-origin "leak" endpoint is not a leak. Reason about takeover impact; do not execute it against real accounts.

## Evidence and deliverable

Provide the flow, the weakness (loose redirect / missing state / missing PKCE / code reuse), the owned code/token delivered to the owned endpoint, and the control refusal. Handle only owned credentials. Attach minimal replay, expected/observed, rival explanation, falsifier, untested flows.

## Versions and tool limitations

Pin the AS/client library and the OAuth/OIDC profile (2.0 vs 2.1, FAPI). Behavior is profile- and library-specific. No flow behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

Exact redirect_uri matching, mandatory PKCE, bound/verified `state`, OIDC nonce, one-time short-lived codes, drop implicit, and FAPI binding (PAR/DPoP) where required. Add regressions asserting loose redirect/missing-state/missing-PKCE flows are refused. Detect redirect_uri anomalies and code replay at the AS.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | An owned code/token is delivered to an owned unintended endpoint, or a flow completes without a required check, where the control refuses: CONFIRMED; FAIL (takeover impact reasoned, not executed). |
| Benign refutation | Exact redirect match / state / PKCE / one-time code defeats the attempt: REFUTED; PASS for the control. |
| Insufficient evidence | A redirect variant accepted but no code/token leak shown: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/auth/offensive-oauth/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's flow-weakness, redirect_uri, PKCE/state/nonce and mix-up craft plus FAPI/2.1 context, re-expressed as owned-client experiments with spec-correct controls, replacing real account takeover with bounded leak/bypass proof. Composes with `token-trust-assessment`, `rt-open-redirect`.
