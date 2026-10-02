<!-- markdownlint-restore -->
<div align="center">

<img src="https://socialify.git.ci/ISO-N/ZZZ-OD-Optimized/image?description=1&font=Inter&language=1&logo=https%3A%2F%2Fgithub.com%2FISO-N%2FZZZ-OD-Optimized%2Fblob%2Fmain%2F.github%2Fimage%2Fellen.png%3Fraw%3Dtrue&name=1&owner=1&pattern=Charlie+Brown&theme=Light" alt="ZZZ-OD-Optimized"/>

---

**ZZZ-OD-Optimized**

<div>
    <img alt="platform" src="https://img.shields.io/badge/platform-Windows-blueviolet">
    <img alt="commit" src="https://img.shields.io/github/commit-activity/m/ISO-N/ZZZ-OD-Optimized?color=blue">
</div>
<div>
    <img alt="stars" src="https://img.shields.io/github/stars/ISO-N/ZZZ-OD-Optimized?style=social">
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/ISO-N/ZZZ-OD-Optimized/total?style=social">
</div>

</div>

## ⚠️ 这个仓库是什么

本仓库是 [**ZenlessZoneZero-OneDragon（绝区零一条龙）**](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon) 的**性能优化分支**，由 `ISO-N` 独立维护与发布。

