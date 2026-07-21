# Changelog

本文档记录 its-stable-llm 的重要变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。版本号建议遵循语义化版本规范。尚未发布的改动记录在 `Unreleased` 部分，正式发布时再移动到对应版本条目。

> **关于首个版本怎么写：**  
> 本仓库当前为首次整理发布。首版记为 `[1.0.0]`，在 `Added` 中汇总本版本已交付的内容，而不是留空。后续改动先写入 `Unreleased`，正式发版时再移到新的版本号下。

## [Unreleased]

### Added

- 暂无。

### Changed

- 暂无。

### Fixed

- 暂无。

### Security

- 暂无。

---

## [1.0.0] - 2026-07-21

首次发布。本版本提供 Silent Inconsistency 论文配套的昇腾 NPU 实验代码、Alpaca 训练数据及社区文档。

### Added

- 新增基于 openPangu-Embedded-1B 的 Alpaca 全参数微调训练脚本（`code/run.py`、`code/train_v1.py`）。
- 新增 HookedTrainer 与 DDP Communication Hook，用于在 All-Reduce 前采集各 Rank 本地 Loss 与梯度范数。
- 新增 Per-Rank JSONL 诊断日志与 Rank0 聚合日志写入能力。
- 新增对照实验脚本：
  - `code/experiments/S1-1.py`：严格一致性（统一随机种子）；
  - `code/experiments/S1-2.py`：轻度失配（Rank0 使用不同种子）；
  - `code/experiments/S1-3.py`：显著失配（各 Rank 使用不同种子）。
- 新增精度对照实验脚本：
  - `code/experiments/S2-1.py`：FP32；
  - `code/experiments/S2-2.py`：BF16。
- 新增本地 Alpaca 训练数据 `data/train-00000-of-00001-a09b74b3ef9c3b56.parquet`。
- 新增昇腾环境变量配置脚本 `code/fix.sh`。
- 新增推理示例 `code/generate.ipynb`。
- 新增稳定性相关脚本 `code/crash_test_v1.py`、`code/crash_test_v2.py`。
- 新增项目说明 `README.md`。
- 新增贡献指南 `CONTRIBUTING.md`。
- 新增安全策略 `SECURITY.md`。
- 新增 Apache License 2.0 许可证文件 `LICENSE`。

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

- 部分训练脚本仍使用硬编码绝对路径，换环境部署前需手动修改。
- 当前未提供统一的 `requirements.txt`。
- `crash_test_v1.py` 中测试集路径存在拼写问题，可能无法直接运行。
- README 中提到的 Gradient-Direction Consistency（梯度方向余弦相似度）为论文诊断指标说明；当前训练脚本主要记录 Loss 与梯度范数日志，未实现该指标的在线计算。
- README 中 S1-1 所述 Deterministic `DistributedSampler` 在当前脚本中未显式使用；S1-2 / S1-3 虽导入 `DistributedSampler`，但未在代码中实际调用。

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
