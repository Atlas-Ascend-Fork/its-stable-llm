<!-- Copyright (c) 2026 Southeast University. This program is free software, you can redistribute it and/or modify it under the terms and conditions of CANN Open Software License Agreement Version 2.0 (the "License"). Please refer to the License for details. You may not use this file except in compliance with the License. THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE. See LICENSE in the root of the software repository for the full text of the License. -->

# Contributing to its-stable-llm

感谢你对 its-stable-llm 的关注与贡献。本仓库主要内容包括：

* 基于 openPangu-Embedded-1B 的 Alpaca 全参数微调脚本；
* 对照实验：S1-1 / S1-2 / S1-3（随机种子策略）、S2-1 / S2-2（FP32 / BF16）；
* 训练过程中记录各 Rank 的 Loss 与梯度范数 JSONL 日志；
* Alpaca 训练数据（Parquet）。

为保证代码质量、实验结果可复现以及社区协作效率，请在提交 Issue 或 Pull Request（PR）前阅读本指南。

## 1. 贡献范围

欢迎以下类型的贡献：

* Bug 修复；
* 训练脚本、诊断日志或实验设置改进；
* 新增或补充实验脚本（如精度消融、更多对照设置）；
* 数据处理与 Loss Mask 逻辑优化；
* 测试用例、测试日志与测试报告补充；
* 文档、示例和使用说明改进；
* 依赖管理与环境配置改进（如 `requirements.txt`）；
* 安全问题修复；
* 代码重构和工程质量提升。

对于影响实验设置（随机种子、采样策略、精度、Loss 计算方式）或诊断指标含义的改动，请在 PR 中说明改动原因、实现逻辑和验证方法。

## 2. 开发与贡献流程

推荐按照以下流程提交贡献：

1. Fork 本仓库到个人账号。
2. 从最新主分支创建独立开发分支。
3. 在开发分支中完成代码、测试和文档修改。
4. 执行必要的语法检查和相关验证。
5. 提交清晰、可追溯的 Commit。
6. 将开发分支推送到个人远程仓库。
7. 向本仓库发起 PR。
8. 根据维护者的检视意见完成修改。
9. 确认所有检视意见已闭环后，由维护者合入。

建议的分支命名方式：

```text
feature/<简短功能名称>
fix/<简短问题名称>
docs/<文档名称>
test/<测试名称>
refactor/<重构内容>
```

示例：

```text
feature/add-cli-path-args
fix/crash-test-parquet-path
docs/update-experiment-readme
test/add-s1-seed-check
```

请避免直接在主分支上开发或提交未经验证的修改。

## 3. Issue 创建规范

its-stable-llm 的 Issue 创建与管理流程遵循 CANN community 仓中的统一规范。提交 Issue 前，请先阅读 community 仓中的 Issue 操作指南，并按照社区要求填写问题描述、复现步骤、环境信息和相关日志。

Issue 操作指南请参考：

```text
https://gitcode.com/cann/community/blob/master/contributor/issue-operation.md
```

在遵循社区统一 Issue 流程的基础上，its-stable-llm 项目建议根据问题类型补充以下项目信息。

### 3.1 Bug Issue

提交 Bug Issue 时，建议结合 its-stable-llm 项目特点提供以下信息：

* 问题标题；
* 分支、版本或 Commit ID；
* 操作系统、Python 版本；
* PyTorch / torch_npu / transformers / datasets 等依赖版本；
* CANN 与驱动版本（如涉及 NPU 训练）；
* NPU 卡数与启动命令（如 `torchrun --nproc_per_node=8 ...`）；
* 使用的实验脚本（如 `code/experiments/S1-1.py`）；
* 实际结果；
* 预期结果；
* 完整错误信息和必要日志；
* 最小复现步骤；
* 问题出现频率；
* 是否存在临时规避方法。

推荐标题格式：

```text
[Bug] <问题简述>
```

示例：

```text
[Bug] S1-2 在 8 卡 DDP 启动时 Comm Hook 未注册
```

### 3.2 功能建议 Issue

提交功能建议 Issue 时，建议说明：

* 当前问题或使用场景；
* 建议增加或修改的能力；
* 预期行为；
* 对现有实验脚本、日志格式、训练超参和兼容性的影响；
* 可选的实现思路；
* 是否愿意参与开发或测试。

推荐标题格式：

```text
[Feature] <功能简述>
```

### 3.3 文档或测试 Issue

文档或测试相关 Issue 可使用以下标题格式：

```text
[Docs] <文档问题简述>
[Test] <测试问题简述>
```

请勿在公开 Issue 中提交密码、Token、私钥、内部地址、个人隐私数据或其他敏感信息。安全漏洞请按照 `SECURITY.md` 或 CANN community 仓中的安全问题处理流程报告。

