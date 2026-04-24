# 全新项目 环境分层与晋级模型

更新日期：2026-04-24
状态：Active Baseline v0.1

关联文档：

- [全新项目 发布前检查清单](./release-checklist.md)
- [全新项目 回滚 Runbook](./rollback-runbook.md)
- [全新项目 大并行与上线门槛](./parallel-and-launch-gates.md)
- [全新项目 数据生命周期与恢复基线](./data-lifecycle-and-recovery-baseline.md)

## 1. 这份文档解决什么问题

这份文档回答的是：

`代码和配置怎么从本地一路走到测试、再走到正式环境，过程中哪些东西绝不能混。`

小白版解释：

- 就是先定“哪几层环境”
- 再定“怎么一级一级往上走”

## 2. 当前环境分层

当前统一定义 4 层。

### 2.1 `local`

用途：

- 开发
- 本地调试
- 本地验证

特点：

- 允许 stub
- 允许假数据
- 不允许接生产 secrets

### 2.2 `ci`

用途：

- 自动校验
- 自动测试

特点：

- 只跑受控、可复现的检查
- 不依赖人工本地状态

### 2.3 `staging`

用途：

- 发布候选验证
- 真实环境级联调
- 回滚演练

特点：

- 配置接近生产
- 但数据、密钥、桶、数据库必须和生产分离

### 2.4 `production`

用途：

- 正式对外服务

特点：

- 最严格的审批和变更门禁
- 不允许实验性配置直接混入

## 3. 当前阶段的硬隔离规则

下面这些东西，环境之间绝不能混用：

- secrets
- database
- object storage bucket
- queue / cache
- provider key
- callback / webhook 配置

小白版解释：

- 测试环境不能偷连正式数据库
- staging 也不能和 production 共用一把钥匙

## 4. 当前推荐的晋级路径

统一路径：

`feature branch -> pull request -> CI -> main -> staging candidate -> staging validation -> production approval -> production`

当前规则：

1. 不允许跳过 CI
2. 不允许从本地直接当成 production 发布
3. 不允许绕过 staging 直接说“这个应该没问题”

## 5. 每层环境的最低要求

| 环境 | 最低要求 |
| --- | --- |
| `local` | 能本地跑通、能执行 `pnpm verify`、不接生产数据 |
| `ci` | 能稳定复现构建和测试结果 |
| `staging` | 有独立 secrets / DB / storage，能跑发布候选验证 |
| `production` | 有审批链、可回滚、可观测、环境与数据完全隔离 |

## 6. 进入 staging 前必须满足什么

至少满足下面这些：

1. `pnpm verify` 通过
2. 高风险改动已 review pass
3. migration 有升级和回退说明
4. 主要观测点已具备
5. 本次版本有发布清单
6. 本次版本有回滚路径

## 7. 进入 production 前必须满足什么

至少满足下面这些：

1. staging 已跑过候选版本
2. staging 验收通过
3. 关键路径人工复核过
4. 回滚方案确认过
5. 谁批准发布已经明确

## 8. 当前阶段的审批链

### 8.1 进入 staging

- Main Controller 准备版本
- Project Owner 批准进入 staging

### 8.2 进入 production

- Main Controller 提交发布建议
- Project Owner 最终批准

后续如果进入团队化交付，再补：

- Platform Owner
- Security Owner
- Release Manager

## 9. 当前阶段不允许的晋级方式

- 直接从未审 PR 分支进入 staging
- 带实验性扩 scope 的版本直接升环境
- 用 local 配置冒充 staging
- 用 staging 数据或密钥混 production

## 10. 配置与密钥规则

当前原则：

1. 配置模板可以进仓库
2. 真实密钥不能进仓库
3. 每个环境单独持有自己的 secrets
4. provider key 默认分环境管理

## 11. 当前阶段的阻断条件

出现下面任一情况，不进入更高环境：

- 环境边界说不清
- secrets 来路不清
- 数据库和 bucket 没分开
- 无法回滚
- 高风险改动没审

## 12. 一句话结论

当前环境晋级模型的核心原则是：

`环境越往上，权限越少、审批越重、数据越真、回滚要求越高，任何时候都不能把不同环境混成一锅。`
