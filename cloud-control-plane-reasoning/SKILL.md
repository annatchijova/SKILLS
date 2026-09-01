---
name: cloud-control-plane-reasoning
description: Reason about cloud compromise on the identity and control-plane graph, not the network diagram — because in cloud the control plane is an internet-reachable API authorized by credentials, it sits beside the data plane rather than above it behind a firewall, and a stolen key is one AssumeRole from the whole account. Use whenever the system is AWS/Azure/GCP/Kubernetes and the question is attack path, blast radius, privilege escalation, or "how bad is this": an SSRF that can reach the metadata endpoint, a leaked cloud key, an IAM/role/trust-policy review, `iam:PassRole` or `sts:AssumeRole` in a policy, a cross-account bucket policy, a service account or workload identity, a compromised container or CI runner in cloud. Trigger on "is this cloud config dangerous", "SSRF severity in cloud", "can they escalate from this role", "cross-account trust", "instance metadata", "what does this service account reach", "cloud lateral movement", or "model the blast radius in AWS/Azure/GCP". Sibling of assume-breach-modeling (this supplies the cloud-specific edges) and authorization-surface-mapping (IAM is its actor×resource×action grid). It does not configure the cloud or write Terraform, and it treats a network diagram alone as an incomplete model.
---

# Cloud Control-Plane Reasoning

On-prem intuition fails in cloud for one structural reason: **the control plane is an
API.** Deleting every snapshot, minting a new admin, exfiltrating a database via a
signed URL, backdooring the identity system — none of it touches the network you drew.
It is an authenticated call to `*.amazonaws.com` / `management.azure.com` /
`googleapis.com`, reachable from anywhere, authorized by a credential. The firewall
that guards the *data plane* (the running workload, the disk, the packets) does not
sit in front of the *control plane*, and the thing an attacker actually wants is the
control plane. Model the network and you have modeled the part that matters least.

The reframes this skill forces, each of which flips a severity most reviewers get
wrong:

- **An SSRF in cloud is usually credential theft, not information disclosure** — if it
  can reach the instance metadata endpoint, it reads the instance-profile credentials
  and becomes whatever that role is. Severity is set by the role, not by the SSRF.
- **Privilege escalation is an API call, not an exploit** — no memory corruption
  needed; `iam:CreatePolicyVersion`, `iam:PassRole` to a fatter service, updating a
  running Lambda's role, is escalation by design of the IAM system.
- **Persistence moved off disk and into identity** — hosts are cattle; a re-image
  removes nothing. The backdoor is an extra access key on a user, a trust-policy edit,
  a new role, a Lambda triggered on an event. (`forensic-persistence` in the cloud key.)

Composes with the library:

- **assume-breach-modeling** — this skill supplies the cloud-specific edges (assume-role chains, metadata pivots); that one runs the reachability graph
- **authorization-surface-mapping** — IAM *is* the actor×resource×action matrix; resolve "what can this identity do" there, don't eyeball the role name
- **credential-material-triage** — a captured cloud key's reach is its policy set plus everything it can assume transitively
- **forensic-logging-design** — control-plane logs (CloudTrail/Activity/Audit) and data-plane logs (S3 data events, VPC flow) are different feeds; you can be blind to one while watching the other
- **forensic-persistence** — cloud persistence lives in IAM and event triggers, not files
- **secret-lifecycle-discipline** — the instance profile / workload identity is a rotating secret whose scope is the real question

---

## Step 1 — Separate control plane from data plane, and find the real target

For the resource in question, split every action into the plane it touches:

- **Data plane** — operating on the contents: reading rows, encrypting a disk, serving
  requests, packets between pods. Guarded by network, security groups, app auth.
- **Control plane** — operating on the resource *as a cloud object* via API: snapshot
  it, change its role, make its bucket public, delete it, replicate it elsewhere,
  read it through a management API that ignores the app.

The attacker's objective is almost always control-plane: it is quieter (looks like
administration — see `dual-use-behavior-adjudication`), more complete (copy the whole
DB via snapshot, no row-by-row exfil), and outside the network controls you built. If
your threat model only defends the data plane, name that gap as the finding.

