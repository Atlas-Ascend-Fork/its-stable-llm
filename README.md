<!--
Copyright (c) 2026 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# its-stable-llm

its-stable-llm 是 [CANN 社区 Intelligent Transportation System SIG](https://gitcode.com/cann/community/blob/master/CANN/sigs/intelligent-transportation-system/README.md) 旗下的大模型训练稳定性分析示例仓，面向昇腾 NPU，提供基于 openPangu-Embedded-1B 的 Alpaca 全参数微调脚本、多卡 DDP 对照实验，以及 Rank 级 Loss / 梯度范数诊断日志能力。

---

## 概述

本仓库主要内容包括：

- 基于 [openPangu-Embedded-1B-V1.1](https://ai.gitcode.com/ascend-tribe/openPangu-Embedded-1B-V1.1) 的 Alpaca 全参数微调脚本；
- 对照实验：`S1-1` / `S1-2` / `S1-3`（随机种子策略对照）、`S2-1` / `S2-2`（FP32 / BF16 精度对照）；
- `HookedTrainer` + DDP Communication Hook：在 All-Reduce 前采集各 Rank 本地 Loss 与梯度范数，并写入 JSONL；
- 本地 Alpaca 训练数据（Parquet）。

在同步数据并行（DDP）全参数微调中，参数经 All-Reduce 后全局一致，但聚合前各 Worker 的优化动态仍可能出现差异。训练脚本记录的诊断字段为：

- **`loss_local` / `loss_reduced`**：各 Rank 本地 Loss，以及 Rank0 聚合后的 Loss；
- **`grad_norm_pre_ar` / `grad_norm_reduced`**：All-Reduce 前梯度范数，以及 Rank0 聚合后的梯度范数。

微调模型发布参考：[Hugging Face – jiujiudahaozi/op_pangu](https://huggingface.co/jiujiudahaozi/op_pangu)

---

## 版本配套

请按下列组合选用软件版本，避免混用不同代际的 CANN / 驱动 / torch_npu 导致冲突。本仓库推荐以 **CANN 8.5.0** 为主版本。

| 组件 | 推荐版本 | 说明 |
|------|----------|------|
| 操作系统 | openEuler / Ubuntu / Debian（Linux aarch64 或 x86_64） | 需已安装昇腾驱动 |
| 昇腾驱动（Ascend HDK） | 25.0.X / 25.2.X / 25.3.X / 25.5.X | 与 CANN 8.5.0 官方配套 |
| CANN | **8.5.0** | 安装 Toolkit + ops；勿与其他大版本混用 |
| Python | **3.10.x** | 也可使用 3.9.x / 3.11.x（需与 PyTorch 匹配） |
| PyTorch | 2.6.0 | 与下方 torch_npu 一一对应 |
| torch_npu（Ascend Extension for PyTorch） | 2.6.0.post5 | 对应 GitCode 分支 `v2.6.0-7.3.0` |
| transformers / datasets | 与训练脚本兼容的近期稳定版 | 建议在独立虚拟环境中安装 |
| 目标硬件 | 昇腾 NPU | 示例按单机 8 卡 DDP |

**CANN 8.5.0 其他可选、不冲突的配套组合（整行选用，勿交叉混装）：**

| PyTorch | torch_npu | Python |
|---------|-----------|--------|
| 2.6.0 | 2.6.0.post5 | 3.9 / 3.10 / 3.11 |
| 2.7.1 | 2.7.1.post2 | 3.9 / 3.10 / 3.11 |
| 2.8.0 | 2.8.0.post2 | 3.9 / 3.10 / 3.11 |
| 2.9.0 | 2.9.0 | 3.10 / 3.11 / 3.12 / 3.13 |

版本配套权威说明见：

- [CANN 8.5.0 版本配套关系](https://www.hiascend.com/document/detail/zh/canncommercial/850/releasenote/releasenote_0000.html)
- [Ascend Extension for PyTorch 版本匹配表](https://gitcode.com/Ascend/pytorch)

> 注意：不要将 CANN 8.5.0 与面向 CANN 8.3 / 9.0 等版本的 torch_npu 插件混用；同一环境中只保留一套 Ascend Toolkit。

---

## 环境准备

1. **安装昇腾驱动与 CANN 8.5.0**  
   按官方文档完成 Ascend HDK 与 CANN Toolkit + ops 安装，并确认 `npu-smi info` 可正常查询设备。

2. **配置 CANN 环境变量**  
   参考仓库中的 [`code/fix.sh`](code/fix.sh)。该文件含本机示例绝对路径，请改为本机实际安装目录后执行：

   ```bash
   cd code
   source fix.sh
   # 或使用 CANN 自带脚本，例如：
   # source /usr/local/Ascend/ascend-toolkit/set_env.sh
   ```

3. **创建 Python 虚拟环境并安装依赖**

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip

   # 先安装与 CANN 8.5.0 配套的 PyTorch / torch_npu（以下为推荐组合示例）
   pip install torch==2.6.0
   # 再按 Ascend 官方说明安装对应 torch_npu 2.6.0.post5 wheel

   pip install transformers datasets
   ```

4. **修改脚本中的本地路径**  
   当前训练 / 实验脚本使用硬编码绝对路径（模型、数据、输出）。运行前请将各脚本中的 `model_path` / `data_path` / `output_path` 改为本机路径。  
   仓库已随附数据：`data/train-00000-of-00001-a09b74b3ef9c3b56.parquet`。  
   基座模型请自行准备：[openPangu-Embedded-1B-V1.1](https://ai.gitcode.com/ascend-tribe/openPangu-Embedded-1B-V1.1)。

5. **语法自检（可选）**

   ```bash
   python -m py_compile code/*.py code/experiments/*.py
   ```

---

## 源码下载

```bash
git clone https://gitcode.com/cann/its-stable-llm.git
cd its-stable-llm
```

仓库地址：[https://gitcode.com/cann/its-stable-llm](https://gitcode.com/cann/its-stable-llm)

---

## 学习教程

| 资源 | 说明 |
|------|------|
| [CANN 开发文档](https://www.hiascend.com/document/detail/zh/canncommercial/850/index.html) | CANN 8.5.0 安装、环境与算子开发 |
| [Ascend Extension for PyTorch](https://gitcode.com/Ascend/pytorch) | torch_npu 安装与版本配套 |
| [openPangu-Embedded-1B-V1.1](https://ai.gitcode.com/ascend-tribe/openPangu-Embedded-1B-V1.1) | 基座模型说明与使用 |
| [Alpaca 数据集](https://huggingface.co/datasets/tatsu-lab/alpaca) | 指令微调数据格式参考 |
| `code/run.ipynb` | 启动命令示例 |
| `code/run.log` | 训练日志样例 |
| `code/generate.ipynb` | 推理示例 Notebook |
| `code/experiments/` | S1 / S2 对照实验脚本入口 |

多卡训练示例（需已配置 NPU 与 CANN，并改好脚本路径）：

```bash
cd code
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export PYTHONNOUSERSITE=1
source fix.sh
torchrun --nproc_per_node=8 --master_addr=localhost --master_port=12355 experiments/S1-1.py
```

---

## 目录结构

```text
its-stable-llm/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── OAT.xml                    # 开源合规扫描配置（CANN-2.0）
├── .pre-commit-config.yaml    # 提交前检查（含 oat-check）
├── .gitignore
├── scripts/
│   ├── oat_check.sh           # 本地 OAT / 文件头合规检查
│   └── add_copyright_headers.py
├── code/
│   ├── fix.sh                 # 昇腾 / CANN 环境变量示例（需改本机路径）
│   ├── run.py                 # 主训练脚本（HookedTrainer；子集 1000 条；仅 per-rank JSONL）
│   ├── train_v1.py            # 早期训练脚本（普通 Trainer，无 Hook）
│   ├── crash_test_v1.py       # 稳定性相关脚本
│   ├── crash_test_v2.py
│   ├── generate.ipynb         # 推理示例
│   ├── run.ipynb              # torchrun 启动示例
│   ├── run.log                # 8 卡训练日志样例
│   ├── fusion_result.json
│   └── experiments/
│       ├── run.py             # 实验目录内训练入口（含 Rank0 聚合日志）
│       ├── S1-1.py            # 全 Rank seed=42
│       ├── S1-2.py            # Rank0 seed=42+999，其余 seed=42
│       ├── S1-3.py            # seed=42+rank*10
│       ├── S2-1.py            # FP32（bf16=False）
│       └── S2-2.py            # BF16（bf16=True）
└── data/
    └── train-00000-of-00001-a09b74b3ef9c3b56.parquet
```

---

## 默认超参

`code/experiments/S1-*.py` / `S2-*.py` 默认配置如下：

| 项 | 值 |
|----|-----|
| `num_train_epochs` | 1 |
| `learning_rate` | 5e-5 |
| `weight_decay` | 0.01 |
| `per_device_train_batch_size` | 2 |
| `gradient_accumulation_steps` | 4 |
| `max_length`（tokenize） | 1024 |
| `bf16` | True（`S2-1.py` 为 False，即 FP32） |
| `TrainingArguments.seed` / `data_seed` | 42 |
| `logging_steps` | 1 |
| `dataloader_drop_last` | True |
| Loss | 仅对 Response token 计算（prompt / padding 置为 `-100`） |
| 分布式 | `torchrun --nproc_per_node=8 --master_addr=localhost --master_port=12355` |

`code/run.py` 另使用训练子集 1000 条，并设置 `warmup_steps=200`、`save_steps=100`；仅写 per-rank JSONL。

---

## 实验设置说明

实验脚本通过 `set_seed` / `torch.manual_seed` 控制进程级随机种子；`TrainingArguments(seed=42, data_seed=42)` 保持不变。

### S1-1 — 严格一致性（`code/experiments/S1-1.py`）

- 全部 Rank：`seed = 42`

预期：各 Rank 随机行为更一致，Loss / 梯度范数离散度较低。

### S1-2 — 轻度失配（`code/experiments/S1-2.py`）

- Rank0：`seed = 42 + 999`
- 其余 Rank：`seed = 42`

预期：Worker 级离散度略升，全局平均 Loss 仍可能较平滑。

### S1-3 — 显著失配（`code/experiments/S1-3.py`）

- 各 Rank：`seed = 42 + rank * 10`（如 rank0→42，rank1→52，…）

预期：Loss / 梯度范数离散度更大；全局 Loss 仍可能看起来正常。

### S2-1 / S2-2 — 精度对照

- `S2-1.py`：`bf16=False`（FP32）
- `S2-2.py`：`bf16=True`

S1 / S2 实验脚本均启用 per-rank JSONL 与 Rank0 聚合 JSONL（`loss_reduced` / `grad_norm_reduced`）。

---

## 贡献指南

参与方式与提交规范见：[CONTRIBUTING.md](CONTRIBUTING.md)

---

## 安全声明

安全范围、漏洞报告与敏感信息管理见：[SECURITY.md](SECURITY.md)

---

## 许可证

本项目基于 [CANN Open Software License Agreement Version 2.0](LICENSE) 开源。

---

## 所属 SIG

本仓库归属 CANN 社区 **Intelligent Transportation System SIG（智能交通系统兴趣小组）**：

- SIG 主页：[intelligent-transportation-system/README.md](https://gitcode.com/cann/community/blob/master/CANN/sigs/intelligent-transportation-system/README.md)
- 邮件列表：intelligent-transportation-system@cann.osinfra.cn

---

## 问题反馈

- 功能问题、缺陷与需求：请在本仓库提交 [Issue](https://gitcode.com/cann/its-stable-llm/issues)
- 安全漏洞：请勿公开披露细节，按 [SECURITY.md](SECURITY.md) 中的私密渠道报告
- 贡献代码：请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，再提交 Pull Request

---

## Contributors

Hong Li · Zhen Zhou · Honggang Zhang · Yuping Luo · Xinyue Wang · Han Gong · Zhiyuan Liu
