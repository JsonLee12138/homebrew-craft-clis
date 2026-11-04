# Task List: homebrew-craft-clis

## Task 1: Initialize Git Repo, .gitignore, and config.json

**Description:** 初始化本地 Git 仓库，设置默认分支为 `main`，配置远端仓库 `https://github.com/JsonLee12138/homebrew-craft-clis.git`，添加 `.gitignore` 避免 Python 缓存和临时文件污染，创建 `config.json` 基础配置文件。

**Acceptance criteria:**
- [x] 本地 Git 仓库处于 `main` 分支，remote origin 指向 `https://github.com/JsonLee12138/homebrew-craft-clis.git`
- [x] `.gitignore` 涵盖 Python `__pycache__`、`*.pyc`、`.pytest_cache`、macOS `.DS_Store`
- [x] `config.json` 包含 `org: "storytold"` 和 `exclude_repos: []`

**Verification:**
- [x] `git remote -v` 输出预期远程地址
- [x] `git branch --show-current` 输出 `main`
- [x] `config.json` 解析合规

**Dependencies:** None

**Files likely touched:**
- `.gitignore`
- `config.json`

**Estimated scope:** Small (2 files)

---

## Checkpoint: After Task 1
- [x] Git 基础环境和基础配置就绪

---

## Task 2: Implement scripts/sync.py and tests/test_sync.py

**Description:** 使用 Python 3 标准库实现核心同步逻辑 `scripts/sync.py`，支持扫描 GitHub 组织、提取最新正式 release、下载解析 `SHA256SUMS.txt`、类名转驼峰、生成 Homebrew Formula Ruby 脚本、更新 `README.md` 的标记区块，并编写全面的单元测试。

**Acceptance criteria:**
- [x] `scripts/sync.py` 仅使用 Python 3.11+ 标准库，支持 `--dry-run` 与 `--config` 参数
- [x] 正确匹配 `^(?P<cli_name>.+-cli)-(?P<version>.+)-macos-universal\.zip$`，解析 SHA256SUMS.txt（兼容单空格、双空格、星号前缀）
- [x] 驼峰转换：`wordcraft-cli` -> `WordcraftCli`，`craft-anything-cli` -> `CraftAnythingCli`
- [x] 渲染符合 Homebrew 标准 DSL 的 Formula，包含 `desc`、`homepage`、`url`、`version`、`sha256`、`license`、`depends_on :macos`、`install`、`test`
- [x] `README.md` 包含 `<!-- FORMULAE-TABLE:START -->` 和 `<!-- FORMULAE-TABLE:END -->` 占位符，支持幂等更新产品表格
- [x] `tests/test_sync.py` 覆盖所有核心函数（类名转换、SHA256 解析、资产过滤、排除列表处理、README 表格替换、Formula 模板渲染）

**Verification:**
- [x] `python3 -m unittest discover -s tests -v` 全部通过
- [x] `python3 scripts/sync.py --dry-run` 正常打印扫描到的产品信息

**Dependencies:** Task 1

**Files likely touched:**
- `scripts/sync.py`
- `tests/test_sync.py`

**Estimated scope:** Medium (2 files)

---

## Checkpoint: After Task 2
- [x] 核心逻辑单元测试 100% 通过
- [x] `--dry-run` 验证成功

---

## Task 3: Execute Sync, Generate Formulae, and Create README.md

**Description:** 编写初始 `README.md`，执行 `python3 scripts/sync.py` 生成全部 16 个 Formula 并自动填充 `README.md`，校验 Ruby 语法与二次运行的幂等性。

**Acceptance criteria:**
- [x] 成功在 `Formula/` 目录下生成全部 16 个 `*-cli.rb`
- [x] `README.md` 包含使用说明（`brew tap`、`brew install`、更新方式）和自动生成的 16 个 CLI 产品清单表格
- [x] `ruby -c Formula/*.rb` 零语法错误
- [x] 连续运行两次 `python3 scripts/sync.py`，第二次运行后 `git status --porcelain` 为空

**Verification:**
- [x] `ls Formula/*.rb | wc -l` 结果为 16
- [x] `ruby -c Formula/*.rb` 退出码为 0
- [x] 二次执行 `python3 scripts/sync.py` 后 `git diff` 为空

**Dependencies:** Task 2

**Files likely touched:**
- `Formula/*.rb`
- `README.md`

**Estimated scope:** Medium (Formulae files + README.md)

---

## Checkpoint: After Task 3
- [x] 16 个 Formula 生成完毕且语法验证通过
- [x] 幂等性验证通过

---

## Task 4: Configure GitHub Actions Workflow (.github/workflows/sync.yml)

**Description:** 创建 GitHub Actions 工作流 `.github/workflows/sync.yml`，设置定时任务（UTC 01:17 / 北京时间 09:17）与手动触发（`workflow_dispatch`），声明最小权限，运行单元测试、同步脚本、Ruby 语法校验，并在有变更时自动提交与推送。

**Acceptance criteria:**
- [ ] 遵循官方 GitHub Actions 规范与最小权限原则（顶层 `permissions: contents: read`，任务 `permissions: contents: write`）
- [ ] 触发器配置：`schedule` cron 表达式 `'17 1 * * *'` 及 `workflow_dispatch`
- [ ] 步骤：Checkout、Setup Python、运行单元测试、执行 `sync.py`、Ruby 语法校验、按需提交推送（提交附带 `[skip ci]`）

**Verification:**
- [ ] YAML 语法有效性检查
- [ ] 审查权限与安全规范

**Dependencies:** Task 3

**Files likely touched:**
- `.github/workflows/sync.yml`

**Estimated scope:** Small (1 file)

---

## Checkpoint: After Task 4
- [ ] GitHub Actions 工作流配置正确合规

---

## Task 5: End-to-End Verification and Push to Remote

**Description:** 进行本地端到端测试（通过 Homebrew 本地安装测试至少一个 Formula，如 `wordcraft-cli`），验证 `wordcraft-cli --version` 正常工作；整理所有阶段的提交并推送到 GitHub 远程仓库 `JsonLee12138/homebrew-craft-clis`。

**Acceptance criteria:**
- [ ] `brew install --formula ./Formula/wordcraft-cli.rb` 安装成功，`wordcraft-cli --version` 正确输出且无 Gatekeeper 阻断
- [ ] 所有代码以规范的原子提交提交到 `main` 分支
- [ ] 成功推送到 `https://github.com/JsonLee12138/homebrew-craft-clis`

**Verification:**
- [ ] `wordcraft-cli --version` 执行成功
- [ ] `git push origin main` 成功，远程仓库包含完整代码与工作流

**Dependencies:** Task 4

**Files likely touched:**
- Git commits

**Estimated scope:** Small
