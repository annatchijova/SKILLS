---
name: rt-osint-methodology
description: Adjudicate public-source relationships and timelines using provenance, competing explanations and controlled synthetic media or transaction datasets.
---

# Open-Source Evidence Correlation

Read [METHODOLOGY.md](../METHODOLOGY.md) before proposing a relationship or timeline.
Use this skill to evaluate a defined claim across supplied public-source artifacts.
Asset collection belongs in rt-osint; correlation does not grant further collection authority.

## Mechanisms and preconditions

- Reposts and syndicated feeds create apparent corroboration without independent observation.
- Entity resolution can confuse shared identifiers, handle changes and unrelated namesakes.
- Upload, capture, publication and event timestamps measure different moments.
- Media metadata can be edited or stripped; transformations change forensic signals.
- On-chain transactions establish transfers under a chain's semantics, not human ownership.
- Infrastructure/code similarity may reflect a common supplier rather than a common actor.
No number of weak correlated signals automatically proves attribution.

## Observation and baseline

State one falsifiable claim, its time window and the exact objects being linked.
Inventory originals, derivatives, source publishers, capture methods and transformation history.
Represent time as intervals with precision, timezone and clock uncertainty.
Represent relationships explicitly: repost-of, same-key, transfer-to or matches-landmark.
Keep identity, intent, sponsorship and technical capability as separate claims.

## Abduction and deduction

Hypothesis: two published artifacts independently document the same event.
Benign rival: one is a cropped/re-encoded copy of the other with a misleading publication time.
Prediction: original-source lineage or shared unique frame defects show dependence;
independent capture evidence survives comparison and aligns within the stated time interval.
Choose a discriminator that could reject the proposed relationship, not a collection quota.

## Bounded laboratory/review procedure

1. Work with supplied, authorized artifacts or synthetic datasets; hash originals before analysis.
2. Build a claim-to-source graph and collapse known repost/feed dependencies for evidence counting.
3. For images, compare stable nonpersonal landmarks and geometry with reference material;
   avoid identifying individuals or locating private residences from media.
4. Compare metadata from two parsers where interpretation matters; preserve disagreement.
5. For chronology, distinguish upload from capture and test alternate timezone/clock assumptions.
6. Use synthetic original/crop/re-encode pairs as controls for similarity and metadata claims.
7. For transaction evidence, record chain ID, block hash/height, transaction index, contract
   and event semantics. Compare provider interpretation with the supplied receipt/state evidence.
8. Treat bridge mint/burn, fees, wrappers and aggregation as explicit transformations;
   equal amounts and close times alone do not prove a cross-chain link.
9. For infrastructure linkage, test a shared-provider alternative using known unrelated fixtures.
10. Stop at the budget or when no available observation can discriminate; retain uncertainty.
11. Produce a bounded decision and evidence needed to reopen it; preserve originals and derivatives.

## Domain failure modes

Error-level analysis and deepfake scores cannot alone prove fabrication or authenticity.
Valid content credentials can attest signed history without proving the depicted event is true.
Missing metadata is common after export and does not establish deliberate concealment.
Shadow analysis needs location, geometry, date and uncertainty; do not report false precision.
Zero-knowledge proof usage does not imply that all rollup transaction data is private.
Finality and challenge windows are chain/version-specific; do not impose one universal interval.
Vendor wallet labels are inherited claims; a transaction counterparty is not necessarily owner.
An IOC shared with a vendor report does not establish actor identity or state sponsorship.

## Evidence and response

Deliver a relationship ledger with claim, source IDs/digests, time interval, dependence group,
supporting/contrary observations, discriminator, result and falsifier.
Use CONFIRMED only for the bounded relationship demonstrated; keep identity hypotheses separate.
For security monitoring, provide observable indicators with validity windows and false-positive
controls, not unqualified actor labels. Validate the detector against unrelated shared-provider data.
Remediate analytic failures through lineage preservation, explicit temporal joins and removal
of unsupported labels from derived reports; preserve the original record of the correction.

## Versions and limits

Record media/parser, chain data, normalization and graph-tool versions and dataset provenance.
Inspect current schema and chain semantics before interpreting receipts or content credentials.
Do not create deceptive personas, run hostile samples or submit confidential artifacts to services.
No media investigation, blockchain query or actor attribution campaign ran during authorship.

## Behavioral acceptance

| Case | Expected verdict |
|---|---|
| Original lineage and unique frame evidence show two reports reuse one capture | CONFIRMED source dependence; FAIL if counted as independent |
| Distinct original captures and timing controls refute the proposed repost relationship | REFUTED dependence claim; preserve separate observations |
| Similar wallet amounts or shared infrastructure lack independent linking evidence | CANDIDATE relationship; WARN, no ownership/actor attribution |

## Provenance

Rewritten from `Skills/recon/offensive-osint-methodology/SKILL.md` at
`a8de813edc9f66f60d44cfe42d47750e89d9930b`.
Treatment: retain source correlation, chronology, media and transaction semantics; replace
deceptive personas, personal tracking and arbitrary attribution thresholds with falsifiable joins.
