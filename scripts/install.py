#!/usr/bin/env python3
"""Install selected packages without touching unrelated skills or credentials."""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLABORATION = {'coauthor-workflow', 'coauthor-github-workflow', 'overleaf-sync', 'gh-local-first',
                 'agent-handoff', 'organize-econ-research-project', 'build-asset-replication'}
WRITING_CORE = {'econ-writing-suite', 'econ-write', 'theory-writing-refinement', 'audit-tex-math',
                'academic-draft-review', 'render-mathdown-tex', 'referee-report', 'ai-slop-lint',
                'design-econ-seminar', 'map-theory-dependencies'}
DEPENDENCIES = {name: WRITING_CORE - {name} for name in WRITING_CORE}
DEPENDENCIES['ai-slop-lint'] |= {'stop-slop'}
DEPENDENCIES['coauthor-github-workflow'] = {'gh-local-first', 'agent-handoff',
                                          'organize-econ-research-project', 'build-asset-replication'}

def available():
    return {p.name for p in (ROOT/'skills').iterdir() if (p/'SKILL.md').is_file()}

def select(profile='all', skills=()):
    names = available()
    selected = set(skills) if skills else (
        COLLABORATION if profile == 'collaboration' else
        names - COLLABORATION if profile == 'writing' else names)
    unknown = selected - names
    if unknown:
        raise ValueError(f'Unknown skills: {sorted(unknown)}')
    queue = list(selected)
    while queue:
        for dependency in DEPENDENCIES.get(queue.pop(), set()) - selected:
            selected.add(dependency)
            queue.append(dependency)
    return sorted(selected)

def fingerprint(folder):
    if folder.is_symlink() or not folder.is_dir():
        return None
    result = {}
    for p in folder.rglob('*'):
        if p.is_symlink():
            return None
        if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store':
            result[p.relative_to(folder).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result

def verify_sources(names):
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())['files']
    for name in names:
        expected = {path.removeprefix(f'skills/{name}/'):record['sha256']
                    for path, record in manifest.items() if path.startswith(f'skills/{name}/')}
        if not expected or fingerprint(ROOT/'skills'/name) != expected:
            raise ValueError(f'{name}: source differs from the distribution manifest.')

def install(destination, names, replace=False, dry_run=False):
    verify_sources(names)
    destination = destination.expanduser().absolute()
    if destination == ROOT or destination.is_relative_to(ROOT):
        raise ValueError('Install outside the source repository.')
    changes = []
    for name in names:
        source, target = ROOT/'skills'/name, destination/name
        present = target.exists() or target.is_symlink()
        if present and fingerprint(source) == fingerprint(target):
            changes.append((name, 'unchanged'))
        elif present and not replace:
            raise ValueError(f'{name} differs; review it before choosing --replace.')
        else:
            changes.append((name, 'replace' if present else 'install'))
    if dry_run:
        return changes
    destination.mkdir(parents=True, exist_ok=True)
    backup = destination.parent/'skill-backups'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    with tempfile.TemporaryDirectory(prefix='.skill-install-', dir=destination.parent) as staging:
        staging = Path(staging)
        for name, action in changes:
            if action != 'unchanged':
                shutil.copytree(ROOT/'skills'/name, staging/name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        applied = []
        try:
            for name, action in changes:
                if action == 'unchanged':
                    continue
                target = destination/name
                if action == 'replace':
                    backup.mkdir(parents=True, exist_ok=True)
                    target.rename(backup/name)
                try:
                    (staging/name).rename(target)
                except BaseException:
                    if action == 'replace':
                        (backup/name).rename(target)
                    raise
                applied.append((name, action))
        except BaseException:
            for name, action in reversed(applied):
                shutil.rmtree(destination/name)
                if action == 'replace':
                    (backup/name).rename(destination/name)
            raise
    return changes

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=['codex', 'claude'], default='codex')
    parser.add_argument('--target-dir', type=Path)
    parser.add_argument('--profile', choices=['all', 'writing', 'collaboration'], default='all')
    parser.add_argument('--skill', action='append', default=[])
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.target_dir:
        target = args.target_dir
    elif args.agent == 'codex':
        target = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))/'skills'
    else:
        target = Path.home()/'.claude'/'skills'
    try:
        result = install(target, select(args.profile, args.skill), args.replace, args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps({'dry_run': args.dry_run, 'skills': dict(result)}, indent=2))

if __name__ == '__main__':
    main()
