# 全新项目 企业级开工前对齐与缺口分析

更新日期：2026-04-24
状态：Draft v0.1

关联文档：

- [全新项目 文档索引](./index.md)
- [全新项目 项目搭建就绪度评估](./project-build-readiness-assessment.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 企业级 AI 就绪度评估](./enterprise-ai-readiness-assessment.md)
- [全新项目 企业 AI 编程规则](./enterprise-ai-coding-rules.md)
- [全新项目 大并行与上线门槛](./parallel-and-launch-gates.md)

## 1. 这份文档解决什么问题

这份文档回答的是：

`拿我们现在这套项目架构、规则、边界，去和大厂做企业级项目开工前通常会定死的东西做一次对齐，看还缺什么。`

这里的“开工前通常会定死”，不是指把所有实现都写完，而是指至少把下面三类东西说清楚：

- 方向不能乱
- 责任不能乱
- 出问题时不能没人接

小白版解释：

- 不是先把楼全盖完
- 而是先确认蓝图、施工规范、责任人、质检方式、出事怎么处理

## 2. 先给结论

结论分三句：

1. `我们已经不是“没地基”的状态。`
2. `我们已经有了比较强的主线治理、边界治理和 AI 编程治理。`
3. `我们还没有达到“大厂企业级项目开工前常见的完整交付治理包”。`

更直白一点：

- 现在已经可以继续沿主链开发
- 但还不适合把当前状态误判成“企业级前置条件已经全部齐全”
- 最大缺口不在“产品方向”，而在“所有权、非功能基线、运维治理、安全设计、环境晋级”这些传统企业工程项

### 2.1 2026-04-24 补件进度更新

第一批企业级地基文档已经开始补齐，当前已新增：

- [enterprise-architecture-spec.md](./enterprise-architecture-spec.md)
- [ownership-and-approval-matrix.md](./ownership-and-approval-matrix.md)
- [nfr-and-slo-baseline.md](./nfr-and-slo-baseline.md)
- [observability-and-alerting-baseline.md](./observability-and-alerting-baseline.md)
- [`.github/CODEOWNERS`](../.github/CODEOWNERS)

第二批治理文档也已补上，当前新增：

- [security/threat-model-and-trust-boundaries.md](./security/threat-model-and-trust-boundaries.md)
- [security/dependency-and-license-gates.md](./security/dependency-and-license-gates.md)
- [data-lifecycle-and-recovery-baseline.md](./data-lifecycle-and-recovery-baseline.md)
- [environment-promotion-model.md](./environment-promotion-model.md)
- [test-strategy-and-acceptance-matrix.md](./test-strategy-and-acceptance-matrix.md)
- [incident-response-and-escalation-matrix.md](./incident-response-and-escalation-matrix.md)

平台门禁也补了第一条自动化执行：

- [repo-ruleset-and-branch-protection-baseline.md](./repo-ruleset-and-branch-protection-baseline.md)
- [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml)
- [`.github/dependency-review-config.yml`](../.github/dependency-review-config.yml)

这意味着：

- 架构定版、所有权、NFR、可观测性、安全设计、数据治理、环境治理、测试策略、事故响应都已经从“缺失”进入“已补第一版”
- 但 GitHub 平台侧强制 ruleset、更多自动化门禁、恢复演练和真正工程化接入仍然没有补完

代码侧第一批“不是只写文档，而是真的开始接线”的补件也已经落下：

- API 已接入 `request_id` / `trace_id` 中间件
- API 错误返回已统一为结构化字段：`message` / `errorCode` / `requestId` / `traceId`
- render run 创建、完成、失败与 step 快照已有结构化日志
- 第一条真实浏览器主链 E2E 已用 Playwright 跑通

这意味着：

- 我们现在已经不是“只有规则，没有执行”的状态
- 但还没有到“平台门禁、告警平台、恢复演练都齐全”的状态

## 3. 大厂开工前通常会先定哪些东西

不同公司写法不一样，但官方框架和工程平台里反复出现的内容，基本都绕不开下面这些：

1. `范围和主链`
   也就是先定这次到底做什么，不做什么。
2. `正式架构设计`
   也就是系统怎么拆、为什么这么拆、代价是什么。
3. `边界和合同`
   也就是哪些结构不能乱改，哪些接口是大家共同依赖的。
4. `所有权和审批链`
   也就是谁负责哪一块，谁有批准权。
5. `分支保护和合并门禁`
   也就是代码不是谁想合就合。
