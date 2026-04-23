# 全新项目 企业 AI 编程规则

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 企业级 AI 就绪度评估](./enterprise-ai-readiness-assessment.md)
- [全新项目 企业 AI 编程操作手册](./enterprise-ai-coding-operating-playbook.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 边界分层、复用策略与模型接口预留](./boundary-reuse-and-provider-strategy.md)

## 1. 这份文档解决什么问题

这份文档只回答一个问题：

`企业如果正式把 AI 编程纳入项目交付，会明确哪些规则？我们这个项目还需要补强哪些？`

这里讨论的不是“AI 好不好用”，而是：

- 哪些代码和数据可以喂给 AI
- AI 可以做什么，不可以做什么
- AI 生成的代码怎么验、谁来批
- 审计、追责、回滚怎么留痕

## 2. 官方资料里，企业最常明确的规则类型

从 OpenAI Codex、Anthropic Claude Code、GitHub Copilot Enterprise 这几类官方资料里，可以提炼出一套比较稳定的企业规则框架。

## 2.1 身份与角色分离

企业通常不会把“能用 AI 编程”和“能配置 AI 编程策略”混在一起。

常见规则是：

- 普通开发者只能使用
- 单独的 admin / security / analytics owner 负责策略和审计
- RBAC、SSO、SCIM、MFA 要跟企业身份系统对齐

这背后的逻辑是：

`AI 工具本身也是受治理的软件，不是每个开发者都能改它的边界。`

## 2.2 托管策略优先于个人配置

Anthropic 和 OpenAI 都明确支持组织级策略高于本地设置。

企业会明确：

- 哪些策略由组织统一下发
- 本地配置能覆盖哪些项
- 哪些项必须 fail-closed

最典型的受控项包括：

- sandbox mode
- approval policy
- internet access
- allowed commands
- MCP / plugin marketplace
- allowed models

这说明：

`企业不是只写一份规范文档，而是尽量把规范变成系统级约束。`

## 2.3 数据边界与内容排除

GitHub Copilot Enterprise 明确提供了 content exclusion。

企业在 AI 编程里，通常会明确两类规则：

- 哪些内容禁止进入 AI 上下文
- 哪些仓库 / 文件 / 目录只能在本地受控环境使用

常见的禁入对象包括：

- secrets
- 私钥
- 生产配置
- 客户数据导出
- 法务/合同文档
- 安全策略文件
- 受限许可证代码

需要注意的是：

`某些平台的 exclusion 在 cloud agent / CLI / agent mode 上并不完全等价，所以企业不能只依赖厂商开关，还要有仓库级红线。`

例如 GitHub 官方文档就明确提到：

- content exclusion 当前不支持某些 Edit / Agent modes
- 对 remote filesystems 和 symlinks 也有限制

## 2.4 工具、命令、网络、插件和 MCP 边界

企业级 AI coding 往往会明确：

- 哪些命令可直接运行
- 哪些命令必须人工确认
- 哪些命令一律禁止
- 哪些网络域名允许访问
- 哪些 MCP server / plugin marketplace 可以接

这一类规则本质上是：

`限制 AI 的行动面，而不只是限制它的文本输出。`

## 2.5 审计、分析与留痕

OpenAI 和 Anthropic 都把治理数据、分析和审计当正式能力提供。

企业通常会要求：

- 谁发起了任务
- 调用了哪个模型
- 执行了哪些命令
- 访问了哪些仓库
- 产生了哪些 diff
- 跑了哪些测试
- 是否经过人工审批

也就是说：

`AI 编程不是“生成完就算”，而是要可回放、可调查、可问责。`

## 2.6 人工审查与合并审批

厂商官方资料都反复强调：

- AI 输出需要人工审查
- 高风险改动不能让代理自己闭环

企业里常见的明确规则是：

- AI 可以起草和实现
- AI 可以辅助 review
- AI 不能替代最终审批人
- AI 不能直接绕过 branch protection

## 2.7 公共代码、许可证与依赖治理

GitHub 官方明确提供：

- public code match reference
- feature policy
- content exclusion

企业在 AI 编程里通常会明确：

- 生成代码如果与公开代码高度相似，要能回看引用
- 不允许把不清楚许可证来源的大段代码直接合入
- 新增依赖要经过许可证和安全扫描

这类规则解决的是：

- 版权风险
- 供应链风险
- “AI 帮你拷了一段，但没人知道从哪来的”这种风险

## 2.8 负责使用与安全基线

