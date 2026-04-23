# 全新项目 企业 AI 编程操作手册

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 企业 AI 编程规则](./enterprise-ai-coding-rules.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 企业级 AI 就绪度评估](./enterprise-ai-readiness-assessment.md)
- [全新项目 实施路线图](./implementation-roadmap.md)

## 1. 这份文档解决什么问题

这份文档回答的不是“AI 能不能写代码”，而是：

`企业在真的用 AI 编程搭复杂项目时，通常会怎么规定角色、权限、边界、审批和证据，才能既提速，又不失控。`

如果把前面的规则文档理解成“红线”，这份文档就是“施工方法”。

## 2. 一句话结论

如果先压成一句话，我的结论是：

`最高权限不等于无限权限。企业级 AI 编程必须把 AI 放进“角色、策略、审批、证据、审计”五层框架里运行。`

换句话说，企业不是把 AI 当成一个“什么都能做的万能开发者”，而是把 AI 放进一套受控工作流里：

- 允许 AI 做大量研究、实现、补测、重构、review 草案
- 但不让 AI 自己决定边界、审批、生产动作和最终放行

## 3. 官方资料里，企业最稳定的做法是什么

## 3.1 OpenAI Codex 给出的信号

从 OpenAI Codex Enterprise 文档里，能提炼出几条非常明确的做法。

### A. 角色和管理权必须分离

Codex Admin Setup 明确建议：

- 用 RBAC 控制 Codex local / cloud 的访问
- 建单独的 `Codex Users` 组
- 建单独的 `Codex Admin` 组
- 通过 SCIM / IdP 让组成员变更可审计

这说明：

`企业不会把“能用 Codex”与“能管 Codex 策略”混成一回事。`

### B. 企业会按组下发不同策略，而不是全员同一档

Codex Admin Setup 和 Managed Configuration 都明确支持：

- baseline policy
- group-specific policy
- fallback policy
- first-match group rule

而且可管的内容很具体：

- `allowed_approval_policies`
- `allowed_sandbox_modes`
- `allowed_web_search_modes`
- `mcp_servers` allowlist
- restrictive command rules

这说明：

`企业级 AI 编程真正落地时，常见形态不是“一个全局开关”，而是一组分层、分组、可审计的策略。`

### C. 云端 Agent 的互联网权限默认应更谨慎

Codex Admin Setup 明确写到：

- cloud agents 默认无互联网访问
- 只有显式允许后，才能配置域名 allowlist、trusted sites 和 HTTP methods

这对我们非常重要，因为它说明：

`即使企业允许 AI 自动执行，也不会默认给它自由联网。`

### D. Managed policy 应该压过本地配置

Codex Managed Configuration 明确给出：

- cloud-managed requirements
- MDM managed preferences
- `requirements.toml`
- `managed_config.toml`

并且要求：

- managed layers 优先级高于本地配置和 CLI 覆盖
- 可限制 approvals、sandbox、web search、MCP、feature flags、command rules

这说明：

`企业规则不能只停留在文档里，最好还要变成工具级约束。`

### E. 企业会同时看分析数据和合规日志

Codex Governance 明确给出三层治理数据：

- Analytics Dashboard
- Analytics API
- Compliance API

用途包括：

- adoption
- governance and cost monitoring
- audit
- investigations
- SIEM / eDiscovery

这说明：

`企业不会只看“代码写得快不快”，还会看可追溯性和可调查性。`

## 3.2 Anthropic Claude Code 给出的信号

Anthropic 在 Claude Code 文档里，给出的企业信号也很清楚。

### A. 中央下发配置是正式能力

Claude Code 的 server-managed settings 文档明确支持：

- centrally configure settings
- settings precedence
- managed-only settings
- fail-closed startup
- audit logging

而且能配置：

- permission deny rules
- disable bypass permissions
- hooks
- environment variables

这说明：

`企业真正需要的不是“每个人自己配置 AI”，而是统一、可控、最好可强制下发的 AI 配置。`

### B. 所有者和管理员范围要收紧

Claude Code 文档明确写到：

- server-managed settings 只能由 `Primary Owner` / `Owner` 管理
- 配置变更会影响整个组织

这说明：

`AI 编程策略本身就是高风险资产，权限必须收窄。`

### C. 监控和追踪要有脱敏策略

Claude Code Monitoring 文档明确说明：

- metrics / events / traces 都可以导出
- prompt 内容默认不记录
- tool 参数默认不记录
- raw API bodies 默认不记录
- 如果开启更详细日志，要自己做 redact / filter

