# 全新项目 企业级 AI 就绪度评估

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 主链图](./main-flow-diagram.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 边界分层、复用策略与模型接口预留](./boundary-reuse-and-provider-strategy.md)
- [全新项目 AI 编程栈方案与结论](./ai-coding-stack-recommendation.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)

## 1. 这份文档解决什么问题

这份文档只回答一个现实问题：

`如果我们不是只做一个能跑的 AI 产品，而是往企业级可交付、可治理、可持续运营的方向走，现在还缺什么？`

这里的“企业级”不等于一上来做得很重，而是指：

- 可控
- 可审计
- 可评估
- 可扩展
- 可治理

## 2. 官方资料里最值得提炼的企业级要求

## 2.1 OpenAI 官方信号

从 OpenAI 官方文档里，可以提炼出几个很明确的生产化要求：

### A. 生产环境不是只把模型接上就算完成

OpenAI 的 `Production best practices` 明确强调：

- 分开 staging 和 production 项目
- 配置 spend limits / rate limits
- 用 secret management，不要把 key 暴露在代码里

这说明：

`企业级 AI 系统必须从一开始就把环境隔离、凭据安全、额度控制纳入系统设计。`

### B. AI 系统必须做 eval

OpenAI 的 `Evaluation best practices` 直接指出：

- 生成式 AI 是可变的
- 传统软件测试对 AI 架构不够
- eval 是生产环境里验证准确性、性能和可靠性的关键手段

这意味着：

`没有评测体系的 AI 系统，不能算企业级。`

### C. Prompt 也应该像资产一样被版本化

OpenAI `Prompting` 文档明确写到：

- 平台提供 long-lived prompt object
- 支持 versioning
- 可以和 eval 关联
- 可以回滚

这对我们很重要，因为这说明：