---

## Step 2 — Identity is the perimeter: draw the trust graph, not the VPC

The boundary in cloud is not the subnet; it is *who can assume what*. Build the graph
whose nodes are principals (users, roles, service accounts, workload identities,
managed identities) and whose edges are:

- **AssumeRole / trust policies** — role A trusts principal B; follow every edge,
  including transitive ones. The reachable set of `*:*` from a starting identity is the
  real blast radius.
- **PassRole** — the quiet escalator: a principal that can `iam:PassRole` a
  higher-privileged role to a service it controls (Lambda, EC2, Glue) *becomes* that
  role's authority without ever holding its credentials.
- **Resource-based policies** — an S3 bucket policy, a KMS key policy, an SQS policy
  granting *another account* access. This is how the boundary you think is the account
  edge is silently a doorway (confused deputy; check the `external ID` on third-party
  roles).
- **Federation / SSO / OIDC** — the identity provider is upstream of every role it can
  vend; compromising it, or a CI provider's OIDC trust, mints cloud identity directly.

The shortest path from any foothold identity to an administrative action is the
finding. It is usually two or three edges and never appears on a network diagram.

---

## Step 3 — The metadata pivot and the foothold-to-credential jump

Whenever a workload can be induced to make an outbound request the attacker chooses
(SSRF, a fetch of attacker-controlled URL, a misconfigured proxy), test the
control-plane consequence, not just the data one:

- **Instance metadata** — IMDSv1 (or IMDSv2 not enforced) returns the instance
  profile's credentials to anything that can hit `169.254.169.254`. That turns a
  "medium SSRF" into "attacker is now this role." Azure IMDS / GCP metadata are the
  same shape.
- **Container / pod identity** — a compromised container inherits its service account /
  workload identity / IRSA role; the node's identity may be broader still. Container
  escape is often unnecessary — the pod's token already reaches the control plane.
- **CI/CD identity** — a build job's OIDC token or stored deploy credential is a
  control-plane identity with, frequently, production rights. The pipeline is inside
  the perimeter you forgot to draw.

For each foothold, ask: *what identity does code running here hold, and what does Step 2
say that identity reaches?* That is the true severity of the foothold.

---

## Step 4 — Escalation and persistence are configuration changes

Enumerate escalation as *permitted API calls*, not vulnerabilities:

- `iam:CreatePolicyVersion` / `AttachUserPolicy` / `PutUserPolicy` — grant yourself more.
- `PassRole` + a service you can launch — inherit a fatter role.
- `UpdateFunctionConfiguration` / update a running resource's role — ride an existing
  higher-privileged identity.
- `AssumeRole` into a role whose trust policy is too broad.

And persistence as *configuration additions* that survive re-imaging: a second access
key on a user, an added trust relationship, a new IAM user/role, a Lambda on a
CloudTrail/event trigger, a modified SSO mapping. Hunt these in the control-plane log,
not on the host — the host is ephemeral and clean.

---

## Step 5 — Know which plane your logging can see

Before claiming detection or doing IR, state which feed covers which plane, because the
classic cloud blind spot is watching one and missing the other:

- **Control-plane logs** — CloudTrail (management events), Azure Activity/Entra audit,
  GCP Admin Activity: every API call, the identity, the source. This is where Step 2–4
  live; without it, control-plane compromise is invisible.
- **Data-plane logs** — S3 data events, VPC flow logs, DNS logs, app logs: often *off
  by default*, high-volume, separately enabled. Exfil via signed URL or a public bucket
  can be entirely absent from control-plane logs.

A detection or IR claim must name the plane it covers. "We have CloudTrail" does not
mean "we would see the exfil"; it means "we would see the API calls that *set up* the
exfil." Route the design through `forensic-logging-design`; do not assert coverage you
have not confirmed per plane.

---

## The one-line test

If your cloud threat model is a network diagram, you have modeled the data plane and
missed the compromise. Redraw it as the identity/trust graph: nodes are principals,
edges are assume-role and pass-role, and the shortest path to `*:*` — usually two hops
and invisible on the VPC picture — is the finding.
