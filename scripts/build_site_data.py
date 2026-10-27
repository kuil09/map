#!/usr/bin/env python3
"""Stage exact canonical site JSON; never deploy or modify a Site checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from validate import ROOT, validate
from build_category_presentation import write as write_category_presentation, write_public, public_projection


def build(out, root=ROOT):
    out = Path(out).resolve()
    # Prevent accidentally overwriting canonical source or historical evidence.
    if out == root or any(out == root / d or root / d in out.parents for d in ('data', 'docs', 'scripts', 'tests', 'schemas', 'exports')):
        raise ValueError('Output must be a staging directory, not repository input/evidence.')
    if any((out / name).exists() for name in ('index.html', 'app.js', '.git')):
        raise ValueError('Refusing a Site/document-root checkout; use a fresh staging directory.')
    validate(root)
    out.mkdir(parents=True, exist_ok=True)
    inputs = write_public(out, root)
    for name in ('photos.json',):
        source = root / 'data' / name
        dest = out / name
        shutil.copyfile(source, dest)
        inputs.append({'file': name, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(), 'bytes': dest.stat().st_size})
    # Classification is derived from the same canonical identity/hash-checked contract as the map.
    inputs.append(write_category_presentation(out, root))
    head = None
    dirty = None
    try:
        top = subprocess.check_output(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL, text=True).strip()
        if Path(top).resolve() == root.resolve():
            head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
            dirty = bool(subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=all', '--', 'data'], stderr=subprocess.DEVNULL, text=True).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    archive, public, policy = public_projection(root)
    manifest = {'canonicalRepository':'https://github.com/kuil09/map','canonicalCommit':head if dirty is False else None,'canonicalHead':head,'canonicalWorkingTreeDirty':dirty,'projection':{'canonicalArchivePlaces':len(archive),'publicPlaces':len(public),'excludedPlaces':len(policy['excludedPlaceIds']),'policyPath':'data/map/public-exclusions.json'},'provenanceRule':'Places and research are explicit public projections; canonical archive data remain unchanged. Input hashes identify the staged bytes. canonicalCommit is set only for a clean data working tree in this repository.','snapshotRelease':json.loads((root/'data/metadata.json').read_text())['snapshotRelease'],'inputs':inputs,'photoBinariesCopied':False,'deployed':False}
    (out / 'canonical-input-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.out), ensure_ascii=False, indent=2))
