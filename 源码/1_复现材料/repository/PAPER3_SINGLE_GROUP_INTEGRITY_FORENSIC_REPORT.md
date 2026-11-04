# Paper 3 — P7.7 Final-Heldout Single-Group Integrity Forensic Audit

审计日期：2026-10-08（Asia/Shanghai）。工作区：D:\dt-talk。唯一目标仓库：D:\dt-talk\DT_LIFECYCLE_ESCALATION。

论文：**Bounded Maintenance Recoverability for Selective Lifecycle Escalation of Digital-Twin Models**。

本报告为静态、只读科学完整性取证。仅新建本报告；未修改源码、配置、模型、种子、CSV、receipt、统计或前期审计，未运行项目、生成器、训练、final-heldout 或 Bootstrap。历史日志中的命令／补丁仅作为证据读取，没有再次执行。没有使用其他论文项目的实验记录。

## 1. Executive Verdict

**已找到可证实的实现／协议层根因：serial→parallel 续跑改变了中心生成上下文，同时保留旧输出的兼容机制没有检查跨方法输入配对。** 精确旧 runner 和旧 protocol 已从目标项目历史会话日志纯内存复原，SHA256 与 239 份旧 receipt 完全匹配。旧入口一次生成 20-center batch，再将 by_id[center] 传给 run_one；新 worker 以 singleton 重新生成 base。生成器不具有跨 batch 的 center-ID sample invariance。239 旧输出保留，961 新输出使用新上下文，切点恰在异常组四个 baseline 与 P7.7 之间。详见第 4–6 节。

这一结论确认入口改变、混合保留及 parity guard 缺失的机制，**没有**声称已重新生成／复现每个数组、初始模型或损失，也不声称绝无未记录的历史环境因素。精确数值反事实及异常对均值差的影响方向仍为 NOT_VERIFIED。

| 关键判断 | 判定 | 源码／记录依据及科学影响 |
|---|---|---|
| (33003,7313,C4) 的 P7.7 与四 baseline 外生数据、初始状态、部署约束不一致 | VERIFIED | 第 3.1 节五 CSV 完整路径，第 2–25 行 scenario/data-role hashes、initial_state_hash、tier/filter；24 stages 均失配，第一阶段已不同。 |
| 所有方法每组共享相同初始化／部署条件 | CONTRADICTED | 同五 CSV 第 2 行直接构成反例；不是正常动作提交后 state 分化。 |
| 还有第二个跨方法字段失配组 | NOT_VERIFIED；本次全检未发现 | 1200 CSV、240 组、28800 行逐组逐 stage 检验仅命中该组；其他 239 组满足本次列明的配对字段。 |
| 问题只涉及一条任务、原 canonical 人口必然未改变 | CONTRADICTED / NOT_VERIFIED | 961 任务采用 singleton 新绑定；存量人口 A7/B8/C5，与当前 full batch 必有的 A6/B8/C6 不同。core\data.py:39–49、sim.py:54–63、main_cfg.py:66 的完整路径见第 5 节。不能由此增加跨方法失配组数量。 |
| 完成／哈希一致足以证明严格配对 | CONTRADICTED | execution_status.json:7–9；SCIENTIFIC_AUDIT.json 的 output_hashes；runner _validate_final_receipt:461–479 未检查跨方法输入／初始化／tier。完整路径见第 2 节。 |
| 原均值准确描述全部存量 | VERIFIED | final_metrics_by_method.csv:2–6 与全体原 service_mse 算术核对差异小于 1.1×10^-17；未产生新筛选结果。 |
| 只修论文文字即可保留严格共同输入的纯方法配对推断 | CONTRADICTED | 披露可保留真实描述，不能补出缺失的共同输入反事实；原 Bootstrap 的计算与严格配对解释须分开。 |

**建议：保留全部原证据，暂不给严格配对推断出具无条件科学冻结结论。** 由研究者选择披露／降级、事后敏感性分析或新的独立验证；任何新计算、生成或实验须另行授权。

等级定义：VERIFIED 为源码、哈希或已有记录直接支持（注明静态行为或存量事实）；INFERRED 为有依据但未直接证实的解释；NOT_VERIFIED 为证据不足或本阶段未执行所需验证；CONTRADICTED 为已有直接反例。NEEDS_RUNTIME_VERIFICATION 明确表示需要运行才能继续核验，本阶段不运行。

## 2. Evidence Inventory

### 2.1 仓库身份与 Git 状态

VERIFIED：Git --show-toplevel 为 D:/dt-talk/DT_LIFECYCLE_ESCALATION，branch=main，HEAD=436ee9960a32a8e94e571ded3fc800a2fa20f3e4，无 remote。所有 Git 查询明确指定目标，例如 git -C D:\dt-talk\DT_LIFECYCLE_ESCALATION status --short --untracked-files=no；未默认在工作区根目录查询，未改 HEAD/reflog。

已有 tracked 修改如下（相对目标仓库），本次保留；最终实现以实际工作树和冻结绑定认定，不能以 HEAD 替代：

~~~text
 M core/p7.py
 M reports/P7_7_FINAL_LIFECYCLE_PROTOCOL.md
 M reports/P7_7_FINAL_LIFECYCLE_PROTOCOL.md.sha256
 M results/p7_6b/task_states/fit/32248_7312_C1.json
 M results/p7_6b/task_states/fit/32248_7312_C3.json
~~~

既有未跟踪的论文／审计文件保留；历史旧源码仅在内存复原，未落盘或恢复工程。交付前以 git --no-optional-locks -C D:\dt-talk\DT_LIFECYCLE_ESCALATION 再次查询，HEAD 与上述五项 tracked 状态保持相同；19 项关键文件 SHA256 快照及 1201 项原 output_hashes 全部复核通过，raw CSV 与 receipt 均为 1200 份。

### 2.2 证据目录

| 证据 | 完整路径、函数／字段、行号 | 用途 |
|---|---|---|
| 前期 Section 5 与统计审计 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SECTION5_AND_STATS_FINAL_READONLY_EVIDENCE.md:134–184、310–357 | 前期异常与旧 runner 缺口；本次独立复核原始记录。 |
| 前期 S3–S4 审计 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_S3_S4_IMPLEMENTATION_CONSISTENCY_AUDIT.md:34–53、550 | 最终工作树及来源绑定；核心 hash 不能证明输入配对。 |
| 最终协议 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json:53–67、115–120、131–168、178–195 | data_seed=7311、零 gate、五方法、20×3×4×5、中心统计。保留的 pending 状态不是未执行证据，实际完成以另行授权与产物为准。 |
| 最终 runner | D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py，run_one:247–325；_run_final_task:486–494；run_final_heldout:868–958 | worker、恢复、数据／模型路径、统计。 |
| base 生成 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py，generate_base_centers:31–65 | batch 起点、数量、seed_offset、profile。 |
| C4 转换 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py，c4_target:55–81；make_scenario_v2:139–155；timeline/hash:161–168 | 场景由 base 派生，摘要 x/y/ts。 |
| RNG 与 tier | D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py，tier:30–33；schedule:36–63；simulate_centers:264–320 | schedule 消耗、slot、中心 RNG、tier。 |
| 默认配置 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py:66、196–209 | 3:4:3 block、条件 tier 概率。 |
| 1200 CSV／receipt | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\*.csv／同名 *.integrity.json | CSV 第 1 行 header、第 2–25 行 stages；receipt 第 3–13 行 valid/task/hash/rows。具体异常路径见 3.1。 |
| 完成状态 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\execution_status.json:3–14、33 | COMPLETED、1200/1200、0 failures、3 workers、239 resumes。 |
| 全体 output 绑定 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_SCIENTIFIC_AUDIT.json:39–45 及 output_hashes | 1200 raw CSV + status，共 1201 项实际 SHA 核验。 |
| 授权 manifest | D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_AUTHORIZATION.json:3–14、21–30，human_authorized / frozen_source_hashes | 最终授权／来源绑定；不是 parity 证明。 |
| 资源调整记录 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\docs\P7_7_FINAL_HELDOUT_PARALLEL_RESOURCE_ADJUSTMENT_20261003.md:7–18、22–39 | serial→parallel、239 继承、execution-only 声明。 |
| 中断 claim | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\interrupted_claims\attempt_p7_7_final_20261003_142433\P7_7_RECOVERABILITY_GUIDED_ratio10_grid33_33003_7313_C4.claim:3–8 | 异常 P7.7 身份／时间。 |
| 存量均值／CI | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\final_metrics_by_method.csv:2–6；D:\dt-talk\DT_LIFECYCLE_ESCALATION\reports\P7_7_FINAL_HELDOUT_STATISTICS.md:3–12 | 既有描述／原 CI，未重做 Bootstrap。 |
| 精确历史源码日志 | C:\Users\92487\.codex\sessions\2026\09\14\rollout-2026-09-14T21-27-11-01a0a019-a852-7350-813a-23a170fa191c.jsonl，2026-10-03 目标仓库事件 | 只筛选本仓库历史记录，内存复原旧版本；详见第 4 节。 |

