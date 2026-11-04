# External PT-A57 and MeDeT source training

The original implementation was found in `new_exercise_revised`. The package
contains its 38 Python files, seven hash-bound frozen selection inputs, and
historical source manifest under `external_source_original`. Collection receipts
record original locations for provenance only; runtime resolves package-local
paths. Launch scripts, the historical preflight and source log are separately
preserved under `external_source_launch_evidence`.

From the package directory, use a new output directory outside the package:

```powershell
python -B retrain_external_sources.py --mode verify --output ../external_verify
python -B retrain_external_sources.py --mode preflight --output ../external_preflight
python -B retrain_external_sources.py --mode train --output ../external_training --device cuda --safe-mode gru-native
```

`verify` checks source/input/reference hashes and Python syntax only. `preflight`
checks imports and frozen inputs without optimization. `train` invokes the
unchanged full original builder (H=1 and H=4, 50 PT epochs and 400 MeDeT iterations),
then compares the two Paper3 H=1 checkpoint states with zero tolerance. H=4 is
trained by the original protocol but is outside this entrypoint's comparison.
Existing output directories are rejected; failure evidence is retained. Tensor
equality and checkpoint byte SHA are reported separately because torch archive
serialization includes the temporary checkpoint filename.

The launch defaults above match the preserved historical scripts. Exact original
interpreter/backend versions remain to be established. Runtime imports and frozen
input loading passed in the fresh Python 3.11 / torch 2.5.1+cu121 environment
(preflight002). Preflight001's Windows NUL-device guard failure is preserved;
the guard now recognizes the exact null-device name before path resolution.
Actual retraining is managed by the resource-gated parallel scheduler and is not yet verified.
The C1 bank and source-only pi50/selection artifacts are verified frozen inputs,
not claimed to have been regenerated here. This entrypoint does not cover the
other six imported MSA identities, three r3 identities, estimator, lifecycle
matrix, figures, or final package acceptance.