这说明：

`企业不是不能做观测，而是要把“记录什么、不记录什么”也当成治理对象。`

## 3.3 GitHub Copilot Enterprise 给出的信号

GitHub 文档里，企业治理也已经非常产品化。

### A. Enterprise 级 Agent 默认更保守

GitHub 文档明确写到：

- Copilot cloud agent 在 Business / Enterprise 下默认禁用
- 必须由管理员启用
- 仓库可以 opt out

这说明：

`企业默认假设 agentic coding 是高影响能力，不会默认全开。`

### B. Content exclusion 很重要，但不能迷信

GitHub 明确支持 content exclusion，但同时也明确限制：

- 不支持某些 Edit / Agent modes
- 对 remote filesystems 和 symlinks 有限制
- 被 IDE 间接暴露的语义信息仍可能被使用

这说明：

`企业不能只靠“排除目录”一个开关来兜底，还要有仓库级和流程级红线。`

### C. 复杂任务要先切得清楚

GitHub 关于 cloud agent 的最佳实践明确强调：

- clear, well-scoped tasks
- complete acceptance criteria
- directions about which files need to be changed
- custom instructions files

这说明：

`企业级 AI 编程不是“随手一句话让它做”，而是把任务单写成适合 AI 的结构化工作指令。`

## 3.4 OWASP 给出的安全信号

OWASP 在 LLM Top 10 和 Prompt Injection Prevention Cheat Sheet 里的信号，对 AI 编程同样成立：

- prompt injection
- sensitive information disclosure
- supply chain risk
- excessive agency

这意味着：

`企业用 AI 编程时，必须默认外部文本、第三方仓库、插件、MCP、脚本输出都是潜在攻击面。`

## 4. 企业 AI 编程的标准治理栈

如果把前面的官方信号抽象一下，我建议把企业 AI 编程治理拆成 7 层。

## 4.1 业务边界层

先定义：

- 项目主链是什么
- 哪些不做
- 哪些能力需要 ADR 才能进入

没有这一层，AI 只会越来越会“扩 scope”。

## 4.2 身份与角色层

至少区分：

- 使用者
- 管理者
- 审查者
- 安全/平台治理者
- 最终审批者

## 4.3 数据与上下文层

明确：

- 哪些文件/目录/数据不准进模型上下文
- 哪些任务可用云端 agent
- 哪些任务只能本地受控执行

## 4.4 执行与工具层

明确：

- sandbox 模式
- 命令 allow / prompt / deny
- 网络访问白名单
- MCP / plugin / skill allowlist

## 4.5 变更与审批层

明确：

- 哪些任务 AI 可直接做
- 哪些任务必须人工批准
- 哪些任务必须主控亲自整合

## 4.6 证据与审计层

明确：

- 改动说明
- 测试证据
- 关键命令
- model / prompt / policy 版本
- 审核结论

## 4.7 观测与成本层

明确：

- adoption
- throughput
- failure rate
- retry / rollback
- model cost
- high-risk command trigger count

## 5. 复杂企业项目里，AI 应该怎么用

这里是最关键的一层。

企业里真正成熟的用法，不是“把项目直接丢给一个 AI 一次性写完”，而是：

`让 AI 在不同阶段承担不同角色，并把复杂项目拆成受控切片推进。`

## 5.1 推荐角色模型

### 主控 Controller

职责：

- 冻结边界
- 拆分任务
- 决定是否并行
- 整合结果
- 最终审查

### 受限 Implementer

职责：

- 在给定文件范围内实现改动
- 补测试
- 生成局部文档

限制：

- 不拥有最终产品方向
- 不跨边界改共享核心层

### Reviewer

职责：

- 查回归
- 查越界
- 查测试覆盖
- 查状态不一致

限制：

- 不替代最终人工批准

### Security / Compliance Reviewer

职责：

- 看密钥、数据、权限、依赖、策略
- 看是否触碰高风险命令或配置

### Human Approver

职责：

- 对高风险改动做最终放行
- 决定是否进入主线或发布

## 5.2 推荐阶段打法

### Phase A：研究与边界冻结

AI 适合做：

- 竞品研究
- 技术路线扫描
- 一手资料整理
- ADR 初稿
- 边界清单初稿

规则：

- 只读为主
- 不开并行写代码
- 先文档，后实现

### Phase B：核心合同层与架构骨架

AI 适合做：

- contract 草案
- schema 草案
- provider interface 草案
- API / worker stub

