# Paper 3 — Canonical Input Verification Protocol Design

日期：2026-10-08（Asia/Shanghai）。工作区：D:\dt-talk。目标仓库：D:\dt-talk\DT_LIFECYCLE_ESCALATION。

方案 ID：PAPER3_CIV_DESIGN_V1。状态：**PLAN_ONLY / NOT_EXECUTED / REQUIRES_SEPARATE_AUTHORIZATION**。

本次仅创建此 Markdown，静态审核方案；没有执行生成器、项目导入、模型、warm-up、训练、候选适配、评估、Bootstrap 或新统计。所有拟议输出目录、manifest 和 verifier 均尚未创建。后续执行与本次设计授权分开。

## Material Passport

| 项目 | 状态 |
|---|---|
| 科学问题 | full-batch 与 singleton 是否产生同一人口及输入；已有记录能达到何种 canonical 对应性证据层级；调度／恢复怎样保持输入不变 |
| 范围 | 20 centers、四场景、24 stages 的输入／profile／资源元数据；已有记录的输入字段来源映射 |
| 验证状态 | 历史／当前源码静态核验 VERIFIED；本方案运行结果全部 NOT_VERIFIED |
| 输出 | 仅 D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_CANONICAL_INPUT_VERIFICATION_PLAN.md |
| 禁止转移的权限 | 本文件不是生成器、模型、统计、代码变更或实验执行授权 |

本方案使用 VERIFIED（直接源码／已有记录证据）、INFERRED（有依据的解释或建议）、NOT_VERIFIED（尚未直接核验／尚未执行）。PLANNED 是操作状态，不是通过结果。任何未来 PASS 须明确认证对象，不能由某一输入检查推导所有科学结论。

## 1. Verified Historical Context

### 1.1 精确历史版本与冻结文件

**VERIFIED：旧 runner / protocol 已再次纯内存复原并核对字节 SHA256，未落盘。**

| 对象及实际路径 | 旧 SHA256 | 证据、函数与行号 |
|---|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py（历史版本，51010 bytes） | 20c0a3546f5cff28dc0dccb3737bc27ee47d81b06fcb94f9fe294ca576e43ec5 | 旧 run_final_heldout:822 整批生成、823 建立 by_id、852 run_one(by_id[center],...)；历史原文与补丁链来自下面完整日志。旧行号不能链接到当前同名文件。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json（历史版本，12151 bytes） | 8785dc1ecf9e8123f47d786b880011774ed952daa56345b6f61e60361d15838d | 旧 data_seed:55、population:132–136、common randomness:147；日志:23875 完成两处 runner 绑定。 |
| 当前同名 runner | ced000f213f8fc9b52a859e683fc6d27dd04a268641c3d6024500f56c1c158fe | _run_final_task:486–493 singleton；run_final_heldout:879–880 的整批 by_id 未传给 :922 提交的 worker。 |
| 当前同名 final configuration | 6339a9247b984b497d1543198b3a7b7c0cfdf9c7bcfd1c52b47b62e17d2fd0df | :55 data_seed；:131–136 final population；:146–149 common exogenous randomness；:178、189 runner hash。 |

历史日志完整路径：

C:\Users\92487\.codex\sessions\2026\09\14\rollout-2026-09-14T21-27-11-01a0a019-a852-7350-813a-23a170fa191c.jsonl

使用的是该长期会话中的 **2026-10-03** 事件，且 payload 明确指向目标仓库。runner 的成功补丁链为 22278→22306→22360→22734→22826→23143→23177→23212→23294→23340→23374→23422→23822→23833→23840→23847；protocol 为 22285→22320→22380→22860→23150→23374→23408→23422→23450→23505→23531→23566→23735→23875。失败补丁不纳入。原历史文件哈希输出分别见 JSONL:23871、23885；serial→parallel diff 见 :24436，成功返回见 :24439。仅解析、在内存应用文本变换，没有执行历史工具指令。

VERIFIED：旧 run_one:235–313 与当前 runner:247–325 逐字相同；旧、新 protocol JSON 只差 /runner/runner_sha256 和 /source_bindings_sha256/scripts/run_p7_7_final.py。它证明方法内部函数／参数未因此改变，不能证明收到的 base 不变。详细取证见 D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SINGLE_GROUP_INTEGRITY_FORENSIC_REPORT.md:174–278。

### 1.2 “原始冻结协议要求 full-batch”的准确范围

- **VERIFIED：**冻结 JSON 指定完整有序人口 33000–33019、data_seed=7311、seeds=7311/7312/7313、C0/C1/C3/C4 和五方法；JSON **没有**独立 generation_mode / batch_size / seed_offset 字段。不能写成“JSON 本身显式冻结 full-batch”。
- **VERIFIED：**精确旧、实际运行绑定的 runner 第 822、823、852 行提供了 full-batch materialization 与同 center 共享 base 的执行语义。
- **INFERRED：**将“有序完整 20-center batch + 旧调用语义”作为恢复原设计的主要 canonical 候选最有依据。因此本方案预先选择该候选，不根据模型性能在两种上下文中择优。
- **NOT_VERIFIED：**完整历史 NumPy／二进制依赖／运行环境已全部复现、当前环境已数值重现旧 full-batch 输入。这必须通过后续输入验证及历史环境证据分层报告。

### 1.3 239 / 961 的两个不同计数对象

以下为已完成取证的记录来源，不是新增性能统计：

| cohort | 轨迹数 | 完整五方法组 | 不完整部分／范围 | 判定 |
|---|---:|---:|---|---|
| legacy serial | 239 | 47（235 trajectories） | 异常 (33003,7313,C4) 的四个 baseline；33000–33002 各 60，33003 为 59 | VERIFIED |
| singleton parallel | 961 | 192（960 trajectories） | 异常组的 P7.7；33004–33019 各 60，33003 为 1 | VERIFIED |
| 存量五方法输入配对组 | 239 组 | 47 legacy + 192 singleton | 不是“239 个旧 canonical 组” | VERIFIED |

证据：D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SINGLE_GROUP_INTEGRITY_FORENSIC_REPORT.md:259–278、313–344、414–418；D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw 下各 receipt:9–10 的 protocol_hash/runner_hash；资源调整文档完整路径为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\docs\P7_7_FINAL_HELDOUT_PARALLEL_RESOURCE_ADJUSTMENT_20261003.md:11–18、28–31。

VERIFIED：异常组 P7.7 为 tight，四 baseline 为 medium，全部 24-stage role hashes 和 initial hash 不同。其他 239 个组在已核字段上相互匹配。存量 20-center 类型 A7/B8/C5 与当前完整 full-batch 必有的 A6/B8/C6 不同。来源旧／新均**不是** canonical 数值对应性的充分条件；不能提前把 239 旧 trajectories 自动纳入，或把 961 新 trajectories 自动废弃。

