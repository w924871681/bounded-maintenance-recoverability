# Stage C 新执行器静态交叉审查

审查日期：2026-10-09。实际仓库：`D:\dt-talk\DT_LIFECYCLE_ESCALATION`。

**实际执行状态：BLOCKED（模型环境）。** 下文静态审查与 50/50 synthetic tests 结论仍成立；实际 Stage C prepare 退出 1，因为 approved 环境缺 psutil/river distribution metadata。未发布模型环境 manifest，没有 warm-up、模型轨迹或 Bootstrap。直接失败记录：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_prepare_observed_failure.json`；独立复核：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_environment_blocker_review.md`。不能将本静态报告理解为实际模型执行已经就绪。

本记录报告源码静态审查、AST 语法检查及只读复核主协调者实际执行的独立测试证据。本审查者没有执行 canonical input loader、生成器、warm-up、模型、最终轨迹、测试或统计。Stage C synthetic tests 由主协调者执行；本记录不以测试通过冒称初始状态通过或实验完成。

## 审查范围与当前结论

**VERIFIED（静态）**：新执行器通过已发布 RUN003 的 F1 文件提供固定输入，保持原 `run_one` 代码对象，隔离三个必要的全局回调，并对实际初始化、部署可行集合、24 阶段输入和离线访问留存证据。没有发现需要改变原方法或科学定义才能排除的静态问题。

**VERIFIED（已读取真实测试产物）**：Stage C attempt001 实际执行 50/50 synthetic methods，零 error/failure/skip；实现开始/结束 SHA 库存一致；原 2535 文件以及 1200 raw CSV/1200 receipts 字节不变。完整证据与哈希列在下文。

**NOT_VERIFIED（本报告完成时）**：60 个初始状态参考、五方法最小组实际配对、完整 1200 轨迹以及当前模型运行环境的实际可执行性。不能依据静态审查或 synthetic tests 宣布 R2/R3 通过。

此报告是下列源码字节的审查快照；之后若实现变化，必须以新的全量独立测试库存和冻结 manifest 为准，不能继续引用旧快照为新源码背书。

| 新文件（均位于 `verification/paper3_canonical_inputs/replication_executor_batch20_v1/`） | 本次审查 SHA256 |
| --- | --- |
| executor_driver.py | bf5fce13949279934e04102119b6fd39a9daa3d0dce169b140953ac271191ee4 |
| executor_worker.py | c036bec2058826f50c65deaec62820239a8aceb29655ca65aee03d63d8ef77c7 |
| fixed_inputs.py | 9078dd2376f970678482e67570f8575f37cf0c6c002f8e06a30188efe5c8f04c |
| provenance.py | af5434d3d1728d2b8eaefd373ef22cffcdc6e762fd79df4b85719744731c4df9 |
| science_adapter.py | 7b97c557814265ee23f8c4b105ba69d9ecdc1cf6ffe049297bd93cfebd3197c6 |
| test_fixed_inputs.py | c0b9b23bff85d695fa48c87e4eed9c4fdfe4a663e51a13b91a1e73ead5587c66 |
| tests/test_provenance.py | a727165017fab2278f69833e32de7f57d84395f1a02292504a7c1eae934f0b49 |
| tests/test_science_adapter.py | 6f2dbf6979358992f51763c5eeaea3315b6bb676b06328c51d167f2eb6325b15 |
| tests/test_executor_worker.py | 230d8389eb1e5966106a4500c9bddeef16582d7b7bf409a1fce78098eced5932 |
| tests/test_executor_driver.py | d29ebb24a807de3ecb38d7c9c3f97a2270d1e12456a920f57507288252d9d866 |

## 原方法及数学语义保持

1. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\science_adapter.py`，`_runner`，151 行：读取并编译已绑定原文件，比较 `run_one` 和 `initial_model` 的代码对象；`isolated_frozen_call`，246 行：复制原 globals，仅允许 `timeline_for_v2`、`scenario_hash_v2`、`initial_model` 三项回调，原 globals 与原代码对象保持不变。没有改写 gate、候选比较、适配预算、成本、seed 或动作提交公式。

2. **VERIFIED**：同文件，`_bank_audit`，265 行：比较实际 11 身份的九项元数据、实际 checkpoint 文件 SHA256、原冻结 resource limits、可行 mask/IDs 和排除 incumbent 的初始候选列表。`run_task`，412 行及 `audited_initial`，448 行：当前方法的原初始化 hash 必须等于独立预先记录的中心/seed hash，失败发生在第一项生命周期决策之前。预先测得一个 hash 不能代替五方法实际初始化核验。

3. **VERIFIED**：同文件，481 行的 `frame = adapted(...)` 调用原函数，随后逐阶段核验输入 hash、初始 hash、tier、bank、decision time、50-update 预算、P7.7 的 A1 严格零边界和 ratio10。514 行开始核验 timeline 无违规、24 阶段完整且最后已完成 service。代码检查本身不能证明尚未运行的任务通过。

## 固定输入与时间顺序

4. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\fixed_inputs.py`，`FixedInputStore.__init__`，185 行：每 worker 一次验证 Stage B 发布图；`_verify_bundle`，209 行：固定 F1、原 batch20 候选的 definition/dependency digest 和已选 bundle digest，重算完整 fingerprint 库存；`load`，273 行：每次只重核所选 center/scenario 的 NPY/JSON 字节、dtype/shape、raw/feature legacy digest、全部 72 roles 及 warm-up/reference。没有重新生成输入。

