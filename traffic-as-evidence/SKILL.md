---
name: traffic-as-evidence
description: Read network traffic as evidence to be interpreted under two hard limits — you usually cannot see the payload (encryption) and rare is usually benign (base rates) — never as a verdict on its own; beaconing, JA3/JA4 fingerprints, timing, volume, and destination reputation are weak signals whose meaning lives in baseline and context. Use whenever a network observation is being read for intent: "this host is beaconing", "periodic connection to an unknown IP", "is this C2", "the JA3 matches a malware family", "DNS looks like exfiltration", "unusual outbound traffic", "the firewall/IDS flagged this flow", "TLS to a suspicious domain". Sibling of dual-use-behavior-adjudication (the same flow is telemetry or C2 by context) and threat-attribution-restraint (a fingerprint match is contact, not identity); it interprets metadata honestly. It does not decrypt traffic or write the IDS signature, and never reads "periodic and encrypted" as "malicious" without a baseline.
---

# Traffic as Evidence

A packet capture does not contain a verdict. It contains flows — source, destination,
timing, size, and, if you are lucky and it is not encrypted, some bytes — and the
meaning of a flow lives in the baseline it deviates from and the neighborhood it sits
in, never in the flow alone. Two facts make network interpretation harder than it
looks, and both are routinely ignored: **most traffic worth investigating is
encrypted** (you are inferring from metadata, not reading content), and **most rare
patterns are benign** (novelty is not malice; the base rate of "weird but fine" dwarfs
the base rate of "weird and hostile").

Two symmetric errors:

- **False MALICE.** Every periodic outbound connection gets called C2. But a telemetry
  agent, a software update check, a certificate revocation poll, and a chat client's
  keepalive all beacon — regular, encrypted, to a CDN you do not recognize. Flagging
  the shape ("periodic + encrypted + unknown destination") without a baseline is how a
  SOC drowns itself in its own update traffic.
- **Over-reading metadata as if it were payload.** A JA3 fingerprint, a packet-size
  pattern, an SNI — these are suggestive, low-resolution, and often forgeable. Treating
  "JA3 matches family X" as "this is malware X" reads a hash of a handshake as though it
  were the decrypted conversation.

Composes with the library:

- **dual-use-behavior-adjudication** — the same flow is a backup job or exfiltration by context; this is that adjudication applied to the wire
- **threat-attribution-restraint** — a JA3/JA4 or infrastructure match is contact between datasets, not identity of hands, and is cheaply spoofed
- **honest-degradation** — encrypted payload is a stated blind spot; inference from metadata is a WARN-grade claim, not a PASS
- **forensic-logging-design** — you can only baseline what you actually record; a claim about traffic is bounded by the visibility of the feed

---

## Step 0 — State what you can and cannot observe (Firstness, honestly)

Before interpreting, write the resolution of your evidence. This is the step most
analysts skip, and it caps every claim downstream:

- **Encrypted flow** — you see endpoints, timing, volume, SNI/certificate, and a
  handshake fingerprint. You do **not** see content. Every conclusion is an inference
  from the envelope; mark it as such.
- **Cleartext flow** — you see payload, but confirm it is not itself attacker-shaped to
  mislead the analyst reading it.
- **Sampled / aggregated** (NetFlow, sampled taps) — you see that a conversation
  happened and how much, not what. Do not narrate content you never captured.

"Encrypted to an unknown host" is a description, not a finding. Write the description
first so you do not smuggle a decrypted story into an envelope you never opened.

---

## Step 1 — Baseline before you call anything anomalous (Secondness)

A flow is anomalous only against a norm for *this* host, *this* service, *this* time.
Establish it or mark it assumed:

- **Does this host normally talk to this destination?** A build server pulling from a
  package CDN every ten minutes is its job; a finance workstation doing the same is a
  sentence worth finishing.
- **Is this beaconing interval / jitter / volume normal for this host's software?**
  Legitimate agents beacon with metronome regularity; so does commodity C2. The
  interval alone does not separate them — the *identity of the endpoint and whether it
  is expected* does.
- **No baseline = a cap, not a verdict.** If you cannot say what normal is for this
  host, you cannot certify the flow malicious or benign; you can only escalate to
  enrich, and you say so.

---

## Step 2 — Read the neighborhood and sequence, not the single flow

One connection is rarely adjudicable; the pattern around it is. A beacon that is
preceded by a phishing-document open and followed by a burst of internal SMB
connections sits in a neighborhood with no benign author. The same beacon alone, to a
CDN, with no predecessor and no successor, has a benign author and you should say so.

- **Corroboration counts independent signals**, not restatements of one flow. The same
  connection appearing in the firewall log and the proxy log is one signal. A proxy
  flow plus a matching process-network event on the endpoint is two.
- **Volume and direction** — small regular out / large irregular in is a control
  channel; large sustained out to one destination is possible exfil. But a nightly
  large outbound is also a backup. The shape narrows the hypothesis; it does not close
  it.

---

## Step 3 — Grade the signal under base rate and forgeability

For each artifact you are tempted to convict on, ask both questions:

- **Base rate** — how many benign hosts also show this? A JA3 shared by every app built
  on the same TLS library is high-base-rate and near-worthless for identification. A
  destination on a public CDN is shared by thousands of benign apps.
- **Forgeability** — how cheaply can it be changed? JA3/JA4 fingerprints are a function
  of the client's TLS stack and are deliberately mutable; domain reputation is gamed
  daily with fresh domains and hijacked-but-clean CDNs. A "match" to a known-bad
  fingerprint is a lead to pull, not a conviction to enter.

A signal that is high-base-rate and cheaply forged (a common JA3 to a CDN) is not weak
evidence — it is essentially none, and aggregating several such signals into a
"picture" builds a conviction out of noise.

---

## Step 4 — Grade the verdict, and let ABSTAIN stand

- **Benign** — expected endpoint, matches baseline, benign author for the sequence; close
  it with the reason.
- **Suspicious** — deviates from baseline, no benign author yet, but signals are
  forgeable / high-base-rate and payload is dark; enrich, do not escalate as malice.
- **Malicious** — a sequence with no benign author, corroborated across independent
  feeds, ideally with at least one signal that is not trivially forgeable.
- **ABSTAIN** — payload encrypted, metadata ambiguous, no baseline. "Cannot adjudicate
  from the wire alone; needs endpoint/host context" is a real finding and names the
  next collection step, rather than convicting an update check.

---

## The one-line test

If your verdict on a flow would be identical with the payload encrypted or in the
clear, you convicted the envelope — the timing, the fingerprint, the reputation — and
those are the signals an adversary shapes most cheaply. Anchor the verdict to baseline,
sequence, and independent corroboration, or abstain and say the payload is dark.
