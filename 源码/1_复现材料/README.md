# 第三篇：论文与复现材料

本包包含论文、LaTeX、代码、必要输入、冻结模型、已保存原始轨迹、统计结果和绘图材料。

## 环境

使用 Windows、Python 3.11 和兼容 CUDA 12.1 的 NVIDIA 驱动。主要依赖版本见 `requirements.txt`；实际核验环境的完整版本见 `环境版本记录.json`。首次安装依赖需要联网；Python、Windows 和驱动由使用者提供。

在本目录打开 PowerShell，将 Python 路径换为本机的 Python 3.11：

```powershell
python setup_environment.py --python C:\Python311\python.exe --output ..\paper3_env
..\paper3_env\Scripts\python.exe -B reproduce.py verify --output ..\paper3_verify
```

`verify` 检查冻结输入、源码绑定和环境，不训练模型。输出目录必须新建且与本包分离。

## 使用已保存结果

```powershell
..\paper3_env\Scripts\python.exe -B rebuild_statistics.py --saved-results-check --output ..\paper3_statistics
..\paper3_env\Scripts\python.exe -B render_reproduced_figures.py --statistics ..\paper3_statistics --output ..\paper3_figures
```

保存的 1,200 条轨迹和 12 张统计表可供核对；按保存结果重算统计不等于模型重训。图 1 保留原始 PDF，图 2、图 3 保留绘图代码及数据。

## 从模型运行

完整生命周期运行入口示例：

```powershell
..\paper3_env\Scripts\python.exe -B run_full_matrix.py --python ..\paper3_env\Scripts\python.exe --workers 1 --batches 120 --min-available-gib 2.5 --output ..\paper3_full
..\paper3_env\Scripts\python.exe -B rebuild_statistics.py --matrix ..\paper3_full --output ..\paper3_new_statistics
```

生命周期入口使用包内冻结源模型和估计器；上游模型和估计器入口及限制见 `ESTIMATOR_REPRODUCTION.md`、`upstream_source_training/EXTERNAL_SOURCE_REPRODUCTION.md` 和各脚本的 `--help`。不同机器的实际耗时不要求逐字节一致。

本次整理只核对和复用已有材料，没有重跑训练。主入口及上游来源、估计器的非训练检查通过；完整上游训练到生命周期结果的独立端到端执行未在本次整理中验证。旧文档中描述“正在运行”的文字属于历史状态，不作为当前进度。


## 复算已完成重放的结果

`2_最终结果` 中的重放统计及用时表对应 `3_已完成重放轨迹`。不重训模型，使用已保存轨迹复算：

```powershell
..\paper3_env\Scripts\python.exe -B rebuild_statistics.py --matrix ..\3_已完成重放轨迹 --output ..\paper3_replay_statistics
```

该操作读取已有 1,200 条轨迹，不重新运行生命周期实验。运行耗时受当时硬件和环境影响。

`环境历史版本` 保存原始发布环境的版本清单、锁文件和运行时规格；其中绝对路径仅为历史来源。`环境版本记录.json` 则记录本次整理检查时实际使用的环境，两者不应混为同一套环境。

## 使用核验环境的完整依赖版本

安装脚本先从 PyTorch 官方索引安装 CUDA 12.1 版本，再安装主要依赖。如需将其余依赖固定到本次核验环境，完成安装后可执行：

```powershell
..\paper3_env\Scripts\python.exe -m pip install -r requirements_核验环境锁定.txt
..\paper3_env\Scripts\python.exe -m pip check
```

锁定清单按本次核验时已安装且 pip check 通过的版本生成；没有在本次整理中新建环境进行完整重装验证。PyTorch wheel 的官方索引与 SHA-256 记录在 `环境版本记录.json`。

原始流程的固定哈希清单直接引用部分测试源码、协议文档及原始受保护结果。为避免来源核验缺文件，这些必需文件随包保留；它们不代表本次执行了测试或训练。