5. **VERIFIED**：同文件，332–333 行：原 data/container 模块导入前调用 `require_authorized_execution`；原 `BaseCenter` 与 `CausalTimeline` 仅在实际 load 时导入，导入来源必须为目标仓库。模型逻辑不在此 loader 中。原 timeline 对数组的复制和 `_segment` 返回独立副本保留。

6. **VERIFIED**：同文件，`decision_data` 446 行、`seal_decision` 463 行、`service` 471 行：执行顺序受状态机约束，stage1–24 依次读取当前 update/assessment、seal、当前 service。初始 `_segment((800,1000),'assessment')` 和 warm-up 保留原角色与原边界；不将本阶段 service 提前提供给在线决策。

7. **VERIFIED**：原 `D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7.py`，`offline_labels` 219 行实际会在 commit/service 后再次读取当前 decision data，并读取最多当前到当前+3 的 future service。新 `fixed_inputs.py`，`_diagnostic_stage` 397 行与 `offline_service` 480 行，仅允许已绑定原函数真实调用帧、当前 seal 和 service 已完成、原 horizon 范围；每次都记录为 `offline_oracle_after_commit`。因此应准确报告存在 post-commit offline oracle 诊断，不能把它写成“程序从不读取未来 service”。本守卫加冻结源码审查支持隔离判断，不声称 Python private 属性构成 OS 沙箱。

## 随机数与初始公平性边界

8. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\science_adapter.py`，`capture_rng_state` 311 行：记录实际已有 Torch CPU/CUDA 状态；正常路径不调用 manual_seed 或 set_rng_state。`restore_failed_task_rng` 仅允许绑定同一个未完成失败任务、同一 input/source/environment 和运行环境的已存状态，不能在方法间人为复制 RNG 以改善结果。

9. **VERIFIED（语义边界）**：原方法的 NumPy minibatch seed 与实际 Torch dropout RNG 是不同来源。新执行器声明固定输入调度不变，但不声明模型输出对 worker 数量不变。预先初始化在独立进程执行，不把额外的 60 次测量混入轨迹 worker RNG。**NOT_VERIFIED**：实际初始化是否完全重复、当前 GPU/runtime 是否出现数值差异，需已授权 Stage C 执行证据；失败时不能通过新 seed、阈值或参数修补论文结果。

## 发布、只读保护与调度

10. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\provenance.py`，`freeze_provenance` 308 行和 `verify_frozen` 409 行：绑定原保护快照、完整原 Python dependency closure、checkpoint bytes、F1 文件、新 executor、当前环境及授权记录。`_model_runtime_environment` 395 行另外冻结当前 CUDA/CUBLAS/MKL 等 runtime variables，不改写 Stage B 环境。`science_adapter.py` 的 `capture_scientific_runtime` 179 行只读取实际库/device、TF32/cuDNN/线程等设置；可能初始化 CUDA runtime，但没有模型、优化器或新 seed 操作。worker 与 driver 绑定实际 runtime receipt/hash/signature，并要求初始化参考与轨迹一致。当前环境冻结不等于恢复历史环境，外部 driver binary inventory 未验证时明确标记；记录保留 `historical_environment_reproduced=False`。

11. **VERIFIED**：同文件，`publish_bytes` 454 行：新 output 原子 hardlink 发布，目标存在则拒绝，保留失败 partial；516 行 write guard 限制 Python 可审计的写入/删除/重命名、拒绝 directory-FD 逃逸、symlink 及 subprocess；550 行 actual code-frame guard 禁止原生成、场景再物化及原 final CLI，允许原 `adapt/train_steps` 方法计算。580 行 import guard 在包代码运行前核 exact bytes。合法 hardlink 发布只允许新 output 内来源与目标；原始快照提供结束时完整性证据，可信 native dependency 的 OS IO 不被错误宣称为完全拦截。

12. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\executor_worker.py`，`_prepare` 76 行：先只读核 manifest，再安装写入/生成/import guards，随后才加入已绑定 repo/site 路径并检查科学授权 gate。`_existing_completed` 257 行：resume 必须核 task、完整科学 receipt、固定 24-stage hashes、初始证书、runtime signature、CSV/audit bytes；不能仅因 runner hash 相容就跳过配对检查。

13. **VERIFIED**：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\replication_executor_batch20_v1\executor_driver.py`，`accepted_records` 51 行、`paired_groups` 244 行：核新 receipts、对应保存的 F1 reference、初始化/runtime证书、原任务 RNG schema/config/environment/actual-state bytes、receipt alias、五方法全 24 阶段外生/初始/deployment 字段；分组不比较后续正常分化的 deployed state；phase gate 按完成和完整性推进，不按性能选择。旧 1200 记录不混入新主结果。原统计与 Bootstrap 不在此 driver 中执行。

## 静态审查发现并已在新执行器中排除的运行阻断

以下修订仅涉及尚未冻结的新执行器；没有更改任何原科学文件。

- **VERIFIED**：worker 在 `-I -S` 下原先缺少 repo import path，load 先于原 runner 的 root-path 初始化，可能找不到 `core.data`。新 worker 89–93 行只在 exact import guard 已安装后加入 manifest 绑定 repo 并检查授权。
- **VERIFIED**：minimal/full 原先使用同一个 `A0001`，可能碰撞独占 worker completion 文件。新 driver 272 行使用 `A_{PHASE}_0001`，request 与 CLI label 一致；没有放松独占发布保护。
- **VERIFIED**：新 provenance guard 显式拒绝 rename/link directory-FD，并禁止 symlink；合法新 partial hardlink 的清理只删除该新 output 名称，不修改其内容。

## 独立测试 launcher 与执行前门槛

新 launcher：`D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_test_launcher.py`。本快照静态盘点新 executor 共 **50** 测试方法：fixed inputs 10、provenance 9、science adapter 10、executor worker 11、executor driver 10。它们独立于已完成 Stage A 的原 42 方法。driver tests 使用碰到比较/转换即失败的性能 sentinel，核验固定矩阵/排序、240 groups、24-stage配对失败、固定最小组与完整余下1195任务推进；所有 provenance/dispatch/publication 都是内存 mock，没有真实模型或磁盘结果读写。

`main` 73 行要求 `-I -S -B`、不存在的专属 pycache prefix、approved interpreter/stdlib/NumPy byte bindings；actual core/imported/scripts/Torch/统计包禁止导入或执行。临时 fixtures 与所有结果只能写入新的 `results/p7_7_integrity_replication_batch20_v1/stage_c_tests/attempt001/`。`protected_check` 65 行在开始/结束时只哈希 2535 原保护文件，明确核 1200 raw CSV 和 1200 integrity receipts。`results.json` 包含 `all_pass`、实际方法库存与完整新实现 `implementation_sha256`；driver prepare 通过 `--test-attempt` 指定已执行的独立 attempt，要求实现与已测库存严格一致，否则重新执行新 executor 全测试；既有失败 attempt 不能覆盖。

主协调者已执行的命令（本审查者未执行）：

```powershell
& 'C:\Users\92487\anaconda3\envs\rcf-dti-py311\python.exe' -I -S -B -X 'pycache_prefix=D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7_integrity_replication_batch20_v1\stage_c_tests\attempt001\_never_created_pycache' 'D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\execution_20261009\stage_c_test_launcher.py' 1
```

## 已完成的独立测试证据

只读复核 `D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7_integrity_replication_batch20_v1\stage_c_tests\attempt001\results.json`，`all_pass` 3 行、`expected_methods` 7 行、`tests_run` 61 行：实际 50/50；`failures/errors/skipped` 均空，`implementation_unchanged_during_test` 为 true。`generator_executed/model_executed/statistics_executed` 均 false。这是 synthetic integrity test 的事实，不是任何模型性能结果。

- results.json SHA256：`005cd0fb6c157420afff0409f7b85a73a3c797c00a7390852c0f71e1f3420dbc`。
- method_inventory.json SHA256：`06ab0992f8175e78f9564ab51c203151fe20eb6a7f4a6e2dcbd6d58e4c5927bc`；它与 tests.log 保留全部实际方法及输出，位于同一 exclusive attempt001 目录。
- original_integrity_end.json SHA256：`3f9714100eebbc0c7bd245b41381a8bc0e62a509c3a7b67ee028e7c53901d438`；其 `all_original_bytes_unchanged=true`、`protected_files_checked=2535`、`original_csv_count=1200`、`original_receipt_count=1200`、`errors=[]`，不会因“结果数量正确”而替代原字节核验。
- 实际测试的全新实现 start/end 库存与本报告 SHA256 表一致；之后若有代码变化必须使用新 exclusive attempt 重测全部方法，不能继续使用此通过记录。

全部新 `.py` 已停止编辑；只有绑定这一通过库存且保持原文件不变后才冻结新 manifest，再进行授权的独立初始化、五方法最小配对 gate 和完整评估。若发现科学不一致，保留原始及新失败证据并停止，不能以新实现代码修订代替科学处置授权。