## 4. Pull Request 提交规范

### 4.1 基本要求

每个 PR 应：

* 聚焦一个明确问题或一组紧密相关的改动；
* 避免夹带无关格式化或大范围无意义修改；
* 说明改动内容和改动原因；
* 关联对应 Issue；
* 说明测试环境、测试方法和测试结果；
* 对新增或修改功能补充必要验证；
* 对接口、配置、目录或行为变化同步更新文档；
* 不包含密码、Token、私钥或敏感地址；
* 不提交无关的大文件、缓存、临时文件、本地模型权重或训练输出；
* 保证新增文件的许可证和第三方依赖兼容；
* 完成所有检视意见闭环。

### 4.2 PR 描述建议

PR 描述至少应包含：

```markdown
## 变更描述 / Description

说明本 PR 做了什么以及为什么需要该改动。

## 改动类型 / Change Type

- [ ] Bug 修复 / Bug Fix
- [ ] 新功能 / New Feature
- [ ] 性能优化 / Performance
- [ ] 代码重构 / Refactoring
- [ ] 文档更新 / Documentation
- [ ] 测试相关 / Test
- [ ] 其它 / Other

## 关联 Issue / Related Issues

- Closes #
- References #

## 测试信息 / Testing

说明测试环境、执行命令、输入数据和关键结果。

## 检查清单 / Checklist

- [ ] 代码符合规范
- [ ] 相关验证已执行
- [ ] 文档已更新
- [ ] 无硬编码敏感信息
- [ ] 提交信息符合规范
```

只有在 PR 合入后应自动关闭 Issue 时才使用 `Closes #编号`；仅用于说明关联关系时使用 `References #编号`。

## 5. 代码规范

### 5.1 Python 代码

* 使用清晰、可读的 Python 代码；
* 建议遵循 PEP 8；
* 函数、类、变量和模块命名应表达实际含义；
* 公共函数和复杂逻辑应提供必要注释或 Docstring；
* 避免重复代码和不必要的全局状态；
* 避免硬编码本地绝对路径；
* 模型路径、数据路径、输出路径应优先使用相对路径、环境变量或命令行参数；
* 新增异常应提供明确的错误信息；
* 不得静默忽略可能影响训练结果或诊断日志正确性的错误；
* 不得在源码中写入账号、密码、Token、私钥或内部网络地址。
* 新增或修改可注释源文件时，应保留 / 补充仓库统一的 CANN Open Software License Agreement Version 2.0 Copyright 文件头（与根目录 LICENSE 一致）；json / csv / parquet / 日志等无法添加注释的文件除外。合规检查见根目录 OAT.xml 与 scripts/oat_check.sh。

### 5.2 实验脚本与数据

对 `code/experiments/` 或 `data/` 进行修改时，应：

* 保持与 README 中实验设置说明一致，或同步更新 README；
* 修改随机种子、采样策略、精度（bf16/fp32）、Loss Mask 时，在 PR 中说明对 S1 / S2 实验含义的影响；
* 修改诊断日志字段时，说明新旧字段差异；
* 避免混入个人、本地或敏感数据；
* 不提交完整模型权重、大规模中间 checkpoint 或无关日志大文件；
* 必要时提供修改前后的对比说明。

当前主要目录约定：

```text
code/                 训练与实验脚本（含 fix.sh、run.py、run.ipynb、run.log）
code/experiments/     S1-1 / S1-2 / S1-3 / S2-1 / S2-2 及 experiments/run.py
data/                 Alpaca Parquet 训练数据（脚本内路径需改为本机路径）
```

实验种子策略以代码为准，并与 README 保持一致：

* `S1-1.py`：全 Rank `seed=42`
* `S1-2.py`：Rank0 `seed=42+999`，其余 `seed=42`
* `S1-3.py`：`seed=42+rank*10`
* `S2-1.py` / `S2-2.py`：精度对照（FP32 / BF16）；`TrainingArguments.seed` / `data_seed` 均为 42

说明：S1 差异主要来自 `set_seed` / `torch.manual_seed`；当前未显式使用 `DistributedSampler`。

## 6. 测试要求

提交 PR 前，至少执行与改动相关的检查。

### 6.1 Python 语法检查

```bash
python -m py_compile code/*.py code/experiments/*.py
```

### 6.2 依赖与环境

本仓库当前未提供统一的 `requirements.txt`。贡献涉及依赖变更时，请在 PR 中写明：

* Python 版本；
* PyTorch / torch_npu / transformers / datasets 等关键版本；
* 是否依赖 Ascend CANN 与 `code/fix.sh` 中的环境变量。

建议在隔离的虚拟环境中安装依赖。如你补充了 `requirements.txt`，请在 PR 中一并说明安装方式。

