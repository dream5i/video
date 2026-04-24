# 全新项目 所有权与审批矩阵

更新日期：2026-04-24
状态：Active Baseline v0.1

关联文档：

- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 Worktree 与分支治理手册](./worktree-and-branching-runbook.md)
- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)
- [全新项目 发布前检查清单](./release-checklist.md)
- [全新项目 回主控提示词](./main-controller-reanchor-prompt.md)

## 1. 这份文档解决什么问题

这份文档把下面这件事讲清楚：

`哪一块归谁负责，哪类改动谁能做，谁必须审，谁最后拍板。`

小白版解释：

- 不是“大家都能改，最后再看”
- 而是先把责任表和签字表定好

## 2. 当前组织形态判断

当前项目还不是多人团队分工很细的阶段，更接近：

- `项目 owner + 主控 + 受控 AI 协作`

所以这份矩阵按“当前单主控、后续可扩展成团队”的方式写。

## 3. 角色定义

## 3.1 Project Owner

职责：

- 定业务方向
- 定优先级
- 定是否接受边界变化
- 对高风险上线或重大范围变化做最终业务批准

小白版解释：

- 你决定“这项目到底往哪走”

## 3.2 Main Controller

职责：

- 架构守门
- 任务拆分
- 共享锁定区改动
- 集成收口
- 最终代码审查

小白版解释：

- 我负责“怎么盖、谁来盖、最后有没有盖歪”

## 3.3 Bounded Implementer

职责：

- 在明确文件边界内实现功能
- 不扩 scope
- 不改共享锁定区

## 3.4 Reviewer

职责：

- 查越界
- 查回归
- 查 contract 破坏
- 查缺测试和缺回滚

说明：

- reviewer 负责“找问题”
- 不负责“替代最终批准”

## 3.5 Security / Platform Owner

当前状态：

- 还没有独立人岗
- 目前由主控代行第一版规则设计

后续职责：

- 安全边界
- 密钥治理
- 平台策略
- 依赖与许可证门禁

## 3.6 Release Approver

当前状态：

- 由 Project Owner 负责

职责：

- 决定是否进入 staging
- 决定是否进入 production

## 4. 区域所有权矩阵

| 区域 | Primary Owner | 谁可以实施 | 谁必须审 | 是否必须人工批准 |
| --- | --- | --- | --- | --- |
| 产品范围与边界 | Project Owner + Main Controller | Main Controller | Project Owner | 是 |
| `apps/web/**` 常规页面与展示层 | Main Controller | Main Controller / bounded implementer | Main Controller | 否 |
| `services/api/**` 常规路由与编排 | Main Controller | Main Controller / bounded implementer | Main Controller | 否 |
| `services/worker/**` 常规 worker 逻辑 | Main Controller | Main Controller / bounded implementer | Main Controller | 否 |
| `packages/contracts/**` | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `packages/workflow-schema/**` | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `services/api/app/domain/**` | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `services/api/app/providers/interfaces/**` | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `services/api/alembic/**` | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `.github/**` / 根配置 / CI | Main Controller | Main Controller | Reviewer + Main Controller | 是 |
| `docs/**` 常规文档 | Main Controller | Main Controller / bounded implementer | Main Controller | 否 |
| 安全规则 / retention / deletion / policy | Security / Platform Owner 代理为 Main Controller | Main Controller | Reviewer + Project Owner | 是 |
| 发版 / 回滚 / 环境晋级 | Release Approver + Main Controller | Main Controller | Project Owner | 是 |

## 5. 哪些改动必须进入高风险审批链

以下改动，默认走：

`实现 -> reviewer pass -> 主控终审 -> Project Owner 批准`

适用范围：

- contract 变化
- workflow schema 变化
- domain model 语义变化
- migration
- provider interface
- auth / role / policy
- retention / deletion
- queue / retry / state machine
- CI / release / rollback 核心规则

## 6. 哪些改动可以受控并行

以下改动可以并行，但仍要按边界分树分支：

- 页面 UI 切片
- 只读列表页
- 非锁定区文档
- 独立测试补齐
- 边界清晰的 adapter 实现

前提：

- 不碰共享锁定区
- 不改主链语义
- 验收标准明确

## 7. 仓库侧落地规则

## 7.1 CODEOWNERS

仓库已补：

- [`.github/CODEOWNERS`](../.github/CODEOWNERS)

当前先以单 owner 方式落地，后续如果进入组织化协作，再替换成团队 owner。

## 7.2 PR 模板

当前已存在：

- `Scope Check`
- `Evidence`
- `Risk Review`
- `Rollback`

这意味着：

- 每次变更不只是交代码
- 还要交范围说明、验证证据、风险结论和回滚路径

## 7.3 平台侧规则

注意：

- `CODEOWNERS` 只是仓库内文件
- 真正的“强制门禁”还要在 GitHub 平台里打开 ruleset / branch protection

小白版解释：

- 光写制度还不够
- 还得把门禁机装上

## 8. 推荐的 GitHub 平台配置

这部分不是仓库代码能自动完成的，但应该作为平台配置目标。

建议至少打开：

1. `main` 禁止直接推送
2. 合并前必须通过 CI
3. 合并前必须有 pull request review
4. 共享锁定区变更要求 code owner review
5. 高风险改动要求人工批准
6. 不允许跳过 required checks

## 9. 当前单人阶段怎么理解这些规则

现在项目还是单 owner 主导，所以会出现一个看起来“像是同一个人既是 owner 又是 approver”的情况。

这不矛盾。

因为当前最重要的是先把下面两件事建立起来：

- 规则先成型
- 后续多人协作时能平滑升级

也就是说：

- 现在先把制度和入口建好
- 后续再把角色从“一个人兼多岗”升级成“多人分岗”

## 10. 后续升级点

以下情况出现时，应升级这份矩阵：

- 仓库迁到组织而不是个人账号
- 出现独立前端 / 后端 / 平台负责人
- 引入企业 SSO / RBAC
- 进入 staging / production 真发布
- 开始多人并行和正式 code review

## 11. 一句话结论

当前项目的所有权模型可以概括成：

`Project Owner 定方向，Main Controller 定实现与收口，bounded implementer 只在明确边界内干活，reviewer 负责找问题，高风险改动必须走人工批准链。`
