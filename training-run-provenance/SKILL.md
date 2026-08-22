---
name: training-run-provenance
description: Get determinism in machine learning where it is actually achievable — the artifact, not the process — by pinning data version, materialized split, code, resolved config, environment and hardware into a sealed manifest, naming the irreducibly nondeterministic parts instead of pretending they are absent, and labeling the reproducibility claim at the level the evidence supports. Use whenever a model is trained, compared, registered, or deployed, whenever two runs disagree, and whenever a result has to be defended later. Trigger on "set the seed", "reproducible training", "why do I get different results", "torch.deterministic", "which model is in production", "model registry", "MLflow/W&B", "we can't reproduce the paper", "retrain", "the metric moved but the code didn't", or a model artifact whose training run cannot be identified. Extends deterministic-core into ML, where floats are the model and bitwise determinism ends at the frozen artifact — after which the decision built on top must be exact again.
---

# Training Run Provenance

`deterministic-core` says: no floats in the decision path. In machine learning
the floats *are* the model, so the rule cannot be applied by banning them. It
is applied by putting the boundary in the right place:

```
training run          →   frozen artifact   →   inference   →   decision
nondeterministic          hashed, immutable     deterministic     exact
provenance-sealed         the seam              given the same    integers/decimals,
                                                artifact + input  sealed, auditable
```

Everything left of the seam is a process you can *describe* but not always
repeat. Everything right of it must be as exact as any other consequential
output path in this library. Most ML systems blur the seam — a model reference
that means "whatever is at `latest`", a threshold that drifts, a score compared
against a number produced by a different data version — and then the whole
pipeline inherits the nondeterminism of the least disciplined stage.

The second thing this skill exists to correct:

> **A seed is not reproducibility.** It makes one program repeat on one machine
> with one library stack. It says nothing about whether the *result* holds, and
> a single-seed number is not a measurement — it is one sample from a
> distribution nobody characterized.

Composes with the library:

- **deterministic-core** — everything to the right of the seam
- **tamper-evident-audit-chain** — the run ledger and the model registry
- **data-leakage-hunting** — the split must be a stored artifact, which is one
  of the fields pinned here
- **model-evaluation-discipline** — variance across seeds is part of the result
- **decision-record-discipline** — why this architecture, what would reopen it
- **honest-degradation** — an unreproducible run is reported as such, never
  rounded up to "reproducible"

---

## Part 1 — The manifest: what a run has to pin

A run that cannot be described cannot be compared, and comparison is the entire
business. Capture these at launch, automatically — a manifest written by hand
after the fact is a memory, not a record.

| Field | Pin | The failure it prevents |
|---|---|---|
| **Data** | content hash of the dataset version, not a path | comparing two models trained on silently different data |
| **Split** | materialized ids/indices + their hash | a library upgrade changing what "seed 42" partitions |
| **Code** | commit SHA **plus dirty-tree state** | "it was this commit" when three files were uncommitted |
| **Config** | the fully *resolved* hyperparameters | the CLI you typed is not the config that ran, after defaults and overrides |
| **Seeds** | every one: language, numeric library, framework, dataloader workers, augmentation | partial seeding, which looks deterministic until it isn't |
| **Environment** | framework, CUDA/cuDNN, driver, OS — and the accelerator model | a result that only exists on that GPU generation |
| **Outputs** | weights hash, metrics, and the metrics' interval | a number with no artifact attached |

Two fields people skip and should not: **dirty-tree state** (the most common
cause of an unreproducible run is uncommitted code) and **hardware**, because
a result that depends on the accelerator model is a real finding and you want
to know it now rather than at the next migration.

Then: **embed the manifest hash inside the artifact**. The question "which run
produced the model that made this decision?" must be answerable from the model
file alone, months later, with the experiment tracker offline.

## Part 2 — Name the nondeterminism you cannot remove

Pretending a training run is deterministic is worse than admitting it is not,
because it converts an expected variance into a phantom bug that someone will
spend a week chasing. The irreducible sources:

- **Float addition is not associative**, and parallel reductions sum in
  whatever order the scheduler produced. Two mathematically identical runs
  diverge in the last bits, and the divergence compounds across steps.
- **Algorithm autotuning** picks kernels by measured speed, so the selection
  depends on machine load.
