---
name: rt-tls-attacks
description: Validate TLS peer identity, negotiated policy, early-data handling and compression preconditions in owned client-server fixtures.
---

# TLS Trust and Transport Assessment

Read [METHODOLOGY.md](../METHODOLOGY.md) before selecting a handshake test.
Separate server configuration, client validation and application replay semantics.
A supported protocol or scanner label is not proof of a complete historical attack.

## Mechanisms and preconditions

- Certificate validation combines trusted issuer, name, validity and application policy.
- mTLS authenticates a certificate; authorization must map its identity to permitted actions.
- Negotiation depends on both endpoints, SNI, ALPN and any terminating proxy.
- TLS early-data acceptance and a duplicated application effect are different claims.
- HTTP compression leakage requires secret/reflected data co-compression and an observable
  length channel; a gzip header alone is insufficient.
- HSTS behavior depends on client state and domain scope, separately from TLS negotiation.
- Historical CBC, export-cipher and memory-disclosure flaws have version and path preconditions.

## Observation and baseline

Record the actual client build, server/terminator, destination, SNI, ALPN and trust store.
Specify the peer identity expected by the application and the allowed protocol policy.
Retain the negotiated result rather than substituting a generic TLS scanner's view.
Use test certificates, synthetic response secrets and a local side-effect counter.
Do not intercept unrelated traffic or disable verification in the tested client.

## Abduction and deduction

Hypothesis: this client omits hostname validation while still accepting the certificate chain.
Benign rival: the scanner connected without the application's intended SNI or trust store.
Prediction: the actual client accepts a trusted but wrong-name test certificate while a
validation-enforcing twin rejects it; both accept the matching-name certificate.
Distinguish failure before handshake from rejection caused by the property under test.

## Bounded laboratory procedure

1. Create an owned loopback/test-network TLS server and isolated application client profile.
2. Establish successful communication with a matching-name, valid, fixture-trusted certificate.
3. Change only the certificate name, preserving issuer and server behavior; record acceptance.
4. Independently test an untrusted issuer and expired certificate, with clock state recorded.
5. For mTLS, compare allowed client identity, trusted but unauthorized identity and no certificate;
   inspect application authorization, not only successful handshake completion.
6. For early data, use a synthetic operation with an instrumented counter and fixture session.
   Compare early and ordinary delivery, duplicate delivery and idempotency-enabled control.
   A new connection that sends a second request is not proof of captured-record replay.
7. For compression, measure encoded wire/body bytes for synthetic data; compare compression
   disabled and reflection removed controls. Do not infer wire length from decoded response text.
8. Limit handshakes and requests before starting; stop on unexpected state or absent controls.
9. Remove test trust anchors and sessions, restore profile settings, and verify normal behavior.

## Domain failure modes

A client lacking old-protocol support cannot demonstrate that a server rejects that protocol.
Load balancing may expose different TLS configurations; record the terminator tested.
A source occurrence of verify=False may belong to a test stub rather than a production path.
Instrumentation that disables pinning changes the property being measured.
TLS fingerprints are not proof of malicious instrumentation or a particular application build.
Certificate transparency records establish logged issuance, not current endpoint ownership.
Compression distinguishability alone does not prove secret recovery at practical query cost.

## Evidence, detection and remediation

Retain sanitized handshake transcripts, certificate fingerprints, trust policy, application
outcomes and fixture counter events. Bound each verdict to client, route and version.
Detect unexpected negotiation changes, validation failures and duplicated state-changing events.
Use maintained TLS libraries with identity validation and deliberate trust-store management.
Authorize mTLS identities explicitly; reject or safely handle early data on sensitive operations.
Separate reflected input from secret-bearing compressed responses where the channel exists.
Retest legitimate clients as well as rejected peers before closing the finding.

## Versions and limits

Record TLS library build, enabled providers, scanner version and platform trust behavior.
Inspect installed help; similarly named flags do not establish FREAK or 0-RTT coverage.
Memory-disclosure and downgrade exploitation are excluded; assess patch/build evidence instead.
No network handshake or scanner was executed during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Actual client accepts trusted wrong-name peer; validating twin rejects it | CONFIRMED hostname-validation failure; FAIL |
| Scanner omitted SNI; actual configured client rejects wrong peer and accepts correct peer | REFUTED client-bypass claim; PASS |
| gzip and TLS 1.3 appear in headers without wire measurements or state evidence | NOT TESTED leakage/replay impact; WARN |

## Provenance

Rewritten from `Skills/crypto/offensive-tls-attacks/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain trust, negotiation, compression and replay distinctions; replace pinning
bypass, interception and memory extraction recipes with owned-fixture control tests.