### 2.3 核验方法与边界

PowerShell、rg、只读 Git、隔离标准库文本／CSV／JSON 解析与 SHA256。没有导入项目模块或初始化模型。全体 240 组逐 stage 比对 scenario_hash、D_upd_hash、D_assess_hash、D_srv_hash；核对 initial_state_hash、center_type、deployment_tier/filter、bank_hash、update_end_ts、decision_ts、scenario_role、任务字段、stage 1–24、各 receipt 输出 hash 与既有审计 manifest。

239 组“配对”仅指这些存量字段，不是重新证明 canonical population、历史依赖环境或所有模型运算正确。读取全体既有 loss 的算术核验不是新的筛选主结果、Bootstrap 或推断。

## 3. Five-Method Input Parity Matrix

### 3.1 文件、字段和行号

| 方法 | 原始 CSV 完整路径 | 原始 receipt 完整路径 |
|---|---|---|
| B0 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B0_Frozen_ratio10_33003_7313_C4.csv，第 1 行 header，第 2–25 行 stages | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B0_Frozen_ratio10_33003_7313_C4.integrity.json，第 3–13 行 |
| B1 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B1_AlwaysMaintainP50_ratio10_33003_7313_C4.csv，第 1 行 header，第 2–25 行 stages | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B1_AlwaysMaintainP50_ratio10_33003_7313_C4.integrity.json，第 3–13 行 |
| B2 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B2_RAVM_ratio10_33003_7313_C4.csv，第 1 行 header，第 2–25 行 stages | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B2_RAVM_ratio10_33003_7313_C4.integrity.json，第 3–13 行 |
| B8 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B8_AlwaysOpen_ratio10_33003_7313_C4.csv，第 1 行 header，第 2–25 行 stages | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B8_AlwaysOpen_ratio10_33003_7313_C4.integrity.json，第 3–13 行 |
| P7.7 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\P7_7_RECOVERABILITY_GUIDED_ratio10_grid33_33003_7313_C4.csv，第 1 行 header，第 2–25 行 stages | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\P7_7_RECOVERABILITY_GUIDED_ratio10_grid33_33003_7313_C4.integrity.json，第 3–13 行 |

### 3.2 五方法配对矩阵

矩阵中的 scenario_hash、initial_state_hash、deployment_filter_hash、deployment_tier 在本组每 CSV 第 2–25 行恒定；三数据 role hashes 逐 stage 比对。receipt 第 9、10、11、12 行分别为 protocol、runner、implementation、output hashes。以下判断均 VERIFIED。

| 方法 | rows / stages | scenario / initial / filter | tier | protocol / runner | implementation | CSV↔output_hash |
|---|---|---|---|---|---|---|
| B0 | 24 / 1–24 | S-old / I-old / F-medium | medium | P-old / R-old | Impl-common | 匹配 |
| B1 | 24 / 1–24 | S-old / I-old / F-medium | medium | P-old / R-old | Impl-common | 匹配 |
| B2 | 24 / 1–24 | S-old / I-old / F-medium | medium | P-old / R-old | Impl-common | 匹配 |
| B8 | 24 / 1–24 | S-old / I-old / F-medium | medium | P-old / R-old | Impl-common | 匹配 |
| P7.7 | 24 / 1–24 | S-new / I-new / F-tight | tight | P-new / R-new | Impl-common | 匹配 |

五方法 bank_hash 均 Bank-common，center_type 均 A；第一阶段五方法 identity_before 均 msa_a57_pt、update_end_ts=1407、decision_ts=1647。后续身份可随正常 RI 分化。相同初始身份名称不等于相同参数状态；明确的 medium/tight 差异也不是仅浮点 hash 格式问题。

| 别名 | 完整 SHA256 | 字段及范围 |
|---|---|---|
| S-old | fab19c15adc3ac357ed3c75e6f30b301303baf1c23d565e45f246fdb92180410 | 四 baseline 的 scenario_hash |
| S-new | cf2a20895ae46255194247dfa47b8479d79f4ec63cdcecb7da3ba9ac7db14714 | P7.7 的 scenario_hash |
| I-old | cef7d88b94b438d7ffbad2e3829767f4092e33ba30c02575f5487fa59ffcb161 | 四 baseline 的 initial_state_hash |
| I-new | ab39d97e11f5ae089c0ba593c4e8cf6cc3fc29bf5cfcde0feb6532983cbb3802 | P7.7 的 initial_state_hash |
| F-medium | 5de5678f276c1f906533b63f643c57f142326486d2bde9a7333530a95089085d | 四 baseline 的 deployment_filter_hash |
| F-tight | 146c7a1531dbe4f97134405d337af52af4c620d4e7dbd17ebd967e212e7622c9 | P7.7 的 deployment_filter_hash |
| P-old | 8785dc1ecf9e8123f47d786b880011774ed952daa56345b6f61e60361d15838d | 239 份旧 protocol_hash |
| P-new | 6339a9247b984b497d1543198b3a7b7c0cfdf9c7bcfd1c52b47b62e17d2fd0df | 961 份当前 protocol_hash |
| R-old | 20c0a3546f5cff28dc0dccb3737bc27ee47d81b06fcb94f9fe294ca576e43ec5 | 239 份旧 runner_hash |
| R-new | ced000f213f8fc9b52a859e683fc6d27dd04a268641c3d6024500f56c1c158fe | 961 份当前 runner_hash |
| Impl-common | 378f2b8644f97e87fa819661da694d1bfcb163e7d183d110edf5f08c9d6dfe3d | 全部 implementation_hash / 当前 core/p7.py |
| Bank-common | c9571436972af00eecdcbd3cf6ee80d54b92ae07ddcaf4f8ff76210ba9099b11 | 五方法的 bank_hash |

### 3.3 output_hash 独立核验

| 方法 | receipt 第 12 行已保存 output_hash | 实际核对 |
|---|---|---|
| B0 | 645d1cee9df046856afb7c7a195497eac35a1c2431dd6c73910be58064db6910 | VERIFIED：实际 CSV SHA256 与 receipt 第 12 行相等 |
| B1 | 3526c7112d0a27410051ca72dca0aa5a9683d49060f545a13726c28c17b2e669 | VERIFIED：实际 CSV SHA256 与 receipt 第 12 行相等 |
| B2 | b790abfe45dc3a5a88fddf08f78987a46b715c02fdc49c7bf779b218016db302 | VERIFIED：实际 CSV SHA256 与 receipt 第 12 行相等 |
| B8 | 13ac5796f800f2bb56704603ad8368dedbbb6363b19ce6e78039d41dea07c270 | VERIFIED：实际 CSV SHA256 与 receipt 第 12 行相等 |
| P7.7 | d4d2efbc6a0c561e2c57effd90abcc2a42c721e22510bfa015fabc42360689d7 | VERIFIED：实际 CSV SHA256 与 receipt 第 12 行相等 |

