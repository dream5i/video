# 全新项目 大并行与上线门槛

更新日期：2026-04-25
状态：Draft v0.1

关联文档：

- [全新项目 实施路线图](./implementation-roadmap.md)
- [全新项目 项目搭建就绪度评估](./project-build-readiness-assessment.md)
- [全新项目 版本门槛证据总表](./version-gate-evidence-ledger.md)
- [全新项目 Worktree 与分支治理手册](./worktree-and-branching-runbook.md)
- [全新项目 发布前检查清单](./release-checklist.md)
- [全新项目 回滚 Runbook](./rollback-runbook.md)

## 1. 这份文档解决什么问题

这份文档只回答 3 个问题：

1. 现在能不能继续开发
2. 什么时候可以全面铺开到大并行
3. 什么时候可以进入上线准备或正式上线

核心原则是：

`开发、并行、上线，不是同一个门槛。`

## 2. 先给结论

当前判断：

- 主链继续开发：`可以，现在就可以`
- 可控并行开发：`可以逐步开始，但不能一下子放大`
- 全面大并行：`现在还没到`
- 外部上线准备：`现在还没到`
- 正式上线：`现在不能`

换句话说：

- 现在不应该停下来等“所有东西全补完”再开发
- 但也不应该把当前状态误判成“已经适合多人/多 Agent 全面铺开，更适合直接上线”

## 3. 三层门槛模型

我建议后面统一用这 3 层判断。

### Gate A：可持续开发

达到这层，说明项目可以沿主链持续往前搭。

### Gate B：可控大并行

达到这层，说明可以把更多页面、adapter、测试、文档、局部模块同时展开，而不会把主线打散。

### Gate C：可上线

达到这层，说明不只是“能演示”，而是具备最小外部交付与回滚能力。

## 4. Gate A：可持续开发

当前状态：

`已达到。`

当前已满足：

- 主链冻结
- Frozen boundaries 已写清
- 合同层和 workflow schema 已有基线
- Web / API / Worker 骨架已联通
- `pnpm verify` 已固定
- CI 基线已补
- 基线提交已存在
- persistence skeleton 已进入代码层
- 数据库主链集成测试已补第一条
- HTTP API 主链集成测试已补第一条
- 主链测试已接入 `pnpm verify` 与 CI
- database backend 已成为默认开发路径
- migration smoke 已接入主链测试

所以：

- 可以继续开发
- 可以继续补 persistence、测试、运行链路
- 不需要停下来等所有后期文档 100% 完备

## 5. Gate B：什么时候可以全面铺开到大并行

这里的“大并行”不是指“随便开几个 Agent”，而是指：

- 多个功能分支并行推进
- 多个 worktree 同时写代码
- 页面、API、Worker、测试能分块并行
- 主控不需要每一步都亲自串行改所有核心文件

### 5.1 进入 Gate B 前必须满足的条件

我建议至少同时满足下面 8 条。

#### 1. 共享核心层在一个短周期内基本稳定

至少下面这些区域不再高频改名或重构：

- `packages/contracts/**`
- `packages/workflow-schema/**`
- `services/api/app/providers/interfaces/**`

#### 2. persistence foundation 已落地第一版

至少要有：

- 首版 SQLAlchemy model
- 首版真实 migration
- repository 从 in-memory 开始向 persistence adapter 切换

原因：

- 如果数据层还在剧烈变化，大并行会频繁冲撞共享锁定区

#### 3. 至少有一条真实集成测试主链

最低要求建议是：

- `创建项目 -> 分析 -> workflow -> render run` 这条链至少有 1 条 integration test

#### 4. worktree 治理从“文档”进入“实际执行”

至少要已经开始：

- 一个任务一分支
- 一个并行写任务一个 worktree
- review pass 单独开树或单独分支

#### 5. PR / review 入口真正被执行

不是只有模板，而是团队或主控已经按模板实际使用：

- scope check
- evidence
- risk review
- rollback

#### 6. CI 不只跑基础校验

除了 `typecheck/build/compileall`，至少再有一层：

- integration test
或
- 最小 contract regression check

#### 7. 高风险区有明确“暂停并行”规则

下面这些区域被触发时，应自动降回串行：

- migration
- provider interface
- state machine
- root config

#### 8. 主控收口节奏可承受

如果主控已经明显跟不上：

- diff 审不过来
- merge 冲突密集
- review pass 形同虚设

那就说明还不该进入全面大并行。

