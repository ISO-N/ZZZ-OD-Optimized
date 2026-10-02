# 发布流程（本分支）

> 本分支 = `ISO-N/ZZZ-OD-Optimized`，是上游 `OneDragon-Anything/ZenlessZoneZero-OneDragon` 的性能优化分支，**独立发布**。
> 上游那一套 CNB 镜像、MirrorChyan 上传、SignPath 签名在本分支都已移除或改为可选。

## 0. 仓库设置（在 GitHub 网页上改，代码里改不到）

fork 出来时会继承上游的设置，下面三项必须手动改，否则会出现「代码里已经切干净了、界面上还指着上游」的情况：

| 位置 | fork 继承到的值 | 处置 |
|---|---|---|
| Settings → General → Features → **Issues** | **关闭** | **当前决定：保持关闭。** 代价已知：README 的提问入口、`.github/ISSUE_TEMPLATE/`、程序标题栏的反馈按钮（指向 `{github_homepage}/issues`）打开都是 404；要启用只是网页上勾一下，不需要改代码 |
| About → **Website** | `https://one-dragon.com/zzz/zh/home.html`（上游官网） | 建议改成 `https://github.com/ISO-N/ZZZ-OD-Optimized`，或留空 |
| About → **Description** | 与上游一字不差 | 建议标明是性能优化分支，例如 `绝区零一条龙 · 性能优化分支（非官方）` |

（可选）`dev` 分支是 fork 时带过来的上游分支，本分支不用，可删。

## 1. 发布模型

推一个 `v*` tag → `.github/workflows/build-release.yml` 自动构建并创建 GitHub Release，产出 8 个附件：

| 附件 | 内容 |
|---|---|
| `ZenlessZoneZero-OneDragon-<版本>-Installer.exe` | 精简安装器 |
| `ZenlessZoneZero-OneDragon-<版本>-Full-Environment.zip` | 带环境完整包 |
| `ZenlessZoneZero-OneDragon-<版本>-Full.zip` | 完整源码包 |
| `ZenlessZoneZero-OneDragon-<版本>-WithRuntime-Full.zip` | 内嵌运行时 + 源码 + 模型 |
| `ZenlessZoneZero-OneDragon-<版本>-WithRuntime.zip` | 内嵌运行时 + 源码 |
| `ZenlessZoneZero-OneDragon-Environment.zip` | 环境 wheels 包（供启动器更新用） |
| `ZenlessZoneZero-OneDragon-Launcher.zip` | 原始启动器更新包 |
| `ZenlessZoneZero-OneDragon-RuntimeLauncher.zip` | 集成启动器更新包（exe + `.runtime`） |

附件名不带仓库名，与上游同名，靠仓库区分——**这是刻意的**：`project_name` 同时决定附件名和「从 `OneDragon-Env` 下载 uv/cpython 的 tag 路径」，改名会让后者 404。

打包清单与逻辑在 `tools/ci/prepare_release_assets.py`；版本号由 `tools/ci/get_version.py` 生成。

## 2. 发布前必查：`deploy/module_manifest.py` 必须是当前源码生成的

**这是最容易踩的坑。** 集成启动器（RuntimeLauncher）内置一份 `module_manifest.py`（打包时由 `deploy/generate_module_manifest.py` 生成），运行时 `GitService._check_manifest_compatible()` 会把它和目标 commit 里的 `deploy/module_manifest.py` 做**字节级相等**比对（只归一化 CRLF）。不相等 → 判定 `RUNTIME_INCOMPATIBLE` → 提示「请先更新启动器」并**阻止代码同步**。

所以：**改了 `src/` 的第三方导入（换库、改采集方式等）后，必须重新生成并提交这个文件**，否则打出来的 WithRuntime 包用户根本同步不了代码。

```shell
uv run python deploy/generate_module_manifest.py
git diff --stat deploy/module_manifest.py   # 有差异就一起提交
```

`build-running-resources.yml` 在 push `main` 时也会重新生成并自动提交它，但那是**下一次**提交的事了——打 tag 前必须已经同步好。

## 3. 首次发布自举

```shell
# 1. 把远端切到自己的仓库（原来是上游）
git remote rename origin upstream
git remote add origin https://github.com/ISO-N/ZZZ-OD-Optimized.git

# 2. 把优化分支合进 main（保留合并记录）
git checkout main
git merge --no-ff perf/optimize-hot-paths
git push -u origin main

# 3. 打 tag 触发发布
git tag v2.1.0
git push origin v2.1.0
```

也可以在 Actions 页面手动跑 `Build and Release` 并勾 `create_release`，它会自动递增版本并推一个新 tag。

## 4. 发布后验收

1. Actions 里 `release` job **确实执行了**（不是 skipped）。
2. Release 页面有 §1 表格里的全部 8 个附件。
3. 这三个地址能直接下（`curl -I` 应是 200）：
   - `https://github.com/ISO-N/ZZZ-OD-Optimized/releases/latest/download/ZenlessZoneZero-OneDragon-Launcher.zip`
   - `https://github.com/ISO-N/ZZZ-OD-Optimized/releases/latest/download/ZenlessZoneZero-OneDragon-RuntimeLauncher.zip`
   - `https://github.com/ISO-N/ZZZ-OD-Optimized/releases/latest/download/ZenlessZoneZero-OneDragon-Environment.zip`
4. 在一台干净机器（或空目录）用 `-Installer.exe` 跑一遍「一键安装」，确认：
   - 安装完后 `git remote -v` 指向本 fork（不是上游）；
   - 「源配置」页下拉里**没有** CNB / Gitee；
   - 首页没有上游公告卡、没有「官方频道」按钮。

## 5. 代码签名（可选）

默认**不签名**，用户首次运行会看到 Windows SmartScreen「未知发布者」提示，属预期现象。

要开启签名：在仓库 Settings → Secrets and variables → Actions 里

- Variables：`ENABLE_SIGNING=true`，以及签名服务要求的 `SIGNPATH_ORGANIZATION_ID`、`SIGNPATH_PROJECT_SLUG`、`SIGNPATH_SIGNING_POLICY_SLUG`；
- Secrets：`SIGNPATH_API_TOKEN`。

`build-release.yml` 的 `sign` job 会自动生效，不需要改 YAML。可用的免费/低价方案见 README 的「关于代码签名」。

## 6. 不要改回去的两处

- `release` job 的条件必须容忍 `needs.sign.result == 'skipped'`。上游原本要求 `== 'success'`，导致非上游 owner 的仓库**永远创建不出 Release**。
- 工作流级的 `permissions: contents: write` 不能删：创建 Release 和手动触发时推 tag 都依赖它。
