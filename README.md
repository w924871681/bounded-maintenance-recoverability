# Bounded Maintenance Recoverability for Selective Lifecycle Escalation of Digital-Twin Models

Third-paper source, frozen inputs, models, figures, saved outputs, and manuscript.

## Contents / 目录

- `源码/1_复现材料/`: runnable entry points, experimental and figure-generation source, frozen inputs, checkpoints, configurations, and dependency files.
- `输出结果/2_最终结果/`: numerical tables and figures from the completed replay.
- `输出结果/3_已完成重放轨迹/`: 1,200 completed replay trajectories and comparison records, stored as individual small files.
- Identical copies of these results remain under `源码/` because the original reproduction commands and integrity manifest use those relative paths.
- `源码/README_FOR_REVIEWERS.md`: detailed English instructions and verification scope; `源码/1_复现材料/README.md` provides Chinese instructions.
- `图/`: manuscript Figures 1–3 in PDF; `pdf/`: manuscript PDF; `LaTeX_Source.zip`: manuscript sources.

The `源码` directory retains the original relative paths required by the reproduction scripts and includes the archived original trajectories and source-integrity bindings. Figure 1 is the original figure PDF; the source and inputs to regenerate Figures 2 and 3 are included.

## Environment / 环境

Windows x86-64, Python 3.11, and an NVIDIA GPU with a driver compatible with CUDA 12.1 are needed for lifecycle/model execution. An internet connection is needed to install Python packages. Windows, Python, the GPU driver, and installation wheels are not bundled. The exact package versions used for the non-training checks are in `源码/1_复现材料/requirements_核验环境锁定.txt` and `环境版本记录.json`. Historical environment records are kept separately in `环境历史版本/`.

In PowerShell at the repository root (if `py` is unavailable, use the path to a Python 3.11 executable):

```powershell
py -3.11 .\源码\verify_archive.py
cd .\源码\1_复现材料
$py311 = (py -3.11 -c "import sys; print(sys.executable)")
& $py311 .\setup_environment.py --python $py311 --output ..\paper3_env
$envpy = (Resolve-Path ..\paper3_env\Scripts\python.exe).Path
& $envpy -m pip install -r .\requirements_核验环境锁定.txt
& $envpy -m pip check
& $envpy -B .\reproduce.py verify --output ..\paper3_verify
```

The verification command checks frozen inputs, source bindings, and the installed environment; it does not train a model. Use new output directories outside the source files.

## Check saved results / 核对已有结果

From `源码/1_复现材料`, after setting `$envpy` as above:

```powershell
& $envpy -B .\rebuild_statistics.py --matrix ..\3_已完成重放轨迹 --output ..\paper3_replay_statistics
& $envpy -B .\render_reproduced_figures.py --statistics ..\paper3_replay_statistics --output ..\paper3_figures
```

Compare the tables with `输出结果/2_最终结果/statistics` (identical copies are kept under `源码/2_最终结果/statistics`). Saved replay statistics were checked against the included tables. The full model-training-to-results chain was not independently rerun during packaging, and a new environment installation was not completed because downloading PyTorch stalled; these checks do not establish full end-to-end reproducibility on another machine. See the reviewer guide for lifecycle execution and scope.

The earlier repository's backup and historical material remain available in the existing `backup/`, `archives/` and other original directories; their paths and the existing release history are retained.