- **不是官方发布**。上游是 `OneDragon-Anything/ZenlessZoneZero-OneDragon`，本分支只是它的一份衍生版本。
- **只做性能优化**，不新增游戏玩法功能：降低 CPU / GPU 占用、减少无谓的图像搬运与重绘、加快冷启动、把重库改成按需加载等。游戏功能与上游保持一致。
- **不提供任何"官方"支持**。本仓库没有 QQ 频道、没有赞助渠道、没有 Mirror酱 等第三方分发渠道，也不会以官方名义回复问题。有疑问请在本仓库提 [Issue](https://github.com/ISO-N/ZZZ-OD-Optimized/issues)；也可以去上游仓库检索同类问题（多数问题两边通用）。
- **许可与署名**：沿用上游的 GPL-3.0 许可；项目 LOGO 版权归 [巡夜子](https://github.com/yokuminto) 及全体上游开发者所有；感谢上游全体贡献者。
- 从上游同步新功能：`git fetch upstream && git merge --no-ff upstream/main`（`upstream` 指向上游仓库）。

## 🚀 功能

与上游一致：

🤖 **自动战斗**：支持自定义逻辑、技能标记、条件、变量等进阶用法

🛡️ **闪避助手**：基于声音、图像一体化模型识别，轻占用，高准确

🧹 **日常清理**：影像店、刮刮乐、咖啡店、材料、奖励等全日常清理

☕ **空洞作战**：基于大模型训练的识别、事件、寻路的功能模块

⏲️ **更多功能**：定时启动、多账号切换、定时任务、自动对话……

## 📸 页面预览

<div align="center">

![App Interface](./image/app.webp#gh-light-mode-only "操作界面")

</div>

## 安装

所有安装包都在本仓库的 [Releases](https://github.com/ISO-N/ZZZ-OD-Optimized/releases/latest) 页面，按需要选一个：

| 包 | 适用场景 |
|---|---|
| `...-Installer.exe` | **推荐**。精简安装程序，运行后自动下载环境依赖与模型 |
| `...-Full-Environment.zip` | 带完整环境的包，不需要再下载任何东西；适合网络受限的机器 |
| `...-Full.zip` | 完整源码包，只需再下载环境依赖 |
| `...-WithRuntime-Full.zip` | 内嵌 Python 运行时 + 源码 + 模型，解压即用，**不需要装 Python** |
| `...-WithRuntime.zip` | 内嵌 Python 运行时 + 源码，模型按需下载，解压即用 |

安装步骤：

1. 在固态硬盘上建一个**全英文、无空格**的空目录（例如 `D:\zzz-od`）。
2. 下载 `...-Full-Environment.zip` 或 `...-WithRuntime-Full.zip`，解压到该目录。
   （下载 `...-Installer.exe` 的话，**以管理员身份运行**它，再选这个目录作为安装目录。）
3. 安装完成后用 **`OneDragon-Launcher.exe`** 启动（以管理员身份运行）。
4. 首次运行会同步代码与环境依赖。**所有依赖（uv / Python / 识别模型）默认从 GitHub 下载**；如果 GitHub 连不上，在「源配置」页把「代理类型」改成 **GitHub 代理**，或填自己的个人代理地址。

### 下载源说明

本分支**只有 GitHub 一个下载源**（代码、uv / Python、OCR 与识别模型全部走 GitHub Release），已移除 CNB 与 Gitee 镜像。地区和源都可以在「源配置」页切换，只有两个地区预设：

- **中国 - GitHub 代理**：pip 走阿里云，GitHub 走 `ghfast.top` 代理。
- **海外**：pip 走 PyPI 官方，不用代理。

### 关于代码签名

本分支**不提供代码签名**，因此首次运行时 Windows SmartScreen 可能提示「未知发布者」。这是预期现象，点「更多信息 → 仍要运行」即可。介意的话请使用上游的官方发布版本。

### 从上游版本换过来

如果你之前装的是上游版本，可以直接把本仓库的包覆盖到原有目录，然后：

- 在「资源管理 → 代码设置」里确认**标准分支是 `main`**（本分支不维护 `test` 分支；如果旧配置里选了 `test`，同步会失败）。
- 代码源选「自动」即可；旧的 Gitee / CNB 代码源选项已经不存在，程序会自动回退到 GitHub。

## 自助排障

按顺序排查：

1. **看日志**：程序目录下 `.log/` 里的最新日志，报错栈一般直接指出原因。
2. **更新到最新**：在「资源管理」页点「代码同步」，并把 OCR 模型与识别模型都更新到最新版本。
3. **网络问题**：本项目所有依赖默认从 GitHub 下载。连不上时在「源配置」页切换「GitHub 代理」，或填自己的代理地址；pip 源至少保证一个可用。
4. **识别不准**：确认游戏是 **1920×1080 窗口模式**，并更新识别模型。
5. **安装失败**：「一键安装」失败时程序会自动打开帮助文档链接；也可以手动看 `.log/` 里的安装日志。装完仍然启动失败，优先尝试重新解压 `...-Full-Environment.zip`（最不容易受网络影响）。
6. **仍没解决**：到本仓库 [Issues](https://github.com/ISO-N/ZZZ-OD-Optimized/issues) 提问，附上日志与截图（游戏内截图按 `F11`）。

上游的[常见问题排查文档](https://docs.qq.com/doc/p/7add96a4600d363b75d2df83bb2635a7c6a969b5)对本分支同样适用（功能与上游一致）。

## ✨ 性能优化点

见仓库提交历史里 `perf:` 前缀的提交。已完成的方向包括：识别链路上的重复整图搬运、YOLO 预处理的 float64 中间体、视觉匹配的按需裁剪、界面面板的无效重绘、重库按需加载加快冷启动、闪光分类器默认启用 GPU 等。

## ⚠️ 免责声明

📌 本项目仅供学习交流

🎨 项目 LOGO 版权归 [巡夜子](https://github.com/yokuminto) 及全体上游开发者所有

⚖️ 使用本工具产生的一切风险需自行承担

🚫 本项目未授权任何个人、商家、自媒体账号等进行售卖

🚫 若您遇到商家使用本软件进行代练并收费，产生的任何问题及后果与本软件无关

🚫 本项目不提供任何"售后"服务

## 🔒 隐私政策 (Privacy Policy)

本程序**默认不采集、不上报**任何运行数据（遥测默认关闭）。详见 [隐私政策](PRIVACY.md)。

Telemetry is **disabled by default**. See the [Privacy Policy](PRIVACY.md).

## 🙏 致谢

本项目的全部游戏功能代码来自上游 [ZenlessZoneZero-OneDragon](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon) 及其贡献者们，本分支只在其之上做性能优化。完整的贡献者名单见 `contributors.yaml`。