`Prompt / planning 模板 / agent instructions` 不应该只是散落在代码里的字符串，而应该进入版本治理。`

### D. 可观测性不是可选项

OpenAI Agents SDK 文档明确提供：

- tracing
- spans
- tool calls
- guardrails

并且说明 tracing 默认开启，但也要注意 sensitive data 配置。

这意味着：

`企业级 AI 系统必须能追踪一次 agent/run/tool 调用链，而不是只知道“结果失败了”。`

### E. 数据治理必须前置

OpenAI `Your data` 文档明确写到：

- 支持 data residency controls
- Zero Data Retention 会影响某些能力
- Responses API 默认有应用状态保留期

这意味着：

`数据保留策略、是否 store、是否 ZDR、是否用扩展缓存，不是上线后再想的问题，而是架构时就要定。`

## 2.2 Anthropic 官方信号

Anthropic 官方资料里，企业级信号也很明确。

### A. 管理策略要能“强制下发”

`Set up Claude Code for your organization` 里写得很清楚：

- 组织管理员要决定 provider
- 要决定 managed settings 如何下发
- 要决定允许哪些工具、命令、MCP server 和网络访问
- 要决定 usage visibility 和 data handling

这说明：

`企业级 AI 系统不只是给用户一个模型，而是要有策略分发与强制执行能力。`

### B. 组织级监控和 ROI 追踪是正式能力

Anthropic 的 analytics / monitoring 文档已经把下面这些做成了正式指标：

- 使用量
- 会话数
- 代码接受量
- 成本
- adoption
- PR / commit / tool usage

这说明：

`企业级 AI 不能只看 token 账单，还要看 adoption、效率、工具调用和业务影响。`

### C. 评测必须是工作流的一部分

Anthropic 的 Evaluation Tool 文档明确支持：

- 测试用例
- 反复重跑
- prompt 修改后的对比

这和 OpenAI 的方向一致：

`Prompt 和 agent 变更，应该默认进入 eval 回路，而不是凭感觉上线。`

### D. 速率和花费要当成一等公民

Anthropic 的 rate limits 文档清楚给出：

- request / input token / output token 限额
- reset header
- workspace 级限制

这意味着：

`企业级 AI 需要内建 rate limit awareness、预算管理和退避策略。`

### E. 数据与合规边界必须写清楚

Anthropic `Claude Code data usage` 明确说明：

- 商业用户默认不用于训练，除非显式加入改进计划
- 商业用户有标准保留期
- 某些 Enterprise 场景可开 ZDR
- 本地缓存和遥测也要单独看

这意味着：

`AI 系统除了模型调用本身，还要治理本地缓存、遥测、反馈通道和错误上报。`

## 2.3 Harness 官方信号

Harness 官方资料给我们的启发，不是“拿来当主 AI 编程基座”，而是：

`它展示了企业级治理层到底长什么样。`

### A. 企业级平台一定会有 RBAC / SSO / Secrets / Audit / Policy

Harness Platform 首页明确把这些列为平台基础：

- RBAC
- SSO
- Secrets
- Governance
- Audit trails

这说明：

`企业级工程平台的底座是治理能力，而不是模型本身。`

### B. Audit 不是简单日志，而是可外部流式导出

Harness audit streaming 文档强调：

- 审计日志可流向外部系统
- 可用于合规、告警、异常检测和长期保存

这意味着：

`企业级 AI 平台不能只把日志留在本地文件里。`

### C. Policy as Code 是真正的“边界固定器”

Harness Policy as Code 文档明确：

- 用 Rego 写策略
- Policy Set 绑定实体和事件
- 可在保存、运行、步骤开始等阶段执行

这对我们非常有启发：

`企业级 AI 最终一定会走向“策略化约束”，而不只是靠人工约定。`

## 2.4 行业通用框架与安全信号

只看模型厂商官方文档还不够。真正走向企业级时，还要参考跨厂商、跨平台的共识框架。

### A. NIST AI RMF 说明“治理不是附属能力”

NIST AI Risk Management Framework 把 AI 风险管理拆成四个持续函数：

- Govern
- Map
- Measure
- Manage

这件事对我们意味着：

`企业级 AI 不能只有“开发和调用”，还必须有治理、风险映射、度量和处置闭环。`

### B. OWASP LLM Top 10 说明“AI 特有攻击面”必须单独治理

OWASP 对 LLM 应用的高频风险点里，最值得我们现在就纳入设计的是：

- prompt injection
- sensitive information disclosure
- supply chain / plugin / tool risk
- excessive agency

这对我们项目尤其重要，因为我们的输入来源本身就是：

- 外部链接
- 外部文案
- 外部素材
- 外部模型

也就是说：

`我们面对的是多层不可信输入，不做 AI 专项安全边界，后面问题会很集中。`

### C. 云厂商 guardrails 说明“输入和输出都要有门禁”

Amazon Bedrock Guardrails 官方文档已经把下面这套逻辑产品化了：

- 先检查输入
- 输入不通过时直接阻断模型调用
- 再检查输出
- 输出违规时覆盖、屏蔽或拦截

这个信号很重要，因为它说明：

`真正成熟的企业级 AI 不是只在结果页补审核，而是把 guardrail 放进运行链路。`

### D. 企业级行业实践已经把 AI 可观测性独立成一层

开源侧比较清楚的信号来自：

- Langfuse：`observability + evals + prompt management + datasets`
- LiteLLM：`gateway + authz + spend management + guardrails + fallback`
- OPA：`policy as code`
- Keycloak：`identity + strong auth + fine-grained authorization`

这说明：

`企业级 AI 产品通常不会把所有治理能力都手写到底，而是会保留产品主链自研，同时适度复用治理底座。`

## 3. 结合我们项目，企业级还缺什么

按我们现在这条线来评估，我把内容分成 3 类：

- `已经具备方向`
- `短期必须补`
- `中期企业增强`

## 3.1 已经具备方向

我们目前已经有的东西，其实不算少：

### A. 主链固定

我们已经明确主链：

`输入 -> 分析 -> 预填充工作流 -> 运行 -> 结果 -> 历史`

这很好，因为企业级系统最怕主链反复漂移。

### B. 边界冻结意识已经有了

我们已经补了：

- 治理文档
- AGENTS 规则
- schema freeze
- implementation roadmap

这相当于已经有了“轻量 policy”的雏形。

### C. provider abstraction 方向是对的

我们已经决定：

- capability-based providers
- OpenAI-first
- Anthropic-compatible

这很关键，因为企业级系统必须能换供应商、做 fallback、做审计。

### D. 运行对象和状态机雏形已经有了

我们已经围绕下面这些对象设计：

- Project
- AnalysisRun
- WorkflowDraft
- RenderRun
- RunStep

这为审计、追踪和回溯打了底。

## 3.2 短期必须补的内容

这些东西不是“以后再说”，而是如果我们想往企业级走，应该很快补上。

### 1. 身份与访问控制模型

当前缺口：

- 没有 auth 方案
- 没有角色模型
- 没有 project scope / org scope

建议：

- 先补最小 auth
- 至少定义：
  - owner
  - member
  - service account

即使首版不做复杂 UI，也要先把数据模型预留出来。

### 2. Secret 管理策略

当前缺口：

- 只有 `.env.example`
- 没有正式 secret source strategy

建议：

- 本地开发：`.env`
- 部署环境：secret manager / KMS
- provider key 不允许散落在业务代码中

### 3. Prompt / Planning 版本治理

当前缺口：

- 我们有 schema，但还没有 prompt registry

建议：

- 至少给下面这些对象加版本治理：
  - analysis prompt
  - script prompt
  - shot plan prompt
  - guardrail prompt

### 4. Evals 体系

当前缺口：

- 我们还没有 eval dataset
- 也没有 regression suite

建议：

- 先做最小 eval：
  - 10 条爆款链接样本
  - 10 条商品 brief 样本
  - 针对 insight / script / shot plan 做 rubric

### 5. Tracing / Observability

当前缺口：

- 我们有 run/step 思路
- 但还没有 trace id / span / tool trace 实现

建议：

- 先补最小 tracing 约定：
  - request_id
  - project_id
  - run_id
  - provider
  - capability
  - latency_ms
  - token/cost

### 6. Audit Event 设计

当前缺口：

- 现在还没有 audit event schema

建议：

- 至少定义 3 类事件：
  - config events
  - run events
  - security events

### 7. Rate limit / Cost 控制

当前缺口：

- provider 预留了
- 但还没有预算与退避设计

建议：

- 在 registry 和 run 层补：
  - retry policy
  - backoff policy
  - monthly budget / soft limit / hard limit
  - provider quota visibility

### 8. 数据治理策略

当前缺口：

- 还没有正式 retention policy
- 也没有明确哪些数据可持久化、哪些不该存

建议：

- 先定：
  - prompts 是否持久化
  - provider raw response 是否持久化
  - traces 是否包含敏感数据
  - 文件保留多久
  - 是否支持区域化存储

## 3.3 中期企业增强

这些不一定现在做，但如果以后要给企业客户交付，迟早会做。

### A. SSO / SCIM

- 企业登录
- 自动用户同步

### B. Policy as Code

- 对 provider 使用、模型选择、敏感操作、上线前检查做策略约束

### C. 审计外部流转

- 把 audit / traces / security events 导到 SIEM 或 observability 平台

### D. LLM Gateway / Centralized provider control

- 做统一出入口
- 做供应商切换、日志、预算和策略拦截

### E. 人工审批与高风险操作门禁

- 例如：
  - 删除项目
  - 改数据保留策略
  - 启用新 provider
  - 发布影响成本的策略

## 3.4 用 AI 做企业级产品，还要补的专项能力

这一节不是通用 SaaS 能力，而是 AI 场景独有、并且我们项目会直接踩到的内容。

### A. 不可信输入隔离

我们项目的输入不是单纯表单，而是：

- 视频链接
- 抖音/外部平台文案
- OCR / transcript
- 用户补充 brief

建议补：

- source trust level 字段
- 原始输入和规范化输入分层存储
- prompt 中明确区分 user content / system instruction / extracted content

### B. Prompt injection 与工具边界控制

因为我们会让模型消费外部内容，所以必须默认把外部文本视为潜在指令污染源。

建议补：

- tool allowlist
- model capability allowlist
- 外部抽取文本不得直接提升为 system instruction
- 高风险工具调用走 blocking guardrail

### C. 模型、Prompt、数据集和结果要能串成“谱系”

企业环境里，最怕的是线上结果异常但追不回去。

建议每次 run 至少记录：

- prompt_version
- model_provider
- model_name
- workflow_schema_version
- eval_set_version
- output_snapshot_hash

### D. 安全与质量不能只做一次离线测试

建议把 eval 分成 3 类：

- 质量评测：insight / script / shot plan 是否达标
- 安全评测：prompt injection / 越权 / 敏感信息泄露
- 稳定性评测：fallback / retry / provider 切换是否导致结构回归

### E. 成本治理需要到“动作级”而不是只到“项目级”

因为我们会有分析、脚本、镜头、渲染等多个步骤，建议把预算控制粒度下沉到：

- stage budget
- capability budget
- provider budget
- org / workspace budget

### F. 人审插槽要在架构上预留

虽然 MVP 不做完整企业协同，但系统设计上建议先保留：

- human_review_required
- approval_status
- approved_by
- approved_at

这样后面做企业审批流时不用大改 run 对象。

## 4. 对我们项目的总体评估

## 4.1 当前成熟度判断

如果按企业级视角粗分，我会这么判断：

- 产品定义：`B`
- 架构方向：`B`
- 治理意识：`B+`
- 企业安全与治理能力：`D`
- 评测与可观测性：`D`
- 身份与权限：`D`
- 预算与合规：`D`

意思不是我们做得差，而是：

`我们现在更像“架构已定、企业护栏未补”的阶段。`

这很正常。

## 4.2 最应该优先补的 6 项

如果要按投入产出比排序，我建议先补这 6 项：

1. `Auth + Role 模型`
2. `Prompt / Planning 版本治理`
3. `Evals 最小回归集`
4. `Trace / Audit 事件规范`
5. `Budget / Rate limit / Retry 策略`
6. `Data retention / sensitive data policy`

## 4.3 我对 Harness 的重新判断

基于这轮企业级视角搜索，我的判断比之前更清楚了：

- Harness 很适合作为“企业治理参考系”
- 但仍然不适合现在进入我们的产品主路径

原因：

- 它解决的是平台治理、DevOps、policy、audit、secrets、RBAC 这些“组织层能力”
- 而我们现在还处在“先把产品主链路和应用内治理打稳”的阶段

所以：

`Harness 现在适合作为我们企业级治理 checklist 的参考，不适合作为当前应用架构主依赖。`

## 4.4 结合当前仓库结构的真实判断

按现在仓库里已经存在的内容看：

- `apps/web`：前端壳已有雏形
- `services/api`：API 和 provider stub 已有方向
- `services/worker`：异步 worker/provider adapter 已有起点
- `packages/contracts`：跨端 contract 已起步
- `packages/workflow-schema`：工作流 schema 已有位置
- `docs/*`：治理和方案文档已经比较完整

但从“企业级 AI”视角看，当前代码层几乎还没有进入这些关键模块：

- auth / tenant / org scope
- audit event schema
- tracing / telemetry
- prompt registry
- eval dataset + runner
- policy enforcement
- retention enforcement

所以更准确的判断应该是：

`我们现在不是“企业级能力不足”，而是“企业级设计结论已经形成，但工程化实现尚未开始”。`

## 4.5 哪些可以复用，哪些必须自己做

### 必须自己做的

- 项目主链领域模型
- intake -> analysis -> workflow -> run 的状态机
- workflow draft schema
- 供应商能力抽象
- 结果页、历史页、版本回放逻辑
- 与营销视频场景强相关的质量 rubric

这些直接决定产品差异化，不适合外包给通用平台。

### 建议优先复用的

- 身份认证与基础权限：Keycloak 或同类 IAM
- AI 可观测性 / prompt / eval 底座：Langfuse 或同类 LLMOps 平台
- 中央模型网关：LiteLLM 或同类 gateway
- 策略执行：OPA / Rego

原因不是省事，而是这些层本来就属于：

- 通用治理层
- 组织安全层
- 平台工程层

### 现在先不要引入过深的

- 全量企业工作流引擎
- 过重的多租户平台抽象
- 复杂的 policy mesh
- 多云多区域统一调度

因为这些会明显拖慢 MVP 主链。

## 5. 对我们项目的推荐方案

我建议把企业级增强拆成两层。

## 5.1 现在立刻补的企业底座

这一层建议直接纳入当前实现计划：

- auth skeleton
- role model
- provider usage budget fields
- trace ids / audit event schema
- prompt registry metadata
- eval fixtures
- retention policy doc

## 5.2 等主链跑通后再补的企业治理层

这一层建议在主链稳定后做：

- SSO / SCIM
- audit streaming
- policy engine
- external observability integration
- enterprise provider gateway

## 5.3 对我们项目的落地建议

如果按“既不失控，也不把系统做重”的原则来落地，我建议分三段。

### 第一段：现在就纳入实现骨架

- `auth skeleton`
- `org_id / user_id / role` 字段
- `run trace ids`
- `audit_event` 表或事件模型
- `prompt_registry` 元数据模型
- `tests/fixtures/evals` 基础样本集
- `retention_policy` 文档和配置项

### 第二段：主链联通后补 AI 治理闭环

- trace 可视化
- prompt version 对比
- eval runner
- cost dashboard
- retry / fallback / circuit breaker
- 敏感字段脱敏规则

### 第三段：有企业交付信号再补组织治理

- SSO / SCIM
- workspace policy
- 审计外发到 SIEM
- provider gateway 管控台
- approval workflow

## 5.4 推荐的最小企业 AI 组合

如果让我给出“当前最稳妥、最不过度设计”的组合，我会这样配：

- 主产品链路：我们自己做
- 模型主提供方：OpenAI
- 次提供方 / reviewer / fallback：Anthropic
- Tracing / prompt / eval：先自留接口，后接 Langfuse
- Gateway：先保留 provider registry，规模上来后再评估 LiteLLM
- Policy：先把规则写成配置和代码断言，二期再评估 OPA
- Identity：先做最小 auth skeleton，企业交付前再接 Keycloak 或企业 IdP

## 6. 最终结论

如果你让我用一句话来总结这轮评估，我的结论是：

`我们现在的架构方向是对的，但如果目标是企业级交付，接下来最该补的不是更多功能，而是评测、追踪、权限、预算和数据治理这五条护栏。`

进一步压缩成执行结论就是：

- 不要现在引入 Harness 进核心产品路径
- 继续保持 OpenAI-first / Anthropic-compatible
- 但从下一阶段开始，把“企业级 AI 护栏”当正式工程对象来做

## 7. 来源

### 官方与标准

- OpenAI Production best practices
  - https://platform.openai.com/docs/guides/production-best-practices
- OpenAI Evaluation best practices
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
- OpenAI Prompting
  - https://developers.openai.com/api/docs/guides/prompting
- OpenAI Agents SDK Tracing
  - https://openai.github.io/openai-agents-python/tracing/
- OpenAI Agents SDK Guardrails
  - https://openai.github.io/openai-agents-python/guardrails/
- OpenAI Data controls
  - https://developers.openai.com/api/docs/guides/your-data
- Anthropic Claude Code admin setup
  - https://code.claude.com/docs/en/admin-setup
- Anthropic Claude Code settings
  - https://code.claude.com/docs/en/settings
- Anthropic Claude Code analytics / monitoring
  - https://code.claude.com/docs/en/analytics
  - https://code.claude.com/docs/en/monitoring-usage
- Anthropic define success criteria and evaluations
  - https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Anthropic Eval Tool
  - https://platform.claude.com/docs/en/test-and-evaluate/eval-tool
- Anthropic Rate limits
  - https://platform.claude.com/docs/en/api/rate-limits
- Anthropic Claude Code data usage
  - https://code.claude.com/docs/en/data-usage
- Harness Platform
  - https://developer.harness.io/docs/platform/
- Harness Audit Trail / Audit Streaming
  - https://developer.harness.io/docs/platform/governance/audit-trail/
  - https://developer.harness.io/docs/platform/governance/audit-trail/audit-streaming/
- Harness Policy as Code
  - https://developer.harness.io/docs/platform/governance/policy-as-code/harness-governance-overview/
- Harness Secrets management
  - https://developer.harness.io/docs/platform/secrets/secrets-management/harness-secret-manager-overview/
- NIST AI Risk Management Framework
  - https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Core / Govern-Map-Measure-Manage
  - https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- OWASP Top 10 for LLM Applications
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Amazon Bedrock Guardrails
  - https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-how.html

### 开源参考

- Keycloak
  - https://github.com/keycloak/keycloak
- LiteLLM
  - https://github.com/BerriAI/litellm
- Langfuse
  - https://github.com/langfuse/langfuse
