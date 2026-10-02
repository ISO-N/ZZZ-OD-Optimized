# 相关仓库

> **本仓库是 [`ISO-N/ZZZ-OD-Optimized`](https://github.com/ISO-N/ZZZ-OD-Optimized)**,是上游 [`OneDragon-Anything/ZenlessZoneZero-OneDragon`](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon) 的**性能优化分支**,独立发布,不接上游的 CNB / Gitee 镜像与 MirrorChyan 渠道。
>
> 本页列出本分支依赖的全部仓库,供开发者和 AI agent 了解全貌与各自落点。标「上游」的是本分支**不维护、只消费**的配套仓。
>
> 本地布局:测试仓建议 clone 到**本仓根目录内**(见下);yolo 训练仓 / 数据集建议放在**与本仓同一父目录**(如 `../OneDragon-YOLO`、`../dataset`)。

## 总览

| 项 | 类型 | 位置 | 用途 | 何时去动 |
|---|---|---|---|---|
| 本仓(主仓) | git | [`ISO-N/ZZZ-OD-Optimized`](https://github.com/ISO-N/ZZZ-OD-Optimized) | 业务代码、GUI、文档、发布一键安装器与启动器 | 日常开发 |
| 上游主仓 | git | [`OneDragon-Anything/ZenlessZoneZero-OneDragon`](https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon) | 本分支的上游,合入上游新功能 | 同步上游更新 |
| 环境与模型仓(上游) | git | [`OneDragon-Anything/OneDragon-Env`](https://github.com/OneDragon-Anything/OneDragon-Env) | uv / cpython 压缩包、OCR 模型 | 不维护,仅消费 |
| yolo 训练仓(上游) | git | [`OneDragon-Anything/OneDragon-YOLO`](https://github.com/OneDragon-Anything/OneDragon-YOLO) | YOLO 模型训练 + release 发布 | 不维护,仅消费 |
| 测试仓(上游) | git | [`OneDragon-Anything/zzz-od-test`](https://github.com/OneDragon-Anything/zzz-od-test) | 测试代码 + 画面截图存档 | 本地跑/改测试 |
| 数据集 | 非git(ModelScope) | 见下 | YOLO 训练数据 | 训练时拉取 |

## 下载源与镜像

- **代码源**:只有 GitHub 一个源,见 `config/repository.yml` 的 `repositories.options`。本分支**不再提供 CNB / Gitee 代码镜像**,`GitService` 的候选回退只有一个候选。
- **环境与依赖下载**:`env_source`(uv/cpython)与 `resource_download.repos`(OCR / YOLO 模型)也全部走 GitHub Release;`source_defaults` 里两项默认值都是 GitHub。上游 `OneDragon-Env` / `OneDragon-YOLO` 的 release 附件被直接消费,本分支不转存。
- **网络不通时**:在「源配置」页把代理类型选成 `GitHub 代理`(走 `ghfast.top`),或填自己的个人代理。`config/repository.yml` 里的 `use_proxy: true` 就是为此保留的。
- **发布产物**:`ZenlessZoneZero-OneDragon-*.zip` / `-Installer.exe` 由本仓 `.github/workflows/build-release.yml` 在 tag 推送时构建,附件名与上游一致(靠仓库区分)。发布步骤见 [发布流程](release.md)。

## 测试仓 `zzz-od-test`(上游)

- **clone 到本仓根目录**(同名 `zzz-od-test/`),本仓 `.gitignore` 忽略它;IDE 设为 `Test Sources Root`。跑/改测试、画面截图存档(`screens/`)都在这。
- ⚠️ **提交坑**:本仓 `git add zzz-od-test/...` 会被 `.gitignore` **静默跳过**,须 `git -C zzz-od-test` 提交。
- 本分支**不在 CI 里跑测试仓**(`test-check.yml` 已删除),本地自行运行:
  ```shell
  uv run --env-file .env pytest zzz-od-test/
  ```
- **AI agent**:Grep/Glob 默认尊重 `.gitignore`,**不会自动搜** `zzz-od-test/`——查/改测试须 `Read`/`grep` 显式指定路径。

## yolo 训练仓 `OneDragon-YOLO`(上游)

- 训练游戏内 YOLO 目标检测模型(迷失之地交互入口、闪光分类、枯壤境界等)。
- **发布**:模型打包成 `<模型名>.zip`,以 release tag `zzz_model` 发布;本仓按 `config/repository.yml` 的 `resource_download.models` 声明消费。
- 本分支只消费,不训练、不发模型。

## 数据集

- 训练数据**非 git 仓**,托管在 [ModelScope](https://modelscope.cn),按 `<玩法>-Dataset` 命名;本地按数据集名建目录(如 `dataset/ZZZ-LostVoidDet-Dataset/`)。
- 本分支不需要数据集(不做模型训练)。
