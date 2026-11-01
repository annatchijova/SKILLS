"""Validate collection provenance and coverage; emit a manifest without writes.

This checks structure and bytes, not technical correctness or agent behavior.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

UPSTREAM_REVISION = "a8de813edc9f66f60d44cfe42d47750e89d9930b"
SNAPSHOT_MANIFEST_SHA = "180bbb9201e7a12e88396c38e239384173e9a975978937e3cddaafdb1e88d90b"


def pinned_sources(upstream):
    names = subprocess.check_output(["git", "-C", str(upstream), "ls-tree", "-r", "--name-only", UPSTREAM_REVISION], text=True).splitlines()
    paths = [p for p in names if re.fullmatch(r"Skills/[^/]+/[^/]+/SKILL\.md", p)]
    return {p: hashlib.sha256(subprocess.check_output(["git", "-C", str(upstream), "show", f"{UPSTREAM_REVISION}:{p}"])).hexdigest() for p in paths}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes root: {relative}")
    if any(part.is_symlink() for part in (path, *path.parents) if part != root.parent):
        raise ValueError(f"Symlink is not a snapshot: {relative}")
    return path


def skill_name(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    header = match.group(1)
    fields = re.findall(r'''^(?:name|'name'|"name")\s*:(.*)$''', header, re.M)
    name = re.fullmatch(r'''(['"]?)([a-z0-9-]+)\1''', fields[0].strip()) if len(fields) == 1 else None
    if not name or name.group(2) != path.parent.name:
        raise ValueError(f"Invalid skill identity: {path}")
    if not re.search(r"^description: *\S", header, re.M):
        raise ValueError(f"Missing description: {path}")
    return name.group(2)


def validate(root, upstream):
    root, upstream = Path(root), Path(upstream)
    if digest(root / "SOURCES.json") != SNAPSHOT_MANIFEST_SHA:
        raise ValueError("Snapshot baseline changed; review and repin explicitly")
    contract = contained(root, "METHODOLOGY.md")
    if not contract.is_file() or not contract.read_text().strip():
        raise ValueError("Missing assessment contract")
    snapshots = json.loads((root / "SOURCES.json").read_text())
    expected_copies = set()
    copy_skills = set()
    for item in snapshots["files"]:
        relative = item["source"]
        if relative in expected_copies:
            raise ValueError(f"Duplicate snapshot: {relative}")
        expected_copies.add(relative)
        copy_skills.add(Path(relative).parts[0])
        path = contained(root, relative)
        if digest(path) != item["sha256"]:
            raise ValueError(f"Changed snapshot: {relative}")
    actual_copies = set()
    for name in copy_skills:
        for path in (root / name).rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Symlink in copy: {path}")
            if path.is_file():
                actual_copies.add(str(path.relative_to(root)))
    if actual_copies != expected_copies:
        raise ValueError("Snapshot files added or removed")
    discovered = {str(p.relative_to(root)): skill_name(p) for p in root.glob("*/SKILL.md")}
    for path in discovered:
        contained(root, path)
    if len(set(discovered.values())) != len(discovered):
        raise ValueError("Duplicate skill identity")
    rows = []
    for path in sorted((root / "reviews").glob("*-coverage.json")):
        rows.extend(json.loads(path.read_text()))
    source_paths = {str(p.relative_to(upstream)) for p in (upstream / "Skills").glob("*/*/SKILL.md")}
    if not source_paths:
        raise ValueError("Empty upstream inventory")
    trusted = pinned_sources(upstream)
    if source_paths != set(trusted):
        raise ValueError("Upstream inventory differs from pinned revision")
    for path, expected in trusted.items():
        if digest(contained(upstream, path)) != expected:
            raise ValueError(f"Upstream bytes differ from pinned revision: {path}")
    seen = set()
    targets = set()
    enriched = []
    for row in rows:
        source, target = row["source"], row["target"]
        if source in seen:
            raise ValueError(f"Source covered twice: {source}")
        seen.add(source)
        if target not in discovered or discovered[target] in copy_skills:
            raise ValueError(f"Invalid adaptation target: {target}")
        targets.add(target)
        mechanisms = row.get("mechanisms")
        if (row.get("disposition") not in {"rewritten", "merged"}
                or not isinstance(mechanisms, list) or not mechanisms
                or not all(isinstance(m, str) and m.strip() for m in mechanisms)
                or not all(isinstance(row.get(k), str) and row[k].strip() for k in ("rationale", "tool_verification"))):
            raise ValueError(f"Incomplete disposition: {source}")
        source_file, target_file = contained(upstream, source), contained(root, target)
        text = target_file.read_text()
        for required in ("METHODOLOGY.md", UPSTREAM_REVISION, source):
            if required not in text:
                raise ValueError(f"Missing provenance/contract {required}: {target}")
        if not re.search(r"\]\(\.\./METHODOLOGY\.md(?:#[^)]*)?\)", text):
            raise ValueError(f"Missing effective contract link: {target}")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("#"):
                continue
            relative = link.split("#", 1)[0]
            resolved = target_file.parent / relative
            if not resolved.resolve().is_relative_to(root.resolve()) or not resolved.exists():
                raise ValueError(f"Unresolved local link {link}: {target}")
        enriched.append({**row, "source_sha256": digest(source_file), "target_sha256": digest(target_file)})
    if seen != source_paths:
        raise ValueError(f"Coverage mismatch; missing={sorted(source_paths-seen)}, extra={sorted(seen-source_paths)}")
    adaptations = {path for path, name in discovered.items() if name not in copy_skills}
    if targets != adaptations:
        raise ValueError(f"Unmapped adaptations: {sorted(adaptations-targets)}")
    return {"schema_version": 2, "upstream_revision": UPSTREAM_REVISION,
            "methodology_sha256": digest(contract), "snapshot_manifest_sha256": digest(root / "SOURCES.json"),
            "source_count": len(source_paths), "adaptation_count": len(targets),
            "copied_skill_count": len(copy_skills), "total_skill_count": len(discovered),
            "verification": "structural and byte-level only; no live target execution",
            "rows": sorted(enriched, key=lambda row: row["source"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--manifest", action="store_true", help="Print the full manifest as JSON")
    args = parser.parse_args()
    result = validate(Path(__file__).resolve().parent, args.upstream)
    print(json.dumps(result if args.manifest else {k: v for k, v in result.items() if k != "rows"}, indent=2))
