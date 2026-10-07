import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1]/'scripts/install.py'
spec = importlib.util.spec_from_file_location('coauthor_install', MODULE_PATH)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallationTests(unittest.TestCase):
    def test_profiles_and_dependency_closure(self):
        self.assertEqual(set(installer.select('collaboration')), installer.COLLABORATION)
        self.assertTrue(installer.WRITING_CORE <= set(installer.select(skills=['referee-report'])))
        with self.assertRaises(ValueError):
            installer.select(skills=['unknown'])

    def test_no_overwrite_and_recoverable_replacement(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root)/'skills'
            installer.install(target, ['overleaf-sync'], dry_run=True)
            self.assertFalse(target.exists())
            installer.install(target, ['overleaf-sync'])
            self.assertEqual(installer.install(target, ['overleaf-sync'])[0][1], 'unchanged')
            entry = target/'overleaf-sync/SKILL.md'
            entry.write_text('Existing user instructions\n')
            with self.assertRaises(ValueError):
                installer.install(target, ['overleaf-sync'])
            self.assertEqual(entry.read_text(), 'Existing user instructions\n')
            installer.install(target, ['overleaf-sync'], replace=True)
            backups = list((Path(root)/'skill-backups').glob('*/overleaf-sync/SKILL.md'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'Existing user instructions\n')

    def test_unrelated_skills_and_symlinks_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root)/'skills'
            target.mkdir()
            unrelated = target/'unrelated'
            unrelated.mkdir()
            (unrelated/'SKILL.md').write_text('keep')
            (target/'overleaf-sync').symlink_to(unrelated, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(target, ['overleaf-sync'])
            self.assertEqual((unrelated/'SKILL.md').read_text(), 'keep')

    def test_changed_distribution_is_refused_before_install(self):
        import json
        original_root = installer.ROOT
        with tempfile.TemporaryDirectory() as root:
            installer.ROOT = Path(root)
            try:
                source = Path(root)/'skills/example'
                source.mkdir(parents=True)
                (source/'SKILL.md').write_text('changed package')
                (Path(root)/'MANIFEST.json').write_text(json.dumps({'files':{
                    'skills/example/SKILL.md':{'sha256':'wrong hash'}}}))
                target = Path(root).parent/(Path(root).name+'-destination')
                with self.assertRaises(ValueError):
                    installer.install(target, ['example'])
                self.assertFalse(target.exists())
            finally:
                installer.ROOT = original_root

if __name__ == '__main__':
    unittest.main()
