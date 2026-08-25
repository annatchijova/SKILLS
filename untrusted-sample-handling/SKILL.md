---
name: untrusted-sample-handling
description: Examine a hostile artifact as what it is — a live adversary you invited onto your desk — with two invariants: never let it execute where it can reach anything real, and never confuse what it CAN do (capability) with what it DID or was aimed at (intent). Use whenever a suspicious binary, script, document, archive, APK, container image, or captured payload is in hand and someone wants to know what it is: "analyze this malware", "is this file malicious", "what does this sample do", "detonate this", "extract IOCs", "reverse this dropper", "is this ransomware". Trigger also on "run it in a sandbox", "the sandbox showed nothing", "what does it target", or a phishing attachment handed over for analysis. Sibling of reverse-engineering (the mechanics of understanding code) and honest-degradation (a partial unpack is a WARN, not a verdict); feeds threat-attribution-restraint (shared code is a lead, never an actor). It does not write detection rules (detection-engineering) and never turns a decryption routine into "ransomware that targets hospitals".
---

# Untrusted Sample Handling

A malware sample is not a file to be understood; it is a live adversary you have
agreed to bring into contact with your systems. Every handling decision is a security
decision, and two cardinal errors account for most of the damage analysts do to
themselves and to the truth:

- **Executing it where it can reach something real** — a host with credentials, a
  mounted share, real network egress, a corporate identity. Detonation is not
  observation; it is *running the attacker's code with your privileges*. A "quick look"
  on your workstation is how the analysis becomes the second incident.
- **Confusing capability with intent** — writing "ransomware that targets hospitals"
  from the presence of an AES routine and a hardcoded string. What a sample *can* do is
  read off its imports and strings and is nearly always broad; what it *was aimed at*
  lives in its config, its target list, its C2, and its trigger conditions, and is a
  separate, evidentiary claim.

The through-line with the rest of the library: **capability is not intent, absence in
a sandbox is not benignity, and shared code is not a shared author.** Each is a place
where a hostile artifact is designed to mislead exactly the analyst who relaxes.

Composes with the library:

- **reverse-engineering** — the mechanics of static/dynamic understanding; this skill governs doing it *safely* and reporting it *honestly*
- **honest-degradation** — packing, encryption, anti-analysis → partial understanding is a WARN that names what it could not reach, never a confident full verdict
- **finding-custody / tamper-evident-audit-chain** — hash the sample first, record provenance, never alter the original; extracted IOCs carry their chain
- **threat-attribution-restraint** — code reuse, a shared packer, a reused C2 are leads; they do not name an actor
- **dual-use-behavior-adjudication** — a sample using legitimate tools (LOLBins) is judged on context, not on the tool
- **detection-engineering** — IOCs and behaviors feed rule-writing there; extraction is not detection

---

## Step 0 — Isolation invariant, decided before you touch it

State the containment *before* the first double-click, not after. The invariant: the
sample must never, at any stage, hold a privilege or reach a resource whose abuse you
are not prepared to treat as compromised.

- **No detonation on a host with anything real** — no domain-joined machine, no saved
  credentials, no mounted shares, no VPN, no production network. A disposable,
  snapshotted VM with controlled (recorded, filtered, or faked) network, treated as
  burned after use.
- **Assume the sample knows it is caged.** Modern samples fingerprint sandboxes (VM
  artifacts, low uptime, no user activity, known analysis tooling) and behave benignly
  to fool you. **Absence of malicious behavior in the sandbox is not evidence of
  benignity** — it is, at best, evidence you could not provoke it here. This is the
  single most misread result in the discipline; treat "sandbox showed nothing" as
  WARN/inconclusive, never PASS.
- **Static-first.** Everything reachable without running it — hash, type, strings,
  imports, entropy, embedded resources, certificates, macro/script source — comes
  first and carries no execution risk. Detonate only to *confirm* a hypothesis static
  analysis raised, never to form the first one.

---

## Step 1 — Custody before curiosity

The moment the sample exists in your hands, before analysis:

- **Hash it (SHA-256) and record provenance** — where it came from, when, how, who
  handed it over. This is the anchor everything else references.
