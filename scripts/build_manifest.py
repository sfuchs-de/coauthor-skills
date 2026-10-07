#!/usr/bin/env python3
"""Refresh distribution hashes after reviewing intended changes; no source evidence reset."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def included(path):
    return path.is_file() and not any(x in {'.git', '.local', '__pycache__', '.venv'} for x in path.relative_to(ROOT).parts) and path.name != '.DS_Store' and path != ROOT/'MANIFEST.json'

def main():
    provenance_path = ROOT/'docs/packaging-provenance.json'
    provenance = json.loads(provenance_path.read_text())
    for entry in provenance['files']:
        if entry['disposition'] != 'excluded':
            path = ROOT/'skills'/entry['path']
            entry['package_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            if entry['package_sha256'] != entry['source_sha256']:
                entry['disposition'] = 'adapted-for-public-distribution'
    provenance_path.write_text(json.dumps(provenance, indent=2)+'\n')
    manifest = {'schema_version': 1, 'files': {}}
    for path in sorted(ROOT.rglob('*')):
        if included(path):
            if path.is_symlink():
                raise ValueError(f'Symlink: {path.relative_to(ROOT)}')
            data = path.read_bytes()
            manifest['files'][path.relative_to(ROOT).as_posix()] = {
                'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(f"Recorded {len(manifest['files'])} distribution files.")

if __name__ == '__main__':
    main()