OWASP 对 LLM / agentic application 的共识里，最值得纳入 AI 编程规则的是：

- prompt injection
- sensitive information disclosure
- supply chain risk
- excessive agency

所以企业通常还会加一层：

- 外部文本默认不可信
- AI 不能基于不可信内容自行提升权限
- 工具调用和高风险输出要再校验

## 3. 对我们当前项目的判断

## 3.1 目前已经有的规则

我们已经具备一些很好的基础：

- 主链固定
- 冻结边界
- 主控统筹模型
- 子 Agent 有限委派
- 高风险改动额外 review pass
- worktree 分离和共享锁定区

这意味着我们已经有了“项目治理”的骨架。

## 3.2 还需要补强的点

如果按企业 AI 编程的视角看，我们还缺 8 条比较关键的规则。

### 1. 数据喂给规则

当前缺口：

- 还没有 `do-not-feed` 清单
- 还没有敏感文件/目录排除清单

### 2. 执行权限矩阵

当前缺口：

- 还没有把命令分成 allow / prompt / deny
- 还没有网络访问白名单

### 3. Cloud 与 Local 的边界

当前缺口：

- 还没有明确哪些任务允许云端 agent
- 还没有明确哪些代码只能本地受控执行

### 4. 审批矩阵

当前缺口：

- 还没有定义 AI review 和 human approval 的分界
- 还没有“哪些改动必须代码 owner / 安全 owner 批准”

### 5. 开源与许可证规则

当前缺口：

- 还没有明说 public-code 相似引用怎么处理
- 还没有依赖引入的 license/security gate

### 6. 证据留存规则

当前缺口：

- 还没有明确哪些任务必须附带命令日志、测试证据、模型/Prompt 版本

### 7. Prompt / Skill / Plugin 治理

当前缺口：

- 还没有针对 skills、plugins、MCP servers 的允许范围
- 还没有组织级 Prompt 资产变更规则

### 8. 失败与回滚规则

当前缺口：

- 还没有把“AI 产生错误改动后如何止损”写成硬规则

## 4. 对我们项目的补强建议

我建议把企业 AI 编程规则直接定成 10 条。

## 4.1 规则一：角色分离

- `main controller` 负责架构、任务拆分、集成、最终审查
- `implementer agent` 只在授权范围内改代码
- `reviewer agent` 只做问题发现，不做最终批准
- `security / platform owner` 负责后续策略、审计和密钥治理

补充原则：

`AI 可以参与实现与审查，但不能同时充当最终审批人。`

## 4.2 规则二：禁止喂给 AI 的内容必须写死

默认禁止进入 AI 上下文的内容：

- `.env`
- `*.pem`
- `*.key`
- `id_rsa*`
- `secrets.*`
- 生产数据库导出
- 客户 PII / 订单原文 / 商家后台导出
- 安全应急手册
- 未授权第三方代码

对于我们项目，再额外加一条：

- 任何真实商家敏感经营数据，不允许直接进入外部模型

## 4.3 规则三：命令与执行权限必须分层

建议至少分成三层：

- `allow`
  - 只读命令
  - lint
  - typecheck
  - test
  - 本地构建
- `prompt`
  - 写文件
  - 安装依赖
  - 数据迁移生成
  - 非破坏性 git 操作
- `deny`
  - `git push`
  - `git reset --hard`
  - `rm -rf`
  - `curl | sh`
  - `kubectl apply`
  - `terraform apply`
  - 直接访问生产环境
  - 直接删除线上数据

对我们这条线，我建议默认：

- 网络访问关闭或强白名单
- 生产环境命令一律 deny

## 4.4 规则四：Cloud / Local 使用边界要明确

建议：

- 本地 agent 可用于普通开发、测试、文档、非生产数据场景
- 云端 agent 只允许接入经过批准的仓库和受控连接
- 含敏感数据、密钥、生产运维上下文的任务，不交给云端 agent

这条规则很重要，因为：

`同样是 AI 编程，本地代理和云端代理的数据暴露面并不一样。`

## 4.5 规则五：高风险改动必须人工批准

以下改动必须人工 review + main controller 收口：

- auth / role / tenant
- billing
- provider interface
- prompt registry
- plugin / MCP / external tool policy
- 数据库 schema / migration
- 删除逻辑
- queue / retry / state machine
- retention / audit / security policy

补充原则：

- AI review 不是 merge approval
- 高风险改动不能由生成者自己放行

## 4.6 规则六：AI 生成代码必须附带验证证据