各自 CSV 对各自 receipt 匹配，不能证明五方法共同输入。

### 3.4 逐阶段 input parity

单元为“四 baseline 相互一致 / P7.7 与 baseline 一致”。均 VERIFIED；CSV 行号适用于第 3.1 节五个实际文件。

| stage | CSV 行 | D_upd_hash | D_assess_hash | D_srv_hash |
|---|---|---|---|---|
| 1 | 2 | 是 / 否 | 是 / 否 | 是 / 否 |
| 2 | 3 | 是 / 否 | 是 / 否 | 是 / 否 |
| 3 | 4 | 是 / 否 | 是 / 否 | 是 / 否 |
| 4 | 5 | 是 / 否 | 是 / 否 | 是 / 否 |
| 5 | 6 | 是 / 否 | 是 / 否 | 是 / 否 |
| 6 | 7 | 是 / 否 | 是 / 否 | 是 / 否 |
| 7 | 8 | 是 / 否 | 是 / 否 | 是 / 否 |
| 8 | 9 | 是 / 否 | 是 / 否 | 是 / 否 |
| 9 | 10 | 是 / 否 | 是 / 否 | 是 / 否 |
| 10 | 11 | 是 / 否 | 是 / 否 | 是 / 否 |
| 11 | 12 | 是 / 否 | 是 / 否 | 是 / 否 |
| 12 | 13 | 是 / 否 | 是 / 否 | 是 / 否 |
| 13 | 14 | 是 / 否 | 是 / 否 | 是 / 否 |
| 14 | 15 | 是 / 否 | 是 / 否 | 是 / 否 |
| 15 | 16 | 是 / 否 | 是 / 否 | 是 / 否 |
| 16 | 17 | 是 / 否 | 是 / 否 | 是 / 否 |
| 17 | 18 | 是 / 否 | 是 / 否 | 是 / 否 |
| 18 | 19 | 是 / 否 | 是 / 否 | 是 / 否 |
| 19 | 20 | 是 / 否 | 是 / 否 | 是 / 否 |
| 20 | 21 | 是 / 否 | 是 / 否 | 是 / 否 |
| 21 | 22 | 是 / 否 | 是 / 否 | 是 / 否 |
| 22 | 23 | 是 / 否 | 是 / 否 | 是 / 否 |
| 23 | 24 | 是 / 否 | 是 / 否 | 是 / 否 |
| 24 | 25 | 是 / 否 | 是 / 否 | 是 / 否 |

第一阶段（CSV 第 2 行）的完整 role hashes：

| 字段 | 四 baseline | P7.7 |
|---|---|---|
| D_upd_hash | 5f85ecc28041106192cb5b9cf3fe4201c18dec47140ea36fbda923a4f988d4fc | eb94e7c840e8cf6041497fe484d368619793c983640a29dea029d07277caf0ad |
| D_assess_hash | 4c4184dde68a56a0c8e2c11c4bfde915610e9259be43ab45ca8d7f22b58aca96 | 64f05c6c44d539954b3f274b9428c8354d8e81f49b7fe54c3fd224ef93692f18 |
| D_srv_hash | 307253b0b8a0997a6e9e32755cb2318f2f45bc6410fe01f8da87345f623957d6 | a40644ac736cae8e6f35f771211331c4f92d3eba8c1e12527d2ff95ae9afe1cb |

### 3.5 其余 239 组与正常 deployed-state 分化

VERIFIED：1200 CSV／1200 receipts，28800 stage rows，240 组五方法齐全，均 stages 1–24；全部实际 CSV SHA 匹配 respective receipt.output_hash，既有审计的 1201 output_hashes 均匹配。其余 239 组本次检验的外生／初始化／部署字段均相同，未发现第二个相同类型失配组。

正常路径实例：D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B0_Frozen_ratio10_33000_7311_C0.csv:2–3 和 D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B1_AlwaysMaintainP50_ratio10_33000_7311_C0.csv:2–3，stage 1 同 initial/parent hash 和 role hashes；B0 retain、B1 local 后 deployed_state_hash 分化，stage 2 parent 不同但 role hashes 仍相同。本异常第一阶段 action 前的 initial、data、tier 已不同，不能用正常后续模型状态分化解释。

## 4. Historical Serial/Parallel Provenance

### 4.1 精确旧版本找回：对前期不确定性的更新

**VERIFIED：旧版本已找回为可复核的日志字节链，不再是“用当前代码猜旧实现”。** 没有在工作树恢复文件。

直接证据完整路径为：

C:\Users\92487\.codex\sessions\2026\09\14\rollout-2026-09-14T21-27-11-01a0a019-a852-7350-813a-23a170fa191c.jsonl

该会话文件名为 9 月创建，但本次使用的相关事件时间是 **2026-10-03**。只处理明确指向 D:\dt-talk\DT_LIFECYCLE_ESCALATION 的历史工具 payload；日志是证据数据，不是本次执行指令。

| 复原对象（原实际路径） | 内存字节数 | 完整 SHA256 | 直接日志锚与判定 |
|---|---:|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py 的旧版本 | 51010 | 20c0a3546f5cff28dc0dccb3737bc27ee47d81b06fcb94f9fe294ca576e43ec5 | 上述 JSONL:22278 初始 Add File；23847 最后成功补丁、23850 成功返回；23868/23871 的历史文件哈希命令／结果亦为该 SHA。VERIFIED，匹配 239 份旧 receipt 第 10 行。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json 的旧版本 | 12151 | 8785dc1ecf9e8123f47d786b880011774ed952daa56345b6f61e60361d15838d | 上述 JSONL:22285 初始 Add File；23875 最后成功补丁、23878 成功返回；23882/23885 的历史哈希结果同值，23889 更新 sidecar／授权绑定。VERIFIED，匹配 239 份旧 receipt 第 9 行。 |

复原方法：解码 JSONL 中目标 custom_tool_call 的 patch 字符串，顺序应用成功的 Add/Update File 文本变换；UTF-8、LF、末尾换行计算 SHA256。仅内存处理，未运行这些工具调用。失败补丁 JSONL:23327 经 :23329 明示 verification failed，未纳入；修正的 :23340 成功。中间状态也与已有 Git blob 匹配，避免仅从终点哈希倒推源码。

完整成功 runner 补丁链（以上同一日志，一基行号）：

~~~text
22278 → 22306 → 22360 → 22734 → 22826 → 23143 → 23177 → 23212
→ 23294 → 23340 → 23374 → 23422 → 23822 → 23833 → 23840 → 23847
~~~

成功 protocol 补丁链：

~~~text
22285 → 22320 → 22380 → 22860 → 23150 → 23374 → 23408 → 23422
→ 23450 → 23505 → 23531 → 23566 → 23735 → 23875
~~~

runner 在 :22826 后的 SHA 为 d4f6b529cf7089e441c0e0e6398473482d11ab2f6e926e6eb68e282c39048666，匹配 Git blob 85d495defbb72b5d975d7278b07fa8521af3e9be；:23422 后为日志所记 f01dc0a11dbd071b401f23ad734d281fb9381018bc09495a9f04734bce37d0ea。protocol 在 :22860 后匹配 Git blob 8ff5dc1ceef9d86213340f0fa7a023a45e5c6abc；:23735 后为 28b9521e0ba7385f4843bc3451b52a19e2967f90503fab3f4326eca3b6f4d43e。

只读历史搜索覆盖目标 Git 对象清单 1768 项；覆盖上述对象长度区间的 5KB–100KB blobs 890 项，按 RAW/LF/CRLF 检查，连同 reachable 目标版本、reflog、只读 fsck 的 unreachable 检查，未在 Git 内匹配这两个旧终点 hash。精确版本最终来自上述既有长期会话日志。预期 sessions\2026\10\03 目录不存在，不等于该日记录不存在。找到精确匹配后停止扩大搜索。

