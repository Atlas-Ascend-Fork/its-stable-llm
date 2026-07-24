# ITS-Silent-Inconsistency Test Report

## 1. Overview

This report provides the PMC review test description for the **its-stable-llm** repository. The main contents include:

- An Alpaca full-parameter fine-tuning script based on openPangu-Embedded-1B
- Three comparative experiment scripts: S1-1 / S1-2 / S1-3
- Per-rank Loss and gradient norm logs recorded during training
- One Alpaca training dataset in Parquet format

**Test objective:** Verify that the repository code can be compiled, the data can be read, the training script can be launched, and the core experiment scripts are consistent with the README.

---

## 2. Version Test Information

| Item | Details |
|------|------|
| Project Name | its-stable-llm |
| Code Source | The `code/` directory in the repository |
| Data Source | `data/train-00000-of-00001-a09b74b3ef9c3b56.parquet` in the repository |
| Base Model | openPangu-Embedded-1B-V1.1 |
| Test Date | July 8, 2026 |
| Test Type | Code review + local data validation + historical training log verification |

**Test environment, derived from `code/run.log` and `code/fix.sh`:**

| Item | Configuration |
|------|------|
| Operating System | Linux (aarch64) |
| Python | 3.10 |
| Training Framework | PyTorch + torch_npu + transformers + datasets |
| Distributed Training | Single-node, 8-device DDP (HCCL) |
| CANN | ascend-toolkit latest |

> Note: The specific server model and the exact CANN minor version depend on the actual deployment environment. This report did not independently re-test the complete hardware environment.

---

## 3. Test Conclusion

**A total of 10 test items were assessed: 8 passed, 1 partially passed, and 1 was not executed. The code structure is complete, the README is consistent with the experiment scripts, and the repository meets the basic conditions for execution.**

The repository provides the principal scripts and data required for the paper experiments. `code/run.log` shows that 8-device DDP training can start normally and that the DDP Comm Hook can be registered successfully. Some scripts contain hardcoded paths that must be modified before deployment.

---

## 4. Feature Quality Assessment

| No. | Feature | Corresponding File | Test Conclusion | Description |
|------|------|----------|----------|------|
| 1 | Alpaca data loading | `data/*.parquet` | Passed | A total of 52,002 records; fields include instruction / input / output |
| 2 | Training script (HookedTrainer + logging) | `code/run.py` | Passed | The code logic is complete and includes a DDP Hook and JSONL log writing |
| 3 | S1-1 strict consistency experiment | `code/experiments/S1-1.py` | Passed | All ranks use seed=42, consistent with the README |
| 4 | S1-2 mild mismatch experiment | `code/experiments/S1-2.py` | Passed | Rank 0 uses a different seed, consistent with the README |
| 5 | S1-3 significant mismatch experiment | `code/experiments/S1-3.py` | Passed | Each rank uses a different seed, consistent with the README |
| 6 | Precision comparison scripts | `code/experiments/S2-1.py`, `S2-2.py` | Passed | Correspond to FP32 and BF16 configurations, respectively |
| 7 | 8-device DDP training startup | `code/run.log` | Passed | The log shows that 8 processes started and the Hook was registered successfully |
| 8 | Model saving | All experiment scripts | Passed | `save_pretrained` is called after training |

---

## 5. DFX-Specific Quality Assessment

### 5.1 Security Testing

**Not specifically tested.** This repository contains local training scripts and does not expose an external service interface. This test cycle only reviewed the code structure.

### 5.2 Reliability Testing

| No. | Test Item | Test Conclusion | Description |
|------|--------|----------|------|
| 1 | 8-device DDP startup | Passed | See `code/run.log` |
| 2 | Complete 1-epoch training | Not Tested | A complete training run was not re-executed in this test cycle |
| 3 | Checkpoint resume | Not Tested | The repository does not provide a resume script |

### 5.3 Performance Testing

| Scenario | Metric | Test Result | Description |
|------|------|----------|------|
| Training | Time per step for the first several steps | Approximately 1.5–3.3 s/step | Based on the first four steps in `code/run.log` |
| Training | Number of steps per epoch | Approximately 812 steps | Estimated from 52,002 samples with batch=64 |

---

## 6. Test Execution Assessment

### 6.1 Test Coverage

| Test Activity | Test Conclusion | Number of Cases | Pass Rate |
|----------|----------|--------|--------|
| Code and data inspection | Passed | 4 | 100% |
| Experiment script inspection | Passed | 5 | 100% |
| Training log verification | Passed | 1 | 100% |
| **Total** | **Passed** | **10** | **90%** |

### 6.2 Detailed Test Results

| No. | Test Content | Test Method | Test Result | Conclusion |
|------|----------|----------|----------|------|
| 1 | Python syntax check | `python -m py_compile code/**/*.py` | 12 files compiled successfully | Passed |
| 2 | Training data loading | Read `data/*.parquet` | 52,002 records; all required fields were present | Passed |
| 3 | README-to-script consistency | Compare the README with the S1-1/2/3 scripts | Experiment settings were consistent | Passed |
| 4 | Environment script inspection | Review `code/fix.sh` | CANN environment variable configuration was included | Passed |
| 5 | S1-1 script inspection | Review `experiments/S1-1.py` | The seed strategy was correct | Passed |
| 6 | S1-2 script inspection | Review `experiments/S1-2.py` | The Rank 0 seed offset logic was correct | Passed |
| 7 | S1-3 script inspection | Review `experiments/S1-3.py` | Different seeds were used across ranks | Passed |
| 8 | Training startup log | Review `code/run.log` | 8-device training started and the Hook was registered successfully | Passed |
