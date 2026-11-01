# Independent final review

Date: 2026-11-01. Scope: collection tooling and eight representative adaptations. Reviewer: this independent review session, separate from the authors. No additional auditor agents were available or invoked.

## Decision

One low-severity tooling defect was reproduced: ambiguous skill identity metadata is accepted. No concrete content defect was identified in the eight reviewed adaptations under the shared methodology contract. This is a bounded review, not certification of all 107 skills or of behavior on live targets.

The existing 16 tests passed. Independent catalog execution returned 107 entries; the snapshot inventory contained 28 copied skill identities, leaving 79 adaptations. The maintainer subsequently reported completed coverage and manifest generation; that integration claim is not substituted for an independent full upstream validation run here.

## IR-01: reject ambiguous identity metadata consistently

**Priority:** low (P3), tooling correctness. **Level:** CONFIRMED BY INDUCTION using isolated temporary fixtures. **Status:** open at review time; authors were notified with anchors. This is not a demonstrated security exploit.

**Files:** `validate_collection.py:40–46`, `catalog.py:20–21`; regression coverage belongs in `test_collection.py`.

**Observed / expected:** a header containing both `name: rt-example` and `name: different-identity` passes the full fixture validator and is catalogued as `rt-example`. An identity validator should reject contradictory definitions rather than certify the first matching occurrence. The catalogue and validator also disagree on quoted scalars: `name: "rt-example"` is rejected by the validator but emitted by the catalogue with quote characters included in the identity.

**Abduction:** both readers select a textual occurrence instead of enforcing one unambiguous metadata identity. Benign rival: the full validation path rejects malformed metadata elsewhere, or the disagreement is solely an intentional restriction on quoted syntax.

**Deduction:** the normal fixture should pass; adding a second contradictory name should be rejected if another guard exists. Restricting quoted syntax would not explain accepting two contradictory unquoted keys.

**Induction:** the normal fixture passed. The duplicate-name fixture also passed the complete `validate()` call and catalogue subprocess. The quoted fixture produced the disagreement above. The benign explanation does not account for duplicate acceptance. Both experiments used the current production reader code; only the source inventory and snapshot baseline were mocked by the existing fixture setup.

**Impact bound:** an edited adaptation can pass structural validation with ambiguous identity metadata. No downstream agent loader was exercised; rejection by another parser, selection of another key, or runtime dispatch consequences are not claimed. The experiment does not show that any current adaptation has duplicate names.

**Reproducer:** run from `red-team`; it creates and cleans temporary files only, leaving repository skills unchanged.

```bash
python3 -B - <<'PY'
import json
import subprocess
from pathlib import Path
from test_collection import CollectionValidationTests
from validate_collection import validate

for label, replacement in (
    ('normal', None),
    ('duplicate_name', 'name: rt-example\nname: different-identity'),
    ('quoted_name', 'name: "rt-example"'),
):
    fixture = CollectionValidationTests()
    fixture.setUp()
    try:
        target = fixture.root / fixture.target
        if replacement:
            target.write_text(target.read_text().replace('name: rt-example', replacement))
        script = fixture.root / 'catalog.py'
        script.write_text(Path('catalog.py').read_text())
        try:
            result = validate(fixture.root, fixture.upstream)
            print(label, 'validator ACCEPT', result['total_skill_count'])
        except ValueError as error:
            print(label, 'validator REJECT', str(error))
        result = subprocess.run(
            ['python3', '-B', str(script), 'red-team'],
            capture_output=True, text=True,
        )
        names = [entry['name'] for entry in json.loads(result.stdout)] if result.returncode == 0 else result.stderr
        print(label, 'catalog', result.returncode, names)
    finally:
        fixture.doCleanups()
PY
```

Observed output, with the temporary path shortened:

```text
normal validator ACCEPT 2
normal catalog 0 ['method', 'rt-example']
duplicate_name validator ACCEPT 2
duplicate_name catalog 0 ['method', 'rt-example']
quoted_name validator REJECT Invalid skill identity: <temporary>/collection/rt-example/SKILL.md
quoted_name catalog 0 ['method', '"rt-example"']
```