- **Never modify the original.** Work on copies; the pristine sample is evidence
  (`finding-custody`). Renaming, unpacking in place, or letting a tool "clean" it
  destroys the artifact you may need to prove something about later.
- **Label live vs inert from the start.** The live sample (for analysis) and any
  defanged/disarmed copy (for sharing, screenshots, tickets) are different objects and
  must never be confused — a "sample" pasted into a chat that is actually live is how
  the artifact escapes containment through the report.

---

## Step 2 — Build the capability inventory (static), kept separate from intent

From static analysis, produce an inventory of what the sample is *equipped* to do —
and label it explicitly as capability, so no reader mistakes it for behavior:

- Imports/syscalls (crypto, network, process injection, file enumeration,
  persistence APIs), strings, embedded config, packing/obfuscation (high entropy →
  packed → your static view is partial, a WARN), signing status, compiler/toolchain.

Capability is broad by construction and therefore weak evidence of purpose on its own.
"Has an AES routine" is consistent with ransomware, with a secure updater, and with a
config decryptor. Do not let the scariest capability write the verdict. Keep this
column strictly apart from Step 3.

---

## Step 3 — Intent requires the config, the target, the trigger — or you abstain

Intent is not inferred from capability; it is read from the choices the author encoded:

- **Target selection** — a hardcoded victim list, a domain/geo/language check, an
  environment guard ("only run if domain == X"). This is where "aimed at" actually
  lives.
- **C2 and tasking** — the real command set, the exfil destination, the operator
  interface. A network capability is not exfiltration until you can show where it sends
  and what.
- **Trigger conditions** — time bombs, kill switches, sandbox checks, activation logic.

If the sample is packed/encrypted/anti-analysis and you cannot reach the config, then
you cannot state intent — and the honest output is a **scoped, degraded** finding:
"capability inventory X; intent not established; blocked by packing/anti-analysis;
would require Y to reach." That is a stronger deliverable than a confident story
extrapolated from an import table. `ABSTAIN` on intent is a valid, defensible verdict.

---

## Step 4 — Grade the IOCs; do not ship noise as intelligence

Extracted indicators are not equal, and a list padded with library artifacts poisons
everyone downstream who blocks on them:

- **Rank by specificity** — a hardcoded C2 domain/IP or a unique cryptographic key
  (high) vs a common Windows API string, a standard library path, or a public-CA
  certificate (noise). Ask the base-rate question: *how many benign programs also
  contain this?* (The link to `dual-use-behavior-adjudication` and to detection
  false-positive budgets.)
- **Flag sandbox-only artifacts** — a domain the sample only contacts because it
  detected the sandbox is an anti-analysis tell, not an IOC to block.
- **Defang before sharing** — `hxxp`, `[.]`, neutered paths — so the intelligence does
  not itself become a delivery mechanism when pasted into a browser or clicked in a
  ticket.
- **Carry provenance** — each IOC references the sample hash and how it was extracted,
  so a consumer can judge and re-derive it (`claim-provenance-discipline`).

---

## Step 5 — Report with the plane of certainty marked

The write-up separates, visibly, what was observed from what was inferred, and marks
where analysis was blocked:

- **Observed** (static facts, sandbox behavior *with the caveat that the sandbox may
  have been evaded*) vs **inferred** (purpose, targeting, attribution).
- **Coverage honesty** — "unpacked layer 1 of 3; layers 2–3 not reached" is stated, not
  smoothed over. A partial analysis presented as complete is the reverse of the
  overclaim in attribution and just as damaging.
- **No actor names from code overlap** — hand shared code, packers, or reused
  infrastructure to `threat-attribution-restraint`; they are clustering leads, not an
  author.
- **Capability and intent stay in separate sections** — so a reader can never quote the
  capability inventory as if it were established intent.

---

## The one-line test

If your verdict required running the sample and you cannot prove the cage held *and*
that the sample did not simply choose to behave for you, you have a hypothesis, not a
verdict — and possibly a second incident. And if you wrote what it "targets" without
pointing at its config, its list, or its C2, you reported the capability and called it
intent.
