import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def python_run(skill, helper, *arguments):
    return subprocess.run([sys.executable, '-B', str(ROOT/'skills'/skill/'scripts'/helper),
                           *map(str, arguments)], capture_output=True, text=True, timeout=30)

class HelperTests(unittest.TestCase):
    def test_math_scalar_and_source_helpers(self):
        result = python_run('audit-tex-math', 'math_check.py', 'numeric-eq',
                            '--lhs', 'x**2', '--rhs', '4', '--values', '{"x":2}')
        self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as root:
            source = Path(root)/'paper.tex'
            source.write_text(r'\section{Model}'+'\n'+r'\begin{equation}\label{eq:a} x=2. \end{equation}'+'\n')
            result = python_run('audit-tex-math', 'extract_tex_math.py', source, '--format', 'json')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('eq:a', result.stdout)
            json.loads(result.stdout)
            result = python_run('audit-tex-math', 'proof_obligation_index.py', source, '--format', 'json')
            self.assertEqual(result.returncode, 0, result.stderr)
            json.loads(result.stdout)
            result = python_run('audit-tex-math', 'tex_line_context.py', source, '--label', 'eq:a', '--window', '1')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('x=2', result.stdout)

    def test_prose_and_layout_checkers(self):
        with tempfile.TemporaryDirectory() as root:
            source = Path(root)/'prose.md'
            source.write_text('The sample contains ten firms. Each firm chooses a price.\n')
            result = python_run('ai-slop-lint', 'ai_slop_lint.py', source, '--format', 'json')
            self.assertEqual(result.returncode, 0, result.stderr)
            json.loads(result.stdout)
            tex = Path(root)/'note.tex'
            tex.write_text(r'\documentclass{article}\begin{document}A note.\end{document}')
            result = python_run('academic-draft-review', 'check_short_note_format.py', tex, '--format', 'json')
            self.assertIn(result.returncode, [0, 1])
            json.loads(result.stdout)

    def test_overleaf_guard_refuses_wrong_remote_without_fetching(self):
        with tempfile.TemporaryDirectory() as root:
            subprocess.run(['git', 'init', '-q', root], check=True)
            subprocess.run(['git', '-C', root, 'remote', 'add', 'origin',
                            'https://example.invalid/not-overleaf.git'], check=True)
            result = subprocess.run(['bash', str(ROOT/'skills/overleaf-sync/scripts/overleaf_preflight.sh'), root, 'main'],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 3)
            self.assertIn('not an Overleaf', result.stderr)

    def test_read_only_tool_help(self):
        for skill, helper in [('gh-local-first', 'audit_actions_usage.py'),
                              ('agent-handoff', 'catchup.py'),
                              ('remarkable-move-render', 'render_move.py')]:
            result = python_run(skill, helper, '--help')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('usage:', result.stdout)

if __name__ == '__main__':
    unittest.main()
