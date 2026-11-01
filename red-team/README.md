# Red Team Assessment Skills

**Language:** English · [Español](README.es.md)

Security work can jump from an alert or suspicious code path straight to a verdict. This collection helps an agent establish what happened, test competing explanations and leave a reproducible record before recommending a change.

It combines domain-specific security workflows with the engineering methods in the parent `SKILLS` collection. Use it for authorized repository reviews, synthetic fixtures and controlled lab work. Each workflow identifies evidence that would support or refute its hypothesis and distinguishes an untested path from a result.

**Inventory:** 79 rewritten domain skills from Claude-Red, plus 28 unchanged snapshots of local methodology skills. The parent collection contains 92 skills; this subcollection contains 107.

**Start here:** [Choose a skill set](#choose-a-skill-set) · [Assessment method](METHODOLOGY.md) · [All 79 source mappings](COVERAGE.md) · [Validation record](VALIDATION.md)

## Choose a skill set

Run one catalog command from the parent `SKILLS` directory. It emits skill names, paths and hashes without descending into nested directories:

```bash
python3 -B red-team/catalog.py general
python3 -B red-team/catalog.py red-team
```

Give the agent paths from one result and ask it to load skills exclusively from that set. The catalog defines selection; the folder does not change an agent's automatic discovery settings. For general work, use only the parent collection and exclude `red-team/` and its descendants. For a red-team session, use only the red-team catalog output.

Suggested instruction: “Use only the skill paths returned by the red-team catalog. Read relevant SKILL.md files and METHODOLOGY.md before acting. Do not load skills from the parent collection.”

For general work: "Use only immediate-child SKILL.md files in SKILLS. Exclude red-team and all its descendants."

## What is in the collection

The 79 domain assessments cover application and API security, authentication, cloud and CI/CD identity, supply chain, containers and Kubernetes, cryptography, fuzzing and binary analysis, wireless and embedded systems, mobile, OSINT, social engineering, Active Directory, endpoint visibility and post-exploitation evidence. See [COVERAGE.md](COVERAGE.md) for each source, destination, retained mechanism and adaptation rationale.

The 28 copied local skills supply shared practices for authorization, hypotheses, evidence, reporting and detection. The six domain skills that existed before the full expansion keep their names; other adaptations use the `rt-` prefix. Select only the workflows relevant to the current question.

## How to use a workflow

Start with [METHODOLOGY.md](METHODOLOGY.md), then read the selected skill. It describes the domain mechanism, baseline and competing explanation, a bounded experiment, controls, evidence to preserve and result interpretation. Embedded acceptance cases specify decisions for given evidence; they do not claim that target tests were run. Check tool availability and version-specific behavior in the actual environment.

The existing methodology copies govern hypothesis testing, evidence, authorization mapping, reporting and detection. Choose a domain workflow when concrete protocol or platform experiments are needed; use pipeline-trust and oracle-driven-fuzzing for their underlying reasoning, rather than running duplicate campaigns.

References to other skills in copied text are preserved verbatim. Resolve them within this catalog. If absent, treat optional composition as unavailable; if a required procedure cannot be performed using the available instructions, report that limitation instead of loading outside the selected collection. These are independent selection boundaries, not an OS sandbox.

## Provenance and verification

Copies are snapshots, not symlinks. SOURCES.json records source revision and per-file hashes. Update copies deliberately from the parent, preserving resources and reviewing diffs; never synchronize automatically over local changes. Adaptations evolve separately from upstream. Read PROVENANCE.md for selection rationale and limitations.

From this directory, run:

```bash
python3 -B -m unittest -v test_collection.py
python3 -B validate_collection.py --upstream /path/to/Claude-Red
```

Validation checks coverage, copied bytes, identities and local links. ADAPTATIONS.json
records hashes of the upstream and adapted files. The validator's `--manifest`
option emits the current manifest for review; it does not overwrite it. Compare
that output with the stored manifest after changes. Behavioral acceptance cases
are specifications; their presence does not mean a live target was tested.
