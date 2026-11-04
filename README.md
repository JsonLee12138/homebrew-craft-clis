# homebrew-craft-clis

[![Sync Formulae](https://github.com/JsonLee12138/homebrew-craft-clis/actions/workflows/sync.yml/badge.svg)](https://github.com/JsonLee12138/homebrew-craft-clis/actions/workflows/sync.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0%20%7C%20MIT-blue.svg)](LICENSE)

全自动、零编译的 macOS Homebrew Tap 仓库，用于一键安装与更新 [`storytold`](https://github.com/storytold) 旗下所有 Craft 系列产品预编译的 Headless CLI 与 MCP Server。

## 核心特性

- ⚡️ **零编译极速安装**：直接下载官方 Universal (`arm64` + `x86_64`) 预编译二进制，无需在本地安装 Rust 工具链编译。
- 🔤 **内置完整字体与词典**：包含官方发布包内置的 `craft-fonts`（中日韩等全量国际字体）与 `craft-i18n`（多语词典及断词模块），告别主库裸编译版字体缺失问题。
- 🍎 **Apple Developer ID 签名与公证**：所有发布包均通过 Apple Developer ID 签名及公证，在 macOS 上开箱即跑，不被 Gatekeeper 阻断。
- 🤖 **每日全自动同步**：通过 GitHub Actions 每日自动探测 upstream 最新正式发布，自动更新版本号与 SHA256 校验和。

---

## 安装与使用

### 方式一：直接安装（免手动 tap）

```sh
# 以 WordCraft CLI 为例
brew install JsonLee12138/craft-clis/wordcraft-cli

# 查看版本
wordcraft-cli --version
```

### 方式二：先 Tap 后按需安装

```sh
# 添加 tap
brew tap JsonLee12138/craft-clis

# 安装常用 CLI 工具
brew install wordcraft-cli pdfcraft-cli craft-anything-cli
```

### 升级工具

```sh
brew update
brew upgrade wordcraft-cli
```

---

## 收录产品清单

<!-- FORMULAE-TABLE:START -->

| CLI | Version | Description | Install Command |
| --- | --- | --- | --- |
| [`cadcraft-cli`](Formula/cadcraft-cli.rb) | `0.17.0` | Computer-aided design and drafting | `brew install JsonLee12138/craft-clis/cadcraft-cli` |
| [`craft-anything-cli`](Formula/craft-anything-cli.rb) | `0.3.0` | Understand how any software works, and craft your own | `brew install JsonLee12138/craft-clis/craft-anything-cli` |
| [`deckcraft-cli`](Formula/deckcraft-cli.rb) | `0.15.0` | Reimplementation of Microsoft PowerPoint in pure Rust | `brew install JsonLee12138/craft-clis/deckcraft-cli` |
| [`designcraft-cli`](Formula/designcraft-cli.rb) | `0.17.0` | Page and layout design editor written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/designcraft-cli` |
| [`effectcraft-cli`](Formula/effectcraft-cli.rb) | `0.21.0` | Motion graphics and compositing tool written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/effectcraft-cli` |
| [`figcraft-cli`](Formula/figcraft-cli.rb) | `0.15.0` | Interface design and prototyping | `brew install JsonLee12138/craft-clis/figcraft-cli` |
| [`filmcraft-cli`](Formula/filmcraft-cli.rb) | `0.17.0` | Open-source, nonlinear video editor written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/filmcraft-cli` |
| [`gridcraft-cli`](Formula/gridcraft-cli.rb) | `0.16.0` | Spreadsheet (Microsoft Excel-style) in pure Rust | `brew install JsonLee12138/craft-clis/gridcraft-cli` |
| [`lightcraft-cli`](Formula/lightcraft-cli.rb) | `0.18.0` | Non-destructive photo editor written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/lightcraft-cli` |
| [`materialcraft-cli`](Formula/materialcraft-cli.rb) | `0.1.0` | Open-source, node-based material designer written from scratch in pure Rust | `brew install JsonLee12138/craft-clis/materialcraft-cli` |
| [`pdfcraft-cli`](Formula/pdfcraft-cli.rb) | `0.18.1` | PDF reader and editor written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/pdfcraft-cli` |
| [`photocraft-cli`](Formula/photocraft-cli.rb) | `0.20.1` | Open-source, photo editor written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/photocraft-cli` |
| [`soundcraft-cli`](Formula/soundcraft-cli.rb) | `0.17.0` | Reimplementation of Avid Pro Tools in pure Rust | `brew install JsonLee12138/craft-clis/soundcraft-cli` |
| [`texturecraft-cli`](Formula/texturecraft-cli.rb) | `0.3.0` | Open-source, 3D texture painting workflow written from scratch in pure Rust | `brew install JsonLee12138/craft-clis/texturecraft-cli` |
| [`vectorcraft-cli`](Formula/vectorcraft-cli.rb) | `0.21.0` | Open-source, vector art tool written by scratch in pure Rust | `brew install JsonLee12138/craft-clis/vectorcraft-cli` |
| [`wordcraft-cli`](Formula/wordcraft-cli.rb) | `0.15.1` | Reimplementation of Microsoft Word in pure Rust | `brew install JsonLee12138/craft-clis/wordcraft-cli` |

<!-- FORMULAE-TABLE:END -->

---

## 自动化机制

本仓库由 GitHub Actions 定时巡检维护：
1. 每天定时扫描 `storytold` 组织下的所有开源仓库。
2. 匹配包含 `*-cli-*-macos-universal.zip` 及 `SHA256SUMS.txt` 的最新正式 Release。
3. 自动生成规范的 Homebrew Formula（`Formula/<app>-cli.rb`）并同步刷新上方的产品清单表。
