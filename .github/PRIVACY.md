# **ZenlessZoneZero-OneDragon 隐私政策**

**最后更新日期：** 2026年2月 (本 fork 版本)

## **引言**

欢迎使用 ZenlessZoneZero-OneDragon（以下简称“本软件”）。本软件是 [上游 ZenlessZoneZero-OneDragon](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon) 的性能优化分支，由 `ISO-N/ZZZ-OD-Optimized` 独立发布。我们深知个人信息对您的重要性，并致力于保护您的隐私。

请在使用本软件前，仔细阅读并充分理解本政策。使用本软件即表示您已同意本政策的全部内容。

### **一、收集的信息及使用目的**

* **运行配置信息**：
  * **信息内容**：您为使用自动化功能而设置的运行参数配置。
  * **使用目的**：用于实现游戏自动登录、执行自动化任务等核心功能。
  * **保存位置**：仅保存在您的本地设备上，不会上传。
* **匿名遥测数据**：
  * **信息内容**：程序启动/关闭事件，附带版本号、commit、运行平台与机器标识（由机器名与架构生成的 UUID，不含个人身份信息）。
  * **使用目的**：统计日活与版本分布。
  * **收集开关**：**默认关闭**。本分支不会主动上报任何数据；仅当您在 `config/privacy.yml` 中显式设置 `telemetry_enabled: true` 时才会采集。

本软件不收集您的账号密码、游戏内数据、截图或键鼠操作记录，也不会上传这些内容。

### **二、信息的共享、转让与公开披露**

我们不会将您的个人信息出售或出租给任何第三方。除以下情况外，我们不会与任何第三方共享您的个人信息：

1. **获得您的明确同意**：在获取您的明确授权后，我们才会与其他方共享您的信息。
2. **法定情形下的披露**：根据法律法规的规定、司法机关或行政机关的强制性要求，我们可能会对外披露您的信息。
3. **与游戏服务器通信**：本软件在运行时需要与游戏官方服务器及官方公告接口通信，相关数据传输将遵循游戏官方的网络及隐私政策。

### **三、您的权利**

根据适用的法律法规，您对自己的个人信息享有访问权、更正权、删除权、撤销同意权与限制处理权。遥测数据默认不采集；若您曾手动开启，删除 `config/privacy.yml` 或将其中的 `telemetry_enabled` 改为 `false` 即可停止采集。

### **四、信息安全保障**

* **开源透明**：本软件代码完全开源，您可以随时审查源代码，以验证我们的隐私保护措施。
* **最小采集**：默认不采集、不上报任何运行数据。

### **五、儿童隐私保护**

本软件不以未成年人为目标用户。我们不会主动收集未成年人的个人信息。如果您是未成年人，请在您的父母或其他监护人的指导下共同阅读并决定是否使用本软件。

### **六、隐私政策的更新**

我们可能会适时修订本隐私政策。当政策发生重大变更时，我们将在本仓库中发布公告。建议您定期查阅。

### **七、联系我们**

如果您对本隐私政策有任何疑问、意见或建议，欢迎通过以下方式与我们联系：

* **GitHub Issues**: [https://github.com/ISO-N/ZZZ-OD-Optimized/issues](https://github.com/ISO-N/ZZZ-OD-Optimized/issues)

### **附：第三方服务列表**

1. **代码托管与更新**
   * **服务商**：GitHub
   * **目的**：代码托管、版本控制与软件更新。
2. **文件下载加速（可选）**
   * **服务商**：ghfast.top
   * **目的**：仅当您在「源配置」中把代理类型选为「GitHub 代理」时，用于为中国大陆用户加速 GitHub 文件下载。默认不启用。
3. **依赖与模型下载**
   * **服务商**：GitHub Releases（`OneDragon-Anything/OneDragon-Env`、`OneDragon-Anything/OneDragon-YOLO`、`astral-sh/python-build-standalone`）
   * **目的**：下载 Python 运行时、uv 与识别模型。

# **ZenlessZoneZero-OneDragon Privacy Policy**

**Last Updated:** February 2026 (this fork)

## **Introduction**

Welcome to ZenlessZoneZero-OneDragon (the "Software"). This Software is a performance-optimized fork of [upstream ZenlessZoneZero-OneDragon](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon), released independently by `ISO-N/ZZZ-OD-Optimized`. We understand the importance of personal information and are committed to protecting your privacy.

Please read and fully understand this policy before using the Software. By using the Software, you agree to the entire contents of this policy.

### **I. Information We Collect and Its Purpose**

* **Running Configuration Information**:
  * **Information Content**: Operational parameter configurations you set to use automation features.
  * **Purpose of Use**: To implement core functions such as automatic game login and execution of automated tasks.
  * **Storage Location**: Stored only on your local device. Never uploaded.
* **Anonymous Telemetry**:
  * **Information Content**: App launch/shutdown events with version, commit, platform, and a machine identifier (a UUID derived from hostname and architecture, containing no personal identity).
  * **Purpose of Use**: Daily-active-user and version-distribution statistics.
  * **Collection Switch**: **Disabled by default.** This fork does not report anything unless you explicitly set `telemetry_enabled: true` in `config/privacy.yml`.

The Software does not collect your credentials, in-game data, screenshots, or input records, and never uploads them.

### **II. Sharing, Transfer, and Public Disclosure**

We do not sell or rent your personal information. We will not share your personal information with any third party, except:

1. **With Your Explicit Consent**.
2. **Disclosure under Legal Requirements**.
3. **Communication with Game Servers**: The Software communicates with official game servers and official announcement endpoints; such traffic follows the game's own policies.

### **III. Your Rights**

You have the right to access, rectify, erase, withdraw consent for, and restrict processing of your personal information. Telemetry is off by default; if you enabled it manually, delete `config/privacy.yml` or set `telemetry_enabled` to `false` to stop collection.

### **IV. Information Security**

* **Open-Source Transparency**: The code is fully open source; you may review it at any time.
* **Minimal Collection**: No runtime data is collected or reported by default.

### **V. Children's Privacy**

The Software is not intended for minors. We do not knowingly collect personal information from minors.

### **VI. Updates to This Privacy Policy**

We may revise this policy from time to time. Significant changes will be announced in this repository.

### **VII. Contact Us**

* **GitHub Issues**: [https://github.com/ISO-N/ZZZ-OD-Optimized/issues](https://github.com/ISO-N/ZZZ-OD-Optimized/issues)

### **Appendix: Third-Party Service List**

1. **Code Hosting and Updates**
   * **Provider**: GitHub
   * **Purpose**: Code hosting, version control, and software updates.
2. **Download Acceleration (optional)**
   * **Provider**: ghfast.top
   * **Purpose**: Only used when you select the "GitHub proxy" option under Source Configuration. Disabled by default.
3. **Dependency and Model Downloads**
   * **Providers**: GitHub Releases (`OneDragon-Anything/OneDragon-Env`, `OneDragon-Anything/OneDragon-YOLO`, `astral-sh/python-build-standalone`)
   * **Purpose**: Downloading the Python runtime, uv, and recognition models.