### 6.3 基础功能验证

根据改动范围选择验证方式。示例：

```bash
# 语法与导入相关改动：至少完成 py_compile

# 数据加载相关改动：确认 Parquet 可正常读取
python -c "from datasets import load_dataset; ds=load_dataset('parquet', data_files={'train':'data/train-00000-of-00001-a09b74b3ef9c3b56.parquet'}); print(len(ds['train']), ds['train'].column_names)"

# 分布式训练相关改动（需昇腾 NPU 环境）：
cd code
source fix.sh
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
torchrun --nproc_per_node=8 --master_addr=localhost --master_port=12355 experiments/S1-1.py
```

如启动命令与当前仓库脚本不一致，以实验脚本实际内容为准，并同步更新 `README.md` 等相关文档。

### 6.4 实验设置与日志验证

涉及实验脚本或诊断日志改动时，应至少验证：

* S1-1 / S1-2 / S1-3 的随机种子策略仍符合 README 与代码实现（见上文）；
* DDP Comm Hook 可正常注册（参考 `code/run.log` 中 `DDP comm hook registered`）；
* Per-Rank 日志字段（如 `loss_local`、`grad_norm_pre_ar`）可正常写入；
* 对 `code/experiments/` 脚本：Rank0 聚合日志字段（如 `loss_reduced`、`grad_norm_reduced`）含义清晰；
  （`code/run.py` 当前仅写 per-rank 日志，未接入 Rank0 聚合 logger）
* 数据预处理中 Response-only Loss Mask 行为正确。

无 NPU 环境时，至少完成语法检查、静态代码审查，并在 PR 中标明未执行端到端训练。

### 6.5 结果验证

涉及训练逻辑、实验设置或诊断指标的修改时，PR 应提供：

* 测试环境（含卡数，如适用）；
* Commit ID；
* 执行命令；
* 使用的脚本与数据；
* 关键输出或关键日志片段；
* 修改前后对比说明；
* 已知限制或未覆盖范围。

不得仅以截图代替可复现的测试命令和原始结果。

## 7. Commit 信息规范

Commit 信息应简洁说明改动类型和内容。推荐格式：

```text
<type>: <简短描述>
```

常用类型：

```text
feat      新功能
fix       Bug 修复
perf      性能优化
refactor  代码重构
docs      文档更新
test      测试相关
build     构建或依赖修改
ci        持续集成修改
chore     其它维护工作
security  安全修复
```

示例：

```text
feat: add CLI args for model and data paths
fix: correct crash_test parquet filename
docs: clarify S1-2 seed strategy
test: add py_compile check for experiment scripts
```

一个 Commit 应尽量对应一个清晰目的。

## 8. 交付件清单

提交功能、实验脚本、数据处理或诊断相关改动时，请根据实际范围检查以下交付件：

* [ ] 源代码；
* [ ] 必要的最小示例数据说明（如适用）；
* [ ] 相关测试或验证步骤；
* [ ] 测试执行命令；
* [ ] 测试日志或关键结果；
* [ ] README 或使用文档；
* [ ] 实验设置 / 日志字段说明；
* [ ] `CHANGELOG.md` 更新（如仓库已维护）；
* [ ] 第三方依赖及许可证说明；
* [ ] 安全影响说明；
* [ ] 已知问题和限制说明。

如某项不适用，请在 PR 中标注 `N/A`，不要直接删除或忽略。

## 9. 文档要求

出现以下变化时，应同步更新文档：

* 安装方式或环境依赖变化；
* Python / PyTorch / torch_npu / transformers 等版本要求变化；
* 启动命令或脚本入口变化；
* 目录结构变化；
* 实验设置（S1 / S2）含义变化；
* 诊断日志字段或输出路径变化；
* 数据格式变化；
* 已知限制变化。

## 10. PR 检视与合入

维护者可能从以下方面检视 PR：

* 需求和实现是否一致；
* 代码逻辑是否正确；
* 实验设置与 README 是否一致；
* 是否引入兼容性问题；
* 验证是否充分且结果可复现；
* 文档是否同步；
* 是否存在敏感信息或安全风险；
* 第三方依赖及许可证是否合规；
* `CHANGELOG.md` 是否更新（如适用）。

提交者应及时回复检视意见。未经确认的问题不得以删除讨论、隐藏日志或修改结论的方式规避。

## 11. 行为准则

参与社区协作时，请保持专业、尊重和建设性：

* 针对技术问题讨论，不进行人身攻击；
* 尊重不同背景和经验水平的贡献者；
* 提供可验证的事实、日志和依据；
* 对测试失败、限制和已知问题如实说明；
* 不伪造测试结果、训练曲线或性能数据。

感谢你为 its-stable-llm 做出的贡献。
