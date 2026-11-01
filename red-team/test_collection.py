"""Negative-control tests for the provenance validator, using isolated fixtures."""
import json
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from validate_collection import UPSTREAM_REVISION, digest, validate


class CollectionValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "collection"
        self.upstream = Path(self.temp.name) / "upstream"
        self.source = "Skills/web/offensive-example/SKILL.md"
        self.target = "rt-example/SKILL.md"
        self.write(self.upstream / self.source, "upstream evidence")
        self.write(self.root / "method/SKILL.md", "---\nname: method\ndescription: Local method\n---\nMethod\n")
        self.write(self.root / "METHODOLOGY.md", "Assessment contract")
        self.write(self.root / self.target, f"---\nname: rt-example\ndescription: Example assessment\n---\nRead [contract](../METHODOLOGY.md).\n{self.source}\n{UPSTREAM_REVISION}\n")
        self.write(self.root / "SOURCES.json", json.dumps({"files": [{"source": "method/SKILL.md", "sha256": digest(self.root / "method/SKILL.md")}]}))
        self.row = {"source": self.source, "target": self.target, "disposition": "rewritten", "mechanisms": ["boundary"], "rationale": "Controlled experiment", "tool_verification": "not executed"}
        self.coverage([self.row])
        self.write(self.root / "validate_collection.py", Path(__file__).with_name("validate_collection.py").read_text())
        for mocker in (
            patch("validate_collection.SNAPSHOT_MANIFEST_SHA", digest(self.root / "SOURCES.json")),
            patch("validate_collection.pinned_sources", return_value={self.source: digest(self.upstream / self.source)}),
        ):
            mocker.start()
            self.addCleanup(mocker.stop)

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def coverage(self, rows):
        self.write(self.root / "reviews/test-coverage.json", json.dumps(rows))

    def test_valid_collection(self):
        result = validate(self.root, self.upstream)
        self.assertEqual(result["source_count"], 1)
        self.assertEqual(result["total_skill_count"], 2)

    def test_changed_copy_rejected(self):
        self.write(self.root / "method/SKILL.md", "changed")
        with self.assertRaisesRegex(ValueError, "Changed snapshot"):
            validate(self.root, self.upstream)

    def test_missing_source_coverage_rejected(self):
        self.coverage([])
        with self.assertRaisesRegex(ValueError, "Coverage mismatch"):
            validate(self.root, self.upstream)

    def test_duplicate_coverage_rejected(self):
        self.coverage([self.row, self.row])
        with self.assertRaisesRegex(ValueError, "covered twice"):
            validate(self.root, self.upstream)

    def test_broken_reference_rejected(self):
        with (self.root / self.target).open("a") as handle:
            handle.write("[missing](../absent.md)")
        with self.assertRaisesRegex(ValueError, "Unresolved local link"):
            validate(self.root, self.upstream)

    def test_unmapped_skill_rejected(self):
        self.write(self.root / "extra/SKILL.md", "---\nname: extra\ndescription: Extra\n---\nExtra\n")
        with self.assertRaisesRegex(ValueError, "Unmapped adaptations"):
            validate(self.root, self.upstream)

    def test_added_copy_resource_rejected(self):
        self.write(self.root / "method/extra.txt", "unexpected")
        with self.assertRaisesRegex(ValueError, "added or removed"):
            validate(self.root, self.upstream)

    def test_rehashed_snapshot_manifest_rejected(self):
        self.write(self.root / "SOURCES.json", '{"files": []}')
        with self.assertRaisesRegex(ValueError, "baseline changed"):
            validate(self.root, self.upstream)

    def test_changed_upstream_rejected(self):
        self.write(self.upstream / self.source, "different source")
        with self.assertRaisesRegex(ValueError, "Upstream bytes"):
            validate(self.root, self.upstream)

    def test_changed_contract_changes_manifest(self):
        before = validate(self.root, self.upstream)["methodology_sha256"]
        self.write(self.root / "METHODOLOGY.md", "Different instructions")
        self.assertNotEqual(before, validate(self.root, self.upstream)["methodology_sha256"])

    def test_plain_contract_mention_rejected(self):
        path = self.root / self.target
        self.write(path, path.read_text().replace("[contract](../METHODOLOGY.md)", "METHODOLOGY.md"))
        with self.assertRaisesRegex(ValueError, "effective contract link"):
            validate(self.root, self.upstream)

    def test_invalid_metadata_rejected(self):
        self.coverage([{**self.row, "mechanisms": " "}])
        with self.assertRaisesRegex(ValueError, "Incomplete disposition"):
            validate(self.root, self.upstream)

    def test_duplicate_identity_rejected_in_both_readers(self):
        self.write(self.root / "catalog.py", Path(__file__).with_name("catalog.py").read_text())
        path = self.root / self.target
        original = path.read_text()
        for names in ("name: rt-example\nname: wrong", "name: wrong\nname: rt-example"):
            with self.subTest(names=names):
                self.write(path, original.replace("name: rt-example", names))
                with self.assertRaisesRegex(ValueError, "Invalid skill identity"):
                    validate(self.root, self.upstream)
                result = subprocess.run([sys.executable, "-B", str(self.root / "catalog.py"), "red-team"], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid skill identity", result.stderr)

    def test_quoted_identity_consistent_in_both_readers(self):
        self.write(self.root / "catalog.py", Path(__file__).with_name("catalog.py").read_text())
        path = self.root / self.target
        self.write(path, path.read_text().replace("name: rt-example", 'name: "rt-example"'))
        self.assertEqual(validate(self.root, self.upstream)["adaptation_count"], 1)
        result = subprocess.run([sys.executable, "-B", str(self.root / "catalog.py"), "red-team"], capture_output=True, text=True, check=True)
        self.assertIn("rt-example", [entry["name"] for entry in json.loads(result.stdout)])

    def test_catalog_rejects_symlink_in_both_modes(self):
        script = Path(__file__).with_name("catalog.py")
        self.write(self.root / "catalog.py", script.read_text())
        outside = Path(self.temp.name) / "external"
        self.write(outside / "SKILL.md", "---\nname: external\ndescription: External\n---\n")
        for mode, selected in (("general", self.root.parent), ("red-team", self.root)):
            with self.subTest(mode=mode):
                link = selected / "escape"
                link.symlink_to(outside, target_is_directory=True)
                try:
                    result = subprocess.run([sys.executable, "-B", str(self.root / "catalog.py"), mode], capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("symlink", result.stderr)
                finally:
                    link.unlink()

    def test_catalog_general_does_not_recurse(self):
        self.write(self.root / "catalog.py", Path(__file__).with_name("catalog.py").read_text())
        result = subprocess.run([sys.executable, "-B", str(self.root / "catalog.py"), "general"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), [])

    def test_missing_contract_rejected(self):
        (self.root / "METHODOLOGY.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing assessment contract"):
            validate(self.root, self.upstream)

    def test_reduced_upstream_inventory_rejected(self):
        extra = "Skills/web/offensive-second/SKILL.md"
        with patch("validate_collection.pinned_sources", return_value={self.source: digest(self.upstream / self.source), extra: "expected"}):
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                validate(self.root, self.upstream)


if __name__ == "__main__":
    unittest.main()
