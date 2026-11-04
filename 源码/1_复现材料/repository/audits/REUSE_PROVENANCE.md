# Reuse Provenance

MSA-DTI source repository: `D:/dt-talk/repository`, discovery HEAD `c52e07c999f059e6e2d83f8370be67a630208823`, public release tag `v1.2.7` at `b679181b3133ab9c3058afcde421d36380001f14`.

RAVM-DT source repository: `D:/dt-trustworthy-maintenance`, discovery HEAD `1b84fbcff8c47fb76dafc313f536f04ba8a9287b`, frozen scientific implementation commit `7ae7fabd9a4e335e774fbcba2f38dfa8827bb8f3`.

| Source repo | Source path | Source SHA-256 | Destination | Reuse mode | Modified? |
|---|---|---|---|---|---|
| MSA-DTI | `core/space/models.py` | `a6c73ffac8a0ccad3232f7ea8e75afccc6f0bb7ae5356ba0a02545c67d6e1017` | `imported/msa_dti/space/models.py` | exact copy | no |
| MSA-DTI | `core/space/profile.py` | `d7abbbcebe5c4dde274aa193c20bdfc733c07b7efb16b00c00566c4aff154db3` | `imported/msa_dti/space/profile.py` | exact copy | no |
| MSA-DTI | `core/space/types.py` | recorded in `audits/reuse_hash_manifest.json` | `imported/msa_dti/space/types.py` | exact copy | no |
| MSA-DTI | `core/space/enumerator.py` | recorded in `audits/reuse_hash_manifest.json` | `imported/msa_dti/space/enumerator.py` | exact copy | no |
| MSA-DTI | `results/limited_validation_formal_protocol/candidate_bank/candidate_bank_manifest.json` | `3cc0aa73598e5ddd5fd68f2cfbf46f669be71df8f6a8144deab08451d4178283` | `imported/msa_dti/bank/candidate_bank_manifest.source.json` | exact copy | no |
| MSA-DTI | `.../assets/formal_h1_a1.pt` | `0953c393d04cca7bea80b9bc3b4edfaaaeca330785c7e16a1052ad3868cb5988` | `imported/msa_dti/bank/formal_h1_a1.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a6.pt` | `eb574956ef4f59ff82ba316ffd8dfedd580031f8d818243be77d1207608795ef` | `imported/msa_dti/bank/formal_h1_a6.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a46.pt` | `34b60214405ed2f5d945eea6a3b2121625819222f36c2dc4ecb229e7409f3f8c` | `imported/msa_dti/bank/formal_h1_a46.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a55.pt` | `ad00ee90288cfcaecd550d42979ae9693fa5fb94350482692755cee521449e1f` | `imported/msa_dti/bank/formal_h1_a55.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a56.pt` | `2a4d81b8669207180e496c3a09dd7f9e6b8bc6b41016a1927099077a1749d5de` | `imported/msa_dti/bank/formal_h1_a56.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a57.pt` | `9faaf152f58bb1be4261369914169868b024f4b5baf7ac621b92619ff25682b5` | `imported/msa_dti/bank/formal_h1_a57.pt` | exact binary copy | no |
| MSA-DTI | `.../assets/formal_h1_a62.pt` | `3bc0540c925c310dbed91dff81d29f9900c109d690fea9a93fc06727cb969b5d` | `imported/msa_dti/bank/formal_h1_a62.pt` | exact binary copy | no |
| MSA-DTI | `outputs/final_e2e_c23_external_d2904_t2904/source_assets/medet_style_h1_a57.pt` | `304c1eac43f12f99ac1693eaa6a3f29238491562b21a18556a51bb27f475a59a` | `imported/msa_dti/bank/medet_style_h1_a57.pt` | exact binary copy; same architecture, distinct source initialization | no |
| RAVM-DT | `vendor/sim.py` | `930fa8ebe34a442d53af16a054955580f2d0c41ef2514a3cfd125b0e6905883d` | `imported/ravm_dt/sim.py` | exact copy | no |
| RAVM-DT | `vendor/main_cfg.py` | `fea128a2649301017a2a8ad6cab3db30392e180c2f3aa1216e9a83fefcd5d005` | `imported/ravm_dt/main_cfg.py` | exact copy | no |
| RAVM-DT | `core/statistics.py` | `e8ef1e2963c60e8b3102d48e19472d902f2666b5c5a5b204a5cd1c6dcbe7a415` | `imported/ravm_dt/statistics.py` | exact copy | no |
| RAVM-DT | `core/protocol.py` | `48254f026a096767271ef784e5ed22f8b24ab3369bf3614a8e23c80b626eff15` | third-paper `core/protocol.py` | behaviorally wrapped; assessment terminology and local root isolation | yes, independent rewrite |
| RAVM-DT | `core/models.py` | `b38b29b74ff4191add5e8c48e9d916529afb67f801830c68e290f07deacfa656` | third-paper `core/models.py` | adaptation/evaluation semantics wrapped around MSA-DTI architectures | yes, independent rewrite |

The full machine-readable source/destination hash comparison is generated as `audits/reuse_hash_manifest.json`. Any mismatch between an “exact copy” source and destination is an audit failure.
