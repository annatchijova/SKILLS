"""List one collection without recursive discovery or duplicate skill names."""
import argparse
import hashlib
import json
from pathlib import Path
from validate_collection import skill_name

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("mode", choices=["general", "red-team"])
args = parser.parse_args()
collection = Path(__file__).resolve().parent
root = collection.parent if args.mode == "general" else collection
entries = []
names = set()
for path in sorted(root.glob("*/SKILL.md")):
    if path.parent.is_symlink() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise SystemExit(f"Skill path escapes collection or uses a symlink: {path}")
    name = skill_name(path)
    if name in names:
        raise SystemExit(f"Duplicate name: {name}")
    names.add(name)
    entries.append({"name": name, "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
print(json.dumps(entries, indent=2))
