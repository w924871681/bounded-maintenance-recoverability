# Stage C 当前模型环境阻断复核

实际目标仓库：`D:\dt-talk\DT_LIFECYCLE_ESCALATION`。日期：2026-10-09。

**最终状态：BLOCKED。** Stage C 新执行器的 50/50 独立 synthetic tests 已通过，但实际 `prepare` 在当前模型环境冻结时退出 1。已核验的直接阻断是当前 approved Python 环境缺少 `psutil`、`river` 的 distribution metadata；只读目录盘点也未见两者的 package 目录。不能据 synthetic tests 通过宣布模型执行就绪。Stage C 的初始化/五方法最小组以及后续完整复核、Bootstrap 均未执行。

本复核只读取现有源码、执行记录、requirements 和已安装 package metadata，没有导入 Torch、river 或模型，没有安装/升级 package，没有重试 prepare 或实验，没有修改任何源码、配置、原结果或 Git。

## 1. 实际失败链

**VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_prepare_observed_failure.json`，`exit_code` 第 8 行为 1，`completed_tool_chunk_id` 第 7 行为 `7f221e`，`exec_session_id` 为 47643；`source_of_observation` 第 5 行明确说明该记录从已结束工具输出转录，不是第二次执行。`exception_type/exception_message` 记录 `ProvenanceError: required scientific packages missing from frozen distribution metadata`。此文件保留实际命令和 observed stack。

直接源代码链（均为新执行器，不是原 frozen runner 的改写）：

| 判定 | 完整路径、函数与行号 | 实际行为与影响 |
| --- | --- | --- |
| VERIFIED | `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\executor_driver.py`，`run`，341 | prepare 进入 `freeze_provenance`，尚未 dispatch 任何模型 worker。 |
| VERIFIED | `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\provenance.py`，`freeze_provenance`，346 | 调用只读 `capture_model_environment`，没有 import 科学包或模型。 |
| VERIFIED | 同一完整 `provenance.py` 路径，`capture_model_environment`，269–270 | 从 site-packages 的 `.dist-info/METADATA` 读取 name/version，要求 numpy、torch、pandas、psutil、river、scipy、scikit-learn 全部在 metadata 集合中；当前集合不满足要求，立即 fail closed。 |
| VERIFIED | 同一完整 `provenance.py` 路径，`_assert`，132 | 抛出 `ProvenanceError`。 |
| VERIFIED | 同一完整 `provenance.py` 路径，`freeze_provenance`，371 | `publish_json(..., 'provenance_manifest.json', ...)` 位于上述失败之后，因此本 attempt 没有发布模型环境 manifest。 |

`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_prepare_attempt01.log` 的第 26 行保存 `completed=12529,total=12529`。该日志只捕获 stdout 的哈希进度；原 stderr traceback 已由上述 observed-failure JSON 保存，不把 stdout 日志误称为完整 stderr 记录。12529 项哈希完成不能证明模型依赖齐备或模型执行成功。

## 2. 当前依赖盘点与原 source 的实际要求

盘点范围仅为 approved interpreter 的：

`C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages`

**VERIFIED（metadata，不是实际库导入测试）**：读取该目录全部现有 `.dist-info/METADATA` 的 `Name/Version`，numpy、torch、pandas、scipy、scikit-learn 存在；未发现 `Name: psutil` 或 `Name: river`，也未发现同名 package/dist-info 目录。未改用其他 Python 路径或其他论文环境兜底。

| 依赖 | 当前 metadata 版本 | 文件与行号 | 冻结 requirements 对应 |
| --- | --- | --- | --- |
| numpy | 2.4.6 | `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\numpy-2.4.6.dist-info\METADATA`，2–3 | `D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\requirements_frozen.txt`，17 |
| torch | 2.5.1+cu121 | `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\torch-2.5.1+cu121.dist-info\METADATA`，2–3 | 同一完整 requirements 路径，32 |
| pandas | 3.0.5 | `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\pandas-3.0.5.dist-info\METADATA`，2–3 | 同一完整 requirements 路径，19 |
| scipy | 1.17.1 | `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\scipy-1.17.1.dist-info\METADATA`，2–3 | 同一完整 requirements 路径，28 |
| scikit-learn | 1.9.0 | `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\scikit_learn-1.9.0.dist-info\METADATA`，2–3 | 同一完整 requirements 路径，27 |
| psutil | NOT_PRESENT_IN_APPROVED_DISTRIBUTION_METADATA | 上述 approved site-packages 只读完整 metadata/目录盘点；实际 prepare 第270行拒绝 | requirements_frozen.txt 没有 psutil 条目 |
| river | NOT_PRESENT_IN_APPROVED_DISTRIBUTION_METADATA | 上述 approved site-packages 只读完整 metadata/目录盘点；实际 prepare 第270行拒绝 | requirements_frozen.txt 没有 river 条目 |

原科学 source 也确实依赖两者：

- **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py`，25 行 `import psutil`。虽新 adapter 不调用原 CLI/resource helper，加载原 runner 仍会执行该顶层 import；不能以 psutil 仅用于 resource query（852、854 行）为由忽略缺失依赖。
- **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py`，12 行 `from river.drift import ADWIN`；`D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7.py`，19–20 行 import river/ADWIN。即使某一 comparator 不调用 detector，原 helper/module 导入仍需该依赖。
- **VERIFIED**：冻结 requirements 没有为 psutil/river 指定版本；**NOT_VERIFIED**：原最终执行使用的准确两包版本及其他传递依赖。不能在没有历史证据时挑任意新版本并声称历史环境已经恢复。

## 3. Python/ABI 声明及其解释边界

**VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\environment.reviewed.json`，857–859 行绑定 interpreter 为 `C:\Users\92487\anaconda3\envs\rcf-dti-py311\python.exe`、Python 3.11.15；5 行保存 AMD64 machine。