### 1.4 Git 与证据基线

VERIFIED：目标 Git root=D:/dt-talk/DT_LIFECYCLE_ESCALATION，HEAD=436ee9960a32a8e94e571ded3fc800a2fa20f3e4，branch=main。查询使用 git --no-optional-locks -C D:\dt-talk\DT_LIFECYCLE_ESCALATION；未改变 index/HEAD/reflog 或 tracked 内容。既有 tracked modifications 为 core/p7.py、reports/P7_7_FINAL_LIFECYCLE_PROTOCOL.md 及其 .sha256、results/p7_6b/task_states/fit/32248_7312_C1.json 和 32248_7312_C3.json；必须保留。

下文 source hashes 的基线取实际工作树，不以 Git HEAD 替代最终冻结实现。前期 forensic 报告仍保留原样。交付前静态复核 24 项既有文件 SHA256 均未变化，原审计的 1201 项 output_hashes 全部匹配，HEAD 与上述 tracked modifications 状态保持；拟议验证输出目录和 verifier 均尚不存在。

## 2. Proposed Canonical Input Definition

### 2.1 候选命名与科学身份

拟议主候选：**P7_7_ORIGINAL_BATCH20_CANDIDATE_V1**。含义是恢复旧入口语义的输入候选，**不是已通过的历史完全复现**。

拟议验证协议：**P7_7_CANONICAL_INPUT_VERIFICATION_V1**。只有在研究者审阅授权、verifier 与 resolved environment 冻结后才能生成验证产物。

若研究者另选统一 singleton，应命名 **P7_7_UNIFIED_SINGLETON_NEW_PROTOCOL_V1** 或明确的新版本；它是新的生成协议／人口实现，不能冒称原始冻结协议或用其数值回写旧记录。此选择不得基于新 loss、CI、排名或改善预期。

### 2.2 主候选静态合同

| 项目 | 预先固定值／规则 | 源码依据及当前等级 |
|---|---|---|
| ordered centers | [33000,33001,...,33019]；一次完整调用，不能分块／重排序传入生成器 | final config:132；旧 runner:822–823，VERIFIED 执行语义 |
| data seed | 7311；不是循环中的模型 seed | final config:55；core/data.py:32、40，VERIFIED |
| n_history / base channels | 17000；12 telemetry +12 masks，即 base.x 24 列 | core/data.py:32、41、52；main_cfg.py:62，VERIFIED |
| drift override | A/B/C drift_prob=0.0 | core/data.py:42–43，VERIFIED |
| generation context | n_centers=20、seed_offset=33000×17=561000、start_center_id=33000、allowed_types 默认 [A,B,C] | core/data.py:44–48；sim.py:264、268–280，VERIFIED |
| global RNG initial seed | 7311+561000=568311；先 type schedule，随后逐 slot center RNG | sim.py:264、271–280，VERIFIED 静态关系 |
| ID mapping | ID=33000+local_id；33003 的 slot=3 | sim.py:279–280、320，VERIFIED |
| type schedule | default (3,4,3)，两个完整 10-center block，整个 full batch A6/B8/C6 | main_cfg.py:66；sim.py:54–63，VERIFIED 结构约束，不是已生成结果 |
| profiles / tier | 保留实际 dt、type、tier、全部 scenario 所需 metadata；不按有利条件重采样 | sim.py:282、319–347；main_cfg.py:196–209，VERIFIED 定义 |
| scenarios | C0/C1/C3/C4；generator_revision=p3_mismatch_v2_r3，固定 r3 config，onset raw index=6520 | core/p3_2_data.py:10、94–168；mismatch config:7、13–18、188–251，VERIFIED |
| features | float32 raw x 追加 dt/4 常量列，25 列 | core/data.py:26–28，VERIFIED |
| stages / slicing | 24，见第 4 节半开原始索引，不按物理 timestamp 直接当数组索引 | core/protocol.py:10–17，VERIFIED |
| model seed / method roles | 输入只有 20×4 个 center–scenario 实现；三 model seeds／五方法只引用同一实现，不重新生成 base | 输入函数无 method/model seed 参数；未来引用不变性 NOT_VERIFIED，需 gate |

上表缩写的全部源码路径为：

- D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\p3_mismatch_v2_frozen.json
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py

表格摘录不能替代完整源码／MainCfg bytes 绑定。任何额外参数、helper 或 import dependency 变化都须冻结为新候选版本；不能保持同 ID 却修改定义。

VERIFIED 的 shape/dtype 静态合同：base 与 raw scenario x 为 (17000,24) float32，y 为 (17000,) float32，ts 为 (17000,) int64；engineered features 为 (17000,25) float32。role x 为 (N,25) float32，y/ts 为 (N,) float32/int64，N 依次 400/240/400。依据为上述 core/data.py:26–28、41、52–61、p3_2_data.py:158–168、protocol.py:10–17、56–58。执行时 dtype.str／native endian 另绑定实际 resolved environment；不得偷偷 cast／换 endian 后宣称 legacy exact match。未来数组是否满足合同仍为 NOT_VERIFIED。

### 2.3 运行阶段边界（均未执行）

本方案拟分三种权限，不能相互推定：

1. **Input-only**：生成／读取 base、profile、场景数组、raw warm-up/reference 输入和 stage role digests；读取库／资源元数据并计算静态 feasibility；不产生模型结果。
2. **Initial-state verification**：另行授权后才可加载模型并按 canonical warm-up 50 steps 构造参数 hash，核验共同初始状态及运行确定性。
3. **Scientific evaluation / statistics**：必须再次明确授权并冻结独立实验／统计协议。Input-only PASS 不自动开放该阶段。

依据：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py，initial_model:31–33 会 load_identity 并 adapt(...,steps=50,seed=seed+center_id)；D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:258、294–296 会初始化、service evaluation 及 offline labels。**本验证不得调用 run_one、final runner CLI、initial_model、DecisionExecutor、adapt、predict、evaluate 或 oracle labels。**

## 3. Generator Dependency and RNG Audit

### 3.1 历史／当前依赖证据与缺口

