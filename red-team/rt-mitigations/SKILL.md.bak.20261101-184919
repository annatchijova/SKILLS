---
name: rt-mitigations
description: Verify binary hardening configuration and measured enforcement using metadata, runtime state and harmless synthetic boundary probes.
---

# Hardening evidence and enforcement

Read [the assessment contract](../METHODOLOGY.md) before using this skill.
Assess what a defense protects, where it applies and what evidence supports enforcement.
Use metadata inspection and owned synthetic fixtures; do not develop bypasses.
Do not disable host protections or change production policy to complete an experiment.

## Inputs and baseline

Obtain the binary digest, loaded modules, architecture, OS build and deployment policy.
Record compiler/linker flags when available and actual runtime configuration.
Define the claimed guarantee before inspecting flags.
Distinguish hardware capability, binary compatibility, configured policy and active enforcement.
An unsupported feature is not an observed bypass.
A setting absent from one module is not proof that every process lacks it.

## Mechanism matrix

| Defense | Relevant boundary | Evidence and limit |
|---|---|---|
| NX/DEP | Page execution permissions | Mappings and policy; no claim about data writes |
| ASLR/PIE | Address placement | Image type and fresh-process mappings; not proof of entropy |
| RELRO | Relocation-related read-only regions | Program headers, binding mode and runtime permissions |
| Stack protector | Instrumented stack-frame integrity | Selected function instrumentation, not every local object |
| CFI/CFG | Permitted indirect-call targets | Metadata plus active policy and covered modules |
| Shadow stack | Return-address consistency | Hardware/OS/process enablement, distinct from forward-edge CFI |
| Memory tagging | Tagged pointer/allocation consistency | Allocation coverage and checking mode; detection is not universal |
| Sandbox/seccomp | Resource and syscall authorization | Effective profile and harmless allowed/denied probes |
| Kernel isolation | User/kernel access separation | Effective OS evidence, not merely a CPU feature flag |

Keep stack exhaustion separate from stack-buffer overwrite when describing protection.
Canaries do not guarantee detection of every out-of-bounds write.
Memory tagging can have coverage gaps and asynchronous reporting.
A CPU advertising a feature does not prove that a process uses it.

## Abduction and strongest benign explanation

Hypothesis: a synthetic worker violates its declared sandbox policy by opening a file.
Strongest benign rival: that path is explicitly allowed, or the worker was launched
without the profile and therefore is not the deployment claimed in the report.
Deduction: a correctly attributed denied operation should fail with the expected policy
result while a permitted operation succeeds in the same profile.

## Discriminating experiment

1. Define a private test directory with two inert files, ALLOWED and DENIED.
2. Record the synthetic profile's exact resource rule and attach it to the test worker.
3. Verify the worker's identity and effective profile through supported platform evidence.
4. Read ALLOWED to confirm the harness and file setup function.
5. Attempt to read DENIED without any alternate access path or bypass technique.
6. Record the return value, policy audit event and whether bytes were returned.
7. Compare with a separate explicitly unconfined fixture process as a sensitivity control.
8. Stop after the policy result; preserve logs and clean up only test-owned files.

For binary hardening, use an evidence matrix rather than inventing runtime proof.
Inspect ELF/PE metadata with installed tools whose version and help were checked.
Correlate headers with runtime mappings of the exact module.
Repeated ASLR samples establish observed variation only; do not infer a probability bound.
If active CFI or shadow-stack enforcement cannot be safely tested, report NOT TESTED.
Do not create control-transfer payloads merely to complete a matrix cell.

## Reproducibility and tool limits

Preserve tool versions, raw metadata, module IDs and policy export hashes.
Document virtualization, compatibility layers and loader differences.
Tools such as checksec summarize heuristics; inspect their underlying evidence.
Debugger launch settings can affect randomization; capture them.
A compiler flag in a build script is weaker evidence than the artifact actually deployed.
Missing privileges to inspect effective policy produce WARN, not a guessed PASS.

## Detection and remediation

Monitor policy-denial events, unexpected executable mappings and hardening drift.
Bind alerts to binary/module identities and process policy, avoiding raw-address signatures.
Enable supported defenses consistently across relevant modules and verify resulting artifacts.
Repair the underlying memory or authorization defect even when a mitigation stops one effect.
Retest valid operations so policy hardening does not silently break permitted behavior.

## Behavioral cases and expected verdicts

- Confirmed synthetic defect: the attached fixture profile promises DENIED cannot be read,
  yet bytes return while attribution and controls pass. CONFIRMED profile-enforcement defect.
- Benign refutation: the supposedly denied resource is allowed by the documented policy;
  the operation matches the contract. REFUTED bypass claim.
- Insufficient evidence: metadata says CFG-compatible but effective process policy is absent;
  enforcement NOT TESTED, control WARN; no universal protection or bypass verdict.

## Output and provenance

Deliver defense, claimed guarantee, configured state, effective evidence and untested scope.
Source: `Skills/exploit-dev/offensive-mitigations/SKILL.md`.
Upstream commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Rewritten reference; upstream platform defaults and mitigation-bypass recipes are not adopted.
