"""Execute original P6 input gates and validate estimator provenance, without fitting.

This is an import/input check only. It never counts frozen estimator replay or
reference trajectory inspection as newly generated training evidence.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE / 'repository'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists() or out.is_relative_to(PACKAGE) or PACKAGE.is_relative_to(out):
        raise RuntimeError('Use a new output directory outside the package')
    out.mkdir(parents=True)
    identity = {'wrapper_sha256': sha(Path(__file__)), 'python': sys.version,
                'training_performed': False, 'full_estimator_acceptance': False}
    try:
        audit = read(PACKAGE / 'upstream_source_training/ESTIMATOR_RECIPE_AUDIT.json')
        for row in audit['source_bindings']:
            if sha(REPO / row['path']) != row['sha256']:
                raise RuntimeError('Frozen estimator implementation changed: ' + row['path'])
        identity['source_bindings'] = audit['source_bindings']
        freeze = read(REPO / 'audits/P6_ESTIMATOR_FREEZE.json')
        checked = []
        for rel, expected in freeze['files'].items():
            path = (REPO / rel).resolve()
            if not path.is_relative_to(REPO) or sha(path) != expected:
                raise RuntimeError('Original P6 frozen input mismatch: ' + rel)
            checked.append(rel)
        identity['p6_freeze_files_checked'] = checked
        for key in ('TEMP', 'TMP', 'MPLCONFIGDIR', 'TORCH_HOME', 'CUDA_CACHE_PATH'):
            cache = out / 'cache' / key
            cache.mkdir(parents=True, exist_ok=True)
            os.environ[key] = str(cache)
        os.environ['MPLBACKEND'] = 'Agg'
        sys.dont_write_bytecode = True
        library_roots = [Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()]
        sys.path[:] = [str(REPO), str(PACKAGE)] + [p for p in sys.path if p and any(
            Path(p).resolve().is_relative_to(root) for root in library_roots)]
        os.chdir(out)
        from retrain_external_sources import install_read_guard
        install_read_guard(out)
        # Keep the actual diagnosed OpenMP import order, without suppressing errors.
        import torch
        from scripts import run_p6
        from scripts import p7_6b_science
        _, config, candidates, folds, centers = run_p6.validate_preflight()
        for module in (run_p6, p7_6b_science):
            if not Path(module.__file__).resolve().is_relative_to(REPO):
                raise RuntimeError('Estimator import escaped the package')
        identity.update(status='PASS_ESTIMATOR_IMPORT_AND_ORIGINAL_P6_INPUT_GATES_ONLY',
                        torch=str(torch.__version__), p6_centers=len(centers),
                        p6_trajectories=len(centers)*len(config['model_seeds'])*len(config['scenarios']),
                        p6_folds=len(folds['folds']), p7_6b_protocol=audit['fit_protocol'])
        (out / 'RECEIPT.json').write_text(json.dumps(identity, indent=2), encoding='utf-8')
        print(json.dumps(identity), flush=True)
    except BaseException:
        identity.update(status='FAIL', traceback=traceback.format_exc())
        (out / 'FAILURE.json').write_text(json.dumps(identity, indent=2), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
