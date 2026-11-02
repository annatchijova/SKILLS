# Third Review: Findings and Requested Corrections

This document records a review of the 73 `rt-*` skills in this collection. It is written for a follow-up review of the Claude-authored adaptation and is intentionally evidence-bounded: confirmed text defects are separated from issues that still need source verification. No procedures in the skills were executed as part of this review.

## Comparison with Astra's prior version

The prior collection version is commit `2accb05`; the domain-craft restoration is commit `8772b3e`. The earlier Astra-authored skills were generally stronger at experimental discrimination and scope control, while intentionally removing or reducing offensive technique. The Claude-authored restoration brought back attack classes, discriminators and representative laboratory procedures, which is useful and should be retained. The goal is to combine those strengths: keep authorized, synthetic-fixture domain craft and restore Astra's stronger controls and evidence boundaries. Do not solve technical errors by deleting the attack class or by reverting wholesale to the pruned versions.

Examples of useful Astra material to preserve in the merged skills:

- **Cryptography:** the earlier `rt-crypto-attacks` requires a non-secret key-generation identifier, operation IDs to distinguish independent operations from duplicate log records, restart/fork testing, an authentication-before-release sink, and a matched invalid-input control. The restored version adds valuable attack taxonomy and lab craft, but should retain those lifecycle discriminators. It now does so in its observation guidance; keep both.
- **OAuth/OIDC:** the earlier `rt-oauth` tests transaction/session binding, issuer/client validation, wrong PKCE verifier, callback replay, refresh rotation grace, and synthetic account linking. The restored version adds redirect variants, implicit-flow exposure, mix-up, and FAPI topics. Keep the attack classes while restoring the earlier transaction-level controls; the current skill should not reduce OAuth assessment to redirect and token leakage.
- **Containers:** the earlier `rt-container-escape` distinguishes container root from host authority, requires host-side canary provenance, tests a suspect bind against a no-bind control, and explicitly says that CAP_SYS_ADMIN or an old kernel banner alone is only a candidate. The restored version adds socket, capability, namespace and cgroup attack classes. Keep those classes, while retaining the host observer, configuration-specific control, and candidate ceiling.

These are comparisons of committed skill text, not claims that Astra's version was fully correct or executed. The prior version is a methodological reference, not a technical authority. Upstream material is likewise a source of domain craft, not proof that a claim is accurate or safe to generalize.

## Confirmed defects corrected in this review

### Cryptographic claims and evidence

In `rt-crypto-attacks`, the restored text previously stated categorically that GCM nonce reuse recovers the authentication key, that uniform constant-time errors remove a padding oracle, that a CSPRNG defeats state cloning, and that percentile statistics establish timing leakage. It also let repeated nonce observation stand beside plaintext recovery and forgery as if those were interchangeable confirmation criteria.

The skill now scopes GCM's consequences to same-key nonce reuse and applicable message/tag conditions; separates IV misuse, plaintext recovery and forgery; requires RSA prerequisites (including the conditions for Håstad broadcast); treats CSPRNG as an implementation/use claim; and asks for a declared timing contrast, sampling plan, noise controls, effect and uncertainty. Uniform error text alone is no longer treated as proof that no observable oracle exists. ECB is scoped to equal aligned blocks under the same key and explicitly does not imply exploitable cut-and-paste impact. RSA remediation no longer treats a large public exponent as a general fix. The earlier Astra key-ID, operation-ID and authentication-boundary controls remain included.

Reference: [NIST SP 800-38D](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf).

### OAuth fragment and current guidance

`rt-oauth` previously said that an implicit-flow fragment leaks through `Referer`. RFC 9110 says a conforming user agent does not include a fragment in the `Referer` field. The skill now points testing toward browser history, scripts and application-specific forwarding and requires evidence for the actual path. It also replaces the unqualified claim that “OAuth 2.1 mandates” the behavior with the current RFC 9700 guidance and asks the assessor to name the applicable profile and PKCE binding requirements.