| 结论 | 完整路径、函数／字段、行号、证据 | 等级 |
|---|---|---|
| batch 改变 RNG context | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py:36–48；D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py:59–63、264–280；相同 ID 不独立种子化。33003 singleton global seed=7311+33003×17=568362，slot=0。 | VERIFIED |
| tier 从中心 RNG/profile 派生 | 同 sim.py，_sample_budget_tier:30–33、simulate_centers:319；MainCfg BudgetCfg:204–208 条件概率。不是只由 type 或 ID 确定。 | VERIFIED |
| C1 / C3 / C4 依赖 metadata 与数组 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py，_physical_shift:84–100 使用 metric_gains/delays/dt；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py:13–81 使用 base_logit、base.y 等。须绑定完整 profile/metadata，而非仅 A/B/C。 | VERIFIED |
| 当前关键生成器在审阅 Git 节点／资源调整日志未见变化 | forensic 报告:257：core/data.py、sim.py、main_cfg.py 在 491231c、60f3589、436ee99 bytes 相同；Oct03 日志未见修改。旧 receipt 仅 implementation_hash 绑定 core/p7.py。 | VERIFIED 的查阅结果；完整历史依赖认证 NOT_VERIFIED |
| 有环境记录但非充分历史运行证明 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\environment.json:2–11 保存 Python 3.11.15／可执行路径／Torch-CUDA；没有 NumPy、timestamp、run_id 或与旧 receipt 的直接绑定。D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\requirements_frozen.txt:17 为 numpy==2.4.6。 | VERIFIED 文件内容；实际旧 phase 的完整环境同一性 NOT_VERIFIED |
| 不能直接运行旧 environment capture | D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\capture_environment.py:9、25–27 导入 torch 并覆盖 audits/environment.json 和 requirements_frozen.txt。 | VERIFIED；本阶段及未来 input-only 都不能用它覆盖原证据 |

### 3.2 后续执行前的依赖冻结清单

PLANNED / NOT_VERIFIED：研究者授权前需要审阅未来 verifier 的纯输入 import closure，绑定：

- Python executable 的路径、版本、字节 SHA；Python/NumPy distribution 元数据、安装位置、关键 NumPy RNG／array／ufunc 二进制文件摘要；OS/architecture/endian、CPU、数值库构建与线程配置。
- core/data.py、core/p3_2_data.py、core/protocol.py、core/common.py、imported/ravm_dt/main_cfg.py、sim.py，以及实际导入的 package __init__.py／其他 helper 的 bytes SHA。
- 完整 MainCfg 默认数据：MissingBlockCfg:40–53、SimDataCfg:57–129、BudgetCfg:196–209，及 core/data.py 覆盖后的 resolved data config；不要只记录几个摘录常量。
- 原／当前 final config 与 mismatch config 的 file SHA，精确旧 runner/protocol reconstruction SHA、当前 verifier SHA 与本计划 SHA；旧 runner 仅作语义证据，不作为 input-only 执行入口。
- native8/source3 manifest、ordered identity metadata、manifest 中的 expected checkpoint SHA、deployment limits 与静态可行全集。若要流式读取 .pt 文件 bytes 重新核 SHA，需后续授权明确涵盖该只读来源核验；否则实际 checkpoint bytes 的认证延至 initial-state/source 阶段。任何情况下都不能在 input-only 中反序列化、加载或执行模型。
- 实际加载位置、模块／可执行来源；禁止 editable package 的另一个项目同名模块阴影覆盖目标仓库来源。未知依赖要列明，不能写 presumed same。

当前不采集新的运行环境、不执行 pip、安装依赖或项目 imports。后续不得为得到更有利输入／损失自动升级、降级或轮换环境。不同环境可在另行预先授权、由历史来源依据驱动的诊断对照中比较；不能静默轮换到某环境恰好匹配后隐藏其余尝试，也不能按模型性能选择。更换任何绑定必须产生新候选版本和新独立验证记录。

### 3.3 两类摘要必须分开

VERIFIED：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\common.py 的 array_digest:22–29 按各数组顺序，先 np.ascontiguousarray，再写 str(shape).encode()、dtype.str.encode()、C 字节到 SHA256。canonical_hash:32–34 用 JSON sort_keys=True、separators=(",",":"),ensure_ascii=False。

- **legacy scenario_hash**：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py:166–168，array_digest(raw scenario x[24 columns], y, ts)。
- **legacy stage role hash**：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py:27–29，array_digest(segment feature x[25 columns], y, ts)；timeline_for_v2:161–163 先加 dt/4。
- **deployment_filter_hash**：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py:299–300，仅 canonical_hash(limits dict)，不绑定 bank 或完整 feasible IDs。
- **bank_hash**：同 p7.py:299 与 core/models.py:96–97，是有序 ModelIdentity.to_dict() 列表摘要，不能用 manifest 文件 SHA 替代。
- NPY 文件／JSON 文件的 byte SHA 与 legacy array_digest 不同，须分列保存；不能相互替代或归一化后冒称旧 hash 一致。

拟新增 schema-versioned input fingerprint 还要绑定 role、span、ID、context、feature definition、profile、bank/feasible metadata 与 dependency/config hashes。旧 digest 未显式绑定这些 context tags。新摘要仅补充 provenance，不替代旧算法。metadata 的非 JSON-native 值转换、浮点表示、dtype、endian、array order 和空值规则须在 verifier code review 时预先定版；不允许遇到 mismatch 后临时改变。

## 4. Input Verification Matrix

### 4.1 结果盲的执行设计

全部为 **PLANNED / NOT_VERIFIED**，只在另行授权后实施：

- F1/F2：两个 fresh process 在同一冻结 environment，各进行一次完整 ordered-20 full-batch materialization。
- S1/S2：独立 fresh process，各对 20 IDs 做 singleton 调用；S1 升序、S2 降序，每次 cfg/data_seed/n_history 相同。它们只用于机制对照，不作为自动替代 canonical 的候选。
- 必须 F1=F2、同 ID 的 S1=S2（全部预定 arrays/profile digests）；**不要求 F=S**。full-v-single 差异是调查结果，不是需要自动重采样“修好”的执行失败。
- 每 context 为 20 个 base、80 个 center–scenario 实现和 5760 个 stage-role summaries（20×4×24×3）。模型 seeds 仅是引用标签；不要把 3 种模型 seed 再传入 base generator。
- 只有冻结输入生成和元数据检查；不计算原／新 service loss、oracle labels、A1 预测、S_m、动作／门控收益、显著性、Bootstrap 或筛除统计。

拟议 verifier 只使用经静态审核的纯输入 helper／等效数组逻辑；不会 import final runner、core/models 或 core/p3_2_models。后者会导入 Torch，core/models.py:21–24 有全局设置，build_identity_bank:62–93 还调用 profile_arch；所以 metadata 从 JSON 字段白名单重建，不能为计数去 profiling 模型。bank 列表保留 native manifest 的 8 identities 原顺序，再追加 source manifest 的 3 assets 原顺序；每项只取 core/models.py:27–37 的九个 ModelIdentity 字段（identity_id、architecture_index、architecture、family、source_initialization_id、checkpoint、checkpoint_sha256、parameter_count、operation_count），不混入训练 loss 或其他附加字段。

