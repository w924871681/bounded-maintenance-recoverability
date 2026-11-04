# 估计器从源码复现

本入口正在全量验收。输入检查和可迁移性检查已通过，不代表模型训练、交叉验证或论文整体结果已经通过。

按本包环境说明安装 `requirements.txt` 后，在本包目录执行，输出目录必须是尚不存在的独立目录：

```powershell
python -B reproduce_estimators.py --mode preflight --output ..\estimator_input_check
python -B reproduce_estimators.py --mode full --output ..\estimator_full_run
```

`full` 默认在输出目录内从原实现训练所需的11个源模型身份，然后逐阶段执行：P6的360条轨迹生成、五折交叉验证、原测试、最终拟合及比较；P7.6B的432条Fit轨迹、原OOF拟合与冻结、Validation开放门槛、432条Validation轨迹、原统计和最终比较。每个阶段单独进程运行，失败后保存证据并停止，不能跳过门槛。

论文原科学源码、种子、数据划分和判据保持原样。运行副本位于输出目录；Git的文件登记操作由检查实际文件字节的SHA256封存记录替代，并明确记录为可迁移来源身份。完整轨迹串行执行，保留原CUDA、数据类型、确定性设置和线程配置。记录中的原引用模型只用于比较；源模型新训练参数必须与其精确一致后才能供后续使用。

`--source-runs EXTERNAL R3 MSA` 是可选的本轮已完成训练复用入口。它重新核对训练回执、新模型文件SHA和全部参数，只接受已通过的三个训练目录。审稿人不需要作者的这些目录，默认命令自带训练过程。最终包还需进行新生成模型到1200条生命周期及论文表图的完整衔接验收；本入口的成功回执不替代该验收，也不代表NAS/C1/pi50选择过程已经重新执行。

查看输出的 `PROGRESS.json`、`stages`、`RECEIPT.json` 和 `FAILURE_*.json` 判断真实进度。已有目录拒绝重用，避免覆盖先前结果或混淆失败证据。