规则：

- 单线程
- 由主控亲自收口
- 高风险区强制 review pass

### Phase C：受控并行实现

AI 适合做：

- 页面切片
- 独立 adapter
- 测试补齐
- 文档补齐
- 只改一个 bounded module 的功能

规则：

- 每个任务单独 worktree
- 每个切片明确允许编辑范围
- 不并行修改共享锁定区

### Phase D：集成与回归

AI 适合做：

- 对照 contract 查不一致
- 生成回归清单
- 扫缺测
- 整理风险说明

规则：

- 由主控整合
- 由 reviewer 补查
- 高风险改动增加人工核验

### Phase E：企业护栏补齐

AI 适合做：

- tracing / audit schema 初稿
- prompt registry 结构
- eval fixture 整理
- cost / retry / fallback 策略初稿

规则：

- 必须和主链架构一致
- 不为了“企业化”把 MVP 主链拖死

### Phase F：发布前关口

AI 适合做：

- release checklist 草案
- 变更说明
- 风险回顾
- 运维文档初稿

规则：

- 最终发布仍由人批准
- 生产变更不交给 AI 自主闭环

## 5.3 任务路由矩阵

| 工作类型 | AI 默认参与方式 | 是否允许并行 | 是否必须人工批准 |
| --- | --- | --- | --- |
| 竞品/技术研究 | 研究、摘要、对比 | 是 | 否 |
| ADR / 边界草案 | 起草 | 是 | 是 |
| Contracts / Schema | 主控实现 + AI 辅助 | 否 | 是 |
| Provider interfaces | 主控实现 + reviewer 复查 | 否 | 是 |
| UI 页面切片 | bounded implementer | 是 | 否 |
| Worker 独立步骤 | bounded implementer | 是 | 视风险而定 |
| Auth / Role / Policy | 主控实现 + security review | 否 | 是 |
| Migrations / deletion / queue / retry | 主控实现 + reviewer | 否 | 是 |
| 测试补齐 | bounded implementer | 是 | 否 |
| 文档整理 | AI 主做 | 是 | 否 |
| 发布 / 部署 / 生产操作 | 人主导，AI 仅辅助 | 否 | 是 |

## 5.4 当你给 AI 最高权限时，企业应该怎么理解

你这次已经明确说，会给我最高权限来做这些事。

但从企业治理角度，最稳妥的解释不是“AI 因此可以做任何事”，而是：

`AI 拥有较高的本地执行能力，但仍然必须受项目边界、环境边界、审批边界和数据边界约束。`

所以我建议把“最高权限”在文档里翻译成下面四条：

### A. 高权限只在本地受控开发环境内成立

不外延到：

- 生产数据库
- 生产部署
- 线上账号操作
- 真实客户数据导出

### B. 高权限不覆盖审批规则

即使有高权限，也不能绕过：

- 高风险改动 review pass
- 人工批准
- OSS / license gate
- security gate

### C. 高权限不覆盖数据边界

即使能读到文件，也不代表应该把文件送进外部模型上下文。

### D. 高权限不等于自动并行扩散

即使 AI 可以做很多事，也仍然应该：

- 先主控
- 后切片
- 再并行

## 6. 我们项目现在应采用的企业 AI 编程规则

结合前面的规则文档和我们的项目状态，我建议现在就正式采用下面这组规则。

## 6.1 总原则

`单主控、强边界、可控高权限、受限并行、人工放行、证据先行`

## 6.2 数据规则

### Do-not-feed 清单

默认禁止进入外部模型上下文：

- `.env`
- `*.pem`
- `*.key`
- `id_rsa*`
- `secrets/**`
- 生产数据库导出
- 客户 PII
- 真实商家后台导出
- 未授权第三方代码

## 6.3 命令规则

### `allow`

- 只读命令
- `lint`
- `typecheck`
- `test`
- 本地构建

### `prompt`

- 写文件
- 安装依赖
- 生成 migration
- 非破坏性 git 操作

### `deny`

- `git push`
- `git reset --hard`
- `rm -rf`
- `curl | sh`
- `kubectl apply`
- `terraform apply`
- 生产环境命令
- 直接删除线上数据

## 6.4 Cloud / Local 边界

- 文档、研究、普通开发、stub 实现：可本地 AI
- 含敏感数据、密钥、生产运维上下文：只允许本地受控，不允许云端 agent
- 未审计仓库、未审计 MCP、未审计插件：默认禁用

## 6.5 高风险审批矩阵