6. `非功能基线`
   也就是性能、稳定性、容量、成本这些底线。
7. `可观测性和告警`
   也就是出问题时要能看见，不是靠猜。
8. `安全设计包`
   也就是威胁建模、密钥管理、依赖和供应链治理。
9. `数据治理`
   也就是哪些数据能存、存多久、怎么删、怎么恢复。
10. `环境和发布晋级路径`
    也就是本地、测试、预发、生产怎么走。
11. `测试和验收策略`
    也就是什么算通过，什么不能发。
12. `事故响应和回滚机制`
    也就是线上出事后谁来处理、按什么流程处理。

## 4. 我们和企业级开工基线的对齐结果

下面这张表里：

- `已明确`：基本已经有可用文档和执行规则
- `部分明确`：有方向，但还没到正式、可执行、可审计的程度
- `未补足`：目前缺口比较明显

| 维度 | 大厂开工前通常会定什么 | 我们现在的情况 | 判断 | 最小补强动作 |
| --- | --- | --- | --- | --- |
| 范围与主链 | 明确这次做什么、不做什么，避免边做边扩 | 主链、冻结边界、MVP 不做项都已明确，且多份文档互相强化 | 已明确 | 继续用 ADR 管范围变更 |
| 领域边界与合同冻结 | 明确核心对象、共享接口、谁都不能随手改的结构 | `schema-and-contract-freeze.md`、`AGENTS.md`、共享锁定区都已存在 | 已明确 | 继续保持主控串行整合 |
| 主控与 AI 协作治理 | 明确 AI 怎么参与、什么时候能并行、谁终审 | 主控模型、review pass、worktree 治理、并行门槛都已成型 | 已明确 | 后续按既定模式执行即可 |
| 正式架构定版 | 不只是“架构草稿”，而是有一份被认定为当前版本的系统设计说明，含取舍和质量属性 | 已新增 `enterprise-architecture-spec.md` 作为当前施工蓝图，后续仍需随着系统演进补 ADR | 部分明确 | 持续把重大变化沉淀为 ADR，不让正式蓝图再次漂回草稿 |
| 所有权与审批矩阵 | 明确 code owner、审批人、谁对安全/数据/平台负责 | 已新增 `.github/CODEOWNERS` 与 `ownership-and-approval-matrix.md`，但仍是单 owner 版，平台规则未强制 | 部分明确 | 补平台 ruleset / branch protection，并在多人协作前升级为团队 owner |
| 分支保护与合并门禁 | 需要 review、状态检查、保护规则、禁止绕过主线 | 已新增 ruleset baseline 文档和第一条 dependency review 自动门禁，但 GitHub 平台侧 ruleset / branch protection 仍需手动配置 | 部分明确 | 把 required checks、required reviews、code owner review 真正绑定到平台规则上 |
| 非功能基线 | 先定性能、稳定性、容量、成本、可恢复目标 | 已新增 `nfr-and-slo-baseline.md`，但仍属于第一版工程底线，还不是正式对外 SLA 包 | 部分明确 | 随着主链稳定，把当前基线升级成可测量、可追踪、可验收的门槛 |
| 可观测性与告警 | 明确日志、指标、trace、告警阈值、dashboard 归属 | 已新增 `observability-and-alerting-baseline.md`，且 API 已接入 `request_id` / `trace_id`、结构化错误和关键 run 日志，但 dashboard / alerting 平台仍未接上 | 部分明确 | 继续把指标、trace、告警真正接进平台，并扩到 worker / provider |
| 安全设计包 | 威胁建模、信任边界、密钥治理、依赖和供应链治理 | 已新增 threat model 与 dependency/license gate 文档，但还没有全部做成自动门禁 | 部分明确 | 把依赖、权限、敏感数据边界继续做成平台化和流水线门禁 |
| 数据治理与恢复 | 定义数据分类、保留、删除、备份、恢复、RTO/RPO | 已新增数据生命周期与恢复基线，但 backup/restore 还没真正演练 | 部分明确 | 把 retention、delete、backup、restore 继续工程化并做演练 |
| 环境拓扑与晋级路径 | 定义 local/staging/prod，版本怎么逐级晋升 | 已新增环境晋级模型，但 staging / production 的真实执行与审批还没跑起来 | 部分明确 | 把环境分层从文档推进到真实配置和发布流程 |
| 测试与质量门槛 | 定义 unit/integration/e2e/perf/security/contract 各自要求 | 已新增测试策略矩阵，主链 integration 与第一条 Playwright E2E 已落地，但 AI eval、性能、安全和更深回归还没完全落地 | 部分明确 | 按矩阵继续扩自动化测试和人工验收插槽 |
| 事故响应与值守 | 出问题谁接、怎么升级、怎么复盘 | 已新增 incident response 矩阵，但还没进入真实 incident drill 或 on-call 机制 | 部分明确 | 后续做真实演练并补更正式的值守和升级链 |
| 变更治理与 ADR | 重大变更要有记录，不允许口头漂移 | 已有 `docs/adr/` 模板和“边界变更走 ADR”原则，但真实 ADR 记录还少 | 部分明确 | 从下一次重要架构决策开始真写 ADR |

