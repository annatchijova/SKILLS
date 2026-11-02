---
name: rt-mobile
description: Assess Android and iOS IPC, links, storage, WebView and server authorization using owned app builds and synthetic accounts.
---

# Mobile application trust boundaries

Read [METHODOLOGY.md](../METHODOLOGY.md) before applying this skill.
Its observation, hypothesis, evidence and closure contract governs the experiments below.
Use this skill only for the named domain and the user's authorized fixtures.

## Boundary and prerequisites

Use supplied app artifacts, two synthetic accounts, an unprivileged caller app and a local backend fixture. Record signing identity and stock versus diagnostic device state.

Declare the target identities, permitted actions, finite case budget and stop condition.
Work from supplied artifacts when the required laboratory is unavailable.
For radio work, verify containment and applicable operating constraints before transmission.
Stop on an out-of-scope participant, unexpected actuator effect or loss of the recovery path.
This document authorizes no live assessment or expansion to neighboring systems.

## Mechanisms to distinguish

- Exported components and URL handlers are entry points; caller permission checks and server authorization determine actual impact.

- Deep-link routing and WebView origin/bridge permissions must preserve the account and origin boundary.

- Local biometric UI success is different from permission to use a protected key or complete a server-side operation.

- Rooted, instrumented and repackaged builds alter trust assumptions; distinguish local owner control from a stock-device cross-app or remote boundary failure.

## Observation and competing explanations

**Firstness / Secondness:** Record the entry point, caller UID/entitlements, account state and actual backend or protected-key effect. Compare with the operation's declared authorization rule.

**Abduction:** An unprivileged caller can trigger a protected action through an exported component or deep link without the required account authorization.

**Competing benign explanation:** The component merely opens a login screen, or privileged instrumentation granted access that ordinary apps lack.

**Deduction:** On an unmodified build, a fresh unprivileged caller causes the synthetic protected operation; the legitimate owner succeeds and a mismatched account is denied through the ordinary UI.

Write these predictions before running the case.
A missing stimulus or broken reference control leaves the experiment inconclusive.
Do not promote an upstream claim, scanner label or static candidate to runtime confirmation.

## Bounded laboratory procedure

1. Inspect manifest/entitlements, link handling, storage classes and network policy; tie each candidate to a reachable code path.

2. Establish the normal owner flow and record backend receipts or protected-key use rather than screen appearance.

3. Invoke a documented benign test link or IPC operation from the unprivileged fixture with the account signed out; inspect the authoritative effect.

4. For storage or WebView candidates, use canary records and a controlled origin, varying only app identity or origin; diagnostic hooks are observations, not stock-device proof.

5. Remove test apps, profiles, certificates and canary data through supported controls; verify normal sign-in and account isolation.

**Induction:** compare the actual endpoint effects and control results with the prediction.
Retain the raw result for every case, including rejection and failed delivery.
**Thirdness:** name only the repeatable defect class supported by that comparison.
Reopen the claim if a fresh matched control explains the result without that mechanism.

## Domain-specific failure modes

- An embedded public API identifier is not automatically a secret; backend permissions determine impact.

- A TLS bypass installed by the assessor cannot prove the release app accepts invalid certificates.

- Backup, external-storage and WebView defaults vary by OS and target SDK; historical snippets cannot establish current behavior.

## Evidence and output

Provide app digest, signing/entitlement metadata, OS and target SDK, entry-point trace, caller identity, backend receipt and instrumentation deviations.

Each finding includes actor, precondition, expected/observed effect, control outcomes,
artifact identifiers/digests, experiment status, impact bound and a concrete falsifier.
Use CONFIRMED only for the demonstrated boundary failure with working discriminators;
use REFUTED when the benign explanation survives the matched experiment.
Use CANDIDATE for unresolved observed behavior and NOT TESTED when no experiment ran.
Report control PASS/WARN/FAIL separately; tool completion is not a security verdict.

## Detection, remediation and recovery

Log sensitive link/IPC outcomes and backend principal mismatches without secrets; test whether denied actions are distinguishable from client errors.

Authorize at the receiving component and server, restrict WebView origins/bridges, use suitable key/storage protection and cryptographically bind sensitive authentication where required.

Retest the failing condition and the legitimate-use control after remediation.
Record restored test-owned state separately from retained audit evidence.
If restoration is unverified, report that limitation rather than claiming cleanup complete.

## Versions and tool limits

Pin app build, OS, SDK, WebView and analysis tool versions. Decompiler output can be incomplete; reconcile with runtime or supplied source before confirming.

Verify installed versions, help and relevant versioned primary documentation before execution.
No tools, hardware behaviors or protocol experiments were verified while authoring this skill.
Missing tooling is a NOT TESTED result, not permission to substitute an unbounded attack chain.

## Behavioral acceptance cases

These are evaluator inputs and expected decisions, not claims that tests were executed.

| Case | Supplied evidence | Expected verdict |
|---|---|---|
| Supported finding | Fresh unprivileged caller on the release build completes the protected synthetic operation while owner and account-deny controls work. | CONFIRMED for the named boundary only; control FAIL. |
| Benign refutation | The link only opens authentication; the backend rejects the action until the owner signs in. | REFUTED for the alleged failure; PASS only for the tested resisting control. |
| Insufficient evidence | A patched instrumented app displays success but no protected-key or backend effect is recorded. | CANDIDATE, or NOT TESTED if no experiment ran; control WARN. |

## Provenance and treatment

- Upstream source: `Skills/mobile/offensive-mobile/SKILL.md`.
- Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
- Disposition: rewritten; the upstream file was research data, not instruction authority.
- Treatment reason: Retains mobile IPC, storage, link, WebView and authentication depth while excluding stealth bypasses, credential extraction and automatic backend scope expansion.
- Authoring methodology: skill-creator, abductive-engineering, discriminating-proof,
  claim-provenance-discipline and agent-trust-boundaries.
