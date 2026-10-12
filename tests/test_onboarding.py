"""Verify onboarding travels with an isolated collaboration-skill installation."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('onboarding_install', ROOT/'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class OnboardingPackageTests(unittest.TestCase):
    def test_protocol_survives_selective_install_without_root_docs(self):
        with tempfile.TemporaryDirectory(prefix='onboarding-install-') as folder:
            destination = Path(folder)/'skills'
            selected = installer.select('collaboration')
            installer.install(destination, selected)
            installed = (destination/'coauthor-github-workflow').resolve()
            relative = Path('references/onboarding-protocol.md')
            self.assertEqual((installed/relative).read_bytes(),
                             (ROOT/'skills/coauthor-github-workflow'/relative).read_bytes())
            self.assertFalse((Path(folder)/'docs').exists())
            # The agent can follow all local references with no toolkit-root docs or network.
            for page in (installed/'SKILL.md', installed/relative):
                prose = re.sub(r'```.*?```', '', page.read_text(), flags=re.S)
                for link in re.findall(r'\]\(([^)]+)\)', prose):
                    if urlsplit(link).scheme or link.startswith('#'):
                        continue
                    target = (page.parent/unquote(link.split('#', 1)[0])).resolve()
                    self.assertTrue(target.is_relative_to(installed), link)
                    self.assertTrue(target.is_file(), link)

    def test_dry_run_does_not_create_destination(self):
        with tempfile.TemporaryDirectory(prefix='onboarding-preview-') as folder:
            target = Path(folder)/'skills'
            selected = installer.select('collaboration')
            actions = installer.install(target, selected, dry_run=True)
            self.assertEqual({name for name, _ in actions}, installer.COLLABORATION)
            self.assertFalse(target.exists())

    def test_existing_protocol_is_preserved_without_replace(self):
        with tempfile.TemporaryDirectory(prefix='onboarding-preserve-') as folder:
            target = Path(folder)/'skills'
            selected = installer.select('collaboration')
            installer.install(target, selected)
            protocol = target/'coauthor-github-workflow/references/onboarding-protocol.md'
            protocol.write_text('Collaborator-specific local guidance\n')
            before = {str(p.relative_to(target)): p.read_bytes()
                      for p in target.rglob('*') if p.is_file()}
            with self.assertRaises(ValueError):
                installer.install(target, selected)
            after = {str(p.relative_to(target)): p.read_bytes()
                     for p in target.rglob('*') if p.is_file()}
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
