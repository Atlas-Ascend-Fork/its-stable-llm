<!--
Copyright (c) 2026 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->

# Changelog

本文档记录 its-stable-llm 的重要变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。版本号建议遵循语义化版本规范。尚未发布的改动记录在 `Unreleased` 部分，正式发布时再移动到对应版本条目。

> **关于首个版本怎么写：**  
> 本仓库当前为首次整理发布。首版记为 `[1.0.0]`，在 `Added` 中汇总本版本已交付的内容，而不是留空。后续改动先写入 `Unreleased`，正式发版时再移到新的版本号下。

## [Unreleased]

### Added

- 新增 `OAT.xml`，配置 CANN-2.0 许可证与 Copyright 扫描策略（参考 ops-nn），并排除 json/parquet/csv/log 等无法添加文件头的类型。
- 新增 `.pre-commit-config.yaml` 与 `scripts/oat_check.sh`，用于提交前合规检查（参考 ops-nn）。
- 为可注释源文件补充 CANN Open Software License Agreement Version 2.0 Copyright / License 文件头（版权主体为 Southeast University）。
- 新增 `.gitignore`。

### Changed

- 根目录 `LICENSE` 由 Apache License 2.0 切换为 CANN Open Software License Agreement Version 2.0。
- 文件头与 `OAT.xml` 版权主体确认为 Southeast University（东南大学）。
- 按 `code/` 实际脚本与 `code/run.log` / `code/run.ipynb` 对齐 `README.md`、`CONTRIBUTING.md`、`SECURITY.md`、`CHANGELOG.md`、`LICENSE`。

### Fixed

- 暂无。

### Security

- 暂无。

---

## [1.0.0] - 2026-07-21

首次发布。本版本提供面向昇腾 NPU 的 Alpaca 全参数微调实验代码、诊断日志、训练数据及社区文档。

### Added

- 新增基于 openPangu-Embedded-1B 的 Alpaca 全参数微调训练脚本（`code/run.py`、`code/train_v1.py`）。
- 新增 HookedTrainer 与 DDP Communication Hook，用于在 All-Reduce 前采集各 Rank 本地 Loss 与梯度范数。
- 新增 Per-Rank JSONL 诊断日志；在 `code/experiments/` 实验脚本中额外写入 Rank0 聚合日志（`loss_reduced` / `grad_norm_reduced`）。说明：`code/run.py` 当前仅启用 per-rank 日志。
- 新增对照实验脚本：
  - `code/experiments/S1-1.py`：全 Rank `seed=42`；
  - `code/experiments/S1-2.py`：Rank0 `seed=42+999`，其余 `seed=42`；
  - `code/experiments/S1-3.py`：`seed=42+rank*10`。
- 新增精度对照实验脚本：
  - `code/experiments/S2-1.py`：FP32（`bf16=False`）；
  - `code/experiments/S2-2.py`：BF16（`bf16=True`）。
- 新增本地 Alpaca 训练数据 `data/train-00000-of-00001-a09b74b3ef9c3b56.parquet`。
- 新增昇腾环境变量配置脚本 `code/fix.sh`。
- 新增推理示例 `code/generate.ipynb`、启动示例 `code/run.ipynb`、训练日志样例 `code/run.log`。
- 新增稳定性相关脚本 `code/crash_test_v1.py`、`code/crash_test_v2.py`。
- 新增项目说明 `README.md`。
- 新增贡献指南 `CONTRIBUTING.md`。
- 新增安全策略 `SECURITY.md`。
- 新增许可证文件 `LICENSE`（首版为 Apache License 2.0；后续在 Unreleased 切换为 CANN-2.0）。

### Changed

- 不适用（首个正式版本）。

### Deprecated

- 暂无。

### Removed

- 暂无。

### Fixed

- 暂无。

### Security

- 明确项目默认本地训练与日志采集，不启动对外网络服务。
- 明确禁止在仓库中提交密码、Token、私钥、内部地址和其他敏感信息。
- 增加普通用户运行、文件权限和依赖安装安全建议（见 `SECURITY.md`）。

### 已知限制

- 部分训练脚本仍使用硬编码绝对路径，换环境部署前需手动修改 `model_path` / `data_path` / `output_path`。
- 当前未提供统一的 `requirements.txt`。
- `crash_test_v1.py` 中测试集路径存在 `.parquet.parquet` 拼写问题，且 `data_files` 键与 `ds[...]` 访问可能不一致，可能无法直接运行。
- 当前训练脚本主要记录 Loss 与梯度范数 JSONL，**未实现**梯度方向余弦相似度的在线计算。
- S1-2 / S1-3 虽导入 `DistributedSampler`，但未在代码中实际调用；实验差异主要来自 `set_seed` / `torch.manual_seed`，`TrainingArguments.seed` / `data_seed` 仍为 42。
- `code/run.py` 使用训练子集 1000 条，且未接入 Rank0 聚合 logger。

---

## 版本记录模板

正式发布新版本时，请复制以下模板，并将版本号和日期替换为实际信息：

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- 新增功能。

### Changed

- 行为、接口、配置或依赖变化。

### Deprecated

- 已弃用但尚未删除的功能。

### Removed

- 已删除的功能。

### Fixed

- Bug 修复。

### Security

- 安全修复或安全策略变化。
```

## 记录规则

更新 `CHANGELOG.md` 时请遵循以下规则：

1. 只记录对用户、开发者、测试或部署有实际影响的变更。
2. 不逐条复制全部 Commit。
3. 使用明确、可理解的描述。
4. 对不兼容变化显著标注。
5. 对配置格式、启动命令、输入输出和默认行为变化进行说明。
6. 对性能和训练结果变化说明测试条件。
7. 对安全修复避免在补丁发布前公开可利用细节。
8. 每个正式版本必须包含版本号和发布日期。
9. 尚未发布的变更统一放在 `Unreleased`。
10. 发布后将对应内容从 `Unreleased` 移入正式版本条目。

## 变更类别说明

| 类别 | 含义 |
|---|---|
| Added | 新增功能、文件、配置或测试 |
| Changed | 已有行为、接口、默认值或依赖变化 |
| Deprecated | 即将删除的功能 |
| Removed | 已删除的功能 |
| Fixed | Bug 修复 |
| Security | 安全修复和安全策略变化 |

## 版本历史补录

如果 its-stable-llm 后续已存在正式发布版本，请根据 Release、Tag、Commit 和历史文档补录版本记录。补录时不得猜测版本日期、性能数据或测试结论，应以可审计的仓库记录和测试材料为准。
