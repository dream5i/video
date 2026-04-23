# 全新项目 AI 编程栈方案与结论

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 边界分层、复用策略与模型接口预留](./boundary-reuse-and-provider-strategy.md)

## 1. 我对你这次问题的理解

这次你问的重点，不是我们产品面向用户提供什么 AI 能力，而是：

`我们这个项目在研发和 AI 编程层面，应该把 Harness、OpenAI、Anthropic 分别放在什么位置。`

也就是要回答：

1. 我们现在该依赖谁做主要 AI 编程与 agent 能力。
2. Harness 要不要进主链路。
3. OpenAI 和 Anthropic 该怎么分工。
4. 后面如果要支持多模型或多供应商，接口应该怎么预留。

## 2. 官方信息里最关键的事实

以下结论仅基于官方资料，且时间点按 `2026-04-23` 看。

### 2.1 Harness 官方表达的核心

根据 Harness 官方 Developer Hub：

- `Harness AI` 的核心定位是把 AI 放进整个软件交付生命周期，而不只是代码生成。
- 官方 `Harness Agents` 页面明确写到，它的 agents 是在 `Harness pipelines` 内执行 DevOps 任务的 autonomous workers，pipeline 是 orchestration layer。
- 官方 `Harness CDE` 页面明确写到，Gitspaces 使用 `devcontainer.json` 作为标准化远程开发环境定义，强调 zero drift。

从官方表述看，Harness 更像：

`AI 驱动的软件交付与平台工程系统`

而不是“我们项目现在最需要的 AI 编程内核”。

这点非常重要。

因为我们现在缺的不是：

- 企业级 pipeline 编排平台
- DevOps agent 控制面
- 远程 Gitspace 平台

我们现在真正缺的是：

- 高质量 AI 编程执行能力
- 清晰的 agent/工具抽象
- 低摩擦的研发闭环

### 我对 Harness 的判断

Harness 很强，但它更适合：

- 团队规模更大之后的工程平台化
- 远程开发环境标准化
- CI/CD、部署、修复、SRE、平台编排自动化

它不适合在我们当前阶段进入最核心产品代码路径。

### 2.2 OpenAI 官方表达的核心

根据 OpenAI 官方文档：

- OpenAI 明确推荐新项目使用 `Responses API`，而不是优先从旧的 Chat Completions 开始。
- 官方 Responses 文档强调它是统一接口，支持 stateful interactions、built-in tools、function calling、structured outputs。
- `GPT-5.2-Codex` 的官方模型页明确写它是“optimized for agentic coding tasks”。
- OpenAI Agents SDK 官方文档明确把 primitives 收敛为：
  - agents
  - handoffs
  - guardrails
  - tracing
- OpenAI 数据控制文档明确写到：`As of March 1, 2023, data sent to the OpenAI API is not used to train or improve OpenAI models unless you explicitly opt in.`

从官方表述看，OpenAI 当前最适合承担的是：

`我们的主 AI 编程与 agent 平台能力`

原因不是“它什么都最好”，而是它在官方产品层面已经把下面这些东西打包得比较完整：

- coding-oriented models
- Responses API
- tools
- state
- agents SDK
- data controls
- tracing / orchestration primitives

### 2.3 Anthropic 官方表达的核心

根据 Anthropic 官方文档：

- `Claude Code` 官方定位就是 terminal-native 的 agentic coding tool。
- 官方页面明确说 Claude Code 可以编辑文件、运行命令、在 CI 中自动化任务。
- 官方页面明确说它支持 `MCP`，可以连接外部工具和数据源。
- Anthropic 的 tool use 文档对 tool schema、tool_choice、tool_result 顺序、strictness 说得非常细，说明它在工具调用这条线上很成熟。
- Anthropic 官方 `Claude Code data usage` 页面明确说：商业用户在商业条款下，Anthropic 不会用发给 Claude Code 的代码或 prompt 来训练生成模型，除非客户选择加入改进计划。

从官方表述看，Anthropic 当前最适合承担的是：

`高质量 AI 编程第二引擎 / reviewer / fallback / MCP 生态兼容层`

也就是说，Anthropic 很适合放在：

- 代码审查
- 复杂工具调用实验
- 多代理补充
- second opinion

但如果只选一个主栈来推进项目，我不会把 Anthropic 放在唯一主依赖上。

## 3. 方案结论

### 3.1 总结一句话

`现在不要把 Harness 放进主开发路径；用 OpenAI 做主 AI 编程与 agent 基座，用 Anthropic 做兼容、校验和补充。`

### 3.2 我建议的角色分配

### A. Harness

定位：

- 暂不进入产品主路径
- 暂不进入代码核心依赖

后续可考虑：

- 团队扩大后的 Gitspaces / CDE
- DevOps pipeline agents
- CI/CD 层自动修复或部署编排

当前不建议：

- 让 Harness 决定我们的应用架构
- 让 Harness 成为日常 AI 编程主依赖

### B. OpenAI

定位：

- 主 AI 编程引擎
- 主 agent orchestration 参考系
- 主接口设计参考

建议承担：

- 编程型主模型
- agent 运行主逻辑
- structured output
- function calling / tool orchestration
- stateful response loop

### C. Anthropic

定位：

- 第二模型通道
- reviewer / fallback / benchmark
- MCP 兼容能力重要参照

建议承担：

- 代码审查与 second opinion
- 复杂工具调用对照实验
- 将来多模型兼容层的第二实现

## 4. 对我们项目最合适的落地方式

### 4.1 现在的研发层

当前阶段，我建议我们这样做：

