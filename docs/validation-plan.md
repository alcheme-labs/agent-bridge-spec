# 产品验证与推进方案

2026-11-13 规范衔接：本文保留原场景/研究日期和事实边界。当前产品目标见 [SPEC](../SPEC.md)，实现无关的接入义务及验收以[当前接入规范](general-integration-contract.md)为准；Node/TypeScript SDK 只是一种[参考实现设计](sdk-and-qingning-integration-design.md)。本轮补规范与独立评审，继续不开发，不将下文历史“下一步”当作新的执行授权。

更新日期为 2026-11-04。用户已授权推进现有项目覆盖核查。本文集中保存推进方案、本轮文档与源码证据、选型建议及未验证边界。当前执行范围为研究、设计与文档，运行原型和开发属于后续阶段。

后续更新：用户提出从青凝现有实现抽取公共组件，并让青凝持续使用，随后授权检查可行性。已完成[当前源码的抽取评估](extraction-assessment.md)。当前主候选调整为公共运行核心与青凝宿主适配，保留现成项目复用和上游贡献；本文下列开源项目事实及条件继续有效，但“先验证 agentd”不再是当前下一项工作。本次同样未开发。

## 目标与当前判断

让应用创建者通过可复用的接入方式，使用户能够选择自己的本机或远端 Agent，使用应用的上下文和获准操作完成任务。开发阶段引入、已有项目补接、发布后用户连接属于同一产品生命周期。

个人应用创建者与应用开发者负责接入，最终用户负责选择自己的 Agent 和授权。个人创建者可以同时承担两种角色。产品仍覆盖原先定义的两个入口，应用内调用 Agent，以及在原有 Agent 宿主中通过应用开放的能力完成工作。

本轮发现了直接面向第三方应用的用户自带 Agent 项目，包括 agentd 和 Plannotator BYOA。“没有类似产品”的判断不成立。文档和源码证明许多核心能力已经存在，但尚未证明某个项目或组合完整满足本文的引擎、权限、恢复和部署要求。应用需要提供自己的业务方法、权限和存储逻辑，属于正常接入责任，不能计作竞品遗漏。

现成项目核查阶段的建议是优先采用现有组件验证，并以贡献上游为投入方向，暂不启动独立通用产品或新协议。该阶段将 agentd 作为应用主动启动用户 Agent 路径的首个验证候选，Plannotator BYOA 作为复用已运行交互会话的对照，Paseo 用于比较远端运行和恢复能力。后续青凝抽取评估已调整推进优先级，见本文顶部更新；这些项目仍是候选，并未锁定生产依赖或取得上游合作承诺。

## 用同一条用户路径判断覆盖

研究阶段暂用资料库和任务管理两个不同领域的应用作为案例。它们用于暴露共性和领域差异，真实消费者及试用者尚待落实。

完整路径为应用作者接入并交付，用户选择 Agent，建立身份与权限关系，提供任务和上下文，Agent 请求操作，应用原业务接口执行，结果保存或展示，用户从原入口继续使用。

| 检查面 | 必须回答的问题 |
| --- | --- |
| 应用作者接入 | 新应用和已有应用分别需要改哪些地方，是否重复编写 Agent 专属代码，原业务方法能否供两个入口复用 |
| 发布后的连接 | 使用者能否连接自己的 Agent，连接与授权是否按使用者区分，发布者是否必须代管用户凭证 |
| 本机 Agent | Agent 究竟运行在最终用户机器还是应用服务器，浏览器或桌面应用通过什么受支持的组件连接它 |
| 远端 Agent | 服务是否已有受支持接口，如何认证和撤权，如何取得获准应用数据并调用应用方法，结果如何回到用户 |
| 两个入口 | A 的应用会话和 B 的原宿主会话分别由谁控制，连接、交互及操作结果是否完整可见 |
| 任务完整性 | 补充问题、批准或拒绝、停止、断线、恢复与不支持能力如何呈现，未知写入是否会导致重复执行 |

