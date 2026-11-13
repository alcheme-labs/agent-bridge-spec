# Agent Bridge Spec

中文 | [English](README.en.md)

定义应用与用户自有本机或远端 Agent 的通用接入规范，并提供参考 SDK 和接入示例。应用可以采用参考 SDK，也可以遵循同一规范独立实现；最终用户在已接入应用或原有 Agent 中连接、授权和完成任务。

官方仓库：[alcheme-labs/agent-bridge-spec](https://github.com/alcheme-labs/agent-bridge-spec)。`local-agent-bridge` 是本地目录名，接入目标不局限于本机。自 2026-11-12 起本目录是独立项目主目录，原 ResearchStudio 文档目录保留历史副本，不再同步。

## 当前阶段

更新时间：2026-11-13。当前交付包括规格、双语规范、参考实现设计及配套 Skill 源码 `0.1.0`。Bridge 运行库仍未开发、抽取青凝代码、构建、发布或完成运行互通，没有可安装公共 SDK 包。Skill 采用独立 GitHub Release 分发，正式版本及发布验证以[发布记录](https://github.com/alcheme-labs/agent-bridge-spec/releases)为准；官方仓库与更新源均为 `alcheme-labs/agent-bridge-spec`。

当前规范为 **normative draft 0.3**，SDK 为 **reference design draft 0.3**。在前轮规范/SDK 分离及安全/恢复规则基础上，本轮补充后台受托决定、结构化输出的保证程度，以及主任务时限/预算的通用规则；具体实现和消费者业务继续分开。

前轮 draft 0.2 经独立角色和裁判关闭的 2 项 P2 保留于[规范补齐记录](docs/reviews/2026-11-13-normative-gap-review.md)，不自动覆盖本修订。本轮经两位未参与编写的独立角色及最终裁判核对，未发现需修订的实质文档问题；结论及检查集中在[受托、产出与限制规则记录](docs/reviews/2026-11-13-runtime-rules-review.md)。所有文档结论均不代替实际兼容证明。实际首发引擎/宿主/连接产品、第二真实消费者、独立接入运行证据、分发与许可仍待落实。

2026-11-12 的[三轮 SPEC 评审](docs/reviews/2026-11-12-spec-review.md)关闭了当时确认的 3 项问题，SDK 原设计也有自己的设计复核；这些结论及旧摘要只适用于各自旧版本，不自动覆盖本修订。2026-11-02 的[协议评审](docs/reviews/2026-11-02-protocol-review.md)同样保留为历史。

## 文档分工

| 文档 | 唯一维护的内容 |
| --- | --- |
| [产品规格](SPEC.md) | 产品目标、角色、完整使用路径、交付物和产品退出条件 |
| [应用与 Agent 接入规范](docs/general-integration-contract.md) | 实现无关的接入义务、能力/标准绑定、权限与效果、恢复、安全隐私及符合性验收；规范性主文档 |
| [规范英文版](docs/general-integration-contract.en.md) | 同一规范的对应英文翻译，条款编号及版本一致；差异以中文原文核对并修正 |
| [Agent 接入 Skill](skills/agent-bridge-integration/SKILL.md)、[中文译文](skills/agent-bridge-integration/SKILL.zh-CN.md) | 指导 AI 按正文开发及审查接入，按用户语言回复；不新增业务或接入规则 |
| [参考 SDK 与青凝接入设计](docs/sdk-and-qingning-integration-design.md) | Node/TypeScript API、host 接点、引擎/工具适配、代码抽留、青凝兼容与来源证据；不规定其他实现必须采用这些接口 |
| [前轮规范缺口评审](docs/reviews/2026-11-13-normative-gap-review.md) | draft 0.2 的范围、标准依据、独立裁决与历史摘要 |
| [本轮运行规则评审](docs/reviews/2026-11-13-runtime-rules-review.md) | draft 0.3 三项通用规则、独立审查、文档检查及未执行运行边界 |
| [ServerAgent 接入期望清单](docs/serveragent-expectations.md) | 原始消费者输入保留；本轮仅采纳三类通用语义，具体非 Node/SDK 接法、业务责任及运行支持仍未交付 |
| [青凝抽取评估](docs/extraction-assessment.md) | 2026-11-04 来源源码、可抽/保留边界与历史判断 |
| [产品验证与推进方案](docs/validation-plan.md) | 现成项目复用、贡献和选型的历史研究，不替代当前规范和状态 |
| [产品定位](docs/product-positioning.md)、[功能与完整流程](docs/v1-features-and-flows.md) | 角色、场景和用户操作基线；当前规范规则以主文档为准 |

先读产品规格理解目标，再读规范实现接入；只有采用本参考 SDK 或参与其开发时才需要 SDK 设计。既有历史评审链接及版本事实保留，不将“文档声明、源码确认、真实流程通过、独立互通通过”混为同一状态。ServerAgent 原始输入保持原样；三项通用规则的采纳不等于支持其全部接入组合，更不把其服务契约、候选验收/启用或维护队列迁入 Bridge。

## 保持的产品边界

- A：在应用内使用自己的 Agent；B：在原有 Agent 中操作应用。两种入口共用原业务方法与授权，分别验收，B 不被迫安装控制整个 Agent 的第二服务。
- 新项目和已有项目遵循同一规范。应用作者完成接入，每位使用者再连接和授权；仅安装连接器不能使封闭应用自动具备业务能力。
- 青凝是来源实践和参考 SDK 首个应用，继续持有自己的身份、业务权限、调度、数据与安装归属；其他应用不依赖青凝账号、服务器或业务模型。
- 规范复用 ACP、MCP 和有明确语义映射的原生接口；不新增通用 RPC、业务数据库、身份中心或 transcript owner。
- 本机/远端、完整输出、写入读回及安全恢复的最终目标保持。只通过运行库、只读演示或单一组合时只能报告相应范围，不能缩减整体目标。
- Bridge 运行库继续不开发。本轮仅按授权新增 Skill、其本地更新检查器及中英译文；后续 Bridge 运行工作先验证一条真实写入路径的可信关联、响应丢失与原业务防重，再按授权推进。

## 配套 Skill

`skills/agent-bridge-integration/VERSION` 是 Skill 版本的唯一来源，当前为 `0.1.0`，与规范 draft 0.3 分别版本化。英文 `SKILL.md` 是自动发现入口，中文文件是对应译文；两者都要求按用户使用的语言回复。

当前采用完整仓库安装方式：保留本目录结构，让宿主读取 `skills/agent-bridge-integration`；支持符号链接的宿主也可链接到该实际目录。Skill 解析实际目录后读取同版规范正文，不复制或维护另一套规范。只复制 Skill 文件夹不能取得正文。当前没有单独发布的 Skill 安装包，也未修改本机已安装 Skill。

初始版本使用完整仓库的固定标签，或下载该 Release 的源码归档：

```sh
git clone --branch agent-bridge-integration-v0.1.0 https://github.com/alcheme-labs/agent-bridge-spec.git
```

每次启用时可执行更新检查，默认 24 小时内复用网络结果；同一新版展示并确认后只自动提醒一次。支持忽略该版和稍后提醒；状态保存在仓库外的用户本机目录，使用文件锁和原子写入。缓存仍可能产生到期提醒，以 `notify` 为准。检查器不安装更新，更新须用户明确同意。它没有后台常驻进程，不承诺未启用时定时检查。

`update-source.json` 的 `repository` 已配置为 `alcheme-labs/agent-bridge-spec`。发布 Skill 时，按 `agent-bridge-integration-v0.1.0` 一类独立标签创建 GitHub Release，并提供实际变更说明；仅推送代码或创建普通 Git tag 不会触发 Skill 更新提醒。详见[更新与状态说明](skills/agent-bridge-integration/references/updates.zh-CN.md)。

检查器使用 Python 3.9+ 标准库；本地验证入口：

```sh
python3 -B -m unittest discover -s tests -p 'test_skill_updates.py' -v
python3 skills/agent-bridge-integration/scripts/check_updates.py check
```

2026-11-13 本地 31 项检查、Skill 结构校验及相对链接/代码语法检查通过；另完成独立行为复核及双语规范保真核对。中文原条款保持不变，仅加语言导航和译文关系说明。测试使用临时本地状态和模拟 GitHub 响应，包含实际跨进程文件锁、CLI 与截断 HTTP 字节流；它们不代替官方仓库上的在线检查，也不代表 Bridge 或应用互通通过。

线上核验须读取实际发布记录，并分别验证已安装版本、较旧版本的新版识别及本机状态去重。各次线上核验的实际结果记录在对应 Release 说明中；本地测试通过不自动证明线上检查成功。

维护者可手动触发 [Verify published Skill](https://github.com/alcheme-labs/agent-bridge-spec/actions/workflows/verify-skill-release.yml)，在隔离环境核验指定的最新发布标签。也可运行 `python3 -B tests/verify_skill_updates_online.py`；它使用匿名 API 和临时状态，模拟较旧版本，不安装更新或修改已发布源码。此项需要网络，不属于默认离线测试。

## 文档维护约定

- 接入义务集中维护在规范，产品规格保留目标，SDK 记录实现选择；摘要和示例不得省略必需安全或验收要求。
- 本目录是后续主入口；原 ResearchStudio 副本不再维护另一套项目定义。
- 产品定义、规范、实现设计、实施与运行验收分别表达；不得把文档存在写成已实现。
- 使用相对链接；引用外部源码时保留来源日期/版本，不依赖当前电脑目录。历史评审摘要不随新修订重写为新版本通过。
- 不放置真实密钥、令牌、认证文件或私密配置。正式许可在后续抽取前核查来源、署名与授权，本目录不自动确定许可。