| ID | 核验对象与规模 | 方法／必须保存字段 | 预先判据 | 证据依据及执行状态 |
|---|---|---|---|---|
| M0 | 历史 bytes、dependency/config/verifier/environment | 旧精确 SHA、实际加载路径、resolved config、授权 ID、import allowlist；源文件开始／结束 SHA | 旧 SHA 不符停止 historical claim；依赖未知只可在明确授权的 current-env 层执行 | §1、§3 直接证据 VERIFIED；runtime preflight NOT_VERIFIED |
| M1 | F1/F2 和 S1/S2 的 20-ID 完整性／重复性 | context、调用 ID 列表／n／offset／slot、seed、x/y/ts、profile、type/tier/dt；数组 shape/dtype/endian/finite flags | ID 唯一齐全、重复 context bitwise 完全相同；不以容差当 exact pass | core/data.py:31–65、sim.py:264–347；NOT_VERIFIED |
| M2 | 20 centers 的 full-v-single comparison | 按 ID 输出每字段 MATCH / MISMATCH / NOT_AVAILABLE；分别 base x/y/ts、完整 metadata、type/tier/dt、类型构成 | 20 个 ID 全覆盖，不按结果选择部分中心；不预先判定哪些必不同 | 同源码；NOT_VERIFIED |
| M3 | 每 context 80 scenario arrays | C0/C1/C3/C4 raw x/y/ts legacy scenario_hash；25-col engineered feature hash；scenario role/onset/config | 同 ID/scenario 绑定，源 base 摘要绑定，重复 context 一致 | p3_2_data.py:94–168、data.py:26–28；NOT_VERIFIED |
| M4 | 每 context 5760 stage-role entries | role、stage、raw half-open span、shape/dtype/ts endpoints、legacy segment digest、window length/count | 无 off-by-one、stage 1–24/三 role 齐全、bounds 合法，使用 features hash | protocol.py:10–42；NOT_VERIFIED |
| M5 | warm-up/reference 输入 | [0,800) 和 [800,1000) 的 raw/feature digests，各 scenario；**不算模型误差／参数** | 同 center 下预期四 scenario pre-onset inputs 相同，重复 context 一致 | protocol.py:60–61；final config:109；p3_2_data.py:10、102–142；NOT_VERIFIED |
| M6 | 11 身份 static resource universe | native8+source3 有序 metadata、limits、bank legacy hash、feasible Boolean mask、ordered feasible IDs、初始 incumbent 排除集 | tier 合法、两限制均应用、重复 identity 拒绝、库 hash 匹配；不加载 checkpoints 为模型 | models.py:62–97、156–157；p3_2_models.py:213–231；p7.py:178–195；NOT_VERIFIED |
| M7 | 1200 existing trajectories 的来源资格清单 | CSV/receipt file byte hashes，task fields，scenario/24-role hashes、type/tier/filter/bank、时间端点、stage1 identity/initial hash；只投影白名单 | 对 F/S 各独立比对，记录 EXACT / MISMATCH / NOT_RECORDED；不因 old/new 标签自动过关 | runner:440–479；forensic §3/§4；NOT_VERIFIED 的 canonical match |
| M8 | 1200 无模型 dispatch descriptors | ordered center/seed/scenario/method 引用 immutable bundle；workers=1/3；升序／反序／固定置换，读取后重新摘要 | 所有 descriptors 引用同 center/scenario fingerprint；schedule 后 exact hashes 不变；不运行模型 | 当前 worker:490 与 resume:896–958 的缺口；NOT_VERIFIED，未来 reader-only 验证 |
| M9 | initial-state gate（另阶段） | 已存 stage1 initial hash 的相等性可作元数据检查；new canonical initial 参数 hash 需 warm-up | Input-only 不生成此 PASS，状态为 NOT_VERIFIED / SEPARATE_AUTH_REQUIRED | core/p6.py:31–33；NOT_VERIFIED 的 canonical initialization |
| M10 | future resume / full-group parity gate | canonical definition/bundle ID、全部 dependency/config/bank/limits fingerprints、task/role bindings、initial-state certificate、outputs 和五方法组 parity | runner hash compatibility 仅来源信息；不得替代所有科学字段；gate 未过不启动模型 | runner:461–479；p7.py:299–300；NOT_VERIFIED，当前不修改入口 |

矩阵使用的 abbreviated source 的完整路径见第 2.2 节，另三个为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\models.py、D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_models.py、D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py；初始化路径为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py，runner 为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py。

### 4.2 Stage 摘要的纯数组定义

VERIFIED 静态定义，未来计算 NOT_VERIFIED。令 b_t=1400+(t−1)×640：

- update：t=1 时 [1000,1400)，否则 [b_t−400,b_t)；
- assessment：[b_t,b_t+240)；
- service：[b_t+240,b_t+640)。

raw counts 为 400/240/400；window=96 时 counts 为 304/144/304，仅长度算术，无需构造训练 tensor。stage24 的 service 为 [16360,16760)，不超过 17000；timestamp 是 sim.py:289 的 8+raw_index×dt，不要混用 raw index 与 physical time。

未来 input-only harness 在授权后对 scene arrays 加 feature_matrix，直接按 spans 取副本摘要。**不调用 seal_decision、service 或 offline_service，不伪造已提交决策，也不计算 service loss。** D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py:67–78 的生产 causal guard 保持原样。Verifier 对预生成 service 输入的离线读取只为已授权的输入完整性检查；这些数组不得被作为未来在线控制器的提前可见数据。

[800,1000) 的 200 点 reference 有 104 个 role-contained windows 是长度关系，不授权算 104 个 squared errors、S_m、estimator 输出或 reset state。

### 4.3 静态部署约束与正常方法分化

VERIFIED：D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\p3_mismatch_v2_frozen.json:261–274 的 tight/medium/loose 上限为 (30000,1500000)/(100000,5000000)/(500000,20000000)。D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\models.py:156–157 同时判参数与 operations。

Input-only 需比较共同有序 bank、资源可行全集及初始 msa_a57_pt 排除后的候选集合。**不能要求后续 actual candidate_count／selected identity／deployed state 恒等**：D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py:178–195 排除当前 identity，gate 与 RI 后身份不同可合法改变实际搜索。同资源 universe 才是外生 parity 义务。

### 4.4 调度／resume 不变性的未来检查

PLANNED / NOT_VERIFIED：

1. 在提交任何方法任务前一次 materialize 并冻结输入 bundle；worker 只按 ID 加载已固定数组，不重新调用 generate_base_centers，不以 worker index、task order、resume count 或模型 seed 修改数据。
2. 明确 immutable registry：center ID→base fingerprint，center/scenario→scene+role fingerprints；1200 task descriptors 只引用该 registry。
3. Reader-only dispatch 测试 workers={1,3} × orders={原 canonical task 顺序、反序、固定置换 q_i=(7i) mod 1200，i=0,...,1199}。置换无 RNG、无新增科学种子；gcd(7,1200)=1。逐 descriptor load/copy 后 hash，完整文件名唯一，无任何模型执行。
4. 用副本模拟 incomplete descriptor receipts 的 interrupted/resume 元数据流程（不触碰原 claims）：同一 immutable input manifest、五方法组一致、24 role entries 完整才可恢复；缺失拒绝，不用旧 runner allowlist 免检。
5. future experiment resume 在 M10 通过且 M9 初始状态已另行认证后才允许 model execution。每个输出还须绑定其输入 ID/hash 与组证书；随任务调度只允许时间／process metadata 改变。
6. 生成与阶段摘要先完成后封存，再为线上程序提供分阶段接口；reader dispatch 通过不证明线上 causal access 已实现，后续实验入口仍需独立静态／运行审核。