应用所在地与 Agent 所在地分别记录。云端应用服务器无法仅凭用户填入 localhost 地址连接用户电脑。远端 Agent 也需具备访问获准应用能力的实际通路。不能用改变执行机器或扩大权限使案例表面通过。

## 第一阶段完成选型与产品定义

主 Agent 负责统一结论，应用接入、Agent 运行与独立验收角色可以并行取证。评审只处理有依据的分歧与反例。

1. 把上述用户路径变成验收表，继承[现有完成标准](v1-features-and-flows.md#首版完成标准)及适用的权限、恢复和重复执行要求。补充本机与远端的连接条件。核对当前文档中本机首版建议与最新目标的关系，提出首版兼容范围，明确其余组合的状态。
2. 按同一张表核对现成方案。初始检查 CopilotKit／AG-UI、acpx、MCP SDK 和 Paseo；发现更贴近目标的 agentd、Plannotator BYOA 后将其纳入主要比较。各候选仅接入所需部分，评估新增进程、状态、凭证管理和维护负担，不把候选清单拼成必须全部部署的技术栈。
3. 区分文档声称支持、源码可确认、真实流程已验证、明确缺失与尚未核实。缺口再区分通用产品工作、协议语义不一致和应用专属接入。记录具体版本、支持接口、许可及生产可用范围，公开仓库本身不证明所有功能均可自由用于目标交付。
4. 从可访问的公开案例、讨论与已有实践寻找重复接入成本的证据。区分项目关注度、实际使用和应用作者愿意采用，直接访谈或联络维护者另按用户授权开展。
5. 输出一份覆盖结论及首版建议，明确可复用部分、真正的共性缺口、尚未验证事项和选择理由。证据集中在本文后续更新，不为每个候选另建流程或状态文档。

第一阶段以可评审的决策结束。交付应能回答采用哪个现成方案能做到什么、还需开发者完成什么、剩余通用工作是否有独立价值，以及下一阶段具体验证哪条连接路径。文档核查不能写成运行验收通过。

## 第二阶段通过实际接入决定投入方向

进入实施授权后，用上述案例比较直接采用现成组件与拟提供的接入方案。先完成一条从真实使用者到结果的路径，再验证另一应用复用、另一入口及其余承诺的 Agent／部署组合。各组合独立记录结果。

衡量首次接入耗时、必须修改的业务代码和配置、Agent 专属适配工作、最终用户操作及恢复步骤、是否依赖维护者手工帮助。先取得现成方案的基线，再判断改善，当前不预设缺少依据的时间或代码量门槛。首次成功之后还需观察用户能否独立重复使用。

| 验证结果 | 对应方向 |
| --- | --- |
| 现成产品已能方便完成用户路径 | 采用现成产品，整理实际需要的接入指南 |
| 共性缺口集中于某个上游的适配、交互或恢复能力 | 准备最小修订和可复现验收，具备对外授权后贡献上游 |
| 多个应用重复需要同一段连接与交互能力，单一上游职责难以承接 | 做可独立采用的接入组件，复用已有运行组件与协议 |
| 剩余工作基本是各应用的业务定义 | 将其保留在各应用，重新判断独立项目的收益 |
| 不同团队独立实现时因共同语义缺失而无法互通 | 优先提出已有规范的扩展或兼容约定，用独立实现和互通测试验证 |

首版只承诺通过完整流程的兼容组合。暂未支持的入口、引擎或部署方式保留为明确缺口，不能以更窄的演示代替原目标。

## 产品与协议同步收敛

现有[通用接入草案](general-integration-contract.md)作为需求检查表和约定草案。核查时为每项语义找到现有 ACP、MCP、AG-UI 或原生接口的对应位置，已有表达直接复用。

只有必要的跨实现行为在现有标准及其扩展机制中无法合理表达，并有独立维护者需要互通时，才评估新协议。公开规范、参考实现、版本兼容规则和互通测试共同支持外部采用。

## 安全与实现约束

应用继续持有业务身份、权限、事务和真实结果，Agent 引擎继续持有原生会话。拟议接入组件的状态仅限真实连接需要，并先检查现有组件能否承担，避免重复会话、凭证或业务状态。

后续实际接入涉及隐私、权限与跨层状态，按至少中风险验证，出现不可逆操作或高影响权限时升级。验证适用的越权拒绝、撤权、并发、重复执行、断线与未知结果，并从原应用读回真实成果。协议支持与界面提示不能代替执行端约束。

当前研究阶段不涉及持久化迁移或部署回滚。若后续替换既有运行组件，实施方案须补齐历史会话与结果兼容、失败切回和在途操作处理。关键约束已有证据后，工作转向接通缺失的用户路径，避免反复增加同类字段和校验层。

## 现成项目研究结论（青凝抽取评估前）

### 核查范围和证据等级

本轮完成公开官方文档、固定提交源码和作者公开运行记录的核查，未安装软件、启动 Agent、调用模型、部署示例或联系维护者。表中“已有”表示文档与所列源码支持，不能替代本项目的运行验收。HEAD 能力也不能直接视作所有已发布包或用户当前版本的能力。

“自己的 Agent”至少有三层不同含义：使用自己的安装和登录、使用自己的配置与插件、复用正在运行的具体会话。用户目标包含前两层，不强制所有场景都复用已打开的终端。不能因为某个候选擅长第三层，就将原有 A 流程中应用创建专属会话的要求删除。

### 项目覆盖与具体缺口

| 项目及核查版本 | 已有能力 | 对本目标的剩余边界 | 判断 |
| --- | --- | --- | --- |
| [agentd][agentd-root]，`d14adbb`，0.9.0 | 第三方页面 SDK、Go 应用服务端 SDK；每用户多机器配对；用户 daemon 主动连接应用；启动 Claude、Codex、Grok；ACP 转发与应用 MCP 工具桥；查看与撤销授权 | 安装产品当前面向 macOS；默认能力达 OS 用户权限，目录限制不是沙箱，服务端能回答 Agent 权限请求；断链终止相应 Agent，不重放旧帧；DSH、完整远端部署体验及跨实例即时撤权未闭合 | 与 A 的应用主动调用路径最接近，先验证其权限与恢复边界。不是可直接全量采用的结论 |
| [Plannotator BYOA][byoa-root]，`4f94993`，server 0.1.3 | 应用服务端 SDK、用户设备码配对、Claude Code/Pi/OpenCode 连接器；应用向已运行会话发消息并接收事件；同一连接可调用应用 MCP 工具；每用户身份与撤销 | 交互会话限定；不能从应用新建或唤醒已关闭的会话；没有 Codex/DSH 的等价连接器；多应用共用会话允许跨应用工具使用；live hub 重启可丢待办和事件；任意远端服务接口不在支持范围 | 最直接的“应用 SDK＋用户连接器＋共同约定”反例，值得复用和贡献；不能替代 A 的全部默认要求 |
| [Paseo][paseo-permissions]，`d682715` | daemon、第三方 SDK、本机/服务器运行、SSH/relay/配对、创建会话、MCP 注入、审批问答、取消和历史读取；Codex、Claude 及其他 provider 路线 | 有权限体系，但当前授权主要是 daemon-wide，direct 密码/本机凭据映射 owner；不等于第三方应用资源隔离；消费者须补历史读取和归并；DSH 社区插件需独立验收 | 远端运行与恢复的强候选，上游补应用授权值得研究 |
| [acpx][acpx-shared]，`00df1b2` | 多 Agent ACP 运行库；嵌入模式有会话 MCP、权限/补充信息回调；支持 Codex、Claude、DSH 等 profile | 不提供发布应用的网络配对产品；共享模式是同 OS 用户 IPC，能力不同于嵌入模式；配置与历史兼容按 profile 区分 | 适配组件，不能单独当完整用户连接产品 |
| [CopilotKit][copilot-runtime]／[AG-UI][agui]，CopilotKit `4f0e86d` | 应用聊天、事件、工具、状态、交互；每请求 Agent 工厂可按认证用户选择远端 endpoint；当前 OSS runtime 已有线程 owner 支持 | 用户安装、配对及 Agent endpoint 绑定需接入；生产浏览器直接注册的 selfManagedAgents 入口有商业许可限制；具体 adapter 须闭合工具和审批 | 应用交互组件，不宜因其未包办连接产品而另造全套 SDK |
| [MCP TypeScript SDK][mcp-auth]，`1e608ca` | 应用资源/工具、HTTP 或 stdio、认证辅助、受保护资源及客户端 OAuth；适合 B 的原宿主操作应用 | 应用提供真实身份绑定、业务权限和可达服务；不负责主动启动任意用户 Agent 或给其安装配对程序 | B 的主要复用基础，应用业务定义属于必要接入工作 |

这些项目存在替代关系。优先选择能承担所需运行方式的现有 owner，避免同时引入多个 daemon、会话数据库和授权服务。

### 应用与 Agent 分别位于哪里

| 实际组合 | 可复用路径 | 尚需验证或明确的边界 |
| --- | --- | --- |
| 发布的 HTTPS 应用 → 用户本机 Agent | agentd 的出站 daemon 配对；或 BYOA 交互会话连接器向应用长轮询 | 用户安装登录、应用/账号绑定、权限及结果恢复。两条出站路径不要求云端服务器访问用户 localhost |
| 发布的应用 → 用户自有远端机器上的 Agent | Paseo 已有远端连接产品；agentd 有 headless CLI；BYOA 受支持交互会话在远端运行并能访问应用时，出站机制原则上适用 | 后两者尚未在本轮做远端验收；交互式远端终端不等于无人值守服务，必须明确审批和会话寿命 |
| 发布的应用 → 用户提供的现有 Agent 服务地址 | CopilotKit 按用户选择兼容 AG-UI endpoint；其他协议由实际 adapter 连接 | 认证、受支持协议、工具回调、取消/恢复都需匹配。不能承诺填任意 URL 即兼容任意 Agent |
| 本地应用 → 本机 Agent | 随附运行组件、acpx 嵌入，或用户共享 daemon/连接器 | 本机同用户 IPC 不等于相互不信任应用的授权隔离；随附和共享选择应减少用户重复安装 |
| 本地应用 → 远端 Agent | 应用能力有远端可达受保护入口或已验证反向桥；控制链可用远端 runtime | 远端看到的 localhost 不是用户电脑。仅传 MCP URL 不能证明应用方法能被调用 |
| 原 Agent 宿主 → 应用（B） | 应用受保护 MCP endpoint；BYOA 可为支持宿主代理其工具 | 宿主负责原会话；应用负责业务权限和效果。跨应用材料披露仍需宿主实际控制，不能用配对成功代替 |

若采用“公网网页直接访问本机服务”，还须验证目标浏览器的本地网络许可、来源限制及用户实际步骤。[Chrome 当前说明][chrome-lna]将公网网站访问 loopback 纳入 Local Network Access，localhost 开发演示不能代替发布后验证。优先使用已有出站路径时，不额外增加这项浏览器权限要求。

### 开发者和最终用户实际要做什么

新应用与已有应用使用同一接入分工。新应用在设计时提供业务能力出口；已有应用在原服务上增设受保护适配入口和界面，继续复用原身份、权限、事务和数据。不存在安全通用的“给未接入、无扩展点的任意应用配置一下即可拥有完整能力”。

采用 agentd 路线时，开发者接应用 SDK、用户身份映射、授权记录存储和 MCP 工具桥，再接任务输入、审批、停止与结果展示。最终用户在自己的机器安装运行服务并完成 Agent 登录，在应用里取得配对信息，在本机确认目标应用，选择机器/Agent 后使用。应用通过已配对的出站链路调用该用户机器。远端机器需另外验证安装、授权、可达性和审批路径，不能默认为本机步骤原样通过。

采用 BYOA 路线时，开发者挂载服务端 handler，接可信应用登录、持久连接存储、按用户路由的 hub、已有 MCP 工具和界面。用户在受支持的交互 Agent 中安装连接器，执行连接命令，在应用登录状态下核对配对码并授权。新配对应用可以投递消息，但其工具按会话起点固定，可能要进入下一会话或按该宿主支持的方式重载，确认工具可见后才能完成业务任务；不能把“已连接”直接当作工具可用。此后可在应用发起任务，或在原 Agent 中使用应用工具。批准仍由原宿主处理；关闭原会话后应用不能自行把它唤醒。纯静态网站还需要相应服务端或经过验证的服务，SDK 不会凭空提供后端。

两条路线都不要求应用发布者统一代管每位用户的模型登录。Agent 所在机器仍需具备有效安装、配置和认证；复用全部插件、记忆、历史与个人设置不是自动成立的承诺。

### 真正还缺什么，以及应该由谁承担

| 剩余工作 | 归属与行动判断 |
| --- | --- |
| 应用业务工具、对象权限、schema、事务、成果读取 | 每个应用原 owner 的正常接入责任，不能计为独立产品机会 |
| 每应用授权、资源范围、撤销旧连接、原生工具权限 | 属连接/runtime 与宿主边界。agentd/Paseo 的现有授权能力可复用，但必须验证能否落实本项目边界；不能靠提示词或目录白名单冒充执行约束 |
| 同会话跨应用材料披露 | 现有草案要求按目的、范围和接收方控制。BYOA 明确允许跨应用工具，原宿主批准提示不等于已经满足该要求。需要受支持宿主策略或上游可接受的独立 profile；可行性和维护者意愿未核实 |
| 连接中断、会话重启、未知业务效果 | 连接器负责如实报告和接续运行状态，原应用负责效果、防重及读回。BYOA 内存 hub、agentd 断链退出、Paseo 历史归并语义不同，不能统一声称“自动恢复” |
| Codex／Claude／DSH 能力一致性 | 对具体 runtime/adapter 做兼容核查，能映射的交互优先修上游。DSH 指 DeepSeek Harness，不等于调用 DeepSeek 模型 API |
| 多系统安装、无头远端、换机、凭证失效和独立接入指南 | 可形成连接产品的价值，但现有项目已有部分交付。先验证重复成本，尚不足以证明另建独立产品有必要 |

应用 A 专属会话可以减少意外混用，但不能据此声称 B 的同宿主跨服务披露已经解决。只读演示也不能替代已要求的写入、防重和成果读回。

### 源码中影响决策的核实与纠错

- BYOA 的 [SPEC][byoa-spec] 与 [store][byoa-store] 区分持久配对/连接和易失 live hub；[hub][byoa-hub] 对重启后未知消息事件可能接收后丢弃；[turns][byoa-turns] 是进程内去重。稳定 session ID 和网络重试不是跨重启任务恢复，更不是业务 exactly-once。
- BYOA 撤权会切断连接授权，但 connector 的 [session][byoa-session] 与 [turns][byoa-turns] 删除关联时没有自动调用宿主 abort。撤权不等于强制停止已运行轮次，更不等于回滚已经发生的效果；原应用仍须在后续方法调用时校验当前授权。
- BYOA 的 [设计说明][byoa-design]已明确交互会话、跨应用工具和宿主批准的取舍。该文件含早期设想，具体当前 API、允许的人类发起方式及可用包以 [server 文档][byoa-server]和 SPEC 为准，不能把计划中的 React UI 或存储适配器写成已交付。
- agentd 的 [server.go][agentd-server] 已有外部 `PairingStore`，不能沿用旧段落认定配对只能存在内存。在线 peers/sessions/bridges 仍属于各 Server 实例，本轮没有确认跨实例路由与即时撤权全链。其[权限说明][agentd-daemon]明确应用服务端能力和非沙箱边界。
- CopilotKit 的 [runtime.ts][copilot-runtime] 已有 `AgentsFactory` 和可信 `identifyUser` 扩展点；[in-memory runner][copilot-runner]已有 owner 检查。不能用落后网页断言其没有多用户支持。旧持久记录迁移及实际发布包仍待验证。[selfManagedAgents][copilot-self] 的商业范围仅影响该生产入口，不代表整个 AG-UI 或 CopilotKit 都不可开源使用。
- [acp-to-agui 的 endpoint][acp-agui] 声明 tools/context/state，却仅将最后一条用户消息传给 ACP run。该参考桥未证明应用工具与上下文完整回传，不能按 README 把聊天演示当完整集成。
- acpx 的 [shared 文档][acpx-shared]明确其能力不同于 embedded runtime；[Claude profile][acpx-claude]默认不载入用户全局 settings；[DSH profile][acpx-dsh]的恢复有原生限制。Paseo 的 [direct admission][paseo-admission]与[权限文档][paseo-permissions]说明 owner/daemon 范围，不能说完全无授权，也不能说已完成每应用最小授权。

### 是否需要新协议

需要共同约定，但现阶段没有证据要求我们另造完整协议。MCP 继续承担应用资源与方法，ACP/原生接口承担受控 Agent 会话，AG-UI 可承担应用界面事件。BYOA 已探索“应用向现有交互会话投递消息、配对和回传”的额外约定，其出现本身就是应先比较和参与的上游。

ACP v1 [正式传输说明][acp-transport]仍以 stdio 为定义传输，允许有文档的自定义传输，远端 HTTP 另属提案；agentd 的 WebSocket 路径不能直接称为所有 ACP 实现都支持的远端标准。现有约定也不能保证任意部署、任意 Agent 或安全策略互通。

优先贡献实际适配和明确兼容行为。只有至少两个独立实现确实需要同一缺失语义、已有扩展方式无法承担，且有人愿意共同维护与做互通验收，才提新标准。现有通用草案继续作为需求与验收依据，尚不冻结为另一条网络协议。

### 需求证据与投入建议

BYOA 的[公开运行记录][byoa-proof]记载 Machine 接入、Workspaces staging 和存储一致性检查，也记录真实模型调用曾失败及工具结构化结果曾不完整。它支持“有应用作者在重复解决这个问题”的判断；这些是同一作者生态的运行记录，本轮未独立复跑，不能等同广泛外部采用。agentd 有第三方 SDK、示例及作者命名的消费者，也不足以证明稳定外部需求。项目数量、stars 和下载量都不替代真实应用作者与最终用户的持续使用。

**建议选择上游优先。** 首先验证 agentd 能否以可接受的授权方式完成原有 A 的应用专属会话路径；用 BYOA 检查原会话复用可以省掉哪些重复工作，用 Paseo 比较远端与恢复。之后只向实际承载该缺口的上游准备最小修订。不要为了统一表面 API，先把这些候选拼成一个新平台。

仍有价值的独立产品条件是：至少两款不同应用重复遇到同一接入障碍，有真实最终用户；该障碍影响完整使用而非仅文档好看；上游职责或明确设计不适合承担；独立组件能复用现有 runtime、会话和业务 owner，确实减少接入与维护成本。独立产品可限于连接和授权交付层，不预设重写 Agent 引擎与协议。

当前不能把“上游可能不接受策略”写成已拒绝，也不能把“存在缺口”写成已证明独立产品值得做。授权后的试用若证明可直接采用，则无需为了开源而开发新项目。

### 评审范围

应用接入、Agent 运行、市场反例和 BYOA 语义分别取证，独立裁判核对关键源码和既有草案要求。裁判确认应修正“没有类似产品”，并支持上游优先、agentd 先验证 A 路径、BYOA 作交互会话对照的建议。裁判同时否定“BYOA 已满足全部范围”“配对即受限执行”“重连即完整恢复”和“有缺口所以必须新协议”的推断。文档结论与产品运行验收分开记录；本轮不声称全部需求通过。

## 前轮提出的运行验证路径

本轮研究与选型建议交付后，下一条待验证的用户路径为：已发布 HTTPS 应用中的真实用户，通过 agentd 配对自己机器上的 Codex 或 Claude，建立该应用专属会话，由获准 MCP 方法完成一次业务写入，再从原应用读回结果。

首先确认真实可执行的权限边界：谁批准本机操作，服务端是否能越过用户限制，应用 B 是否能访问 A 的会话或材料，撤权后旧连接是否失效。若现有配置无法满足，记录阻断点及适合贡献的位置，不用全自动批准或放宽权限换取演示通过。此后才验证断线后的未知效果和防重、B 入口、第二应用复用及远端/其他引擎组合。每个组合独立报告，首条通过不代表全目标通过。

该运行验证尚未开始，仍遵守“先不开发”。需要后续进入实施范围及真实应用入口后执行；本轮未对外发消息、提交 issue/PR 或承诺上游合作。

## 主要证据索引

以下固定源码用于复核；动态文档按 2026-11-04 所见记录。主要项目许可为 BYOA 的 MIT OR Apache-2.0、agentd/acpx 的 MIT、Paseo 的 Apache-2.0；具体依赖、商业组件和分发内容仍须按实际采用版本核对，当前未发生代码复制或分发。

[agentd-root]: https://github.com/nguyenvanduocit/agentd/blob/d14adbb2b952f49cf7bd013781110592c8423a3b/README.md
[agentd-server]: https://github.com/nguyenvanduocit/agentd/blob/d14adbb2b952f49cf7bd013781110592c8423a3b/sdk/goserver/server.go
[agentd-daemon]: https://github.com/nguyenvanduocit/agentd/blob/d14adbb2b952f49cf7bd013781110592c8423a3b/daemon/README.md
[byoa-root]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/README.md
[byoa-server]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/packages/server/README.md
[byoa-spec]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/docs/SPEC.md
[byoa-design]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/docs/design.md
[byoa-proof]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/docs/PROOF.md
[byoa-store]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/packages/server/src/store.ts
[byoa-hub]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/packages/server/src/hub.ts
[byoa-turns]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/packages/connector-core/src/turns.ts
[byoa-session]: https://github.com/plannotator/byoa/blob/4f94993abf0fe7bcd6f6554978c967dbffd5a5fe/packages/connector-core/src/session.ts
[paseo-permissions]: https://github.com/getpaseo/paseo/blob/d68271565ab150ce4c854c5b40c1c7bf1604231b/docs/permissions.md
[paseo-admission]: https://github.com/getpaseo/paseo/blob/d68271565ab150ce4c854c5b40c1c7bf1604231b/packages/server/src/server/session-admission-auth.ts
[acpx-shared]: https://github.com/openclaw/acpx/blob/00df1b223f41491f4bcf4f9fed6a7518b255675a/docs/shared-sessions.md
[acpx-claude]: https://github.com/openclaw/acpx/blob/00df1b223f41491f4bcf4f9fed6a7518b255675a/agents/Claude.md
[acpx-dsh]: https://github.com/openclaw/acpx/blob/00df1b223f41491f4bcf4f9fed6a7518b255675a/agents/DeepSeekHarness.md
[copilot-runtime]: https://github.com/CopilotKit/CopilotKit/blob/4f0e86deaebb9d6e6d4625cbed4087912aee6d0c/packages/runtime/src/v2/runtime/core/runtime.ts
[copilot-runner]: https://github.com/CopilotKit/CopilotKit/blob/4f0e86deaebb9d6e6d4625cbed4087912aee6d0c/packages/runtime/src/v2/runtime/runner/in-memory.ts
[copilot-self]: https://docs.copilotkit.ai/claude-sdk-typescript/backend/self-managed-agents
[agui]: https://docs.ag-ui.com/concepts/architecture
[mcp-auth]: https://github.com/modelcontextprotocol/typescript-sdk/blob/1e608caeb5130b2ad0fa067c84b26a038c1c6e36/docs/serving/authorization.md
[acp-agui]: https://github.com/namanrajpal/acp-to-agui/blob/f1de1beae40ed70445a5b7270d607fcb9761ee45/backend/agui_endpoint.py
[acp-transport]: https://agentclientprotocol.com/protocol/v1/transports
[chrome-lna]: https://developer.chrome.com/docs/modern-web-guidance/guides/security/local-network-access
