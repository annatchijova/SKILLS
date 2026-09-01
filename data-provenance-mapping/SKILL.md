---
name: data-provenance-mapping
description: You cannot protect, delete, or report on data whose flow you have not mapped — a "delete my data" request, a breach-scope estimate, or a "we don't store PII" claim is only as true as your knowledge of where the data actually went, and it always went further than the schema says: into backups, logs, caches, analytics, data warehouses, search indexes, third-party processors, exports, and derived features. Use whenever the question is where sensitive data lives or goes: "handle this DSAR / right-to-be-forgotten", "did we delete all their data", "what's the blast radius of this breach", "do we store PII", "is this anonymized", "map our data flows", "privacy impact assessment", "we log the request body", "we sent it to this vendor", "GDPR/CCPA data mapping". Sibling of claim-provenance-discipline (a data-handling claim must carry where the data actually is) and credential-material-triage (the "where does it still persist after you rotated it" move, applied to PII); it maps the real flow, not the intended one. It does not write the privacy policy or the deletion job, and never accepts the architecture diagram as evidence of where the data actually went.
---

# Data-Provenance Mapping

Every strong statement about sensitive data — "we deleted it," "we don't retain that,"
"the breach was limited to these records," "it's anonymized" — is a claim about *where
the data is*, and it is true only to the depth of your map. The recurring, expensive
error is that data always travels further than the schema admits. The row you deleted
was copied into last night's backup, logged in full by a debug statement, cached at the
edge, shipped to an analytics vendor, indexed for search, and distilled into a model's
training set. **The PII you forgot is the breach; the copy you did not delete is the
failed DSAR.**

Two failure modes, both from mapping intent instead of reality:

- **Mapping the intended flow.** The architecture diagram shows the data going where you
  designed it to go. The actual flow includes the debug log that captured the whole
  request body, the one-off CSV a analyst exported to their laptop, the queue that
  retains messages for seven days, and the processor you integrated in 2021 and forgot.
  The diagram is a hypothesis; the flow is discovered.
- **Treating a delete as an erasure.** "We deleted the row" reads as "the data is gone"
  while the same data persists in six derived and backup locations, each of which
  independently answers "yes, we have it" to the next subpoena or attacker.

Composes with the library:

- **claim-provenance-discipline** — "we don't store that" / "it's deleted" is a claim that must carry the actual list of stores it was checked against
- **credential-material-triage** — the same "the string outlives the rotation" reasoning: a secret rotated still lives in git history and logs; PII deleted still lives in backups and exports
- **dependency-provenance** — a third-party processor is supply chain for your data; its retention is your exposure
- **honest-degradation** — "we cannot currently enumerate everywhere this went" is the real status of most systems and is a finding, not a failure to hide
- **assume-breach-modeling** — the breach blast radius is the full set of stores, including the ones off your primary systems

---

## Step 0 — Separate the intended flow from the actual flow

State the design flow (the diagram) explicitly, then treat it as a *starting
hypothesis* to be refuted by discovery, not as the answer. Firstness here is "where does
this data physically exist right now," not "where did we mean for it to go." The gap
between the two is exactly where forgotten copies live, and closing your investigation
at the diagram is how a debug log full of PII survives every deletion.

---

## Step 1 — Enumerate the shadow stores where data silently lands

For each category of sensitive data, walk the places it accumulates outside the primary
table, because these are what deletion and breach-scope routinely miss:

- **Logs** — request/response bodies, error traces, access logs (the debug line that
  logged the full payload is the classic PII leak)
- **Backups and snapshots** — DB backups, volume snapshots, disaster-recovery copies
- **Caches and CDNs** — edge caches, in-memory stores, materialized views
- **Analytics and telemetry** — product analytics, session replay, tracking pixels
- **Warehouses and lakes** — the ETL that copied prod into the analytics warehouse
- **Search indexes and queues** — Elasticsearch, Kafka retention, message brokers
- **Third-party processors** — every vendor you send data to (Step 4)
- **Exports and human copies** — CSVs, reports, screenshots, support tickets, that
  spreadsheet on someone's laptop
- **Derived data** — ML training sets, features, embeddings, aggregates (Step 2)

The output is a list of stores, each of which will independently answer "do you have
this person's data?"

---

## Step 2 — Follow the data into its derivatives; "anonymized" is a claim to test

Derived data inherits the original's sensitivity until proven otherwise. A hash of an
email is still a stable identifier that links records; an embedding can often be
inverted or matched; an aggregate re-identifies at low counts; a "pseudonymized" dataset
re-links the moment its key table leaks. "Anonymized" is not a status you assign — it is
a property you test against a re-identification attempt (the same base-rate and
adversary discipline as data leakage). Until tested, a derivative is another store on
your Step 1 list, not an exemption from it.

---

## Step 3 — For deletion and DSAR, completeness is the entire task

A deletion or subject-access request is only as good as its coverage. A delete that
clears the primary row but misses the backups, the logs, the warehouse, and the
processors is a false "done" that the next audit or breach exposes. Walk every store
from Step 1 and account for each explicitly: **deleted**, **retained with a stated
lawful reason** (e.g. a backup on a fixed rotation, documented), or **unreachable /
unknown**. This is the same move as tracking where a rotated secret still lives — the
fix is not done until every persistence site is accounted for, not just the obvious one.

---

## Step 4 — Third parties extend your map into systems you do not control

Any processor you send sensitive data to is part of your data's blast radius, and their
retention, sub-processors, and breaches are your exposure. The map does not stop at your
network boundary; it extends to every vendor edge, and each is a store you must be able
to name, bound, and (for a DSAR) propagate the request to. A data flow that goes dark at
"…and then we send it to the vendor" is unmapped, not finished (`dependency-provenance`).

---

## Step 5 — Degrade honestly: name the unmapped stores

Most real systems cannot currently enumerate everywhere a given datum went, and the
honest status is to say so: "mapped to these N stores; logs older than 30 days and two
legacy exports not yet accounted for." A bounded, partial map with its unknowns named is
worth far more than a confident "we don't have that data" that a single debug log
refutes under oath. An unmapped store is not an empty store — do not resolve the unknown
to zero.

---

## The one-line test

If you cannot list every place a piece of sensitive data physically lives — including
the copies you never intended to make — you cannot honestly claim to have deleted it,
protected it, or scoped its breach. Map the actual flow, or state which stores remain
unmapped and stop treating the diagram as the territory.