## 5. Planned Outputs and Hash Bindings

### 5.1 独立位置（拟议，不创建）

唯一当前交付为本 Markdown。未来 input-only 如获授权，拟定输出根：

D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\P7_7_CANONICAL_INPUT_VERIFICATION_V1\<run_id>\

run_id 用预先分配的不可复用 ID，不依据模型结果命名。父目录及真实 resolved path 须确认不在 results/p7_7、不通过 junction/symlink 指向任何冻结记录；目录已存在或内容碰撞即停止，不能覆盖／清空。本阶段不 mkdir，不写以下任何文件。未来 verifier 的拟议源码位置为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\verification\paper3_canonical_inputs\verifier_v1\verify_inputs.py（未创建）；先另行授权实现和静态审核，freeze SHA 后才申请 input-only 执行。

| 拟议文件／目录（相对于上方完整新根） | 内容／绑定 | 当前状态 |
|---|---|---|
| authorization_manifest.json | 人工授权 ID／范围、canonical candidate、只输入限制、approved verifier/config/environment hashes | NOT_VERIFIED，未创建 |
| definition_manifest.json | ordered IDs、seed/n/history/context、resolved MainCfg、场景／role/schema规则、无性能选择规则 | NOT_VERIFIED，未创建 |
| source_environment_manifest.json | 源码 import closure、旧恢复 SHA、实际 interpreter/NumPy/OS/endian/二进制库、verifier 来源；未知项显式列出 | NOT_VERIFIED，未创建 |
| inputs/F1,F2,S1,S2/center_<id>/ | base x/y/ts、完整 profile、四 scenario arrays；存储 native dtype/shape/C order，分别 file SHA 与 legacy array hashes | NOT_VERIFIED，未创建 |
| base_input_inventory.jsonl | 每 context/ID 的 arrays/profile fingerprints 与 provenance | NOT_VERIFIED，未创建 |
| scenario_input_inventory.jsonl | 80 entries/context，raw scene 与 features 独立摘要、onset/definition/source base | NOT_VERIFIED，未创建 |
| stage_role_inventory.jsonl | 5760 entries/context，half-open bounds、role、x/y/ts、window counts、ts endpoints、legacy digest | NOT_VERIFIED，未创建 |
| bank_feasibility_inventory.json | 有序 11 metadata、checkpoint byte bindings、limits、full feasible masks 与初始排除集 | NOT_VERIFIED，未创建 |
| full_vs_singleton_matrix.csv | 每 center/field 的 F/S EXACT/MISMATCH/NOT_AVAILABLE，含差异类别；不含任何模型性能 | NOT_VERIFIED，未创建 |
| repeatability_schedule_resume_checks.jsonl | F/F、S/S、reader-only scheduling／resume 的每项判据与输入摘要；失败仍保留 | NOT_VERIFIED，未创建 |
| existing_input_match_inventory.csv | 全 1200 task 的来源 cohort、F/S 输入字段映射、可核／缺失字段、资格层；不含 loss 或新模型结果 | NOT_VERIFIED，未创建 |
| validation_certificate.json | 逐层 INPUT_DIGEST_MATCHED 等状态；initial-state 固定 pending separate authorization；不得直接写全文科学 PASS | NOT_VERIFIED，未创建 |
| run_manifest.json | 授权／定义／依赖绑定，输入文件与 inventories、checks/certificate 的明确白名单 SHA；不绑定自身、outputs_inventory 或 completion receipt | NOT_VERIFIED，未创建 |
| outputs_inventory.json / execution_receipt.json | 新文件 SHA、图依赖闭包、开始／结束来源与原文件完整性摘要、verifier exit／coverage | NOT_VERIFIED，未创建 |

暂不规定模型／统计输出位置；它们属于另外的协议和授权，不可借此根目录自动开始。

### 5.2 无循环哈希的绑定规则

拟议 schema V1 由人工和 code review 在任何生成前冻结：

1. definition_digest：canonical definition 的固定科学字段规范 JSON；包括 ordered context 与哈希算法版本，不含 run_id/time/result。
2. dependency_digest：实际源码、configs、NumPy/Python/environment、metadata library 的有序来源清单；文件 byte SHA 与规范元数据独立绑定。
3. per-center / per-scenario / per-role fingerprints：ID、科学 materialization context（full-batch20 或 singleton 及其固定参数）、dtype/shape/role/span 等元数据 + native array legacy digests + profile/resource/bank。F1/F2、S1/S2 是执行副本标签，只进入 run provenance；它们与 run_id、时间和调度信息都不能混入输入 fingerprint，否则重复输入同摘要目标会自相矛盾。
4. input_bundle_digest：按固定 center/scenario/stage/role 排序聚合全部输入 fingerprints，F1/F2 应 exact 同值。单独记录 context definition_digest，不能因为 arrays 偶然相同就抹掉其生成来源。
5. run manifest file SHA：绑定 run_id、授权、implementation、environment，以及明确列举的 definition/source-environment、输入 payload/inventories、checks/certificate 文件 SHA；不绑定自身、outputs_inventory 或 execution_receipt。随后 outputs_inventory 列出已完成文件（可包括 run_manifest）的 SHA，不绑定自身或 execution_receipt。
6. execution_receipt 最后绑定该 run_manifest 与 outputs_inventory SHA；不把 receipt 自己的 SHA 写入自己。其文件 SHA 可在最终交付时另行读取显示。开始／结束 source hash 改变阻断通过。

只以已冻结 exact hash 判据认证；数值差异诊断如要保存，应在授权中另明确范围，不可用事后 tolerance 将 exact mismatch 改成 match。NPY 容器 metadata 的变化不应被误解为 array 数值变化，因此两种 SHA 分列。

### 5.3 结果盲与原产物保护

Input verifier 可流式计算原 CSV file byte SHA 与 receipt 绑定，但对 CSV 的科学读取只允许预先列明的输入／来源字段投影：method/config/center/seed/scenario/stage、scenario_hash、D_upd/D_assess/D_srv hashes、center_type、deployment_tier/filter、bank_hash、time endpoints、scenario_role、stage1 initial/identity 元数据。不得输出或解释 service_mse、J_life、assessment loss、gain、predicted_R、offline labels、action收益、排名或显著性。

