"""Negative tests for portable integrity records, without source-paper inputs."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("verify_package", Path(__file__).resolve().parents[1] / "scripts/verify_package.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def make_package(self, root):
        data = root / "guide.txt"
        data.write_text("Original analysis", encoding="utf-8")
        manifest = {"schema_version": 1, "files": {"guide.txt": {"size": data.stat().st_size, "sha256": hashlib.sha256(data.read_bytes()).hexdigest()}}}
        (root / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
        return manifest

    def test_valid_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_package(root)
            package.verify_manifest(root)

    def test_changed_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_package(root)
            (root / "guide.txt").write_text("Different text", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Changed package"):
                package.verify_manifest(root)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_package(root)
            (root / "guide.txt").unlink()
            with self.assertRaisesRegex(ValueError, "Missing package"):
                package.verify_manifest(root)

    def test_extra_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_package(root)
            (root / "unrecorded.txt").touch()
            with self.assertRaisesRegex(ValueError, "Unexpected"):
                package.verify_manifest(root)

    def test_unsafe_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.make_package(root)
            manifest["files"]["../outside.txt"] = manifest["files"].pop("guide.txt")
            (root / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unsafe manifest"):
                package.verify_manifest(root)

    def test_duplicate_json_key(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            json.loads('{"files": {}, "files": {}}', object_pairs_hook=package.no_duplicate_keys)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_package(root)
            (root / "guide.txt").rename(root / "outside.txt")
            (root / "guide.txt").symlink_to(root / "outside.txt")
            with self.assertRaisesRegex(ValueError, "Symlink"):
                package.verify_manifest(root)