**Complete fix criterion / falsifier:** one shared metadata contract rejects duplicate identity keys in both entrypoints and either consistently decodes or consistently rejects quoted identities. Normal valid headers still work. Add negative controls for both key orders and a positive control for the selected supported syntax. A rerun rejecting the duplicate fixture in both paths while preserving the ordinary fixture closes the demonstrated defect. No code fix was made by this reviewer.

## Independent scenario review

These are 24 newly constructed evidence scenarios, evaluated manually against the live documents and `METHODOLOGY.md`; they are not executions of target systems or automated evaluations of an agent. “CONFIRMED” below describes the verdict warranted **if the stipulated evidence were supplied**, not a target finding from this review. Control outcomes remain bounded to the named property. The scenarios deliberately exercise mechanisms beyond the embedded acceptance examples.

| Skill | Positive evidence scenario and warranted verdict | Benign scenario and warranted verdict | Insufficient evidence scenario and warranted verdict |
|---|---|---|---|
| `rt-ai-security` | An unchanged owner identity requests one permitted fixture action; a delegated worker exceeds a declared one-call budget, and the second sink event is recorded. The same worker under enforced budget produces only one event, while the legitimate call succeeds. CONFIRMED budget-enforcement failure; FAIL, not a general model jailbreak. | A response contains B's unique marker, but the captured input shows A explicitly supplied that marker; retrieval IDs contain only A's documents and the B-only retrieval control is denied. REFUTED cross-tenant retrieval claim for this run; PASS for that tested boundary. | Reloaded summary text loses its source labels, but no subsequent retrieval, policy decision or sink trace is retained. CANDIDATE provenance-loss consequence; WARN. A text change alone does not establish an unauthorized action. |
| `rt-dependency-confusion` | A runtime lock remains intact, but a transitive build plugin resolves from the alternate fixture repository, against a predeclared plugin-source policy. Cold-cache logs and digest identify the alternate; explicit plugin source binding restores the intended package and the build control still succeeds. CONFIRMED plugin source-selection failure; FAIL, no execution-impact inference. | An alternate fixture package has a larger version but is incompatible with the pinned platform. Candidate logs explain its exclusion, and the selected intended digest matches policy. REFUTED wrong-origin claim for this restore; do not claim the source binding resisted a compatible alternate. | A cache-only restore returns the intended digest after a mapping edit; no cold resolution was captured. Source-binding effectiveness remains NOT TESTED; WARN despite a successful restore. |
| `rt-request-smuggling` | In an isolated translation chain, captures and parser events show one frontend message becoming two backend messages, with the extra inert marker parsed only on the reused connection. Ordinary paired requests remain aligned and disabling reuse removes the association error. CONFIRMED framing/association failure for that topology; FAIL. | Raw metadata differs across a protocol translation, but normalized body extents and fixture response IDs agree at every hop across repeated ordinary sequences. REFUTED claim based only on metadata differences; PASS for the observed agreement, not every framing case. | Two responses appear in a capture, but no connection IDs were preserved and the client may have retried. CANDIDATE association anomaly; WARN until retry and connection explanations can be distinguished. |
| `rt-deserialization` | A permitted outer data object contains an untrusted nested type; ordered events from the real adapter show the nested inert hook runs before its denial. Normal nested data still loads; pre-resolution rejection prevents the hook. CONFIRMED nested type-admission failure; FAIL, not arbitrary code execution. | The endpoint decodes bytes into an opaque queue envelope; the consumer demonstrably uses a data-only schema and rejects unknown type fields, while legitimate records pass. REFUTED executable-reconstruction claim for the traced route; PASS for that route only. | The sentinel class exists only in an instrumented loader fixture; the deployed adapter's byte provenance and class availability are unknown. CONFIRMED fixture ordering at most; production reachability NOT TESTED and WARN. |
| `rt-anti-forensics` | A synthetic collector export silently deduplicates two distinct sequence IDs sharing a timestamp, then asserts complete coverage. The preserved original and independent receipt ledger contain both; unique-timestamp controls retain both. CONFIRMED evidence-completeness validation defect; FAIL, no malicious-intent inference. | Host and collector times differ by a measured fixed offset; sequence IDs, receipts and retention records fully reconcile after the documented conversion. REFUTED timestamp-tampering inference for these records; PASS for this reconciliation. | A recovered event matches its stored digest but the acquisition sequence boundaries were never recorded. Integrity since hashing is supported; acquisition completeness remains unknown, WARN. Do not call reconstruction complete. |
| `rt-edr-evasion` | Marked events are locally generated, centrally indexed and matched by the intended alert rule, but no alert is created within the declared alert deadline. A matched endpoint under the same policy alerts, and health controls pass. CONFIRMED alert-stage failure; FAIL for alerting, not collection or prevention. | A harmless diagnostic action is prevented before process creation, with the prevention decision retained and the health marker arriving normally. Absence of a process-start event is explained; REFUTED collection-gap inference for that action. PASS for the observed prevention only. | The synthetic heartbeat replay triggers an alert after injection directly into analytics. Downstream rule behavior is observed; endpoint-to-collector continuity remains NOT TESTED, WARN. No evasion-resistance conclusion follows. |
| `rt-wpa3-sae` | Within a declared authentication-load ceiling, measured AP scheduling delays legitimate SAE associations beyond the agreed service deadline; idle controls succeed and a matched admission-control configuration restores timely association. CONFIRMED bounded availability-control failure for that load/configuration; FAIL, no password-leakage claim. | A transition advertisement includes more than one AKM, while both endpoint logs show the unchanged required profile negotiated SAE and exchanged the canary normally. REFUTED downgrade inference from advertisement alone; PASS for this observed negotiation. | A canary exchange succeeds after AP configuration changes, but neither negotiated AKM nor saved profile identity is retained. CANDIDATE policy-enforcement question; WARN. Connectivity alone does not identify the security mode. |
| `rt-exploit-development` | Public fixture replay frees allocation generation G, then a later reachable operation reads G after release. Allocation/lifetime instrumentation identifies the first invalid access; an ownership-preserving build and valid neighboring inputs pass. CONFIRMED reachable lifetime defect; FAIL, no arbitrary-write or code-execution claim. | A format-looking string reaches a logging API only as a data argument; captured call arguments and runtime output show a constant format and literal rendering. REFUTED format-interpretation claim on that path; PASS for the tested invariant. | A reduced-width arithmetic model wraps, but the actual binary's operand width and public length constraints are unknown. Model behavior is established; product defect remains CANDIDATE, runtime NOT TESTED and WARN. |