前期 D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SECTION5_AND_STATS_FINAL_READONLY_EVIDENCE.md:182、354 的“精确旧 runner 未找到”是当时证据范围的结论；本报告用新增历史证据更新它，保留前期报告原样。

### 4.2 旧入口与新入口的直接差异

下方“旧行号”仅指 SHA=20c0… 的内存复原历史版本，**不是当前同名文件对应行号**；直接历史文本锚为上述 JSONL:23833 的最终入口补丁及 :24436 的 serial→parallel diff（:24439 成功返回）。

~~~python
# 旧 D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py
818: def run_final_heldout() -> dict:
822:     bases = generate_base_centers(cfg["final_population"]["centers"],
                                      data_seed=cfg["common_behavior"]["data_seed"])
823:     by_id = {int(base.center_id): base for base in bases}
825:     tasks = [(center, seed, scenario, method)
826:              for center in cfg["final_population"]["centers"]
827:              for seed in cfg["final_population"]["seeds"]
828:              for scenario in cfg["final_population"]["scenarios"]
829:              for method in methods]
843:     for index, (center, seed, scenario, method) in enumerate(tasks, start=1):
852:             frame = run_one(by_id[center], seed, scenario, cfg,
                                method, allow_final=True)
~~~

VERIFIED：旧 serial 一次生成 20 个中心，所有同 center 的任务引用该批次同一 base。旧版本没有 _run_final_task。

当前 D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py 的实际行号：

~~~python
486: def _run_final_task(task):
488:     center, seed, scenario, method = task
490:     bases = generate_base_centers([int(center)],
                                      data_seed=cfg["common_behavior"]["data_seed"])
493:     frame = run_one(bases[0], int(seed), scenario, cfg, method, allow_final=True)

879:     bases = generate_base_centers(cfg["final_population"]["centers"],
                                      data_seed=cfg["common_behavior"]["data_seed"])
880:     by_id = {int(base.center_id): base for base in bases}
922:     futures = {pool.submit(_run_final_task, task): task for task in pending}
~~~

VERIFIED：主进程虽然仍生成整批 by_id，实际 worker 不使用它；worker 按 singleton 重新 materialize base。问题在调用上下文改变，不能泛化成“多进程必然改变数据”。

### 4.3 科学函数、配置和历史依赖

| 对照 | 证据与实际行为 | 判定及影响 |
|---|---|---|
| run_one | 旧完整路径见上，旧函数 235–313；当前 D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:247–325。函数源码逐字相同，文本 SHA=a5092acaef2062afb1e614c1a5524d5c454656f967421b315bb6d17c81d230d2。 | VERIFIED：方法内部执行未由该次 parallel 修改改变；其接收的 base 已变，故相同函数不保证相同输入。 |
| FrozenA1Observer / final_configs | 同文件旧 129–164 / 226–227；当前 141–176 / 238–239，逐字相同。 | VERIFIED：冻结 A1 观察器及五方法清单保持。 |
| 旧 protocol→当前 protocol | 旧 SHA=8785… 与当前 D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json（SHA=6339…）解析后的 JSON，仅 /runner/runner_sha256 与 /source_bindings_sha256/scripts/run_p7_7_final.py 两处不同。 | VERIFIED：仅 runner 绑定变化；data_seed、gate、阈值、模型库配置、成本、population、统计计划值相同。不能推出 materialized data 相同。 |
| 生成器 Git bytes | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py、D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py、D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py 当前 SHA 分别为 6cd7e375d40c8ecf390fe37dee270d93890b3981f666e521e17441612f304d5e、930fa8ebe34a442d53af16a054955580f2d0c41ef2514a3cfd125b0e6905883d、fea128a2649301017a2a8ad6cab3db30392e180c2f3aa1216e9a83fefcd5d005；与目标 Git 491231c、60f3589、436ee99 三节点逐字相同；同日志 Oct03 目标写入／patch 记录未见这三文件改动。 | VERIFIED：审阅 Git/日志未发现这些生成器源码在该资源调整中变化。NOT_VERIFIED：receipt 没有直接绑定其历史运行 bytes，不能把“未见改动”升级为历史全运行环境完全证明。 |

### 4.4 239 继承输出与 961 新输出的混合保存

VERIFIED：全体 receipt 的 hash pair 仅两类；旧 pair 为 239，当前 pair 为 961，implementation_hash 全部相同。旧 pair 的任务键按精确旧源码顺序与冻结 comparator 顺序，**恰好是任务 1–239**，不存在散落的旧任务。

| 旧入口任务序号 | 任务 | 既有输出绑定 |
|---:|---|---|
| 1–180 | 33000、33001、33002 各 60 任务 | 旧 pair |
| 181–239 | 33003 的前 59 任务 | 旧 pair |
| 239 | (33003,7313,C4,B8) | 旧 pair；本组四个 baseline 已完成 |
| 240 | (33003,7313,C4,P7.7) | 中断 claim；最终 CSV／receipt 为当前 pair |
| 241–1200 | 33004–33019，各 60 任务 | 当前 pair |

直接证据：

- D:\dt-talk\DT_LIFECYCLE_ESCALATION\docs\P7_7_FINAL_HELDOUT_PARALLEL_RESOURCE_ADJUSTMENT_20261003.md:7–18 记录旧 attempt、保留 239、一个中断 claim 和明确 legacy allowlist；:22–31 记录 parallel 续跑、有效旧输出不重跑、缺失任务重新开始。
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\interrupted_claims\attempt_p7_7_final_20261003_142433\P7_7_RECOVERABILITY_GUIDED_ratio10_grid33_33003_7313_C4.claim:3–8，attempt=p7_7_final_20261003_142433、method=P7.7、center=33003、seed=7313、scenario=C4；started_utc=2026-10-03T07:19:03.595133Z（北京时间 15:19:03）。
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\execution_status.json:4–6、14、33，新 attempt=p7_7_final_parallel_20261003_152959，UTC 07:29:59 至 09:27:15（北京时间 15:29:59 至 17:27:15），workers=3，resume_events=239。
- D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:46–52、461–479，_validate_final_receipt 接受精确旧 hash pair；:896–904 收取有效旧 frames，其余进入 pending；:921–934 仅为 missing tasks 生成并保存新 frame；:957–958 合并两类 frames 形成既有统计。

**判定：**异常 P7.7 与中断／资源调整的任务身份和绑定链为 VERIFIED；没有部分 claim 被误当成 completed CSV 的证据，旧文档也规定整任务重新开始。不能据此认定 CUDA、资源不足或无记录重试是根因。

## 5. Generator and RNG Mechanism Trace

### 5.1 为什么同一 center ID 不构成 stable sample key

| 完整路径、函数、行号 | 代码行为 | 判定与科学含义 |
|---|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py，generate_base_centers:31–48 | 要求 contiguous ordered IDs；MainCfg() 后设置 data_seed；调用 simulate_centers(cfg,len(center_ids),seed_offset=center_ids[0]*17,start_center_id=center_ids[0])。 | VERIFIED：batch 首 ID 和长度进入生成器，模型 seed 不参与此 base 生成。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py，simulate_centers:264、271–280 | rng0=RandomState(sim.seed+seed_offset)；先生成 type_schedule，再按 local_id 从 rng0.randint 抽取每中心 rng。 | VERIFIED：中心局部 RNG 取决于 schedule 消耗和批次 slot，而非直接以最终 center_id 种子化。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py，_make_type_schedule:54–63 | 构造类型 block、shuffle，直至达到请求 n_centers，最后截断。 | VERIFIED：n=20 需要两个 block，n=1 只需一个；RNG draw order 不同。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py，simulate_centers:282–317 | 中心 RNG 采样 dt、latent workload、metrics、schema/drop、missingness、noise。 | VERIFIED：改变中心 rng 上下文可以同时影响 x、y、profile；未重新生成或量化这些具体差值。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py，_sample_budget_tier:30–33；simulate_centers:319–320 | 在上述 RNG draws 后按 center_type 条件概率 rng.choice tier，然后赋 start_center_id+local_id。 | VERIFIED：tier 从 RNG 与 profile 派生；不是固定由中心编号或 A/B/C 类型唯一决定。 |

