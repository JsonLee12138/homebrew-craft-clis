# Implementation Plan: homebrew-craft-clis

## Overview

构建并维护全自动、零编译的 macOS Homebrew Tap 仓库 `JsonLee12138/homebrew-craft-clis`。
该仓库通过 Python 3 标准库脚本与 GitHub Actions 每日定时巡检 `storytold` 组织，自动发现发布包含 `*-cli-*-macos-universal.zip` 和 `SHA256SUMS.txt` 的产品，自动生成 Homebrew Formula（`Formula/<app>-cli.rb`）并同步刷新 `README.md` 中的产品清单。

## Architecture Decisions

- **零依赖 Python 3 标准库**：使用 `urllib.request`、`json`、`re`、`concurrent.futures`、`pathlib`、`unittest`，无任何 pip 依赖，CI 和本地即开即用。
- **Token 认证与并发优化**：优先使用 `GITHUB_TOKEN` 环境变量；若本地未设置且处于 macOS/终端环境，尝试通过 `gh auth token` 读取以避免 GitHub 匿名 API 速率限制（60 次/小时）。使用 `ThreadPoolExecutor` 并发获取 releases 提升同步速度至 15 秒内。
- **精准哈希校验**：严格从官方发布包含的 `SHA256SUMS.txt` 提取 64 位 SHA256，绝不伪造或留空哈希。
- **Formula 规范与 Homebrew 兼容性**：遵循 Homebrew 4.x/7.x DSL 规范，类名采用 PascalCase（如 `craft-anything-cli` -> `CraftAnythingCli`），声明 `depends_on :macos`，`bin.install "<app>-cli"`。
- **保护策略与幂等性**：除非显式列入 `config.json` 的 `exclude_repos`，否则不随意删除已存在 Formula。重复执行同步脚本输出 100% 幂等，无版本更新时 `git diff` 为空。
- **CI 最小权限与自动化**：GitHub Actions 工作流遵循最小权限原则（顶层 `contents: read`，任务层 `contents: write`），定时 09:17 CST（UTC 01:17）运行，且带 `workflow_dispatch` 手动触发，集成测试与 Ruby 语法门禁。

## Task List

### Phase 1: Foundation & Git Setup
- [ ] Task 1: 初始化 Git 仓库、`.gitignore` 与 `config.json` 基础配置

### Checkpoint: Foundation
- [ ] 本地 Git 仓库初始化完成，关联远程 `origin`，基础文件到位

### Phase 2: Core Logic & Tests (TDD)
- [ ] Task 2: 编写同步与解析核心逻辑 `scripts/sync.py` 及完整单元测试 `tests/test_sync.py`

### Checkpoint: Core Logic Verification
- [ ] 单元测试 `python3 -m unittest discover -s tests -v` 全部通过，覆盖类名转换、SHA256 解析、正则匹配、README 替换与异常处理

### Phase 3: Formula Generation & Idempotence
- [ ] Task 3: 运行同步生成 16 个 Formula 并编写/更新 `README.md`
- [ ] 校验 `ruby -c Formula/*.rb` 语法及二次执行的幂等性（无额外 diff）

### Checkpoint: Formula Quality
- [ ] 全部 16 个 Formula 语法合规，README 表格准确更新，两次运行 `git status --porcelain` 为空

### Phase 4: CI/CD Pipeline
- [ ] Task 4: 编写 GitHub Actions 工作流 `.github/workflows/sync.yml`

### Checkpoint: CI Quality
- [ ] 遵循最小权限、定时 Cron 表达式准确、包含测试与 Ruby 语法门禁、安全推送

### Phase 5: Verification & Push
- [ ] Task 5: 本地实测 Homebrew 安装及推送代码至 GitHub 远程仓库

### Checkpoint: Complete
- [ ] 远程 `main` 分支已推送，代码、CI、文档与 Formula 均就绪

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| GitHub API 速率限制 (403 Rate Limit) | High | 支持 `GITHUB_TOKEN` 环境变量，并在本地未配置时自动回退读取 `gh auth token` |
| 上游 release 产物命名变动或缺失 SHA256SUMS.txt | Medium | 严格正则匹配，缺失或校验失败时警告跳过，保留已有 Formula 不误删 |
| 生成的 Ruby 脚本存在语法错误 | High | CI 及本地同步均增加 `ruby -c Formula/*.rb` 门禁 |
| CI 提交死循环触发 CI | Low | 提交信息附带 `[skip ci]` 标签 |

## Open Questions

无。所有需求与设计原则已在 `SPEC.md` 与 `docs/intent/homebrew-craft-clis.md` 中完全确认。
