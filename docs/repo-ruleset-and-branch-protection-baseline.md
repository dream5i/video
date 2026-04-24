# 全新项目 仓库 Ruleset 与 Branch Protection 基线

更新日期：2026-04-24
状态：Active Baseline v0.1

关联文档：

- [全新项目 所有权与审批矩阵](./ownership-and-approval-matrix.md)
- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)
- [全新项目 依赖与许可证门禁](./security/dependency-and-license-gates.md)

## 1. 这份文档解决什么问题

这份文档回答的是：

`除了仓库里的文档和代码，我们还应该在 GitHub 平台上把哪些门禁真正打开。`

小白版解释：

- 前面的规则更像“制度”
- 这份文档更像“把门禁机装到门口”

## 2. 当前阶段的目标

当前目标不是一口气把所有企业平台能力都开满，而是先把最关键的 6 个门禁落成平台规则。

## 3. `main` 分支的最低规则

建议在 GitHub ruleset 或 branch protection 中至少打开：

1. 禁止直接推送到 `main`
2. 禁止 force push
3. 禁止删除 `main`
4. 合并前必须通过 required status checks
5. 合并前必须有 pull request review
6. 共享锁定区变更要求 code owner review

## 4. 当前建议的 required status checks

至少把下面这些检查列为 required：

- `verify`
- `dependency-review`

小白版解释：

- 一个查“代码和测试基本过没过”
- 一个查“有没有把高风险依赖带进来”

## 5. 当前建议的 review 门槛

## 5.1 普通改动

- 至少 `1` 个 review

## 5.2 共享锁定区或高风险改动

- 至少 `1` 个 code owner review
- 需要 review pass 证据

## 5.3 安全、删除、migration、provider 改动

- code owner review
- review pass
- 人工批准

## 6. 当前建议打开的其他规则

- Require conversation resolution
- Require linear history
- Dismiss stale reviews

如果平台支持，还建议：

- Require last push approval
- Restrict who can bypass rules

## 7. 当前阶段不建议开放的例外

- 不给普通开发分支直推 `main`
- 不给 AI agent 绕过 ruleset 的特权
- 不把高风险变更放进“管理员可直接跳过”的默认路径

## 8. 共享锁定区和规则的关系

下面这些区域，建议在日常 review 时重点对应 code owner review：

- `packages/contracts/**`
- `packages/workflow-schema/**`
- `services/api/app/domain/**`
- `services/api/app/providers/interfaces/**`
- `services/api/alembic/**`
- `.github/**`

## 9. 当前已落到仓库的对应物

当前仓库里已经有：

- [`.github/CODEOWNERS`](../.github/CODEOWNERS)
- [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml)
- [`.github/dependency-review-config.yml`](../.github/dependency-review-config.yml)

这意味着：

- 规则不再只是口头要求
- 已经开始有第一条自动化依赖门禁

## 10. 当前仍然需要手动配置的项

下面这些不是仓库文件能自动打开的，还要在 GitHub 仓库设置里配：

- ruleset / branch protection
- required status checks 绑定
- required review 数量
- code owner review 强制
- bypass 权限控制

## 11. 一句话结论

当前平台门禁基线的核心原则是：

`让 main 分支默认难进而不是默认好进，先用自动检查拦一层，再用 review 和审批拦一层。`