### 5.2 我建议的判断

当前状态是：

`已经可以进入小范围可控并行，但还没到全面大并行。`

原因主要有 3 个：

- persistence 已有第一版，默认也已切到 database，但还没有经过真实并行开发轮次验证
- 集成测试已经并入统一 CI / verify，也已覆盖 migration smoke 和少量关键异常返回，但仍不够完整
- worktree 规则虽然定了，但还没经过实际并行轮次验证

### 5.3 什么时点可以宣布进入 Gate B

我建议用下面这句作为内部判断标准：

`当集成测试覆盖更多关键异常场景、第一次真实 worktree 并行协作跑通、以及一次主控 review 收口顺利完成后，才进入全面大并行。`

## 6. Gate C：什么时候可以进入上线准备

这里说的“上线准备”，至少应是：

- 开始准备 staging
- 开始对外可用版本收口
- 开始做发布候选版本

### 6.1 进入上线准备前必须满足的条件

我建议至少满足下面 10 条。

#### 1. 主链不再依赖 stub 才能演示

至少用户主感知路径要成立：

- 创建项目
- 得到分析结果
- 生成 workflow
- 发起 render run
- 看到结果或稳定的结果占位

#### 2. 数据层已稳定

至少应具备：

- 真数据库
- migration 可执行
- rollback 方案明确

#### 3. 环境分层明确

至少要有：

- local
- staging
- production

并且不能混用：

- secrets
- buckets
- databases

#### 4. provider 成本与失败治理初步具备

至少要能说明：

- 主 provider 是谁
- fallback 怎么做
- 超时 / 重试怎么做
- 成本上限怎么控

#### 5. 测试至少覆盖最小发布闭环

最低建议：

- unit：contract / schema / transform
- integration：主链至少 1 条
- e2e：至少 1 条可演示链

#### 6. 观测点具备

至少能看到：

- 失败位置
- run status
- step status
- trace / request id

当前进度：

- `2026-04-25` 已新增内部 `/observability` 页面和 `GET /api/observability/summary`
- 已能看到主链健康、异步任务、provider 摘要和失败热点
- 但外部 metrics / alerting、告警演练、worker/provider 深度 trace 仍未达到上线准备标准

#### 7. 发布清单和回滚 Runbook 进入可执行状态

不是只有文档存在，而是：

- 本次版本真的能按清单走
- 问题出现时真的能按 runbook 回退

#### 8. 文案与真实能力一致

如果当前只做到：

- 结果包
- demo 输出
- stub render

那上线文案不能伪装成“完整成片平台”。

#### 9. 敏感数据与外部模型边界已确认

至少要明确：

- 哪些数据禁止进模型
- 哪些任务不能用云端 agent
- secrets 如何管理

#### 10. 人工批准链路明确

至少要明确：

- 谁批准进入 staging
- 谁批准进入 production
- 高风险变更谁放行

## 7. Gate C：什么时候可以正式上线

我建议把“正式上线”定义得更严格一点。

进入正式上线，至少再多 4 条：

1. staging 已跑过真实发布候选版本
2. 至少经历过一次非演习式回滚推演
3. 主链关键失败模式有人工兜底方案
4. 成本、失败率、人工介入率在可接受范围内

## 8. 我们现在要不要先把这些全补完，再开始开发

结论是：

`不要等全部补完再开发，但要先补齐会阻断“大并行”和“上线”的最小前置件。`

也就是采用：

`边开发主链，边补 Gate B / Gate C 的关键阻断项。`

## 9. 我建议现在的执行顺序

### 9.1 现在立刻继续开发的

- persistence foundation
- SQLAlchemy model
- Alembic 首版真实 migration
- repository adapter
- 主链第一条 integration test

### 9.2 这批必须在“大并行”前补到位

- persistence 第一版落地
- 至少 1 条真实 integration test
- 第一次真实 worktree 并行协作
- review pass 按 PR 模板实际跑通

### 9.3 这批必须在“上线准备”前补到位

- staging / production 环境分层
- secrets 管理
- provider failure / retry / cost guardrail
- 至少 1 条 e2e 主链
- 发布清单按真实版本走通一次
- 回滚 Runbook 演练一次

## 10. 最终判断

压成一句话就是：

`现在已经适合继续开发主链，但不适合直接全面大并行，更不适合直接谈上线；最稳的做法是先把 persistence、真实测试、worktree 实战和环境分层补到位，再放大并行和进入上线准备。`
