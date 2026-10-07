"""Exercise handbook update/save semantics against disposable local repositories."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class CoauthorGitWorkflowTests(unittest.TestCase):
    def git(self, directory, *args, ok=True):
        env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TERMINAL_PROMPT='0', GIT_AUTHOR_NAME='Synthetic author',
                   GIT_AUTHOR_EMAIL='author@example.invalid', GIT_COMMITTER_NAME='Synthetic author',
                   GIT_COMMITTER_EMAIL='author@example.invalid')
        result = subprocess.run(['git', '-C', str(directory), *args], env=env,
                                text=True, capture_output=True, timeout=20)
        if ok and result.returncode:
            self.fail(result.stderr)
        return result

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='coauthor-git-')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.remote, self.a, self.b = root/'remote.git', root/'a', root/'b'
        self.git(root, 'init', '--bare', '--initial-branch=main', str(self.remote))
        self.git(root, 'clone', str(self.remote), str(self.a))
        (self.a/'note.md').write_text('Initial note\n')
        self.git(self.a, 'add', '--', 'note.md')
        self.git(self.a, '-c', 'commit.gpgsign=false', 'commit', '-m', 'Initial fixture')
        self.git(self.a, 'push', '-u', 'origin', 'main')
        self.git(root, 'clone', str(self.remote), str(self.b))

    def commit(self, folder, filename, text):
        (folder/filename).write_text(text)
        self.git(folder, 'add', '--', filename)
        self.git(folder, '-c', 'commit.gpgsign=false', 'commit', '-m', 'Fixture update')

    def test_fetch_preserves_dirty_and_untracked_work(self):
        self.commit(self.b, 'remote.md', 'Coauthor update\n')
        self.git(self.b, 'push', 'origin', 'main')
        (self.a/'note.md').write_text('My unfinished edits\n')
        (self.a/'untracked.md').write_text('Not committed\n')
        before = self.git(self.a, 'rev-parse', 'HEAD').stdout
        self.git(self.a, 'fetch', 'origin')
        self.assertEqual(before, self.git(self.a, 'rev-parse', 'HEAD').stdout)
        self.assertEqual((self.a/'note.md').read_text(), 'My unfinished edits\n')
        self.assertEqual((self.a/'untracked.md').read_text(), 'Not committed\n')
        self.assertFalse((self.a/'remote.md').exists())

    def test_fast_forward_pull_refuses_divergence_without_losing_work(self):
        self.commit(self.a, 'local.md', 'Local committed work\n')
        local_head = self.git(self.a, 'rev-parse', 'HEAD').stdout
        self.commit(self.b, 'remote.md', 'Remote committed work\n')
        self.git(self.b, 'push', 'origin', 'main')
        result = self.git(self.a, 'pull', '--ff-only', 'origin', 'main', ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(local_head, self.git(self.a, 'rev-parse', 'HEAD').stdout)
        self.assertEqual((self.a/'local.md').read_text(), 'Local committed work\n')
        self.assertEqual(self.git(self.a, 'status', '--porcelain').stdout, '')

    def test_unstage_keeps_working_edit(self):
        (self.a/'note.md').write_text('Keep this change\n')
        self.git(self.a, 'add', '--', 'note.md')
        self.git(self.a, 'restore', '--staged', '--', 'note.md')
        self.assertEqual(self.git(self.a, 'diff', '--cached').stdout, '')
        self.assertEqual((self.a/'note.md').read_text(), 'Keep this change\n')
        self.assertIn('Keep this change', self.git(self.a, 'diff').stdout)

    def test_merge_base_updates_preserves_both_lineages(self):
        self.git(self.a, 'switch', '-c', 'alex/revise-introduction')
        self.commit(self.a, 'local.md', 'Research branch work\n')
        local_head = self.git(self.a, 'rev-parse', 'HEAD').stdout.strip()
        self.commit(self.b, 'remote.md', 'Team base update\n')
        self.git(self.b, 'push', 'origin', 'main')
        self.git(self.a, 'fetch', 'origin')
        remote_head = self.git(self.a, 'rev-parse', 'origin/main').stdout.strip()
        self.git(self.a, '-c', 'commit.gpgsign=false', 'merge', '--no-edit', 'origin/main')
        self.assertEqual((self.a/'local.md').read_text(), 'Research branch work\n')
        self.assertEqual((self.a/'remote.md').read_text(), 'Team base update\n')
        self.git(self.a, 'merge-base', '--is-ancestor', local_head, 'HEAD')
        self.git(self.a, 'merge-base', '--is-ancestor', remote_head, 'HEAD')
        self.assertEqual(self.git(self.a, 'status', '--porcelain').stdout, '')


if __name__ == '__main__':
    unittest.main()
