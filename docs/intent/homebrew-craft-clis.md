# Intent: homebrew-craft-clis

Confirmed Date: 2026-11-04

## Statement of Intent

- **Outcome（目标产物）**：构建 `JsonLee12138/homebrew-craft-clis` 仓库，通过每日一次（含 `workflow_dispatch` 手动触发）的 GitHub Actions 自动扫描 `github.com/storytold` 组织，将所有含 macOS CLI 产物的产品生成并更新为 `Formula/<app>-cli.rb`，直接自动提交到 `main` 分支。
- **User（使用者）**：在 macOS 上使用 Craft 系列 CLI / MCP 的开发者，通过一行 `brew install JsonLee12138/craft-clis/<app>-cli` 即可完成安装与升级。
- **Why now（核心价值）**：`Homebrew/homebrew-core` 目前仅覆盖一半产品（新仓库受限于建仓满 30 天等门槛），且官方主库的裸源码编译版不含外挂仓库的 `craft-fonts`（中日韩等内置字体）与 `craft-i18n`（多语词典/断词）；直接复用 `storytold` 官方公证签名的 `*-cli-*-macos-universal.zip` 既能全量覆盖所有产品，又保留完整字体、词典及 Apple 公证签名。
- **Success（验收标准）**：自动发现并生成当前全部 16 个 `*-cli` 的 Formula 且本地 `brew install` 验证通过；后续上游发新版或新增 `*craft` 产品时，CI 仅需拉取官方 `SHA256SUMS.txt` 在数秒内自动更新 Formula 与 `README.md` 列表。
- **Constraint（边界约束）**：无 `storytold` 上游仓库权限（纯公开 GitHub API 每日巡检）、零 Rust 源码编译、不转存安装包（直接指向官方 Release URL）、支持可选排除列表、统一 `<app>-cli` 命名防止覆盖官方桌面版 Cask。
- **Out of scope（明确不做）**：不做 Linux / Windows 支持、不从源码编译未发版仓库、不在本仓库发布 GitHub Release 附件、不维护桌面版 `.dmg` Cask、不设 PR 人工审批流。
