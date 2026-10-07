import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

LIBRARY = Path(__file__).resolve().parents[1]/'skills/corpus-econ-writing/references/library'
spec = importlib.util.spec_from_file_location('public_corpus_edition', LIBRARY/'expansion/scripts/edition.py')
edition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edition)

class PublicAdaptationTests(unittest.TestCase):
    def test_only_exact_pinned_non_scientific_adaptation_is_accepted(self):
        old_base = edition.BASE
        with tempfile.TemporaryDirectory() as root:
            edition.BASE = Path(root)
            try:
                path = Path(root)/'database/QUALITY_RECEIPT.json'
                path.parent.mkdir()
                path.write_text('redacted receipt')
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                original = hashlib.sha256(b'original receipt').hexdigest()
                mapping = Path(root)/'PUBLIC_ADAPTATIONS.json'
                mapping.write_text(json.dumps({'files':{'database/QUALITY_RECEIPT.json':{
                    'source_sha256':original, 'package_sha256':actual}}}))
                self.assertTrue(edition.frozen_matches(path, original))
                self.assertFalse(edition.frozen_matches(path, 'wrong source hash'))
                path.write_text('tampered receipt')
                self.assertFalse(edition.frozen_matches(path, original))
                data = Path(root)/'database/writing_database.json'
                data.write_text('changed scientific data')
                mapping.write_text(json.dumps({'files':{'database/writing_database.json':{
                    'source_sha256':original, 'package_sha256':edition.digest(data)}}}))
                self.assertFalse(edition.frozen_matches(data, original))
            finally:
                edition.BASE = old_base

if __name__ == '__main__':
    unittest.main()