The eight documents provide enough domain-specific constraints to reach these bounded decisions when read with the shared contract. No contradiction requiring a skill edit emerged from this exercise. This does not establish that every agent will follow the instructions correctly.

## Executed checks and reviewed files

- Python runtime: 3.12.3, GCC 13.3.0.
- `python3 -B -m unittest -v test_collection`: 16 tests, 0.125 seconds, `OK`, exit 0. Includes snapshot mutation, added resources, source inventory, coverage, contract links, symlinks, and nonrecursive catalogue controls.
- `python3 -B catalog.py red-team`: exit 0; 107 catalogue entries. `SOURCES.json` supplied 28 unique copied skill directories.
- IR-01: actual validator and catalogue execution against temporary normal, duplicate-name and quoted-name fixtures, as reproduced above. No repository fixture or tooling edits.
- Fully read: `METHODOLOGY.md`, `validate_collection.py`, `test_collection.py`, `catalog.py`, and all eight `SKILL.md` files named in the scenario table. Also read `README.md` for the selection and validation contract and inspected the snapshot inventory for counts.
- Applied personal methodology skills: abductive-engineering, audit-before-patch, discriminating-proof, red-team-auditing, dual-use-behavior-adjudication, claim-provenance-discipline, remediation-driven-reporting; git-discipline informed the state checks. The explicit report-only assignment limited repository mutation to this new report.