**VERIFIED（仅 wheel 声明）**：

- `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\torch-2.5.1+cu121.dist-info\WHEEL`，4 行：`Tag: cp311-cp311-win_amd64`；其 METADATA 29 行 `Requires-Python: >=3.8.0`。
- `C:\Users\92487\anaconda3\envs\rcf-dti-py311\Lib\site-packages\numpy-2.4.6.dist-info\WHEEL`，4 行：`Tag: cp311-cp311-win_amd64`；其 METADATA 50 行 `Requires-Python: >=3.11`。

**INFERRED（限声明层面）**：当前 interpreter 的 Python/平台声明与上述两 wheel tags 相符。**NOT_VERIFIED**：实际 Torch native load、NumPy C-ABI 互操作、CUDA/cuDNN/driver 的当前可执行性、模型数值/初始化重复性。不能把 tag 相符当作这些运行事实已通过；本次停止前没有进行实际模型库/runtime query。

`D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\environment.json`，2–11 行另有 Python 3.11.15、Torch 2.5.1+cu121、CUDA 12.1、GPU 与 cuDNN flags 的存量记录。**VERIFIED**：文件中保存这些字段。**NOT_VERIFIED**：该早期环境记录是否完整、是否足以唯一绑定实际最终 P7.7 环境；它未列 psutil/river 版本，不能补足本次缺失的历史信息。

## 4. 已完成与未完成的科学证据

| 阶段/声明 | 判定 | 证据与边界 |
| --- | --- | --- |
| 新 Stage C synthetic methods | VERIFIED | `D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7_integrity_replication_batch20_v1\stage_c_tests\attempt001\results.json`，3、7、61 行：all_pass=true，50/50；不是模型性能结果。 |
| 此测试结束时原 2535 文件、1200 CSV/1200 receipts | VERIFIED | 同一 results.json，46–54 行；original_integrity_end.json 保存错误列表为空与原字节不变。 |
| 实际模型环境 prepare | VERIFIED: FAILED | observed-failure JSON；exit1，缺 required distribution metadata。 |
| 新模型环境 manifest/初始证书/raw/workers | VERIFIED: NOT_CREATED_BY_THIS_ATTEMPT | 对授权新 results 根进行只读文件盘点：只有授权文档与 stage_c_tests 目录；provenance_manifest.json、initial_state_manifest.json、raw、workers 不存在。此判断不是权限拒绝；相应父目录可读取。 |
| Stage C warm-up/原模型/优化器、新轨迹、Bootstrap | VERIFIED: NOT_EXECUTED | observed-failure JSON 的 warmup/model/new_trajectories/new_bootstrap 字段及失败发生在 dispatch 之前的源码链；未进入 C/D/E。 |
| 完整模型依赖历史复现、R2/R3、240 组科学配对及纠正后性能/CI | NOT_VERIFIED | 本次环境 gate 阻断，不能用 Stage A/B 或 synthetic tests 替代这些尚未执行的科学事实。 |

## 5. 处置边界

保留 Stage A/B 与 50-test 通过记录，同时记录模型执行 **BLOCKED**。本次不安装包、不从远程获取源码、不创建或切换另一个 Python 环境、不修改 requirements，也不重试模型阶段。

下一步需要研究者明确决定独立环境核验/补全方式，并先只读追踪 psutil/river 的历史版本与依赖证据。若授权补全当前环境或选用另一独立环境，必须重新冻结该模型环境、传递依赖/native 文件及实际 runtime metadata，重新检查与 Stage B 固定 F1/NumPy/interpreter bindings 的关系；不能覆盖 Stage B 已完成的 input-only manifest。另一环境也不得冒称已经恢复原历史环境。

以下动作不应自动执行：删除缺失依赖 gate；以 dummy/stub modules 伪造 psutil/river；改写原 runner/helper 顶层 imports；安装未经核验的任意版本；为了通过 gate 改动原 seed、模型、阈值、维护预算、source checkpoint 或数据生成；直接进入 warm-up、final-heldout、Bootstrap。环境修复方案不得按预期性能或显著性改善方向选择。

## 6. 关键证据 SHA256

| 完整路径 | SHA256 |
| --- | --- |
| `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_prepare_observed_failure.json` | 484486fa2d2af651d1d2d03f6533f8ab55cfd2f3bebcbed72560add47e7bf421 |
| `D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_prepare_attempt01.log` | 2dda25fbe44a2ddc46d72e07b3d8cd2f14e25f9f2bde8ee623a57a967a2c7f83 |
| `D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\requirements_frozen.txt` | aa7f267400111ffcd3a2b4d501557150a8130abe61c83a36ffc6ccdff96a37f4 |
| `D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\environment.json` | 62032b84e25bd8284352a3db87091c54b8209232092f1fc212f9af782d5de015 |
| `D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7_integrity_replication_batch20_v1\stage_c_tests\attempt001\results.json` | 005cd0fb6c157420afff0409f7b85a73a3c797c00a7390852c0f71e1f3420dbc |
