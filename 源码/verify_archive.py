#!/usr/bin/env python3
"""Verify extracted package files against the included SHA-256 manifest."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys

root=Path(__file__).resolve().parent
manifest=root/'SHA256_MANIFEST.json'
try:
    records=json.loads(manifest.read_text(encoding='utf-8-sig'))['files']
    seen=set()
    for index,record in enumerate(records,1):
        name=record['path']
        parts=PurePosixPath(name)
        if not name or parts.is_absolute() or any(p in ('','.','..') or ':' in p for p in parts.parts) or name in seen:
            raise RuntimeError('Unsafe or duplicate manifest path: '+str(name))
        seen.add(name)
        path=(root/Path(*parts.parts)).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing or out-of-package file: '+name)
        digest=hashlib.sha256();size=0
        with path.open('rb') as stream:
            while chunk:=stream.read(1024*1024):
                digest.update(chunk);size+=len(chunk)
        if size!=record['bytes'] or digest.hexdigest()!=record['sha256']:
            raise RuntimeError('File size or SHA-256 mismatch: '+name)
        if index%2000==0:
            print(f'Checked {index}/{len(records)} files',flush=True)
    print(f'PASS: {len(records)} files match the included SHA-256 manifest.')
except Exception as error:
    print('FAIL:',error,file=sys.stderr)
    raise SystemExit(1)