原 final metrics、paired Bootstrap、CI、动作收益报告不得作为输入 verifier 的决策输入；source manifest 中的训练／validation loss 字段同样排除。文件 bytes 哈希不是性能分析。未来新的模型输出在输入方案冻结／审定前不生成、更不查看。原结果已被观察，故“结果盲”指新方案的操作与决策标准不依赖新模型结果，不能宣称研究者从未看过原最终结果。

原 D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7 的全部 CSV、receipts、metrics、CI/status/claims，冻结源码/config/models 与前期审计保持只读；不修正 hash、manifest、sidecar 或原 output。未来 verifier 的 write allowlist 仅独立 run 根，原文件起止 SHA 和访问范围进入新 receipt。

### 5.4 当前静态证据 SHA 快照

以下只是已经读取文件的摘要，未来授权前仍须核对；不是运行完成证书。

| 实际文件完整路径 | SHA256 |
|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SINGLE_GROUP_INTEGRITY_FORENSIC_REPORT.md | 08cd3143813819a5d8cb4aae35c9a3cfcbe90a418a9f15a89a65e65a97e2d09a |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json | 6339a9247b984b497d1543198b3a7b7c0cfdf9c7bcfd1c52b47b62e17d2fd0df |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\p3_mismatch_v2_frozen.json | 529655647c1359e2a164cddc3c5c8b534f5cdbad53e2ede29ada477910975646 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py | ced000f213f8fc9b52a859e683fc6d27dd04a268641c3d6024500f56c1c158fe |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py | 6cd7e375d40c8ecf390fe37dee270d93890b3981f666e521e17441612f304d5e |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py | 0f5a5bff889a0ac866793dc49b21680f927af13c9e6fc3d5c3d75bbf4d9d5b27 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py | 8468b32f245e91c9bcbbb95d93b2dea07b75087d951184fb429cc1f7201cc367 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\common.py | 10c8dcf936e60e6b9b992778310648e258ed5a105d290d09434ba0c968183aaa |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py | 7597861c7bddd8e32080a3f83eff0ab0bc0f55db6c6b11aec773794f33cc2b07 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py | 378f2b8644f97e87fa819661da694d1bfcb163e7d183d110edf5f08c9d6dfe3d |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\models.py | 55028939faab38ea23736d191647f33f08ad48f14f204bbecf55bb3d76642e7e |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_models.py | 05aef843c99e3e4054c6b99a47063e85e6138c50bbb829c39183221a08765982 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py | fea128a2649301017a2a8ad6cab3db30392e180c2f3aa1216e9a83fefcd5d005 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py | 930fa8ebe34a442d53af16a054955580f2d0c41ef2514a3cfd125b0e6905883d |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_model_bank_manifest.json | e607a65adfb05b91bf8d9ebac77052d6e13223dfd54e47e655167e20c92342c8 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_2_source_bank\p3_mismatch_v2_r3\source_training_manifest.json | 84ab3d962e9a566303060fa98febcadef26eb1e5d472f81d32d986c35de3b940 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\environment.json | 62032b84e25bd8284352a3db87091c54b8209232092f1fc212f9af782d5de015 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\requirements_frozen.txt | aa7f267400111ffcd3a2b4d501557150a8130abe61c83a36ffc6ccdff96a37f4 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\execution_status.json | 9595a844666a4956bd8f2c235809e0f4965805578697bf6e9b24a5eeb13fbd75 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_SCIENTIFIC_AUDIT.json | c25c01b2b89b43e01d22c157a3bbb39d5321d43fe3cefbeb8dfb9500f175b8dd |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_AUTHORIZATION.json | 8f142dccb24a5260f46f4498ac9aa2869db814ceed9c6fafca47f3fbd9fb83da |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\__init__.py | 2eb599b6fa82980c2876a578e58c1bc3e42023720056766f60bcf298416e5a59 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\__init__.py | 5ddf6f7296705aadfcbcd3bab925e03addf0c11a71e212511664dba3657ed0cf |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\__init__.py | 0114da6465e378037d9c01edffe201729334b4e1cae45e6b174488debf76f5f8 |

## 6. Existing Result Reuse Criteria

### 6.1 必须区分的四个认证层级

这些是拟议资格门槛，不是当前通过结果。原字节始终保留，任何部分资格清单不授权筛除统计或替换论文主结果。

| 层级 | 预先规定的证据门槛 | 可支持的结论／不可越级事项 | 当前等级 |
|---|---|---|---|
| R0 HISTORICAL_ONLY | 原 CSV/receipt/output SHA、task/source cohort 字段有效并保留 | 如实报告历史存量与来源；不证明 canonical membership | 现有记录字节／来源已取证 VERIFIED；本次未重算其性能 |
| R1 SAVED_INPUT_DIGEST_MATCHED | 获准 full-batch reference 的同 ID/scenario legacy scenario hash、24×3 role hashes、time endpoints、记录的 type/tier/limits/bank/static feasible metadata exact match；missing field 单独标记 | 证明已保存／可核验的输入和资源字段对应 recovered reference；不证明未保存完整旧 metadata、全部历史依赖、canonical 初始化或模型行为 | NOT_VERIFIED，待 input-only |
| R2 STRICT_GROUP_ELIGIBLE | 同 center–seed–scenario 五方法均 R1；另行授权的 canonical initial-state certificate 证明共同起始状态与源 checkpoints/50-step rule；方法/source/config/causal provenance 合格 | 某完整五方法组的严格比较候选资格；需研究者审核纳入范围，不自动授权结果计算 | NOT_VERIFIED；超出 input-only |
| R3 CENTRE_COMPLETE / POPULATION_COMPLETE | 中心全部 3 seeds×4 scenarios 均 R2；原全人口主比较再要求全部 20 中心达到 R3 | 对应原 20-center 聚合与人口的完整资格；不自动把新复核称为未见 heldout | NOT_VERIFIED；需后续认证／科学授权 |

只有数组及相关 profile/type/tier/limits/bank/static feasible metadata、scenario/role 摘要均满足相应 R1 判据，才可对两个 reference 分别记录 SAVED_INPUT_DIGEST_MATCHED；仅 arrays 相同不够。缺失字段仍明确 coverage 与 NOT_VERIFIED。这是可核验保存字段的对应，不把不同科学 context 的完整 provenance fingerprints 改成相同，也不得篡改原 receipt 的来源。

“旧记录属于已恢复 canonical population”的足够证据需要注明层级：

- **输入对应层：**精确旧入口 provenance 已恢复 + 记录的全 scenario/role/resource 字段对获准 reference exact match + task/output 字节链有效，可签发 R1。
- **完整历史人口／环境层：**还需旧 base/profile 原件或可信完整摘要、历史 dependency/environment/run 绑定与 matching reconstructed arrays。当前缺失项不得用 R1 填补；若无此证据，只能称“保存输入对应当前冻结的恢复候选 reference”，不能称完整历史环境已复现。
- **严格模型比较层：**需要 R2/R3，包括另授权的 warm-up/initial-state 验证与科学来源审核。输入吻合不能独自证明训练、方法实现和初始参数的 canonical 一致性。