Reviewed byte identities (SHA-256):

```text
e7c492306fc77a7f1c9aaa5a9a0e91b1d1c9901a716ae0a2bc7c93415e10b82e METHODOLOGY.md
124794d2ed993474bdb4448969a18fb3698807a4c7d058c6d3122467fe12a681 validate_collection.py
0e368776db6d986cc1fe6ab05b9a58884b9cf265d6177d6f091bac3c22ba13e9 test_collection.py
d3f6aab8483451d0a18ba5f2a007556de56c08db995139444359e6ae3f2d223b catalog.py
765432c5374edc6effcb0f34dc52e3a7b457ac1cf0212e310624b4a8184bff85 rt-ai-security/SKILL.md
557537cef52490faed7b3209c263622973914f075253d24d086d1e4488d4a784 rt-dependency-confusion/SKILL.md
f273dc8a127127183d680322012166fb8626b65275aee29c8c7741d39c45cf6f rt-request-smuggling/SKILL.md
b0a7708f297e01c99ff89557d80beb5aef42e3f0f85b5929a261e3321e047ace rt-deserialization/SKILL.md
32ece97050a1f86169e371a3026a808388ad119825c2747f301848661c123834 rt-anti-forensics/SKILL.md
ac9b829ba00698f03dc85a8f854ddc78800e8609711d18d4ba175a8ee10b1928 rt-edr-evasion/SKILL.md
d07300a7910ec2541701006e2d91b9965b2f18578e379a59596d7fbe0c8cee49 rt-wpa3-sae/SKILL.md
6763ca4c8f795dff7395f8447105aea006e779785bed0ac5ba33bd33c643baa5 rt-exploit-development/SKILL.md
```

## Refuted concerns and limitations

- A model-generated answer is not treated as proof of an executed tool effect: the AI skill explicitly records proposed calls, policy decisions and sink state separately.
- The dependency skill does not assume universal highest-version selection or equate download with execution; both suspected simplifications were refuted by the live text.
- The native-defect skill explicitly limits arithmetic models to model confirmation and requires the actual product path for product confirmation. Synthetic demonstrations are not silently promoted to deployed exploitation.
- Missing platform coverage and generated manifest files were assigned to the integration owner, not treated as review findings. Their subsequent completion, and changes to cloud/pipeline skills, were reported by the maintainer; those additional files were not independently reviewed here.
- No live targets, model endpoints, package registries, radio devices, EDR systems, gadget chains or exploit payloads were exercised. No current external product/version claims were verified or relied upon.
- Full pinned-upstream validation, stored manifest comparison, upstream fidelity of every adaptation, and byte verification of every copied resource were not independently executed. Existing unit tests mock the pinned source inventory; their green result is not evidence for the actual upstream Git revision.
- The worktree was under active integration. SHA-256 identities above bind conclusions to the files actually reviewed; subsequent author fixes require rerunning the reproducer and relevant tests. The Git base does not by itself identify uncommitted collection bytes.
- Only `reviews/independent-review.md` was written in the repository by this reviewer. No skills, tooling, manifests, coverage files, commits or tags were changed. No CRONOS tool was invoked.

## IR-01 closure — 2026-11-01

**CLOSED — independently verified for the demonstrated defect.** Reran `python3 -B -m unittest -v test_collection` from `red-team`: all 18 tests passed in 0.346 seconds (exit 0). Inspected both added identity tests: each invokes the live `validate()` function and a subprocess running a temporary copy of the current `catalog.py` with the current `validate_collection.py`. Duplicate names are rejected in both orders by both readers; the quoted scalar is accepted and catalogued as `rt-example` without quote characters. The catalogue now imports the shared `skill_name` reader; its source enforces one name key, including quoted key spellings. Quoted-key variants were source-inspected, not separately exercised in this closure. The original finding and pre-fix evidence above are preserved; this closure supersedes its open status. Full real upstream validation (79 sources / 79 adaptations / 28 copies / 107 total) was reported by the integration owner and was not rerun here. No broader audit or tooling changes were performed.
