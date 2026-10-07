#!/usr/bin/env python3
"""Offline distribution validation; no network, credentials or agent-model calls."""
import ast
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE = {
    'personal-path': re.compile(r'/Users/(?!example(?:/|\b)|<)[\w.-]+/|/home/sfuchs/'),
    'private-network': re.compile(r'tail73d214|(?:192\.168\.86\.72|100\.114\.120\.81)'),
    'private-email': re.compile(r'(?i)(?:sfuchs\.de|Simon\.Fuchs)@|@atl\.frb\.org'),
    'token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)'),
    'credential-url': re.compile(r'https?://[^\s/<>]+:[^\s/<>]+@'),
}

def scan_text(text, label, failures):
    for rule, pattern in SENSITIVE.items():
        if pattern.search(text):
            failures.append(f'{label}: {rule}')

def main():
    failures = []
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    actual = set()
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if any(x in {'.git', '.local', '__pycache__', '.venv'} for x in rel.parts) or path.name == '.DS_Store':
            continue
        if path.is_symlink():
            failures.append(f'{rel}: symlink')
        if path.is_file() and path.name != 'MANIFEST.json':
            actual.add(rel.as_posix())
    if actual != set(manifest['files']):
        failures.append(f'Unexpected/missing files: {sorted(actual ^ set(manifest["files"]))}')
    links = 0
    for name, record in manifest['files'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name:
            failures.append(f'Unsafe manifest path: {name}')
            continue
        path = ROOT/relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != record['sha256'] or len(data) != record['size']:
            failures.append(f'{name}: changed distribution file')
        if len(data) >= 100_000_000:
            failures.append(f'{name}: exceeds GitHub regular-file size budget')
        if path.suffix in {'.pdf', '.png', '.jpg', '.jpeg', '.docx', '.xlsx', '.zip', '.pyc'}:
            failures.append(f'{name}: prohibited source/binary document')
        if path.suffix == '.sqlite':
            if not name.startswith('skills/corpus-econ-writing/references/library/'):
                failures.append(f'{name}: unapproved database')
                continue
            with sqlite3.connect(path.as_uri()+'?mode=ro', uri=True) as db:
                if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    failures.append(f'{name}: SQLite integrity')
                for line in db.iterdump():
                    scan_text(line, name, failures)
            continue
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            failures.append(f'{name}: unapproved binary')
            continue
        if name != 'scripts/validate.py':
            scan_text(text, name, failures)
        if path.suffix == '.py':
            try:
                ast.parse(text)
            except SyntaxError as error:
                failures.append(f'{name}: syntax error line {error.lineno}')
        if path.suffix == '.md':
            stripped = re.sub(r'```.*?```', '', text, flags=re.S)
            for target in re.findall(r'\]\(([^)]+)\)', stripped):
                target = target.strip('<>')
                if urlsplit(target).scheme or target.startswith('#'):
                    continue
                candidate = (path.parent/unquote(target.split('#', 1)[0])).resolve()
                if not candidate.is_relative_to(ROOT) or not candidate.exists():
                    failures.append(f'{name}: missing/outside link {target}')
                links += 1
    names = []
    for path in sorted((ROOT/'skills').glob('*/SKILL.md')):
        text = path.read_text()
        fields = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not fields or not re.search(r'^description: .+', fields[1], re.M):
            failures.append(f'{path.parent.name}: invalid frontmatter')
            continue
        name = re.search(r'^name: ([a-z0-9-]+)$', fields[1], re.M)
        if not name or name[1] != path.parent.name or len(name[1]) > 64:
            failures.append(f'{path.parent.name}: invalid name')
        names.append(path.parent.name)
    result = {'skills': len(names), 'files': len(actual), 'markdown_links': links,
              'failures': sorted(set(failures)), 'network_used': False}
    print(json.dumps(result, indent=2))
    return bool(failures)

if __name__ == '__main__':
    sys.exit(main())