## 5. 哪些是我们已经做得比较好的

这部分要单独说清楚，不然容易误判成“什么都没做”。

我们现在已经做得比较扎实的，是下面 4 类：

### 5.1 主线很清楚

当前主链：

`intake -> analysis -> prefilled workflow -> run -> result -> history`

这件事很重要，因为企业项目最怕的不是慢，而是方向漂。

### 5.2 边界很清楚

我们已经把很多容易失控的地方提前冻住了，比如：

- 不做的大项
- 共享锁定区
- contract-first
- provider interface
- workflow schema

这会直接减少后面返工。

### 5.3 AI 协作规则比很多普通项目更清楚

我们不是在“随便让 AI 写”，而是已经有：

- 主控统筹
- 有限委派
- reviewer pass
- 高风险改动额外审查
- worktree 治理

这其实已经比很多团队强。

### 5.4 发布和回滚意识已经有了

虽然还不完整，但至少下面两件事已经开始落地：

- 发版前要检查
- 出问题后先止血再回滚

这说明项目不是“只顾往前写代码”。

## 6. 当前最需要持续补强的 6 个企业级前置件

如果只抓最关键的，不铺太大，我认为最缺的是这 6 个。

### 6.1 正式架构定版文档

专业说法：

- `Architecture Design Specification`

小白版解释：

- 现在我们有“架构草稿”
- 但还缺一份“这版系统就按这个施工”的正式蓝图

当前状态：

- 已新增 [enterprise-architecture-spec.md](./enterprise-architecture-spec.md)

剩余工作：

- 把后续重大变化继续收进 ADR

### 6.2 所有权和审批矩阵

专业说法：

- `Ownership / CODEOWNERS / Approval Matrix / RACI`

小白版解释：

- 还缺“哪块代码归谁拍板、谁来批、谁来兜底”的清单

当前状态：

- 已新增 [ownership-and-approval-matrix.md](./ownership-and-approval-matrix.md)
- 已新增 [`.github/CODEOWNERS`](../.github/CODEOWNERS)

剩余工作：

- 把单 owner 版升级成平台强制门禁和团队 owner 版

### 6.3 非功能基线

专业说法：

- `NFR / SLO / Error Budget / Capacity Budget`

小白版解释：

- 还缺“系统至少要多稳、多快、能扛多少量、能花多少钱”的底线

当前状态：

- 已新增 [nfr-and-slo-baseline.md](./nfr-and-slo-baseline.md)

剩余工作：

- 把基线从“第一版工程底线”升级成“真实测量和验收门槛”

### 6.4 可观测性和告警基线

专业说法：

- `Observability Contract`

小白版解释：

- 还缺“系统出问题时，应该看哪里、谁会收到告警、看到什么字段”的规定

当前状态：

- 已新增 [observability-and-alerting-baseline.md](./observability-and-alerting-baseline.md)

剩余工作：

- 把字段、日志、trace、告警真正接到代码和平台里

### 6.5 安全设计包

专业说法：

- `Threat Model / Trust Boundaries / Secret Management / Supply Chain Gate`

小白版解释：

- 还缺“别人怎么攻击我们、哪些边界最危险、密钥怎么管、新依赖怎么卡”的正式说明

当前状态：

- 已新增 [security/threat-model-and-trust-boundaries.md](./security/threat-model-and-trust-boundaries.md)
- 已新增 [security/dependency-and-license-gates.md](./security/dependency-and-license-gates.md)

剩余工作：

- 把安全规则继续变成自动门禁和真实执行流程

### 6.6 数据和环境治理包

专业说法：

- `Data Lifecycle + Environment Promotion + Backup/Restore`

小白版解释：

- 还缺“数据存多久、怎么删、怎么恢复、本地怎么升到测试再升到生产”的整套规则

