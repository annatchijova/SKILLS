---
name: rt-tls-attacks
description: "Red-team assessment of TLS/SSL configuration boundaries: protocol-downgrade and legacy-protocol exposure (POODLE, DROWN, FREAK, BEAST), compression oracles (CRIME/BREACH), Heartbleed, weak ciphers/keys, certificate validation and shared-key reuse. Re-expressed as scoped enumeration against owned endpoints with testssl.sh-class evidence and clear PASS/WARN/FAIL control scoring instead of live interception."
---

# TLS/SSL Configuration-Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's TLS craft as scoped configuration assessment: it names the vulnerability classes and their indicators, scoring each control PASS/WARN/FAIL from enumeration evidence rather than executing a live downgrade/interception against third parties.

## Scope and prerequisites

TLS findings are mostly configuration posture: which protocols, ciphers, and extensions the endpoint accepts, and whether certificate validation and key hygiene hold. Scan owned endpoints. Active MITM/downgrade is an impact class to reason about; confirm exposure by the server's accepted configuration, not by intercepting real sessions.

Declare target hosts, attempt budget, stop condition. Config-only authorization yields a hypothesis marked NOT TESTED.

## Attack surface and classes

- **Legacy protocols** — SSLv2 (DROWN), SSLv3 (POODLE), export ciphers (FREAK), TLS 1.0 CBC (BEAST).
- **Compression oracles** — TLS compression (CRIME), HTTP compression + reflection (BREACH).
- **Implementation** — Heartbleed (OpenSSL 1.0.1-1.0.1f), ROBOT, Ticketbleed.
- **Weak crypto** — weak ciphers, small keys/DH params, RSA key reuse across hosts (DROWN cross-protocol).
- **Certificate** — expired/self-signed/wrong-host, weak signature, chain issues, missing HSTS.

## Mechanism and observation

Enumerate the accepted configuration and compare to a secure baseline.

**Firstness:** Record exactly what the server accepts (protocols, ciphers, extensions, cert details) from the scanner. **Secondness:** State the secure baseline (TLS 1.2/1.3 only, strong ciphers, valid cert, HSTS) and the deviation. **Thirdness:** Infer the vulnerability class only after the accepted configuration is confirmed.

## Abduction and refutation

**Mechanism hypothesis:** The endpoint accepts a legacy protocol/cipher/extension (or reuses a key) that enables a known downgrade/oracle/leak.

**Competing benign explanation:** The legacy protocol is actually refused (scanner false positive from a probe artifact); the cipher is offered but never negotiated with modern clients; HSTS preload defeats strip; the "shared key" is not actually reused; the OpenSSL build is patched.

## Deduction and controls

A modern handshake succeeds with strong parameters (positive control). A confirmed finding shows the server accepting the weak protocol/cipher/extension where a hardened config would refuse. Predeclare the accepted indicator (e.g. "SSLv3 + CBC accepted"). Refusal of legacy protocols / HSTS preload / patched build are PASS controls; an offered-but-not-negotiated weak cipher may be WARN.

## Induction: bounded procedure

Owned endpoints.

1. **Enumerate.** Run testssl.sh (and sslscan/tlsx for breadth) for full protocol/cipher/vuln output in JSON.
2. **Confirm per class.** POODLE (SSLv3+CBC accepted), DROWN (SSLv2 or shared RSA key with an SSLv2 host), FREAK (export ciphers), BEAST (TLS 1.0 CBC negotiated), CRIME (TLS compression), Heartbleed (vulnerable OpenSSL + heartbeat).
3. **Key reuse.** Extract the certificate modulus; hash and compare across scoped hosts to find shared keys (DROWN cross-host).
4. **Certificate.** Validate chain, host, expiry, signature strength, HSTS.
5. **Score.** Record each control PASS/WARN/FAIL; separate "accepted/negotiable now" from "offered but legacy-client-only".

Record results including refutations. Keep finding status separate from the control score.

## Craft notes (leads)

testssl.sh flags map directly to classes (`--poodle`, `--drown`, `--freak`, `--beast`, `--crime`, `--heartbleed`). DROWN also applies when a modern host shares its RSA key with any SSLv2-enabled host — hence the modulus-hash comparison across infrastructure. BREACH needs HTTP compression + a secret + reflected input (an app-layer condition, not pure TLS). Heartbleed is version-pinned to OpenSSL 1.0.1-1.0.1f.

## Domain-specific failure modes

A scanner "vulnerable" can be a probe artifact — confirm the protocol is actually accepted in a real handshake. An offered weak cipher that no modern client negotiates is WARN, not FAIL. HSTS preload defeats SSL-strip at the client. Cross-host key reuse is the subtle DROWN condition; check it explicitly.

## Evidence and deliverable

Provide the host, the accepted configuration (scanner output), the class and its indicator, any shared-key finding, and the PASS/WARN/FAIL per control. Attach minimal replay, expected/observed, rival explanation (false positive / not negotiated), falsifier, untested hosts.

## Versions and tool limitations

Pin the TLS stack/OpenSSL version and testssl.sh version. Scanners can produce false positives; corroborate with a real handshake. No endpoint behavior was verified by this content; confirm the live configuration first.

## Remediation and detection

TLS 1.2/1.3 only, disable SSLv2/3 and export/CBC-legacy ciphers and TLS compression, patch OpenSSL, strong keys/DH params, no key reuse across hosts, valid certs and HSTS preload. Add a regression asserting legacy protocols are refused. Detect legacy-protocol handshakes and expired/weak certs via monitoring.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | The server accepts a legacy protocol/cipher/extension (or reuses a key) enabling a named class, confirmed in a real handshake: CONFIRMED; control FAIL. |
| Benign refutation | The legacy protocol is refused / weak cipher not negotiated / build patched: REFUTED; PASS (or WARN if merely offered). |
| Insufficient evidence | A scanner flag not corroborated by a handshake: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/crypto/offensive-tls-attacks/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's downgrade/oracle/implementation/cipher/cert craft and its indicator table, re-expressed as owned-endpoint configuration assessment scored PASS/WARN/FAIL with handshake corroboration, replacing live interception with bounded posture evidence. Composes with `rt-crypto-attacks`, `rt-network-attacks`.