静态参数追踪，不作 RNG 运行：

| 33003 所在上下文 | n_centers | batch 起点 | local slot（零基） | rng0 初始整数 seed |
|---|---:|---:|---:|---:|
| 精确旧 serial full batch | 20 | 33000 | 3 | 7311 + 33000×17 = 568311 |
| 当前 singleton worker | 1 | 33003 | 0 | 7311 + 33003×17 = 568362 |

上述整数与 slot 由源码直接计算为 VERIFIED；各 RNG 抽样值、canonical 数组和 initial_state 的反事实重现为 NOT_VERIFIED，未执行。

D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py:204–208 规定 A 的 tier 概率 (tight,medium,loose)=(0.25,0.45,0.30)，B=(0.35,0.45,0.20)，C=(0.45,0.40,0.15)。因此本异常两侧均为 A 而 tier 分别 medium/tight，与源码允许的机制一致；不应把相同 A 型当作环境相同的证据。

### 5.2 从 base 到 C4、初始化和部署可行性

| 完整路径、函数／字段、行号 | 实际行为 | 判定与影响 |
|---|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py，c4_target:55–81 | 对 base.y 的 logit，结合 base.metadata["base_logit"] 与冻结 causal lags/weights 构建 C4 replacement。 | VERIFIED：相同 C4 名称不保证相同 target realization；base 差异传播到场景。 |
| 同完整路径，make_scenario_v2:139–142；timeline_for_v2/scenario_hash_v2:161–168 | 复制 base.x/y 后在 onset 以后替换 C4 y；按 x/y/ts 摘要；无 method 或模型 seed 参数。 | VERIFIED：两种输入上下文间的差异不是方法动作生成的外生随机性。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py，feature_matrix:26–28 | telemetry 加 dt/4 特征。 | VERIFIED：profile 与原始数组共同影响模型输入。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py，initial_model:31–33 | 加载 incumbent，在 timeline.warmup() 做 50 updates，seed=seed+center_id。 | VERIFIED：两侧适配规则相同，但 warmup data 可不同；实际 initial_state_hash 已不相同。未反事实重训。 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py，run_one:253–267、298–304 | 加载同冻结 source manifest/bank/incumbent；以 base.budget_tier 选 deployment_limits；记录 scenario、initial、tier、service hashes。 | VERIFIED：输入生成差异同时进入评估环境、初始状态与候选可行性。 |

### 5.3 全人口 materialization 的额外证据

从 1200 份 CSV 第 2 行 center_type/deployment_tier 和 receipt 第 9–10 行聚类，VERIFIED：

| center | 存量 center_type | 存量 tier | legacy/current 任务数 |
|---:|---|---|---|
| 33000 | C | medium | 60/0 |
| 33001 | B | medium | 60/0 |
| 33002 | A | tight | 60/0 |
| 33003 | A | medium（59）/tight（1） | 59/1 |
| 33004 | B | medium | 0/60 |
| 33005 | B | medium | 0/60 |
| 33006 | A | tight | 0/60 |
| 33007 | C | loose | 0/60 |
| 33008 | C | tight | 0/60 |
| 33009 | C | tight | 0/60 |
| 33010 | C | medium | 0/60 |
| 33011 | B | loose | 0/60 |
| 33012 | A | medium | 0/60 |
| 33013 | A | tight | 0/60 |
| 33014 | A | medium | 0/60 |
| 33015 | B | loose | 0/60 |
| 33016 | B | tight | 0/60 |
| 33017 | B | loose | 0/60 |
| 33018 | B | medium | 0/60 |
| 33019 | A | medium | 0/60 |

证据源完整目录为 D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw；具体命名模板为各冻结 method_config_id + "_" + center + "_" + seed + "_" + scenario + ".csv/.integrity.json"，不是另一项目的 profile 表。该表只是现有字段计数，不是新增统计端点。

存量 A7/B8/C5 在五个方法间类型计数相同（33003 两侧均为 A）。当前 generate_base_centers 对完整 20 个中心采用默认 MainCfg、默认 allowed_types=A/B/C；D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py:66 的 (3,4,3)，配合 D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py:54–63，结构上保证完整 20-center batch 为 A6/B8/C6。

**VERIFIED：存量人口不是当前完整 20-center 调用的同一类型组成。** 已确认入口上下文改变涉及 961 份新绑定任务，而非只有异常 P7.7 一个任务。**NOT_VERIFIED：**其余 singleton centers 与原 canonical batch 的逐数组／逐 profile 差异、哪些中心会变化以及原 intended population 的全部参数。本阶段没有重新生成原 20-center batch，不能据计数宣称另有多少“错误组”或选择应作废的中心。

## 6. Root-Cause Assessment

| 候选解释／机制 | 完整路径、函数／字段、行号与实际证据 | 判定 |
|---|---|---|
| 旧 serial 整批生成，新 parallel 单中心生成 | 精确旧源码由上述历史 JSONL:22278–23847 复原并匹配 R-old；旧 run_final_heldout:822–823、852 使用 full batch/by_id；当前 D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:490、493 使用 singleton。 | VERIFIED |
| RNG/context 对 sample identity 不具 batch 不变性 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py:36–48；D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py:59–63、264–280、319–320，改变 batch 起点、数量、slot 和 RNG 路径。 | VERIFIED（源码机制） |
| legacy 保留切点在本组方法之间 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw 下全体 receipt 第 9–10 行旧键恰为任务 1–239；五个异常 receipt 完整路径见第 3.1 节；中断 claim 完整路径见第 4.4 节、第 4–8 行恰为任务 240。 | VERIFIED |
| receipt 恢复检查缺少实验配对验证 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py，_validate_final_receipt:461–479 校验单文件及旧 hash allowlist，不比较同组五方法的 data/initial/tier；run_final_heldout:957–958 合并存量。 | VERIFIED |
| 上述切换造成当前存量混用两种 input realization | 五个异常 CSV 第 2–25 行、receipt 第 9–12 行，以及已复原旧／新调用链共同证实。四 baseline 为 old/medium，P7.7 为 new/tight。 | VERIFIED：实现与协议层的根因链。具体数组／模型数值的完整反事实复现尚未执行。 |
| resource 文档所说“同一 run_one、冻结参数未变” | D:\dt-talk\DT_LIFECYCLE_ESCALATION\docs\P7_7_FINAL_HELDOUT_PARALLEL_RESOURCE_ADJUSTMENT_20261003.md:28、36；精确旧／新函数和 protocol 对照见第 4.3 节。 | VERIFIED（狭义） |
| 由此推出“调整仅改变速度、不改变实现的输入环境” | 同文档第 3、28、36 行的宽泛 execution-only 解释，被实际 CSV/tier 与生成入口差异反驳。 | CONTRADICTED |
| 相同 core implementation_hash 就保证科学配对 | 五异常 receipt 第 11 行相同，但 CSV 输入字段不同。当前 core/p7.py 与冻结绑定匹配。 | CONTRADICTED |
| 由 RI 或 local 动作导致正常后续 state 分化 | 五异常 CSV 第 2 行 initial_state_hash、三数据 role hashes、tier 在首次动作前即已不同。 | CONTRADICTED（用于解释本异常时） |
| 中断保存了部分轨迹并冒充完整轨迹 | claim 非 CSV；已有 CSV 全部 24 stages、output hash 匹配。当前 runner:905–934 的 pending 整任务流程。 | NOT_VERIFIED；现有证据不支持该解释 |
| CUDA nondeterminism、OOM、隐含重试或其它临时文件损坏 | 没有独立直接记录；明确 tier/data hash 差异已存在更直接的输入上下文机制。 | NOT_VERIFIED，不能写成根因 |
| 唯一数值原因已通过反事实实验复现 | 未执行生成器、模型或 final-heldout；旧 receipt 未完整绑定每个历史依赖的 bytes／环境。 | NOT_VERIFIED |

