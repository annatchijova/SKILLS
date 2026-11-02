---
name: rt-reporting
description: Assemble assessment reports with evidence-bound findings, reproducible severity reasoning, intact provenance and explicit retest status across exports.
---

# Assessment Report Integrity

Read [METHODOLOGY.md](../METHODOLOGY.md) before promoting observations into findings.
Use this skill to package a completed or partial assessment for review and remediation.
It does not authorize external submission, evidence deletion or additional target testing.

## Mechanisms of reporting failure

- Summaries can promote hypotheses by dropping conditions, versions or failed controls.
- Several instances of one root cause can inflate counts unless grouping is explicit.
- A chain is only as demonstrated as its missing edges; severity does not add arithmetically.
- Cropped screenshots and rewritten requests can lose the facts needed to reproduce a claim.
- Export pipelines can drop labels, links, tables or redactions present in the source document.
- A closure label can confuse risk acceptance, fix deployment and verified remediation.

## Observation and baseline

Inventory finding IDs, original observations, controls, artifact identifiers and target revisions.
For each claim identify actor, resource, action, preconditions and demonstrated effect.
Keep CANDIDATE/CONFIRMED/REFUTED/NOT TESTED separate from PASS/WARN/FAIL control status.
Store remediation workflow state separately: open, deployed, verified or accepted risk.
Define intended readers, required format and authorized evidence retention before exporting.

## Abduction and deduction

Hypothesis: an executive summary overstates a finding by removing its authorization precondition.
Benign rival: the body contains an independent executed test that supports the stronger wording.
Prediction: tracing the summary sentence to its run reveals either the missing prerequisite
or additional evidence; a faithful rewrite preserves the strongest supported scope.
Never repair a report by inventing an experiment or reconstructing absent terminal output.

## Bounded document-review procedure

1. Work from a copy of supplied artifacts; retain immutable originals in the evidence store.
2. Draft each finding as impact, minimal fixture replay, expected/actual result and control.
3. Explain the violated invariant, affected versions and exact reachability conditions.
4. Label each chain edge as observed, code-supported or untested; do not inherit confirmation.
5. Assign severity only from supported metrics. If CVSS is required, record its version,
   full vector, metric rationale and verified calculator implementation/output.
6. Keep organizational impact judgment distinct from the technical score and uncertainty.
7. Write the summary from the completed evidence table; reconcile counts by status and class.
8. Generate requested formats from one source and compare rendered findings with that source.
9. Test redaction with synthetic secret fixtures in an export copy; inspect text extraction,
   image layers, attachments and metadata rather than trusting a black rectangle.
10. Stop when every claim has evidence or an explicit gap; do not perform new target actions
    merely to make the report look complete. Preserve the gap and the proposed experiment.

## Compact finding record

| Field | Required content |
|---|---|
| Identity | Stable finding ID, component/version and assessment window |
| Claim | Actor, boundary, effect and status with bounded scope |
| Proof | Artifact IDs/digests, controlled input, expected/observed result, negative control |
| Rival | Strongest benign explanation and evidence that refuted or retained it |
| Impact | Demonstrated consequence and separately labeled untested chain edges |
| Repair | Structural fix, owner, interim control and detection requirement |
| Retest | Original case, legitimate control, class variant and evidence needed for closure |

## Domain failure modes

Hashing personal data does not automatically anonymize it, especially low-entropy identifiers.
Redact derivatives, retain authorized originals, and use stable nonsecret evidence references.
Screenshot timestamps may reflect capture rather than event time; retain both when relevant.
A fixed release announcement is not a successful retest of the assessed deployment.
A higher business priority does not justify changing unsupported CVSS metric values.
Removing sensitive metadata from a distributed copy is not permission to destroy audit evidence.
Retest failures must remain visible even if other findings are resolved.

## Detection and remediation delivery

For each actionable finding name the event that should have recorded the demonstrated effect,
the responsible identity, correlation keys and a benign control for the proposed detection.
Report missing telemetry as a separate gap rather than claiming the test was undetected.
Specify the invariant the fix must enforce across sibling routes or consumers.
Closure requires actual retest artifacts and remaining limitations, not a uniform green label.

## Versions and tool limits

Record converter/template versions, report source digest and any scoring implementation.
Verify supported schema when exporting to a tracker; imports can silently map statuses wrongly.
Inspect generated artifacts without sending evidence to public converters or outside services.
No external report submission, scoring tool or retest was executed during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Summary asserts anonymous access but trace requires privileged fixture identity | CONFIRMED report overstatement; FAIL until corrected |
| Summary's stronger wording traces to a separate controlled anonymous test | REFUTED overstatement allegation; PASS for that claim |
| Vendor says fixed but no tested version or retest artifact is supplied | NOT TESTED remediation; WARN, retain open verification |

## Provenance

Rewritten from `Skills/utility/offensive-reporting/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain finding structure, scoring rationale, evidence and retest workflows;
replace canned severity assumptions and automatic evidence wiping with traceable review.