当前状态：

- 已新增 [data-lifecycle-and-recovery-baseline.md](./data-lifecycle-and-recovery-baseline.md)
- 已新增 [environment-promotion-model.md](./environment-promotion-model.md)
- 已新增 [test-strategy-and-acceptance-matrix.md](./test-strategy-and-acceptance-matrix.md)
- 已新增 [incident-response-and-escalation-matrix.md](./incident-response-and-escalation-matrix.md)

剩余工作：

- 把这些规则进一步接进真实环境、真实演练和自动化门禁

## 7. 哪些缺口会真正阻碍下一阶段

不是每个缺口都同样紧急。

我把它分成两类。

### 7.1 不会阻止我们继续开发，但会阻止我们“企业级放大”

包括：

- 正式架构定版
- CODEOWNERS / ownership matrix
- NFR / observability baseline
- 安全 threat model

意思是：

- 现在还能继续搭
- 但如果马上进入大并行、多人协作、强上线节奏，就会开始出治理问题

### 7.2 不补的话，后面上线和长期维护会越来越危险

包括：

- 数据生命周期和恢复目标
- 环境晋级模型
- incident response
- 完整测试策略

意思是：

- 前面还能靠小心推进
- 但越往后越不能继续靠“人脑记住”

## 8. 主控判断：我们现在处在哪个阶段

我的主控判断是：

`我们现在处在“可持续开发，未完成企业级开工补件”的阶段。`

换成更直白的话：

- 地基已经不是空的
- 主梁已经立起来了
- 施工规范也有一部分了
- 但还缺几份正式验收标准、责任表和安全手册

所以现在最稳妥的判断不是：

- “什么都别做，先停工”

也不是：

- “已经完全可以按企业级规模全面铺开”

而是：

`继续沿主链开发，同时补齐最关键的企业级前置件。`

## 9. 我建议的补强顺序

建议按下面顺序补，不要乱序铺太大。

### 第一批：先补会影响主控收口和大并行的

1. 正式架构定版文档
2. `CODEOWNERS` 和 ownership matrix
3. NFR / SLO baseline
4. observability / alert baseline

### 第二批：再补会影响上线和企业交付的

5. threat model / trust boundaries
6. dependency / license gates
7. data lifecycle / backup / restore / RTO / RPO
8. environment promotion model

### 第三批：最后补运营治理闭环

9. test strategy matrix
10. incident response / escalation matrix
11. 真实 ADR 沉淀机制

## 10. 对“现在能不能继续做”的结论

可以继续做。

但要把这句话说完整：

- `可以继续开发主链`
- `可以继续做当前受控阶段的实现`
- `还不适合宣布“企业级前置条件已完全补齐”`

如果要进入：

- 大并行
- 多人协作
- staging 收口
- 更正式的上线准备

那我建议先把第 1 批补件做掉。

## 11. 参考基线

下面这些官方资料，不是要我们照抄，而是用来对齐“大厂通常会先定哪些东西”。

### 官方工程与治理基线

- GitHub CODEOWNERS
  - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub Rulesets
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- GitHub Protected branches
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub Dependency review
  - https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review
- AWS Well-Architected Framework
  - https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Microsoft Azure Well-Architected
  - https://learn.microsoft.com/en-us/azure/well-architected/
- NIST AI Risk Management Framework
  - https://www.nist.gov/itl/ai-risk-management-framework
- OWASP Top 10 for LLM Applications
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/

### AI 与企业治理基线

- OpenAI Production best practices
  - https://platform.openai.com/docs/guides/production-best-practices
- OpenAI Evaluation best practices
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
- OpenAI Agents SDK Tracing
  - https://openai.github.io/openai-agents-python/tracing/
- Anthropic Claude Code admin setup
  - https://code.claude.com/docs/en/admin-setup
- Anthropic Claude Code settings
  - https://code.claude.com/docs/en/settings
- Anthropic Claude Code analytics / monitoring
  - https://code.claude.com/docs/en/analytics
- Anthropic Claude Code data usage
  - https://code.claude.com/docs/en/data-usage
- Harness Platform
  - https://developer.harness.io/docs/platform/
- Harness Audit Trail / Audit Streaming
  - https://developer.harness.io/docs/platform/governance/audit-trail/
  - https://developer.harness.io/docs/platform/governance/audit-trail/audit-streaming/
- Harness Policy as Code
  - https://developer.harness.io/docs/platform/governance/policy-as-code/harness-governance-overview/