以下改动必须：

- 主控收口
- 独立 review pass
- 人工批准

适用范围：

- auth / role / tenant
- migration
- provider interface
- prompt registry
- retention / audit policy
- queue / retry / state machine
- deletion logic
- 任何新外部 provider / MCP / plugin

## 6.6 证据包要求

AI 产出的改动进入主线前，至少附带：

- 改动目的
- 影响范围
- 跑过的测试
- 未覆盖风险
- 关键命令记录

高风险改动再附加：

- model / provider
- prompt / instruction / policy version
- reviewer 结论
- rollback 思路

## 6.7 回滚与事故规则

如果 AI 产出导致问题：

- 先止血
- 再回滚
- 最后复盘

并补记录：

- 哪个 agent
- 哪条任务单
- 哪个 prompt / policy / model
- 哪个测试没拦住
- 后续补什么护栏

## 7. 这套规则怎么落到我们仓库里

## 7.1 已经落下来的文档

- `AGENTS.md`
- `MEMORIES.MD`
- `docs/build-governance-and-agent-operating-model.md`
- `docs/enterprise-ai-coding-rules.md`
- `docs/enterprise-ai-readiness-assessment.md`
- `.codex/managed_config.example.toml`
- `.codex/requirements.example.toml`
- `.codex/managed_config.project.toml`
- `.codex/requirements.project.toml`
- `codex/rules/default.rules`
- `docs/security/ai-coding-policy-matrix.md`
- `docs/security/do-not-feed-and-exclusion-list.md`
- `docs/review/high-risk-change-checklist.md`

## 7.2 这次新增的文档作用

这份文档的作用是把“企业规则”翻译成“企业打法”。

也就是明确：

- 哪些阶段该让 AI 多做
- 哪些阶段必须主控亲自做
- 哪些阶段能并行
- 哪些改动必须人工批准

## 7.3 这次已经落下来的配置件

这次已经把“可执行约束模板”补到了仓库里：

1. `.codex/managed_config.example.toml`
2. `.codex/requirements.example.toml`
3. `codex/rules/default.rules`
4. `docs/security/do-not-feed-and-exclusion-list.md`
5. `docs/review/high-risk-change-checklist.md`

下一步如果继续往下走，最值得补的是：

1. 把 project 模板改成你们真实组织策略
2. 增加仓库级 content exclusion 与 cloud agent policy
3. 增加审计与 evidence 模板
4. 把高风险审批矩阵接入真实研发流程

## 8. 最终结论

如果把这次结论压到最直接的执行层面，就是：

- 企业级 AI 编程不是“给 AI 最高权限就行”，而是“给 AI 受控的高权限”
- 复杂项目不能交给一个 AI 一次性闭环，而应该按角色和阶段拆开
- AI 最适合承担研究、草案、受限实现、补测、review 辅助、文档整理
- 最终边界、合并、发布、生产动作，仍然应由主控和人工批准链路来把关

## 9. 来源

### OpenAI

- OpenAI Codex Admin Setup
  - https://developers.openai.com/codex/enterprise/admin-setup
- OpenAI Codex Governance
  - https://developers.openai.com/codex/enterprise/governance
- OpenAI Codex Managed configuration
  - https://developers.openai.com/codex/enterprise/managed-configuration
- OpenAI Codex use cases
  - https://developers.openai.com/codex/use-cases

### Anthropic

- Anthropic Claude Code Admin Setup
  - https://code.claude.com/docs/en/admin-setup
- Anthropic Claude Code Server-managed settings
  - https://code.claude.com/docs/en/server-managed-settings
- Anthropic Claude Code Monitoring
  - https://code.claude.com/docs/en/monitoring-usage
- Anthropic Claude Code Analytics
  - https://code.claude.com/docs/en/analytics
- Anthropic Claude Code Data Usage
  - https://code.claude.com/docs/en/data-usage

### GitHub

- GitHub Copilot policies
  - https://docs.github.com/en/copilot/concepts/policies
- Managing access to GitHub Copilot cloud agent
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/access-management
- Content exclusion for GitHub Copilot
  - https://docs.github.com/en/copilot/concepts/context/content-exclusion
- Best practices for using GitHub Copilot to work on tasks
  - https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results
- Files excluded from GitHub Copilot code review
  - https://docs.github.com/en/copilot/reference/review-excluded-files

### 安全参考

- OWASP Top 10 for LLM Applications
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Prompt Injection Prevention Cheat Sheet
  - https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
