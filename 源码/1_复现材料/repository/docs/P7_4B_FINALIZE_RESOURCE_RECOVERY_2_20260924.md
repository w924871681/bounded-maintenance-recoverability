# P7.4B Finalize Resource Recovery 2 — 2026-09-24

## Trigger and preserved state

Under the separately committed direct-resume amendment, the exact frozen
`C:/Users/92487/anaconda3/python.exe -u scripts/run_p7_4b.py finalize`
command was launched once at 2026-09-24 15:29:41 Asia/Shanghai as PID 24832.
The pre-launch integrity, paired-path, preflight, and memory checks are recorded
in the monitoring record; the launch logs are
`results/p7_4b/finalize_direct_20260924_152941_stdout.log` and `_stderr.log`.

At approximately 15:58–15:59 Asia/Shanghai, available physical memory was
1.269 GiB and, eleven seconds later, 0.399 GiB. Both readings were below the
established 1.5 GiB two-sample runtime stop boundary. PID 24832 was verified
as the exact P7.4B finalize command and was the only process stopped. No
matching P7.4B Python process remained. WeChat/Weixin, QQMusic, and every
other application/process were left untouched. Finalize stderr and stdout
were empty. Available memory was 1.714 GiB immediately after the stop and
0.878 GiB on a subsequent check, indicating ongoing external fluctuation.

Fit and Validation materialization remain at 288/288. All eight intermediate
files listed in `P7_4B_FINALIZE_USER_PAUSE_20260924.md` were checked after the
stop and their SHA-256 hashes still match that record exactly. No
`leave_one_center_out.csv`, final report, or final scientific audit was
produced. In-memory bootstrap progress is not recoverable. There is no
P7.4B scientific PASS/FAIL verdict yet, and this is a resource stop rather
than a scientific failure.

## Deferred execution-only recovery

Do not launch another finalize process while available memory is low. Continue
fifteen-minute read-only monitoring and report memory/status; the scientific
ETA is unavailable while execution is deferred. The direct-resume amendment's
minimum remains two fresh readings at least ten seconds apart of at least
2.3 GiB available, budgeting 0.8 GiB for the process and retaining the 1.5
GiB runtime reserve. This is a minimum launch gate, not a guarantee against
external memory swings. Do not close or otherwise interfere with other apps.

Before any later launch, reconfirm no matching process/orphan, frozen preflight,
all 288 Validation trajectory/scales/integrity receipts and stagewise A0/A1
path equality, and the eight persisted intermediate hashes. Use only the exact
frozen finalize command and new timestamped logs. Keep the two-sample 1.5 GiB
runtime stop rule. Never modify scientific inputs, silently retry a
scientific/leakage/pairing/scale/hash failure, or access heldout centers
33000–33019, Alibaba, or P8.