**根因结论：**本次已超越前期“可能是 batch/single 差异”的推测，找回了精确旧入口，并将任务切点、输入字段和兼容检查串成直接证据链。可确认的根因是**中心生成调用上下文被改变却仍将两种上下文的输出视为兼容恢复结果，且没有跨方法 input-parity guard**。不能声称已算出偏差大小、影响方向、唯一所有数值因素或完整重演了历史环境。

## 7. Scope of Affected Scientific Claims

### 7.1 八项范围问题的答复

| 问题 | 结论／判定 | 完整路径、函数／字段、行号与证据 |
|---|---|---|
| 1. 跨方法输入异常是否仅一组？ | VERIFIED：本次全量存量字段／hash 检验仅 (33003,7313,C4)。不能扩展为“其余等于原 canonical batch”。 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw 下 1200 CSV 第 2–25 行 scenario/data-role、initial、tier/filter 等；具体异常完整路径见 3.1，更广 provenance 见 5.3。 |
| 2. 是否影响该组全部 24 stages？ | VERIFIED：五方法共同输入在全部 24 stages 不成立，四个 P7.7-versus-baseline 比较均失配。四 baseline 之间六种两两 input parity 仍成立。 | 第 3.1 节五 CSV 完整路径，第 2–25 行；第 3.4 节逐 stage 三 role hash 矩阵。不能写成 baseline 之间也失配。 |
| 3. 是否改变可行候选集合？ | VERIFIED：medium/tight 限制不同；本库可行身份 11/8，排除当前身份后候选 10/7。 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\p3_mismatch_v2_frozen.json:261–269；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\models.py，feasible:156–157；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py，source_candidates:178–195。见 7.2。 |
| 4. 全方法同初始状态／部署约束的声明是否成立？ | CONTRADICTED：stage 1 已是反例；同身份名、warm-up rule、core hash 不等于 actual state/tier 相同。 | 五异常 CSV 第 2 行 initial_state_hash、identity_before、tier/filter；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py，initial_model:31–33。 |
| 5. 1200/1200 与 1201 hashes 还能证明什么？ | VERIFIED：任务齐全、24-stage 完整、各 receipt/manifest 的字节一致。NOT_VERIFIED：共同环境、原 canonical population、全部依赖一致、科学配对有效性。 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\execution_status.json:7–9、33；D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_SCIENTIFIC_AUDIT.json:44–45 及 output_hashes；runner _validate_final_receipt:461–479。 |
| 6. 原均值是否准确描述存量？ | VERIFIED：全体原 service_mse 与存储 means 在浮点表示量级一致；不能据此认定纯 method effect。 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\final_metrics_by_method.csv:2–6；D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py，_trajectory_metrics:501–511、_center_metrics:528–530、_make_statistics:555–560。 |
| 7. 原 paired CI 的解释边界？ | VERIFIED：数值上重采样 20 个 center-ID-matched 存量差值。NOT_VERIFIED：严格共同输入下纯方法效果 CI；33003 的差值混入 context 变化。 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:578–591；D:\dt-talk\DT_LIFECYCLE_ESCALATION\reports\P7_7_FINAL_HELDOUT_STATISTICS.md:3、7–10。详见第 8 节。 |
| 8. 能确定异常对最终均值差的影响方向吗？ | NOT_VERIFIED：没有匹配输入下的 P7.7/baseline 反事实；tight、候选少不保证 service loss 单调。 | 五异常 CSV 第 2–25 行 service_mse 与输入字段；D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py:183–191 无跨环境单调保证。观察差值符号不是污染方向。 |

### 7.2 可行集合差异

VERIFIED：同 bank_hash，medium=100000 parameters/5000000 operations，tight=30000/1500000。feasible 同时检查两个上限。以下 identity 在 medium 可行、tight 不可行：

| identity | parameters | operations | 完整路径、字段、行号 |
|---|---:|---:|---|
| msa_a1_pt | 77921 | 155712 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_model_bank_manifest.json:5、12–13 |
| msa_a6_pt | 78977 | 157760 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_model_bank_manifest.json:16、23–24 |
| msa_a62_pt | 12033 | 2230336 | D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_model_bank_manifest.json:71、78–79 |

三个 r3 identity 均 tight 可行：p3v2_a57_regime_b 与 p3v2_a57_regime_c_control（5697/1050688）、p3v2_a46_regime_c（7137/1339424），见 D:\dt-talk\DT_LIFECYCLE_ESCALATION\artifacts\p3_2_source_bank\p3_mismatch_v2_r3\source_training_manifest.json:78–123；其他五 native identity 亦 tight 可行。medium 全部 11，tight 为 8。

D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py:182–191 在适配前排除当前及不可行 identity。现有 D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\B8_AlwaysOpen_ratio10_33003_7313_C4.csv:2–25，全部 gate_open=1、feasible_candidate_count=10；D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\raw\P7_7_RECOVERABILITY_GUIDED_ratio10_grid33_33003_7313_C4.csv:2–25，19 个 gate-open 行均 feasible_candidate_count=7。本次只核对字段，没有重新适配／评估候选。

论文影响：该组不能是“同部署约束下门控减少搜索”的严格对照，候选数量差不能全部归因于 gate；tier filtering 也不同。

### 7.3 全体存量均值

直接抄录 D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\final_metrics_by_method.csv:2–6，非筛选后结果：

| 方法 | 原 mean_lifecycle_service_loss |
|---|---:|
| B0 | 0.006049676514516644 |
| B1 | 0.002985070205270142 |
| B2 | 0.004535350747396975 |
| B8 | 0.0024859688219723572 |
| P7.7 | 0.002524255871657655 |

VERIFIED：仅为存量描述核验，对全部 28800 个既有 service_mse 字符串作标准库十进制求和／均值比较；每方法 5760 行、240 组、各组 24 行、各中心 12 组，原平衡设计下等价于 stage→seed/scenario→center 聚合。与保存 method means 差异均小于 1.1×10^-17。没有生成筛选结果、区间、Bootstrap、排名或替代统计文件。

P7.7 保存 gate_open_rate=0.3314236111111111（约 33.14%），同文件第 6 行；它仍是含异常组的存量描述，不能证明全输入配对。

原平衡 mean 每组权重为 1/(20×12)=1/240，每 stage 在组内为 1/24。这个权重不证明污染可以忽略，也不提供方向；一个直接反例已经否定配对全称声明。

### 7.4 比前期更广的范围与边界

VERIFIED：33003 的 60 trajectories 为 59 old/medium + 1 new/tight；其 (33003,C4) 的 15 个 method×seed 记录为 14 old + 1 new；P7.7 在同 center、seed=7313 的四 scenario 初始化也仅 C4 改变。这些是同一异常的横向投影，不是第二个独立异常组。

VERIFIED：961 新输出采用 singleton provenance；存量 A7/B8/C5 直接否定当前 full-batch A6/B8/C6 composition 同一性。**若“更大范围”指生成上下文与 canonical population 承诺，确有更广问题；若指观测的跨方法字段失配组数量，仍仅一组。** 不能把其他 239 组直接称为所有条件均正确的原 canonical 人口，也不能未经新证据把 961 条全部宣告错误。

## 8. Consequences for Paired Bootstrap

### 8.1 实际聚合与重采样

VERIFIED，D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py：