References: [RFC 9110](https://datatracker.ietf.org/doc/rfc9110/), [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html).

### Container capability and cgroup scope

`rt-container-escape` previously treated one `CapEff` value as universally meaning all capabilities and described `release_agent` as a generic CAP_SYS_ADMIN route. The skill now requires decoding the bitmask against the running kernel's capability limit, scopes `release_agent` to cgroup v1 plus its additional preconditions, and states that cgroup v2 lacks that interface. It also avoids claiming that a hardened configuration cannot escape in general: any PASS is limited to the vectors and configuration tested. Astra's host-side canary and no-bind comparison are preserved as the preferred discriminator.

References: [proc_pid_status(5)](https://www.man7.org/linux/man-pages/man5/proc_pid_status.5.html), [proc_sys_kernel(5)](https://man7.org/linux/man-pages/man5/proc_sys_kernel.5.html), [cgroups(7)](https://man7.org/linux/man-pages/man7/cgroups.7.html).

### Zigbee, Thread and Matter separation

`rt-zigbee-thread-matter` previously attributed Matter PASE/CASE to Thread and presented the three protocol families' commissioning and anti-replay controls as interchangeable. It now gives Zigbee, Thread and Matter separate assessment paths; describes Thread's commissioner/joiner and PSKc flow separately from Matter PASE/CASE; and treats an open join window as exposure rather than proof that an unauthorized join succeeded. Evidence and regression cases must remain protocol-specific.

Reference: [Thread Commissioning White Paper](https://www.threadgroup.org/Portals/0/documents/support/CommissioningWhitePaper_658_2.pdf).

### Evil-twin controls

`rt-evil-twin` previously presented server-certificate validation, PMF and WPA3 as equivalent controls against rogue AP association and credential disclosure. It now separates association, credential/challenge disclosure and application-traffic exposure. It scopes server-certificate validation to Enterprise RADIUS authentication, PMF to robust management-frame protection, and WPA3 to its selected authentication mode and client profile. A result for one property cannot substitute for another. Microsoft's driver documentation describes PMF as protecting specified management/action frames, supporting this narrower scope: [Microsoft PMF documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/network/oid-wdi-task-connect).

### Mitigation taxonomy

`rt-mitigations` previously grouped Intel LAM with MTE as if both were memory-safety mitigations and described CFI/CET as a combined universal ROP/JOP control. It now distinguishes CFI policy, CET shadow stack and IBT, and describes LAM as pointer metadata support rather than a drop-in memory-corruption mitigation. Remediation is scoped to the platform and feature actually available.

References: [Intel Linear Address Masking](https://edc.intel.com/content/www/jp/ja/design/platforms/core-processor-series-3-datasheet-volume-1-of-2/001/linear-address-masking-lam/), [Intel CET overview](https://www.intel.com/content/www/us/en/developer/articles/technical/technical-look-control-flow-enforcement-technology.html).

`rt-windows-mitigations` now explicitly warns that the catalog is not a universal per-process policy: inventory build, hardware and system/app policy, including signer options. The exact feature descriptions and availability still require a per-feature check against Microsoft's current documentation.

### Network, concurrency and filesystem semantics

- `rt-network-attacks` now distinguishes DNSSEC data authentication from application-side destination validation needed for rebinding/SSRF; scopes DHCP-snooping trusted ports to verified infrastructure; and no longer treats sticky MAC as a substitute for 802.1X identity policy.
- `rt-race-condition` now says packet alignment can reduce arrival spread but cannot prove simultaneous execution, and a constraint protects only the invariant and write path it actually covers.
- `rt-toctou` now says `openat` alone is not a symlink defense and final-component `O_NOFOLLOW` is not a whole-path guarantee. The opened object and path-resolution policy must both be checked.
- `rt-wpa3-sae` now separates transition downgrade, implementation-specific SAE side channels and PMF; each has a distinct control and refutation. `rt-deauth-disassoc` scopes PMF to negotiated protection of specified robust management frames and the relevant association state.
- `rt-mobile` and `rt-iot` now avoid absolute bans on all PII/backups or all firmware keys. The guidance distinguishes unprotected sensitive data and private secrets from protected backup policy and public verification material.
- `rt-phishing` now separates DMARC domain alignment from lookalike detection and reports mail delivery, scanner-filtered user actions and reports as different outcomes. Current reference: [RFC 9989 DMARC](https://www.rfc-editor.org/rfc/rfc9989.html). `rt-cicd-secrets` scopes IMDSv2/hop-limit claims to the tested network path and does not claim finite masking tests cover all encodings.
- `rt-netexec` no longer translates `Pwn3d!` into a universal privilege/code-execution meaning; it requires version/module interpretation and corroboration. Exact NetExec behavior remains on the verification queue below.
- `rt-tls-attacks` now distinguishes configuration exposure from demonstrated exploitability and requires the named attack's additional preconditions. The exact attack-specific preconditions still need primary-source review before the skill is considered fully audited.

### Confirmation scope and Peirce

`METHODOLOGY.md` and `rt-reporting` now require every `CONFIRMED` result to name the exact proposition and system scope: a deliberately vulnerable fixture, the assessed target/version/configuration, or an impact inference. A fixture can validate a method or mechanism; it cannot confirm that a different target shares the defect. `PASS/WARN/FAIL` remain control statuses and cannot substitute for finding epistemic status.

Peirce is a requirement and remains in all `rt-*` skills. No omission was accepted on the grounds that the triad was unnecessary. The required operational use is: Firstness records the observation without interpretation; Secondness states the explicit baseline and deviation; Thirdness infers only the repeatable class supported by the discriminator, with the inference scope stated. Abduction proposes the mechanism and strongest benign rival; deduction gives distinct predictions and a negative control; induction tests and records either result. A fixture observation must not be worded as a target-wide law.

## Items still requiring independent verification

These are review leads, not adjudicated defects. Check the live lines and current primary/vendor documentation before changing them:

1. `rt-windows-mitigations`: verify each feature description, availability and scope against [Microsoft's exploit-protection reference](https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection-reference) and a pinned target build; the new warning does not itself validate the technical details.
2. `rt-netexec`: inspect the pinned version's source/help and test exact protocol/module output meanings; do not reintroduce a generic `Pwn3d!` mapping.
3. `rt-tls-attacks`: verify BEAST, DROWN, POODLE, FREAK, CRIME, Heartbleed, ROBOT and Ticketbleed prerequisites against authoritative protocol/vendor sources.
4. Other wireless claims: verify EAP certificate-validation, group negotiation and anti-replay semantics against the named standard/profile and implementation. Do not generalize from a single AP/client control.
5. `rt-keylogger-arch`: verify what hook types and registration state can be enumerated through documented OS interfaces, and distinguish API state from EDR telemetry.
6. Review all remaining acceptance tables for explicit proposition, fixture/target scope, negative control and an independent finding status. The earlier report found the pattern repeatedly, but each row still needs a live-file check before being called defective.

## Audit method and limits

- Scope: all 73 directories named `rt-*`; non-`rt-*` author-created skills were excluded as requested.
- Method: static reading of authored skill text, comparison with the preceding committed versions and cited upstream provenance, plus spot verification against primary standards/vendor documentation for the corrected claims above.
- No skill procedure was executed; no target or attack outcome was assessed. This document does not certify the technical correctness of unlisted statements or runtime behavior.
- No tests were run. This was documentation review and editing only.
- Governing skills used: `abductive-engineering`, `red-team-auditing`, `audit-before-patch`, `surgical-patcher`, `daubert-defensible-writing`, `claim-provenance-discipline`, and `crypto-misuse-reasoning`.