- 主研发执行：继续以我现在这条 `Codex / OpenAI` 路线为主
- 架构设计：按 OpenAI 的 `Responses + Agents + tool abstractions` 思路设计
- 抽象层：按 capability/provider 的方式预留 Anthropic
- DevOps：先不用 Harness 进入关键路径

### 为什么这样最合适

因为我们现在最需要的是：

- 快速建出主链路
- 让 AI 真正参与编码和重构
- 把工具和 provider 抽象先定稳

而不是：

- 先搭一个大而全的软件交付平台

### 4.2 现在的产品层

如果以后我们的产品内部也要加入 AI agent 能力，我建议技术上先按下面分层：

- orchestration API
- provider registry
- capability interfaces
- OpenAI primary adapters
- Anthropic secondary adapters

不要直接写成：

- `use_openai_everywhere()`

也不要直接写成：

- `Harness decides the pipeline`

## 5. 具体技术建议

### 5.1 主编排接口：按 OpenAI 风格设计，但不锁死 OpenAI

也就是说，我们自己内部要定义：

- `AgentRequest`
- `AgentResponse`
- `ToolCall`
- `StructuredResult`
- `RunTrace`

然后：

- OpenAI adapter 去适配 Responses API
- Anthropic adapter 去适配 Messages / tool use / Claude Code style tools

这样做的好处是：

- 工程上先吃到 OpenAI 现成生态的红利
- 架构上不被 OpenAI 绑定死

### 5.2 工具系统：优先做 MCP-friendly

Anthropic 官方强调 MCP，OpenAI 官方也支持 MCP 文档服务器与 remote MCP 工具能力。

所以我建议我们自己的工具抽象直接向 MCP 兼容靠。

具体做法：

- 工具统一 schema 化
- 工具输入输出结构化
- 工具能力声明化
- 未来可以映射到 MCP server

这会让我们同时兼容：

- OpenAI 风格 tools
- Anthropic 风格 tools
- 本地 CLI / 内部系统工具

### 5.3 模型抽象：按能力，不按厂商

建议直接定义：

- `CodingAgentProvider`
- `CodeReviewProvider`
- `PlanningProvider`
- `ToolUseProvider`

而不是：

- `OpenAIProvider`
- `AnthropicProvider`

后者可以存在于 adapter 层，但不能暴露成业务层依赖。

### 5.4 状态与审计：照 OpenAI 的 tracing / Responses 思路做

我们自己的系统要有：

- request id
- run id
- step trace
- tool trace
- provider trace
- cost/usage trace

OpenAI 官方在 Agents SDK 和 Responses 上对 tracing、state、structured items 的方向是对的，这一套很适合我们借鉴。

### 5.5 数据与隐私：默认按最严格模式设计

OpenAI 官方提供 `store: false`、ZDR、data residency 等控制。
Anthropic 官方也明确了商业条款下不会用商业用户的代码和 prompt 做训练，除非客户显式加入改进计划。

所以我们的工程默认应该这么做：

- 默认不依赖“服务端永久记忆”
- 敏感上下文在我们自己的系统里控
- provider 请求尽量最小化传输
- 所有 provider usage 和 retention 做配置化

换句话说：

`我们自己的系统负责记忆和状态，模型服务只负责推理和工具调用。`

## 6. 分阶段建议

### 6.1 Phase 1：现在立刻执行

选择：

- `OpenAI-first`
- `Anthropic-compatible`
- `Harness-later`

行动：

- 按 OpenAI-first 的 agent 抽象来搭代码骨架
- 先定义 provider interfaces
- 先定义 tool schema
- 先不接 Harness

### 6.2 Phase 2：骨架稳定后

加入：

- Anthropic provider adapter
- 多模型对照评测
- reviewer / fallback 流程

### 6.3 Phase 3：团队和工程复杂度上来后

再评估：

- 是否要引入 Harness Gitspaces
- 是否要把 CI/CD agent 化
- 是否要把部署、修复、回滚、SRE 放进 Harness

也就是说，Harness 不是现在不用，而是：

`不是 MVP 阶段的第一依赖。`

## 7. 最终结论

如果你现在要我给一个最明确、最可执行的结论，我的结论是：

### 结论 A

`我们现在的 AI 编程主栈，应该选 OpenAI 做主，不要先选 Harness 做主。`

### 结论 B

`Anthropic 应该作为第二能力层和兼容层预留，而不是被排除。`

### 结论 C

`Harness 适合以后接在工程平台层，不适合现在决定我们的应用核心架构。`

### 结论 D

`架构上必须按 capability/provider abstraction 来做，这样你后面无论加 OpenAI、Anthropic、还是别的模型，都不用推翻系统。`

## 8. 我建议你现在批准我继续做的事情

如果按这个方案往下走，下一步最合理的是直接进入搭建：

1. 建仓库骨架
2. 建 shared contracts
3. 建 provider interfaces
4. 先接 OpenAI primary adapter 的空实现
5. 预留 Anthropic adapter 位置

## 9. 官方来源

### Harness

- [Overview of Harness AI](https://developer.harness.io/docs/platform/harness-ai/overview/)
- [Harness Agents](https://developer.harness.io/docs/platform/harness-ai/harness-agents/)
- [Harness Cloud Development Environments Overview](https://developer.harness.io/docs/cloud-development-environments/overview/)

### OpenAI

- [Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [GPT-5.2-Codex model page](https://developers.openai.com/api/docs/models/gpt-5.2-codex)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data)

### Anthropic

- [Claude Code overview](https://code.claude.com/docs/en/overview)
- [Define tools / tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Claude Code data usage](https://code.claude.com/docs/en/data-usage)
