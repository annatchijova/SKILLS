---
name: rt-vuln-classes
description: "Reference taxonomy of memory-safety and low-level vulnerability classes for triage and hunting: out-of-bounds read/write, use-after-free, double-free, type confusion, integer overflow/underflow, uninitialized memory, NULL deref, format string, and race/TOCTOU. Each class with its invariant, root-cause signature, typical sink, exploitability tendency and detector. Re-expressed as a classification aid for owned-target triage, not a payload collection."
---

# Vulnerability Class Taxonomy

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract when classifying.
This revision restores the upstream's vuln-class material as a classification reference: each class names the invariant it violates, how to recognize it, where it tends to be exploitable, and how to detect it — a lookup aid for triage, not a set of weaponized payloads.

## Scope and use

Use this to assign a defensible class to a bug found by fuzzing, review or crash triage, and to reason about where to hunt its siblings. Classification is an inference from evidence (`rt-bug-identification`), and exploitability per class is a tendency, not a verdict (`rt-crash-analysis`).

## The classes

Each entry: the violated invariant → recognition signature → typical sink → exploitability tendency → detector.

- **Out-of-bounds read** — access past a buffer's bounds. Signature: read of adjacent/unmapped memory; info leak. Sink: array/pointer arithmetic, length miscompute. Tendency: info leak (ASLR defeat) more than control. Detector: ASan, bounds checks.
- **Out-of-bounds write** — write past bounds. Signature: corrupted adjacent data/metadata. Sink: unchecked copy/index. Tendency: high (overwrite pointers/metadata). Detector: ASan, canaries.
- **Use-after-free** — use of freed memory. Signature: access to a dangling pointer; reallocation controls contents. Sink: lifetime/ownership error. Tendency: high (type confusion, control). Detector: ASan, MTE.
- **Double-free** — freeing twice. Signature: allocator abort/corruption. Sink: duplicate ownership. Tendency: medium-high (allocator exploitation). Detector: ASan, hardened allocator.
- **Type confusion** — treating an object as the wrong type. Signature: field misinterpretation, bad vtable. Sink: unchecked downcast, union misuse, deserialization. Tendency: high. Detector: UBSan (vptr), CFI.
- **Integer overflow/underflow** — arithmetic wraps past the type's range. Signature: undersized allocation, bypassed bounds check. Sink: size/length math. Tendency: medium (gateway to OOB). Detector: UBSan.
- **Uninitialized memory** — reading before writing. Signature: nondeterministic values, leaks. Sink: missing init path. Tendency: info leak. Detector: MSan.
- **NULL/near-NULL deref** — dereferencing NULL. Signature: fault at low address, no attacker control. Tendency: usually DoS only. Detector: crash triage.
- **Format string** — user input as a format. Signature: `%n`/`%x` effects. Sink: `printf(user)`. Tendency: read/write primitive. Detector: compiler format warnings.
- **Race / TOCTOU** — check and use not atomic over shared state. Signature: behavior depends on timing. Sink: check-then-act (see `rt-toctou`, `rt-race-condition`). Tendency: varies. Detector: TSan, invariant tests.

## Mechanism and observation

Classify by the broken invariant, not the crash site.

**Firstness:** Record the first wrong operation and the data it corrupted/leaked. **Secondness:** State the memory-safety invariant the class violates (bounds, lifetime, type, initialization, arithmetic range, atomicity). **Thirdness:** Assign the class only after the root cause (not the fault site) matches the invariant.

## Classification discipline

- One bug can present as several classes (an integer overflow causing an OOB write) — name the root class and the downstream effect separately.
- A crash site rarely equals the bug class — root-cause first.
- Exploitability tendency is a prior, not a verdict — confirm with `rt-crash-analysis`.
- Memory-safe languages eliminate most of these by construction; note when the class is impossible in the target language.

## Domain-specific failure modes

Classifying by the faulting frame instead of the root cause mislabels the bug. Collapsing an integer-overflow-to-OOB into just "OOB" loses the fix site. Treating a class's exploitability tendency as a verdict overclaims. A NULL deref labeled "high" is the common over-call.

## Deliverable

For each bug: the assigned root class, the violated invariant, the downstream effect class (if any), the detector that would catch it, and a pointer to its exploitability triage. Keep the classification evidence-based and language-aware.

## Provenance and treatment

Upstream research: `Skills/fuzzing/offensive-vuln-classes/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's vulnerability-class material as an invariant-based classification reference with detectors and exploitability tendencies, replacing a payload collection with a triage lookup aid. Composes with `rt-bug-identification`, `rt-crash-analysis`, `rt-toctou`, `invariant-hunting`.