- _trajectory_metrics:501–511，24-stage mean；
- _center_metrics:528–530，中心内 seed/scenario mean；
- _make_statistics:555–560，20-center 等权 method mean；
- :578–591，按 center_id 连接 P7.7/baseline，20 个中心差值，以 seed=2904 联合重采样 4000 次；
- :675–678，已保存报告的 difference 列是 replicate means 的均值，不是原样本中心差值均值。前期审计已指出，本次不改统计、不重算 Bootstrap／CI。

D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json:158–168 指定 center unit，paired_rule 包含 “where valid”。完成记录不能替代这个科学条件。

### 8.2 原 CI 可以怎样解释

直接来源 D:\dt-talk\DT_LIFECYCLE_ESCALATION\reports\P7_7_FINAL_HELDOUT_STATISTICS.md:7–10，原样保留：

| 原比较 | 原保存 95% CI |
|---|---|
| P7.7 − B0 | [-0.004331739509, -0.002806662431] |
| P7.7 − B1 | [-0.0005919769468, -0.0003479246183] |
| P7.7 − B2 | [-0.002397977491, -0.001687318467] |
| P7.7 − B8 | [0.000001238427689, 0.00009941572676] |

VERIFIED（数值操作层）：它们是既有 20 个 center-ID-matched、含混合输入上下文差值的重采样区间。输入异常不会自动使存量均值算错，也不会使中心联合重采样的程序机制消失。

NOT_VERIFIED（严格实验推断层）：不能无条件解释为所有组同外生环境、同初始状态、同部署约束下的纯方法差异。33003 一个分量包含 method 与 materialization context 的共同变化；Bootstrap 只重采样已有混合分量，不能补出共同输入反事实或识别其偏差。

Path 1 若保留 CI，宜称原混合存量的中心级差值重采样区间，同步披露不配对事实及严格解释的限制。不要笼统宣布 CI 数字“全部无效”，也不要称严格配对实验已完整验证。未来是否调整推断须由研究者选择，不由本报告自动决定。

NOT_VERIFIED：筛除后 CI 是否跨零、差值方向／大小、排名变化；现有 losses 与 tight tier 不识别污染方向。本次未计算这些事后统计。

## 9. Three Scientific Remediation Options

以下均为方案设计，未执行。选择依据应是既定科学对象和证据强度，不能以论文结果是否改善决定。三路径均保留原始记录／统计，不覆盖历史事实。

### 9.1 Path 1：保留全部原结果并充分披露

可保留：1200 完成事实，原损失／动作／成本／gate 均值作为全体存量描述，已确认算法机制、零 gate 与冻结参数，以及异常组四 baseline 之间的 input parity。

必须降级：所有方法每组同环境／同初始化／同部署条件的全称声明，该组作为严格受控 P7.7 对照的解释，全体原 CI 的纯方法严格配对解释，以及存量完全等于单一 canonical 20-center materialization 的声明。

建议披露文字（供研究者选择，未写入论文）：

> The stored evaluation combined 239 trajectories from a batch-materialized serial phase with 961 trajectories from a singleton-materialized parallel phase. In one of the 240 center–seed–scenario groups (33003, 7313, C4), the Proposed trajectory differed from all four baselines in exogenous data, initial model state, and deployment tier across all 24 stages. The reported full-data means describe these preserved records; the original center-level resampling intervals do not by themselves establish a strictly input-matched method-only comparison.

证据：D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:490、493、896–904、957–958；精确旧入口第 4.2 节；五异常 CSV 第 2–25 行、receipt 第 9–12 行的完整路径见 3.1。

局限：文字可以改变声明范围，不能恢复缺失配对。若核心论文结论要求严格共同输入推断，仅 Path 1 不足。

### 9.2 Path 2：239 matched groups 的事后敏感性分析

**只设计，不筛除、不计算。** 应另行冻结判据和计划并取得授权。

以 scenario/data-role hashes、initial、tier/filter/bank、任务齐全等完整性字段选择 matched groups，不能以 loss、改善幅度、显著性或排名选择。五方法共同去掉同一异常组，不能只删 P7.7 一条，也不能把该分析自动替换原冻结主结果。

中心级方案：

- G_c 是中心剩余共同配对组。19 中心各 12 组，33003 为 11 组；合计 239 组／1195 trajectories，**仍为 20 个统计中心**。
- 先每组平均 24 stages，再中心内对 G_c 等权平均，最后 20 中心等权：
  L_(m,c)=(1/|G_c|)Σ_(g∈G_c)[(1/24)Σ_(t=1)^24 ℓ_(m,g,t)]；
  L_m=(1/20)Σ_c L_(m,c)。
- D_c=L_(P7.7,c)−L_(baseline,c)。若将来授权 Bootstrap，联合重采样中心及其所有配对方法记录；不能把 239 组／stages 当独立中心，也不能全组 pooling 从而降低 33003 的中心权重。
- 4000/2904 为原协议；新敏感性方案须明确是否沿用、聚合／区间／独立输出位置、全部比较和不择优规则，再获授权执行，不能修改旧产物。

依据：D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json:159–164；D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:501–530、578–591；第 3 节全体 parity 检验。

局限：33003 从 12 改 11 组，seed/scenario 构成变化，改变 estimand。虽以完整性而非效果选择，仍是事后分析；不能称原冻结确认性结果，也不能证明 239 组等于原 full-batch canonical 人口。应明确 exploratory sensitivity 与全体描述的区别。本次未算新均值、差值或 CI。

### 9.3 Path 3：新独立协议纠正输入配对

先另行授权一个 outcome-blind 的输入完整性阶段，检查全部 20 IDs 的 canonical materialization；不能根据新模型效果选择 batch 或 singleton。精确旧 runner 已恢复，但仍需明确历史依赖边界和原科学意图，冻结 canonical context。

需要预先冻结的条件（仅设计，不是本次修改指令）：

1. 生成器／依赖版本、data_seed、batch 起点／长度／排序、ID↔slot、类型 schedule、RNG draw order 或 stable sample key；固定 x/y/ts/profile/tier 摘要。若改为新 per-center 协议，明确是新协议，不能假称已恢复旧实现。
2. 在独立输出位置固定每 center 的 base/scenario、每 center–seed 的初始状态，同组全部方法从相同副本开始。预先定义 exact hash 与必要确定性容差，不能事后放宽。
3. 绑定生成器、场景转换、checkpoints/bank、warm-up、参数／operation limits、50-update、cost unit、gate=0、阈值、冻结 estimator/scaler、五方法、24 stages、population、中心统计；不因已见结果重新训练／调参／选择种子。
4. 开始前及恢复时检查同组五方法的 data/initial/tier/filter/bank parity 与 provenance，不能仅凭 legacy allowlist。预先定义部分组恢复、失败、完整组 receipts 和保存规则。
5. 新 manifest、执行来源、receipts、全量 parity 与审计独立保留；不得写回旧 1200 CSV 或只替换 Proposed。
6. 新统计和报告在结果生成前冻结，报告全部比较、负面证据、与旧记录差异及原 heldout 已观察的事实。

| 执行范围 | 能回答的问题 | 局限 |
|---|---|---|
| 单组定向复核，全部五方法共同输入 | 检查已知异常组在同一冻结环境下的状态、约束、结果；可作为局部历史复核 | 不能只运行／替换 P7.7，不能证明另外 19 中心或 961 新任务的 original canonical 同一性；独立保存，是否合入主结果需另行科学论证。 |
| 完整 20×3×4×5 独立重建 | 提供单一新冻结 input protocol 下完整配对／人口／评估 | 成本较高；原 heldout 已被观察，应称完整性纠正后的独立复核，不能称全新未见确认性评估；不得顺便优化参数或覆盖旧结果。 |
| 新预定、未见人口的独立验证 | 检验修订协议在新人口的可复核性与方法证据 | 不能替代旧异常披露；IDs／人口按科学方案定义，不能按有利结果挑选；需单独授权。 |