证据依据：D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:440–479 单任务 byte/task binding；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py:166–168 scenario digest 未含完整 metadata；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py:27–29、60–61 的 segment/warmup input；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py:31–33 初始化；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py:299–300 bank/limits hashes。以上源码行为 VERIFIED；R1–R3 是否满足 NOT_VERIFIED。

### 6.2 不可省略的 missing-evidence 规则

现有 CSV 未必保存完整 base arrays、全部 profile/metadata、dtype/shape 或依赖环境。不得把缺失字段填为 regenerated 值并声称旧数据原本如此。

M7 每字段保存 OBSERVED_MATCH / OBSERVED_MISMATCH / NOT_RECORDED / NOT_VERIFIABLE；R1 certificate 明确 observed coverage。dt 可从记录 time spacing 作一致性诊断，但不能把推算值伪装成原显式字段。匹配 engineered-role hashes 对 dt-feature 提供强输入一致性证据，仍须记录证据形式。

对于未保存但完整历史认证必需的字段，保持 NOT_VERIFIED 并阻断相应认证层；不必删除所有历史描述。原 source manifest 的 byte SHA 和已保存 bank hash 可以支持其公开字段一致性，不能替代重新执行 profiling 的事实。本方案只核元数据中的参数／operation 数量，不重新测量真实模型 FLOPs、准确率或性能。

### 6.3 旧／新记录适用同一盲判据

- legacy 239 trajectories 全部按 M7 判断；旧 binding + batch 来源不是自动 R1。
- singleton 961 全部按 M7 判断；新 binding 不是自动排除理由，但是否对 batch reference exact match 尚未知。
- 异常组四个 old baseline 即使 R1，缺少同 context 的匹配 P7.7，仍不能组成 R2。不能只把 new P7.7 接上或自动重跑一条。
- 已配对的其他 239 组含 192 singleton 组；“五方法彼此一致”不等于“canonical reference 一致”。所有 20 centers、80 scenarios 都要检查。
- 初始 hash 的五方法相等仅为已有状态 parity；不能认证 canonical warm-up。Input-only verification certificate 的 initial_state_verified 必须为 false/pending，不能据 input hash 将其改 true。
- 后续 state、history、actual candidates 的正常分化不作为输入认证失败理由；初始 state/source universe 与外生数据才是共同条件。

### 6.4 部分可复用集合的科学含义

若只一部分组达到 R2／R3，只能提交完整资格 inventory；不能直接生成新的均值、CI、Bootstrap 或主表。部分组重用／补充复核、是否维持原 population/estimand、中心内 seed/scenario 平衡及统计单位，都要单独审核。

若另行设计 sensitivity，仍以中心聚合；不能把 239 个存量 matched groups 或 239 条 legacy trajectories 当 239 个独立中心。资格报告必须独立于性能结果，避免按显著性决定保留集合。

## 7. Failure and Stop Conditions

本节是未来执行的预定 gate，不是本次出现失败。检查结果全为 NOT_VERIFIED，源码风险依据 VERIFIED（见 §§1–4）。

| 触发条件 | 预定动作 | 不允许的自动处理 |
|---|---|---|
| 历史旧 runner/protocol SHA 不匹配 | 停止该 historical reconstruction claim，保留错误及来源；重新审阅记录 | 用当前文件代替旧版、跳过失败 patch 或捏造来源 |
| 历史环境不完整／无法绑定 | 历史完全复现认证保持 NOT_VERIFIED；仅在研究者明确同意 current-env 层后进行该层比较 | 擅自安装环境或默认历史相同 |
| source/config/verifier/package hash 在执行中变化、路径错指另一项目 | 中止认证，保存起止 provenance 与错误，不启动模型 | 改 manifest 迎合变化、静默 fallback |
| 无明确授权／output 根已存在或 resolve 指向冻结目录 | 启动前停止，报告 exact path | mkdir 原 results、覆盖、删除、重命名已有记录 |
| ID 缺失／重复／顺序或 full-batch size 错、n_history/seed/ratio/shape/dtype/finite/timestamp/span 非合同值 | 标记 invalid materialization，停止该候选通过；保留完整诊断 | 自动重 seed、reorder generator call、分块补齐或更换输入 |
| F1/F2 或 S1/S2 重复不确定 | 认证停止；保留 context/环境/差异字段，研究者审阅 | 反复跑到 match、事后放宽浮点容差 |
| F 与 S 不同 | 正常记录 MISMATCH；继续已授权的完整输入 inventory，完成所有 20 IDs 比较 | 当作失败去“修” generator、挑选较好 context |
| 存量 record 与 F/S 均不匹配或 required metadata 不可得 | 标为 unmatched / unresolved，阻断相应复用资格，仍保留原字节与全体 inventory | 默认其为 corruption，覆盖 hash 或只挑匹配文件 |
| reader 调度／resume 改变输入 hash、跨方法数据／tier／静态 universe 不一致 | 阻断未来模型执行和恢复 PASS，保留失败 receipts | 以 runner compatibility 或 task complete 免检 |
| canonical initial-state certificate 缺失 | Input-only 正常结束，initial stage pending；不升级 R2 | 在 input-only 中偷偷 warm-up、使用 saved equality 当新认证 |
| import/load/adapt/predict/evaluate/oracle/statistics 路径被触发或出现模型性能字段输出 | 立即停止，记录越界及 side effects；不继续试验 | 自动训练／评估／bootstrap、解释 loss、修改方案追求更好结果 |
| 全 20 IDs /80 scenarios /24×3 roles／全部 1200 存量映射 coverage 不完整 | 不出全覆盖证书；保留 partial coverage | 将抽样或部分成功当完整 PASS |

失败仍应完整报告；未获授权的重试、补跑、依赖替换或校正不得执行。full-v-single 的差异不能导致删除历史结果；归类只能基于预先定义的输入及来源门槛。

## 8. Scientific Remediation Decision Tree

这是预先声明的 **INFERRED（科学处置建议）**；各分支事实需未来证据，当前结果 NOT_VERIFIED。没有以 loss、CI 或论文效果作为分支。

