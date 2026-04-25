# ADR-0004：单主控、有限委派、主控终审与受保护主线

状态：Accepted
日期：2026-04-25

## 标题

当前项目采用：

- 单主控统筹
- 有限委派
- 主控集成
- 主控终审
- 受保护 `main`

## 背景

这个项目的重要特点是：

- 由 AI 深度参与搭建
- 会长期持续开发
- 未来可以进入多 Agent 并行
- 但当前仍处于单 owner / 单主控阶段

如果没有明确治理模型，很容易出现：

- 今天主控统筹，明天主控又像普通执行者一样乱写
- 子 Agent 同时改共享核心层，导致主线漂移
- 代码改完没人真正收口
- 分支和门禁规则写了，但实际上没人执行

## 决策

我们正式决定：

- 主控负责架构判断、任务拆分、关键层实现、集成和最终审查
- 子 Agent 只做边界清晰、写入范围独立、验收标准明确的任务
- 共享锁定区默认由主控亲自改，或由主控串行整合
- 所有进入主线的改动都走分支和 PR 流程，不直接推 `main`
- 当前 `main` 必过检查包括：`verify`、`dependency-review`

当前共享锁定区包括：

- `packages/contracts/**`
- `packages/workflow-schema/**`
- `services/api/app/domain/**`
- `services/api/app/providers/interfaces/**`
- `services/api/alembic/**`
- 根配置文件

当前阶段的补充规则：

- 由于项目仍是单 owner 阶段，暂不强制独立 reviewer 审批数
- 等到第二个真实 reviewer 稳定进入协作后，再升级为 required review 和 code owner review

## 备选方案

1. 主控什么都自己做，不做任何委派

优点：

- 决策最集中
- 不容易出现并行冲突

缺点：

- 速度会受限
- 一些边界清晰的任务浪费并行机会

为什么没有采用：

- 当前项目后续明确会进入可控并行，完全不委派会降低效率

2. 一开始就全面并行放开给多个 Agent

优点：

- 速度可能很快

缺点：

- 共享核心层会更容易冲突
- 主线很容易被多头带偏

为什么没有采用：

- 当前阶段还没有达到全面大并行门槛

3. 现在就强制要求 1 个独立审批和 code owner 审查

优点：

- 看起来更接近多人企业团队

缺点：

- 当前单 owner 阶段会把仓库锁死
- GitHub 不会把 self-approval 当成独立评审

为什么没有采用：

- 现在采用的是单人阶段可执行的安全版门禁，等角色条件成熟后再升级

## 影响

产品影响：

- 功能推进速度会比无治理并行慢一点，但方向更稳

架构影响：

- 共享核心层更不容易被并行改乱
- 主线边界可以由主控持续收口

数据 / contract 影响：

- 共享 contract、schema、migration 等高风险区改动会更谨慎

开发流程影响：

- 以后默认走 `分支 -> PR -> 检查 -> 合并`
- 高风险改动继续要求额外 review pass

## 实施与回滚

实施方式：

- 继续使用 worktree / 分支治理
- 子 Agent 任务单必须标明职责范围、写入文件和验收标准
- 主控在合并前做最终 review 和收口

需要同步的文档：

- `docs/build-governance-and-agent-operating-model.md`
- `docs/worktree-and-branching-runbook.md`
- `docs/parallel-and-launch-gates.md`
- `docs/repo-ruleset-and-branch-protection-baseline.md`
- `docs/github-platform-gates-rollout-checklist.md`

回滚条件：

- 如果后续团队角色明显变化
- 或者仓库已经进入多人稳定协作阶段，需要升级治理模式

回滚方式：

- 不直接删规则
- 先补新的治理 ADR，再升级 CODEOWNERS、review 规则和平台门禁

## 关联文档

- `docs/build-governance-and-agent-operating-model.md`
- `docs/worktree-and-branching-runbook.md`
- `docs/parallel-and-launch-gates.md`
- `docs/repo-ruleset-and-branch-protection-baseline.md`
- `docs/github-platform-gates-rollout-checklist.md`
- `docs/main-controller-reanchor-prompt.md`