依据：第 4–5 节精确旧／新入口与生成机制、D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py:461–479 的 guard 缺口及人口组成。更广 context 差异已证实，单组复核不足以认证原全人口；建议先全 20-center input-only 验证，再决定局部还是完整评估。本次未启动任何阶段。

## 10. Recommended Next Step

由研究者先决定希望保留的证据强度：

- 接受充分披露的描述性存量比较：Path 1，降低严格配对推断范围。
- 了解已观测失配组的结论敏感性：另行冻结／授权 Path 2，保持 20 中心聚合，不以是否有利作为采纳标准。
- 坚持全部方法共同环境／初始化／部署约束的严格设计：需要 Path 3 新独立验证；优先全 20-center 输入核验，再冻结实验复核范围，不能自动只替换 P7.7。

本阶段到本报告结束。未创建后续工程，未生成筛选后结果，未运行验证，未修改论文。研究者选择路径和具体范围前不执行修改或实验。

## 11. Remaining Uncertainty

| 未解决事项 | 判定与现有证据边界 | 继续核验条件 |
|---|---|---|
| 旧完整运行环境是否被直接认证 | NOT_VERIFIED：旧 runner/protocol 精确恢复；三生成器在审阅 Git／Oct03 日志未见变更，但旧 receipt 第 11 行仅绑定 core/p7.py，不能覆盖所有依赖／环境。 | 更多已有 environment/source manifest，或另行授权的独立输入验证；不能假称当前文件完整代表旧环境。 |
| context 改变是否是全部数值差异的唯一原因 | INFERRED 为主要直接机制；唯一性和精确数值重演 NOT_VERIFIED。入口改变、混合保留、guard 缺失已 VERIFIED。 | 新冻结反事实／历史复核，保留旧结果，本阶段不执行。 |
| 961 新任务相对 original full-batch 的逐数组／profile 差异 | NOT_VERIFIED：存量 A7/B8/C5 对当前 full-batch A6/B8/C6 不同已 VERIFIED，但不能逐个指定会变的中心。 | 全 20 输入验证另行授权，不能按模型结果选择 context。 |
| 污染对均值差／CI 的方向、幅度 | NOT_VERIFIED：缺匹配反事实；未执行筛除统计。 | Path 2 是敏感性，不等于反事实因果偏差；Path 3 提供新共同输入结果。 |
| 单组纠正能否恢复原全人口严格设计 | NOT_VERIFIED；更广 provenance 不保证。 | 明确 canonical population，全 20 inputs 验证后冻结复核范围。 |
| 更多跨方法失配组 | 本次覆盖字段全量 240 组未发现；不能外推到未保存 trace 全部值或未核验端点。 | 若扩展核验先定义对象；不得随结果移动判据。 |

**NEEDS_RUNTIME_VERIFICATION（未执行）**：canonical batch/single 数值对照、初始模型／候选适配反事实、匹配输入的 losses、纠正后完整评估。新的 Bootstrap／筛除统计同样未获本阶段授权；本报告不是自动批准。

### 11.1 关键已有文件 SHA256 快照

供后续核对实际字节；未创建 sidecar 或归档副本。

| 完整路径 | SHA256 |
|---|---|
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SECTION5_AND_STATS_FINAL_READONLY_EVIDENCE.md | c8870de368cf25437e6a7a97ca9f52c5d3764c4930b1a1bd507fe9178b22a505 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_S3_S4_IMPLEMENTATION_CONSISTENCY_AUDIT.md | 95e97c4c743631fe906376b70a98fe808d4b3a83cb09a4ab87f32b8a2c9281a4 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\configs\P7_7_FINAL_LIFECYCLE_PROTOCOL.json | 6339a9247b984b497d1543198b3a7b7c0cfdf9c7bcfd1c52b47b62e17d2fd0df |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\scripts\run_p7_7_final.py | ced000f213f8fc9b52a859e683fc6d27dd04a268641c3d6024500f56c1c158fe |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p3_2_data.py | 0f5a5bff889a0ac866793dc49b21680f927af13c9e6fc3d5c3d75bbf4d9d5b27 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\data.py | 6cd7e375d40c8ecf390fe37dee270d93890b3981f666e521e17441612f304d5e |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p7.py | 378f2b8644f97e87fa819661da694d1bfcb163e7d183d110edf5f08c9d6dfe3d |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\models.py | 55028939faab38ea23736d191647f33f08ad48f14f204bbecf55bb3d76642e7e |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\protocol.py | 8468b32f245e91c9bcbbb95d93b2dea07b75087d951184fb429cc1f7201cc367 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\core\p6.py | 7597861c7bddd8e32080a3f83eff0ab0bc0f55db6c6b11aec773794f33cc2b07 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\sim.py | 930fa8ebe34a442d53af16a054955580f2d0c41ef2514a3cfd125b0e6905883d |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\imported\ravm_dt\main_cfg.py | fea128a2649301017a2a8ad6cab3db30392e180c2f3aa1216e9a83fefcd5d005 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\execution_status.json | 9595a844666a4956bd8f2c235809e0f4965805578697bf6e9b24a5eeb13fbd75 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\final_metrics_by_method.csv | c0ba7101474e7ad70828d618001b0b36c37e48a27c59e9c1b1187a9b18aa4c6d |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\results\p7_7\final_metrics_by_center.csv | 2b32aa5779b0c632e3c33f2ba662820b45f1ed4ae78385e24c46b760e541ee5a |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\reports\P7_7_FINAL_HELDOUT_STATISTICS.md | 8e4d360a35f9ac9c3cff543b3e17725a3f93eada6cb40a75ed7f5a8a82a8aacd |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\docs\P7_7_FINAL_HELDOUT_PARALLEL_RESOURCE_ADJUSTMENT_20261003.md | c76579e557ec825eda4be1d636a245a366589e1d0b000808e34f47293638cbe5 |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_SCIENTIFIC_AUDIT.json | c25c01b2b89b43e01d22c157a3bbb39d5321d43fe3cefbeb8dfb9500f175b8dd |
| D:\dt-talk\DT_LIFECYCLE_ESCALATION\audits\P7_7_FINAL_HELDOUT_AUTHORIZATION.json | 8f142dccb24a5260f46f4498ac9aa2869db814ceed9c6fafca47f3fbd9fb83da |

## 12. Required Human Authorization Before Any Modification

本任务仅允许新建 D:\dt-talk\DT_LIFECYCLE_ESCALATION\PAPER3_SINGLE_GROUP_INTEGRITY_FORENSIC_REPORT.md。未来需研究者明确授权具体范围：

- 输入-only 20-center 验证：canonical context、依赖／环境、独立产物位置与检查标准。
- Path 2 筛选敏感性／新 Bootstrap：先冻结输入判据、20-center 聚合、区间、全部报告方案。
- 单组五方法、完整评估或新人口验证：先审阅完整协议、预算、input guard、绑定与独立输出位置。
- 新源码／生成器／receipt guard／协议版本：应为新的可审阅变更，保留旧来源链，不追改历史 manifest。
- 论文文字／统计解释：本报告建议不自动写入论文，不自动批准保留严格配对推断。

**绝不能自动执行：**改原源码／冻结配置／模型／种子／零阈值，训练／重新拟合／调参，重跑 final-heldout，新 Bootstrap／筛选后主结果，删除／筛除／覆盖／重命名原记录，Git reset/checkout/clean，远程恢复覆盖本地目录，只替换 Proposed，按改善结果选择方案，或隐去已知反例。新验证不能消除旧实验异常的披露义务。

**最终结论：**已证实实现／协议层根因；观测的跨方法失配仍仅一组，但 wider materialization/provenance 超出一条 Proposed 任务。只修文字不能恢复严格配对推断；若仍坚持该目标，需要另行授权的新独立验证。本次交付报告、保留现状，等待研究者决定下一阶段。