~~~text
研究者审阅并授权 input-only scope + verifier + definition + resolved environment
  │
  ├─ 未授权 → 只保留现有描述性证据；本阶段停止
  │
  └─ 已授权
       │
       ├─ exact旧源码／执行来源或当前依赖门槛不能满足
       │    → 不宣称完整历史复现；可另批 current-env 新reference验证
       │      若不愿／不能定义可信reference → 历史描述性证据
       │
       └─ 来源层明确
            │
            ├─ 重复性／ID／role／资源／调度parity gate失败
            │    → 保存诊断、停止认证与模型阶段；重新审核需新授权
            │
            └─ 输入验证完成，逐20-center比较F/S及所有存量
                 │
                 ├─ 某些record无法对canonical匹配／证据缺失
                 │    → 提交R0/R1 inventory；不做筛选统计
                 │      若目标仍是全20-center严格设计 → 评估完整独立复核
                 │
                 └─ 所有相关保存输入达到R1
                      │
                      ├─ initial-state阶段未授权／不通过
                      │    → 只认证输入；严格比较保持NOT_VERIFIED
                      │
                      └─ 另授权initial/source/causal验证达到R2/R3
                           │
                           ├─ 所有20 centers人口资格完整
                           │    → 研究者审核可复用／独立复核协议；
                           │      不自动改原统计，仍承认heldout已观察
                           │
                           └─ 缺口仅已知组，且其余全部资格已认证
                                → 可设计同canonical五方法局部复核；
                                  独立保存，是否合并需另外协议／授权
~~~

### 8.1 什么情况下旧记录可继续使用

必须达到所声称的层级：R1 对应保存输入，R2 对应完整五方法组，R3 对应原中心／人口。旧 239 条若符合 R1 可作为输入匹配的历史记录；只有完整组和后续 initial/source/causal 认证才具有严格比较候选资格。新 961 条同样判据，不以 old/new 标签决定。

原模型统计不能因输入 verification PASS 自动当作全实验重复验证 PASS。已有记录与新参考恰好 match 也不证明所有历史环境细节已恢复。证据层级必须出现在后续论文和 certificate 中。

### 8.2 单组复核何时有意义、何时不足

同 canonical environment 下完整执行异常组五方法，可回答局部公平输入／状态／部署条件问题，作为定向 integrity replication 有科学意义。必须单独授权，不可只替换 P7.7。

若其他 19 centers、192 singleton 组的 canonical 数值／initial provenance 尚未认证，单组复核不能恢复全文全人口严格比较。即使局部复核有利／不利，也不能用结果作为是否扩展的决定依据。只有先完成全部输入门槛，并且其余全体资格已足够认证，才可以另行审阅“局部补充如何与已认证历史记录组成一致协议”；本方案不默认批准这样的混合分析。

### 8.3 什么情况下应设计完整 1200 轨迹独立复核

若研究目标仍要求原全 20-center 同一 canonical 人口和严格共同输入，而存在跨中心／跨场景 canonical 不匹配、历史 provenance 不足、initial状态不能认证，或选择了新统一 input protocol，完整 20×3×4×5 独立复核是恢复统一证据的主要方案。若研究者要求每条轨迹都由同一纠正协议独立产生，亦应完整执行，不能称局部拼接为完整重建。

先冻结新的 input bundle、model/state/causal/receipt guard、独立输出、全部比较与统计计划，再另行授权。不能现在修改 generator 或启动 1200 任务。完整复核失败／负面结果也应保存并报告，不得按显著性决定取消或重做。

**VERIFIED 的事实边界：**33000–33019 的原最终模型结果已被观察。即使完整纠正复核成功，只能称完整性纠正后的独立复核／replication；不能称从未见过的全新 held-out evaluation。真正新未见人口须独立预定义和授权，且仍须披露原异常。

### 8.4 什么情况下仅保留历史描述性证据

未授权新的输入／状态／实验验证；无法建立可信 canonical reference；关键依赖／初始化／输入资格持续不足；或研究者选择不坚持严格配对目标时，已有均值／记录可如实保留为披露充分的历史存量描述，不能继续无条件声称全体共同输入的纯方法配对推断。

这不要求删除原结果，也不是因为结果“不够好”。处置基于证据资格。

### 8.5 防止结果驱动的选择与调整

预先固定 primary full-batch candidate、对照 singleton、全覆盖字段、exact判据、metadata缺失规则、reader schedule、来源层级、停止规则和分支；授权／verifier SHA 在新数组生成前提交。输入报告交研究者审阅，再决定下一授权层。

不计算或显示新模型 loss，不查询原 metrics/CI 选择 context；不按预期改善改变 seeds、centers、bank、gate、阈值或场景；不因后续模型结果不利取消已规定报告或切换 canonical definition。任何科学理由修改均需说明与输入／来源证据的关系、独立版本、新授权和全部历史保留，不得静默追改。不得把未观察的新结果当作取消／延迟／选择复核路径的标准。

## 9. Explicit Human Authorization Requirements

**本次只完成方案。研究者审阅前不得执行。** 后续授权应是具体、可核对的范围，至少包括：

| 下一阶段 | 需要明确授权的对象 | 不包含的权限 |
|---|---|---|
| verifier 实现与静态 code review | 新独立 verifier 的允许写路径、纯输入 imports/helper、hash/schema、stage slicing、metadata reconstruction、读字段白名单 | 不修改原 runner/generator/config，不自动执行任何生成 |
| input-only 运行 | 已审定 verifier/plan/definition/source/environment SHA，F1/F2/S1/S2、全部20输入/80场景/5760roles每context、reader-only schedule/resume、原1200metadata映射、独立 run 根 | 不加载／profiling／适配模型，不算loss/oracle/A1/Bootstrap，不修改原结果 |
| historical environment 的进一步恢复或诊断 | 具体已有证据读取、环境候选／构建操作、独立位置、预定来源判据 | 不覆盖原环境/config，不静默按结果轮换依赖 |
| initial-state verification | canonical input bundle，checkpoint/optimizer/50-step seed与environment，验证覆盖及新独立产物 | 不进行候选适配、生命周期评估、训练estimators或调参 |
| 局部五方法或完整1200独立复核 | 人口／input/state/source bundle、零gate/模型/种子/成本等冻结参数、完整causal和receipt guard、资源预算、独立执行／输出计划 | 不替换旧CSV/receipts，不选择有利结果，不冒称全新未见heldout |
| sensitivity／新Bootstrap／论文修订 | 明确科学问题、资格集合／中心聚合／区间／报告方案、独立结果与具体论文修改范围 | Input-only PASS 不授权统计、原CI更新或全文科学冻结 |

禁止自动执行：原代码／Git状态／配置／模型／种子修改，warm-up，source candidate adaptation，训练／重新拟合／调参，final-heldout，Bootstrap／新统计，删除／筛除／覆盖／重命名任何原产物，旧 receipt/manifest 补写，修复单一 Proposed，按预期性能改善选择或调整方案。

**交付结论：**完整20中心批量生成是有精确旧执行语义支持的主要 canonical 候选；历史完整环境及数值对应性尚未验证。后续 input-only 可独立比较两个 materialization context 并给出分层资格，但不能重新认证初始参数或恢复全文严格模型推断。本文件提交后停止，等待研究者审阅与授权。
