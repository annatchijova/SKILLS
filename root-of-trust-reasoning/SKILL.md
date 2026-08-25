---
name: root-of-trust-reasoning
description: Reason about integrity you cannot verify from inside the thing you are verifying — a compromise below your vantage point is invisible because it controls what you see, so a bootkit that owns UEFI or SPI flash shows a spotless OS to every OS-level scanner, and trust must be anchored to a root below the layer that could lie. Use whenever integrity, boot, or attestation is the question: "is this machine clean", "detect a bootkit / rootkit / UEFI implant", "Secure Boot", "measured boot", "TPM attestation / PCRs", "remote attestation", "can we trust this device's health check", "firmware integrity", "our EDR says it's clean", "supply-chain implant below the OS". Sibling of tamper-evident-audit-chain (measured boot is a hash chain of the boot sequence, in silicon) and honest-degradation (an unmeasurable layer is a WARN, not a PASS); it reasons about where trust can be anchored. It does not flash firmware or configure the TPM, and never accepts a system's report about its own integrity from a layer that a compromise could control.
---

# Root-of-Trust Reasoning

You cannot verify the integrity of a system from inside it. A compromise that sits
*below* your vantage point controls everything you are able to observe, so it can show
you exactly the clean system you are looking for. A UEFI bootkit that owns the SPI
flash loads before the OS, before the kernel, before your endpoint agent — and every
one of those later components asks the machine questions the bootkit gets to answer. The
scanner is standing on a floor the malware installed. **A system asked to report its own
integrity reports whatever its compromiser permits.**

This is not a scanning-coverage problem to be solved with a better signature; it is an
epistemic one. The two failure modes are both forms of trusting a witness the adversary
owns:

- **Verifying from within the compromised layer.** Asking the OS whether the OS is
  clean; running AV to detect a bootkit that loaded first; trusting a health attestation
  computed by software the implant can patch. The poisoned witness testifies to its own
  innocence.
- **Trusting an attestation without checking its root.** Accepting a TPM quote without
  verifying it is signed by a key you actually anchored to a trusted manufacturer;
  replaying no event log against the PCRs; ignoring revocation currency (`dbx`) so a
  known, revoked bootkit still satisfies Secure Boot. An attestation whose root you did
  not establish is theater with cryptography on it.

Composes with the library:

- **tamper-evident-audit-chain** — measured boot is exactly a hash chain: each stage measures the next into the TPM before executing it, so a later stage cannot rewrite an earlier measurement
- **honest-degradation** — a layer you cannot measure (no TPM, closed firmware, no attestation) is unverified, a WARN; never infer clean from silence
- **assume-breach-modeling** — reason as though the layer below you is already hostile, and ask what that buys the attacker
- **deterministic-core** — a measurement is only comparable if it is canonical and reproducible; a "known-good" PCR set must be computed the same way every time
- **claim-provenance-discipline** — "the device is healthy" is a claim that must carry which root vouched for it and what it actually measured

---

## Step 0 — Locate your vantage point and name everything below it

Place your verification tool in the stack, and list every layer that loads *before* it:
hardware/CPU microcode, SPI flash / BIOS, UEFI firmware, SMM, bootloader, hypervisor,
kernel, then your agent. Your tool's authority ends at the layer that loaded it;
everything beneath is something it can only observe *through*, and therefore something a
compromise there can hide. Write this list first — it is the map of what your evidence
structurally cannot see.

---

## Step 1 — Name the poisoned-witness problem for this specific check

For the integrity question in front of you, state who is answering it and what they had
to be trusted to be for the answer to mean anything. "The EDR reports no rootkit" — the
EDR runs in an OS whose boot it did not verify; it can detect peers and lower-skill
threats, not something beneath its own load point. Making this explicit converts a false
"clean" into an honest "clean *as seen from ring 0*, which a ring -2 implant would not
disturb."

---

## Step 2 — Anchor to a root below the threat

Integrity has to be rooted in something the threat could not have altered after the
fact. Measured boot is the canonical shape: starting from an immutable hardware root of
trust, **each stage measures (hashes) the next component into a TPM PCR before handing
control to it.** Because a PCR can only be extended, not overwritten, a component that
gets compromised later cannot rewrite the measurement that was taken before it ran. The
chain is trustworthy up to the first link you cannot anchor — the immutable boot ROM /
hardware root. Trust flows *up* from there, never down from the OS.

---

## Step 3 — Treat attestation as a claim to validate, not a green light

A TPM quote or a remote attestation is evidence only if you check its root and its
content:

- **Root of the signature** — is the quote signed by an attestation key that chains to a
  manufacturer/endorsement key you actually pinned? An unrooted signature proves
  nothing.
- **What it measured** — replay the boot event log and confirm it reproduces the PCR
  values; a PCR set with no log to explain it is an opaque number.
- **Against a known-good, computed canonically** — compare to an expected measurement
  derived the same way every time (`deterministic-core`), not to "looks plausible."
- **Revocation currency** — is `dbx` up to date, so revoked/known-bad bootloaders
  (BlackLotus-class) are actually rejected rather than validly signed? Secure Boot with
  a stale revocation list validates the very thing it should refuse.

---

## Step 4 — Degrade honestly where you cannot measure

Most environments have layers you cannot anchor: no TPM, a closed/opaque firmware blob,
a device that offers no attestation, a supply-chain step you cannot inspect. The honest
output is a bounded WARN — "boot integrity established from the TPM up to the bootloader;
SPI-flash contents not independently verified; firmware below X unmeasured" — not a PASS
inferred from the absence of an alarm. An unmeasurable layer is exactly where an
implant hides *because* it is unmeasurable; naming it is the finding, and it is worth
more than a confident clean bill an implant would happily let you sign.

---

## The one-line test

If the thing telling you the system is clean could itself be the compromise, you have a
rumor, not an attestation. Anchor the measurement to a root below the layer that could
lie — or state plainly that the layer is unverified and stop calling silence "clean."
