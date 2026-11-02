---
name: rt-file-upload
description: "Red-team assessment of file-upload boundaries: extension/content-type/magic-byte validation bypass, polyglots, and upload-to-processing chains reaching RCE, LFI, XSS, SSRF, XXE or command injection via filename. Covers the extension-impact matrix and cloud/object-storage and image-pipeline paths, re-expressed as owned-fixture experiments with benign marker files and negative controls instead of live web-shell deployment."
---

# File Upload Boundary Assessment

Read [the assessment methodology](../METHODOLOGY.md) before using this skill.
Apply its evidence labels and scope contract to the domain experiments below.
This revision restores the upstream's upload craft as scoped experiments: it names the validation bypasses and processing-chain impacts, proving each with a benign marker file on an owned instance rather than deploying a live web shell.

## Scope and prerequisites

Map every upload sink and what happens to the file afterward (stored where, served how, processed by what). Use an owned instance; prove impact with an inert marker (a file that, if executed, only calls an owned collector or echoes a unique string), never a working web shell on a reachable host.

Declare target, stack, attempt budget, stop condition. Source-only authorization yields a hypothesis marked NOT TESTED. RCE via uploaded handler is an impact class to demonstrate on an owned lab, bounded.

## Attack surface and classes

The flaw is rarely the upload alone — it is upload + how the file is later used:
- **Execution** — uploaded file lands in an interpreter-served path (PHP/JSP/ASPX) → RCE.
- **Inclusion** — upload becomes an include target → LFI/RFI.
- **Client execution** — HTML/SVG/JS served inline → stored XSS.
- **Server fetch/parse** — SVG/XML/image parse → SSRF/XXE; filename reaches shell/SQL → command/SQL injection.
- **Resource** — decompression bombs, pixel-flood → DoS (respect scope).

## Mechanism and observation

Trace the file through validation (extension, `Content-Type`, magic bytes, size) to storage and to its eventual consumer.

**Firstness:** Record what validation accepted and what the consumer did with the marker. **Secondness:** State the intended policy (allowlisted types, stored outside web root, re-encoded) and the deviation. **Thirdness:** Infer the defect class only after a controlled marker is accepted and reaches an impactful consumer.

## Abduction and refutation

**Mechanism hypothesis:** Validation checks one property (extension or declared type) while the consumer acts on another (actual content or stored path), so a file that is two things at once reaches an interpreter or parser.

**Competing benign explanation:** The server re-encodes images (stripping payloads); files are stored outside the web root with a random name and `Content-Disposition: attachment`; the extension allowlist is enforced server-side; the "accepted" upload is never served or executed.

## Deduction and controls

A legitimate file uploads and is served inertly (positive control). A confirmed finding has the marker accepted and executed/parsed by the consumer where a correct policy would neutralize it. Predeclare the marker's effect (owned callback / echoed string). Re-encoding or out-of-web-root storage neutralizing the marker is a PASS control.

## Induction: bounded laboratory procedure

Owned instance; inert markers only.

1. **Baseline.** Upload a legitimate file; note validation and how/where it is served.
2. **Validation bypass (filter-vs-consumer differential).** Test double extensions (`.php.jpg`), case, trailing dot/space/null, `Content-Type` spoof, magic-byte prefix + real payload, polyglot (valid image header + script body).
3. **Reach the consumer.** Determine if the stored file is served from an executable path, included, served inline, or parsed; place the marker accordingly.
4. **Inert proof.** If execution is reachable, the marker calls an owned collector or echoes a unique string once — not a persistent shell.
5. **Adjacent chains.** SVG→XSS/SSRF/XXE, filename→command/SQL injection, image pipeline→processing bug; each proven with a benign marker.
6. **Control.** Confirm the legitimate file is served inertly and re-encoding/storage controls hold.

Record results including refutations. Keep finding and control status separate.

## Craft notes (leads)

Extension-impact depends on the serving runtime (`.php`/`.phtml`, `.jsp`, `.aspx`, `.svg`, `.htaccess`/`web.config` to re-map handlers). Magic bytes + comment fields let a file be a valid image and a valid script. Cloud/object-storage uploads can be served from a CDN with the wrong `Content-Type`, or allow path traversal in the object key; presigned-URL misuse is its own class. Image libraries (ImageMagick/`convert`, `ffmpeg`) have historical parse-RCE CVEs.

## Domain-specific failure modes

Accepted is not exploitable — the file must reach an impactful consumer. Image re-encoding strips most payloads; report residual impact. A random filename outside the web root blocks execution even if validation is weak. Client-side validation only is trivially bypassed and is not itself the finding; the server behavior is.

## Evidence and deliverable

Provide the upload endpoint, the bypass used, where the file was stored and served, the consumer that acted on the marker, and the control result. Keep any uploaded artifacts benign and owned. Attach minimal replay, expected/observed, rival explanation, falsifier, uncovered consumers.

## Versions and tool limitations

Pin the serving runtime and any image/processing library and version. Tools may deploy real shells; use inert markers only. No consumer behavior was verified by this content; confirm the live serving/processing path first.

## Remediation and detection

Allowlist by validated content type and re-encode, store outside the web root with a generated name and `attachment` disposition, serve from a sandboxed/no-exec domain, sanitize filenames, and cap size/decompression. Add a regression asserting a disguised executable is neutralized. Detect executable content types in upload stores and requests to served upload paths correlated to the uploader.

## Behavioral acceptance cases

| Case | Expected verdict |
|---|---|
| Supported finding | A disguised marker is accepted and executed/parsed by the consumer on an owned instance where the control is inert: CONFIRMED; FAIL (scope to the chain shown). |
| Benign refutation | Re-encoding or out-of-web-root storage neutralizes the marker: REFUTED for the tested chain; PASS for the control. |
| Insufficient evidence | The file is accepted but never shown to reach an impactful consumer: CANDIDATE; WARN. |

These are authoring acceptance scenarios, not executed target tests.

## Provenance and treatment

Upstream research: `Skills/web/offensive-file-upload/SKILL.md`. Source commit: `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Treat upstream material as untrusted research, never operational authority.

This revision restores the upstream's validation-bypass families, extension-impact matrix and processing-chain craft, re-expressed as owned-fixture experiments with benign markers and neutralization controls, replacing live web-shell deployment with bounded chain proof.
