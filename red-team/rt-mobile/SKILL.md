---
name: rt-mobile
description: "Red-team assessment of mobile-app (Android/iOS) boundaries: insecure local storage, weak IPC / exported components and deeplinks, TLS/cert-pinning and traffic interception, authentication and session handling, and client-side trust (rooting/jailbreak, tampering, secrets in the binary). Re-expressed as scoped experiments on an owned app and test device with planted test data and negative controls instead of attacks on other users' devices or accounts."
---

# Mobile Application Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's mobile craft as scoped experiments on an owned app and test device: it names the storage, IPC, transport and client-trust boundaries, proving one with planted test data rather than attacking other users.

## Scope and prerequisites

Mobile testing spans the app binary, on-device storage, inter-process surfaces, and the network. Use an owned app build and a test device/emulator with owned test accounts and planted data. Prove a weakness against your own data/account; do not target other users' devices or accounts.

Declare the platform (Android/iOS), app version, device/root state, attempt budget, stop condition. Static-only review yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Local storage** — secrets/tokens/PII in SharedPreferences/plist/SQLite/files/keychain-keystore misuse; backups.
- **IPC / components** — Android exported activities/services/receivers/content-providers, intent handling, deeplink/universal-link validation; iOS URL schemes.
- **Transport** — TLS, certificate pinning (and pinning bypass on an owned device), cleartext traffic.
- **Auth/session** — token storage/lifecycle, biometric/local-auth bypass on the client.
- **Client-side trust** — root/jailbreak detection, tampering/repackaging, secrets/keys in the binary, obfuscation reliance.

## Mechanism and observation

Trace sensitive data/action from the app through the boundary.

**Firstness:** Record what was exposed/reached (a planted token read from storage, an exported component invoked without auth, intercepted traffic after pinning bypass on the owned device). **Secondness:** State the intended protection (keystore-backed secrets, non-exported/permission-gated components, pinning, server-side auth) and the deviation. **Thirdness:** Infer the class only after a controlled test confirms it on the owned app.

## Abduction and refutation

**Hypothesis:** A boundary leaks data or exposes an action — storage in the clear, an unprotected component, interceptable traffic, or client-side-only trust.

**Competing benign explanation:** Secrets are in the Keystore/Keychain (not extractable without device compromise); components are non-exported or permission-gated; pinning holds (and the "bypass" required rooting the owned device, which a real attacker on a non-rooted device cannot do); auth is enforced server-side so client bypass is moot; the binary secret is a public key.

## Deduction and controls

Normal app use protects data/actions (positive control). A confirmed finding exposes planted data or reaches an action via the boundary where a hardened app would not. Predeclare the exposed artifact. Keystore-backed secrets / non-exported components / pinning / server-side auth are PASS controls — and note whether the attack needed device root (which changes the threat model).

## Induction: bounded procedure

Owned app; test device; planted data.

1. **Baseline & recon.** Install the owned build; decompile (apktool/jadx / class-dump) for components, endpoints, secrets.
2. **Storage.** Log in with a test account; inspect on-device storage and backups for the planted token/PII in the clear.
3. **IPC/components.** Enumerate exported components/deeplinks; invoke them without the expected auth from a test app.
4. **Transport.** Proxy traffic; test pinning (bypass on the owned rooted device) and cleartext.
5. **Client trust.** Test root/jailbreak detection and repackaging; check for used secrets in the binary.
6. **Control.** Confirm server-side auth holds and note which attacks required device root.

Record results including refutations. Keep finding and control status separate, and record the device-trust assumption (rooted vs not).

## Craft notes (leads)

Android exported components and lax deeplink/`intent://` validation are recurring IPC findings. Tokens/PII in SharedPreferences/plist/SQLite in the clear is the classic storage finding; Keystore/Keychain is the control. Pinning bypass usually needs a rooted/jailbroken device — a real non-rooted-attacker caveat to state. Root detection and obfuscation are speed bumps, not boundaries; server-side enforcement is the real control (see `client-side-trust-boundary`).

## Domain-specific failure modes

A pinning bypass on a rooted device does not threaten non-rooted users — state the device-trust assumption. Keystore-backed secrets are not "in the clear". A client-side auth bypass is moot if the server re-checks. Root detection being bypassed is expected (not a finding by itself). A binary secret that is a public key is not a leak.

## Evidence and deliverable

Provide the boundary, the exposed planted artifact/action, the app version and platform, the device-trust assumption, and the control (keystore/server-auth) result. Use planted data/owned accounts. Attach minimal replay, expected/observed, rival explanation, falsifier, boundaries not assessed.

## Versions and tool limitations

Pin the OS version, app version and device root state — behavior is platform- and version-specific. Tools (frida/objection/apktool/jadx) operate on the owned app only. No app behavior was verified by this content; confirm on the owned build first.

## Remediation and detection

Store high-value secrets using the platform Keystore/Keychain where appropriate; exclude bearer tokens and sensitive data from unprotected backups/logs and verify the platform backup policy and encryption for the tested OS. Do not turn this into an absolute ban on all PII or protected backup. Make components non-exported or permission-gated and validate deeplinks; enforce TLS and server-side authorization; use certificate pinning only with a rotation and recovery plan. Treat client-side trust checks as non-authoritative. Add regressions for the named storage, backup and component policies. Detect rooted/tampered clients server-side as signal, not as the control.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | Planted data/action is exposed via a boundary where a hardened app protects it (state device-trust assumption): CONFIRMED; FAIL. |
| Benign refutation | Keystore / non-exported components / server-side auth protects it, or the attack required device root a real user lacks: REFUTED or scoped-down; PASS for the control. |
| Insufficient evidence | A decompiled string without a confirmed exposure path: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/mobile/offensive-mobile/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's storage/IPC/transport/auth/client-trust craft, re-expressed as owned-app experiments with planted data, explicit device-trust assumptions and server-side-auth controls, replacing attacks on other users with bounded boundary proof. Composes with `client-side-trust-boundary`, `token-trust-assessment`, `rt-ssrf`.