- **Nondeterministic kernels** (scatter-add, some pooling and interpolation
  backward passes) have no deterministic implementation on some backends.
- **Dataloader worker interleaving** changes batch composition.
- **Distributed reduction order** varies with topology and timing.
- **Library and driver upgrades** change numerics with no API change.

What to do, in order:

1. Turn on the framework's deterministic mode and the fixed-algorithm flags
   where they exist. Measure the throughput cost — it is often 10–30% and it is
   frequently worth paying for anything you will need to defend.
2. Seed every source, including the dataloader workers and augmentation.
3. Where an op has no deterministic implementation, **write it down in the
   manifest** rather than silently accepting it.
4. For anything that must be bitwise reproducible, pin the container image by
   digest and record the accelerator model, then verify by rerunning and
   comparing hashes — a claim of bitwise determinism that was never re-run is
   an assumption.

## Part 3 — Label the claim at the rung the evidence supports

The epistemic ladder of `red-team-auditing`, transplanted. Never let a run
float without a level.

| Level | Claim | What earns it |
|---|---|---|
| **REPRODUCED-BITWISE** | rerunning yields the identical artifact | rerun on the pinned stack, weight hashes match |
| **REPRODUCED-STATISTICALLY** | rerunning yields a metric inside the stated interval | N reruns with different seeds, spread reported |
| **RERUN-ONCE** | one rerun landed close | a single repeat, no interval |
| **UNREPRODUCED** | the run exists and is fully described | the manifest alone — the honest default |

`UNREPRODUCED` with a complete manifest is a perfectly respectable state and
describes most training runs ever performed. What is not respectable is calling
it reproducible because a seed was set.

The practical consequence for comparisons: **two runs that differ by less than
the seed-to-seed spread are the same run.** Before any "A beats B", you need
B's variance. Three seeds is the usual minimum, and reporting the spread costs
nothing but two more runs.

## Part 4 — The registry is an append-only ledger

Models are evidence. Treat the registry the way `tamper-evident-audit-chain`
treats any record that might be challenged:

- **Append-only.** New version, never overwrite. A mutable `latest` tag means
  the model that produced last Tuesday's decision may no longer exist.
- **Immutable references everywhere.** Serving config points at a version and a
  hash, never at a moving tag.
- **Each entry seals the previous.** Then "which models were deployed between
  these dates, and in what order" is answerable and verifiable.
- **Keep the failed and abandoned runs.** They are the variance data, and they
  are the record of what was already tried — deleting them makes the next
  person repeat the experiment.
- **Log the inference-time inputs to a decision, not just its output**
  (`forensic-logging-design`), including the model version. Otherwise a
  disputed decision cannot be reconstructed even with a perfect registry.

And to the right of the seam, `deterministic-core` applies unmodified: the
threshold that converts a score into an action is exact, versioned and sealed;
it is not a float that someone tuned in a notebook and typed into a config.

---

## Deliverable

```
## Run <id> — <purpose>
Data <hash> | Split <hash> | Code <sha, clean|dirty> | Config <hash>
Env: <framework/CUDA/driver/OS> | Accelerator: <model, count>
Seeds: <all of them>
Nondeterminism accepted: <ops/flags that could not be pinned>

Result: <metric> [<interval>] over <n> seeds
Reproducibility: <REPRODUCED-BITWISE | -STATISTICALLY | RERUN-ONCE | UNREPRODUCED>
Artifact: <weights hash>   Manifest hash embedded in artifact: yes/no
Compared against: <run id> — same data version? same split? Δ vs seed spread
```

## Anti-patterns

- "We set seed = 42" offered as a reproducibility claim.
- Storing the split seed instead of the materialized split.
- Reporting a single-seed metric as the result, then comparing it to another
  single-seed metric and declaring a winner inside the noise.
- Training from a dirty working tree and recording only the commit.
- Pinning Python packages while leaving CUDA, the driver, and the accelerator
  model unrecorded.
- A deployed model whose training run cannot be identified from the artifact.
- A mutable `latest` tag in the serving path.
- Deleting failed runs, discarding both the variance data and the record of
  what was already tried.
- Comparing against a baseline trained on a different data version.
- Letting the nondeterminism of the training run leak past the frozen artifact
  into the decision, where exactness is still required and still achievable.