进入主线前，至少要有：

- 改动说明
- 影响范围
- 测试结果
- 未覆盖风险
- 关键命令记录

高风险改动再增加：

- model / provider
- prompt / instruction version
- reviewer 结论

## 4.7 规则七：开源引用和依赖引入要受控

建议明确：

- 大段来源不明代码不得直接合入
- 遇到 public-code match，要记录来源并人工判断许可证风险
- 新增依赖必须经过 license + security 扫描
- GPL / AGPL 项目只作结构参考或 sidecar 候选，不默认混入核心链路

## 4.8 规则八：Prompt、Skill、Plugin、MCP 要纳入治理

建议：

- 默认禁用未审计 plugin marketplace
- 默认禁用未登记 MCP server
- 共享 Prompt / Skill 走版本化管理
- 高风险 skill 不能内联执行任意 shell

这条对我们尤其重要，因为后面如果要让 AI 更强，很容易自然长出：

- 自定义 skill
- MCP server
- 外部工具链

如果没有准入规则，边界会很快失控。

## 4.9 规则九：AI coding 的安全基线要单独写

建议把下面这些写成硬规则：

- 外部抓取文本视为不可信输入
- 不可信输入不得直接进入 system / policy 层
- 工具参数要由代码层校验，不由模型自由拼接
- 对外部输出做敏感内容和异常动作检查

## 4.10 规则十：使用效果、成本和异常要能监控

企业里不会只看“有没有生成代码”，而会看：

- adoption
- PR / task throughput
- 成本
- 回退率
- 问题率
- 高风险命令触发次数

对我们当前阶段，最小可做的是：

- 记录高风险任务数
- 记录 provider / model 使用量
- 记录失败重试和人工接管次数

## 5. 我对这次问题的结论

结论很直接：

`要补强，而且应该补强。`

我们现在的项目治理文档已经能保证“沿着一条主线走”，但还不够覆盖企业 AI 编程真正关心的：

- 数据喂给边界
- 执行权限边界
- 人工审批边界
- 许可证与供应链边界
- AI 产出证据边界

## 5.1 还需要一份“怎么用”的操作文档

这份文档主要回答的是：

- 规则是什么
- 边界是什么
- 哪些点要补强

但如果项目要真的按企业方式推进，还需要再多一层：

- 复杂项目里 AI 该怎么分角色
- 哪些阶段该单线程
- 哪些阶段可以受控并行
- 给了 AI 高权限之后，如何仍然保持受控

这部分已经单独整理在：

- [全新项目 企业 AI 编程操作手册](./enterprise-ai-coding-operating-playbook.md)

## 6. 推荐马上补上的落地件

我建议把这件事拆成三层。

### 第一层：现在就写进仓库规则

- `AGENTS.md`
- 这份 `enterprise-ai-coding-rules.md`
- `enterprise-ai-coding-operating-playbook.md`

### 第二层：已经落成模板的可执行配置

- `.codex/managed_config.example.toml`
- `.codex/requirements.example.toml`
- `.codex/managed_config.project.toml`
- `.codex/requirements.project.toml`
- `codex/rules/default.rules`
- `docs/security/ai-coding-policy-matrix.md`
- 敏感目录 exclusion 清单
- 高风险命令规则

### 第三层：进入企业交付时再平台化

- SSO / SCIM
- 审计外发
- 统一 gateway
- policy as code

## 7. 来源

### 官方资料

- OpenAI Codex Admin Setup
  - https://developers.openai.com/codex/enterprise/admin-setup
- Anthropic Claude Code Admin Setup
  - https://code.claude.com/docs/en/admin-setup
- Anthropic Claude Code Settings
  - https://code.claude.com/docs/en/settings
- Anthropic Claude Code Data Usage
  - https://code.claude.com/docs/en/data-usage
- Anthropic Claude Code Analytics
  - https://code.claude.com/docs/en/analytics
- GitHub Copilot policies
  - https://docs.github.com/en/copilot/concepts/policies
- GitHub Copilot content exclusion
  - https://docs.github.com/en/copilot/concepts/context/content-exclusion
- GitHub Copilot exclude content
  - https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot
- GitHub Copilot public code matching
  - https://docs.github.com/en/copilot/how-tos/get-code-suggestions/find-matching-code
- GitHub Copilot code review administration
  - https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/manage-copilot-code-review

### 安全参考

- OWASP Top 10 for LLM Applications
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Prompt Injection Prevention Cheat Sheet
  - https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
