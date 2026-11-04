# Paper 3: reviewer reproduction package

This archive contains the paper PDF and LaTeX, code, frozen inputs and checkpoints, original trajectories, completed replay trajectories, numerical tables and figure materials. The archive also contains dependency versions and the original runtime specification.

## Requirements

- Windows x86-64, Python 3.11, and an NVIDIA GPU with a driver compatible with CUDA 12.1 for the lifecycle/model execution.
- Internet access for installing Python packages. Python, the operating system, NVIDIA drivers and package-installation wheels are not bundled in this archive.
- Sufficient disk space for a new Python environment and for any new experiment outputs. Outputs must be written outside the extracted source directory.

## Installation and file check

Extract the entire archive to a new directory. From its root, check every listed file using Python 3.11:

```powershell
py -3.11 .\verify_archive.py
```

Open PowerShell in `1_复现材料`. The setup script creates a new environment, installs PyTorch 2.5.1+cu121 from the official PyTorch index and installs the main requirements from PyPI:

```powershell
$py311 = (py -3.11 -c "import sys; print(sys.executable)")
& $py311 .\setup_environment.py --python $py311 --output ..\paper3_env
$envpy = (Resolve-Path ..\paper3_env\Scripts\python.exe).Path
& $envpy -m pip install -r .\requirements_核验环境锁定.txt
& $envpy -m pip check
& $envpy -B .\reproduce.py verify --output ..\paper3_verify
```

The version-lock file records the environment used for the non-training checks. The separate `环境历史版本` directory records the earlier published runtime specification; its absolute paths are historical identifiers. The wheel URL and SHA-256 are in `环境版本记录.json`.

## Recompute tables from saved outputs

From `1_复现材料`, the following command reads the 1,200 saved replay trajectories in `3_已完成重放轨迹` and writes statistics to a new folder; it does not retrain a model:

```powershell
& $envpy -B .\rebuild_statistics.py --matrix ..\3_已完成重放轨迹 --output ..\paper3_replay_statistics
& $envpy -B .\render_reproduced_figures.py --statistics ..\paper3_replay_statistics --output ..\paper3_figures
```

Compare the tables with `2_最终结果/statistics`. To reaggregate the archived original trajectories instead, use `rebuild_statistics.py --saved-results-check --output ..\paper3_original_statistics`. The original and replay timings describe different runs and can differ; scientific fields are compared separately from timing.

## Execute the lifecycle experiment

The following runs the full 20-center, 3-seed, 4-scenario, 5-method lifecycle matrix using the included frozen source models and estimators. It is computationally intensive and writes new results:

```powershell
& $envpy -B .\run_full_matrix.py --python $envpy --workers 1 --batches 120 --min-available-gib 2.5 --output ..\paper3_full
& $envpy -B .\rebuild_statistics.py --matrix ..\paper3_full --output ..\paper3_new_statistics
```

This replays recorded random states and is not a new unseen holdout or an independent random realization. The upstream source-model and estimator training entry points are included; their documented full, freshly trained end-to-end chain was not independently rerun as part of this packaging. Non-training source, input and environment checks passed, and saved-result statistics were reproduced. Hardware, drivers and freshly installed dependencies may affect execution and measured time.

Figure 1 is provided as the original PDF; the package contains data and generation code for Figures 2 and 3. See `1_复现材料/README.md` and `ESTIMATOR_REPRODUCTION.md` for further scope and commands.
