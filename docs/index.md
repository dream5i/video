# 全新项目 文档索引

更新日期：2026-04-24
状态：Draft v0.1

## 1. 这份文档解决什么问题

当前仓库已经有较多文档。

如果没有一个统一索引，后面很容易出现：

- 找不到哪份文档是当前有效版本
- 同一件事在不同文档里重复但不一致
- 新进入项目的人不知道先看什么

所以这份文档的目标是：

`给这套文档建立导航、阅读顺序和 source-of-truth 关系。`

## 2. 推荐阅读顺序

如果是第一次进入项目，建议按下面顺序看。

### Step 1：先看项目主线和范围

1. [README.md](../README.md)
2. [product-mvp-prd.md](./product-mvp-prd.md)
3. [main-flow-diagram.md](./main-flow-diagram.md)

### Step 2：再看结构和边界

4. [information-architecture-and-page-wireframes.md](./information-architecture-and-page-wireframes.md)
5. [enterprise-architecture-spec.md](./enterprise-architecture-spec.md)
6. [technical-architecture-draft.md](./technical-architecture-draft.md)
7. [boundary-reuse-and-provider-strategy.md](./boundary-reuse-and-provider-strategy.md)
8. [frontend-shell-reuse-checklist.md](./frontend-shell-reuse-checklist.md)
9. [schema-and-contract-freeze.md](./schema-and-contract-freeze.md)

### Step 3：再看怎么实施

10. [implementation-foundation-plan.md](./implementation-foundation-plan.md)
11. [implementation-roadmap.md](./implementation-roadmap.md)
12. [build-governance-and-agent-operating-model.md](./build-governance-and-agent-operating-model.md)
13. [ownership-and-approval-matrix.md](./ownership-and-approval-matrix.md)
14. [test-strategy-and-acceptance-matrix.md](./test-strategy-and-acceptance-matrix.md)
15. [incident-response-and-escalation-matrix.md](./incident-response-and-escalation-matrix.md)
16. [local-development-runbook.md](./local-development-runbook.md)
17. [worktree-and-branching-runbook.md](./worktree-and-branching-runbook.md)
18. [parallel-drill-first-wave.md](./parallel-drill-first-wave.md)
19. [parallel-and-launch-gates.md](./parallel-and-launch-gates.md)
20. [repo-ruleset-and-branch-protection-baseline.md](./repo-ruleset-and-branch-protection-baseline.md)
21. [main-controller-reanchor-prompt.md](./main-controller-reanchor-prompt.md)

### Step 4：最后看企业与 AI 编程治理

22. [database-persistence-and-migration-plan.md](./database-persistence-and-migration-plan.md)
23. [data-lifecycle-and-recovery-baseline.md](./data-lifecycle-and-recovery-baseline.md)
24. [environment-promotion-model.md](./environment-promotion-model.md)
25. [nfr-and-slo-baseline.md](./nfr-and-slo-baseline.md)
26. [observability-and-alerting-baseline.md](./observability-and-alerting-baseline.md)
27. [release-checklist.md](./release-checklist.md)
28. [rollback-runbook.md](./rollback-runbook.md)
29. [project-build-readiness-assessment.md](./project-build-readiness-assessment.md)
30. [enterprise-prebuild-alignment-gap-analysis.md](./enterprise-prebuild-alignment-gap-analysis.md)
31. [enterprise-ai-readiness-assessment.md](./enterprise-ai-readiness-assessment.md)
32. [enterprise-ai-coding-rules.md](./enterprise-ai-coding-rules.md)
33. [enterprise-ai-coding-operating-playbook.md](./enterprise-ai-coding-operating-playbook.md)
34. [security/ai-coding-policy-matrix.md](./security/ai-coding-policy-matrix.md)
35. [security/do-not-feed-and-exclusion-list.md](./security/do-not-feed-and-exclusion-list.md)
36. [security/threat-model-and-trust-boundaries.md](./security/threat-model-and-trust-boundaries.md)
37. [security/dependency-and-license-gates.md](./security/dependency-and-license-gates.md)
38. [review/high-risk-change-checklist.md](./review/high-risk-change-checklist.md)

## 3. Source Of Truth 映射

为了避免后面互相打架，当前建议按下面关系理解。

### 产品范围

- 主文档：
  - [product-mvp-prd.md](./product-mvp-prd.md)
- 快速判断辅助：
  - [main-flow-diagram.md](./main-flow-diagram.md)

### 页面与体验结构

- 主文档：
  - [information-architecture-and-page-wireframes.md](./information-architecture-and-page-wireframes.md)
- 前端壳复用与组件来源：
  - [frontend-shell-reuse-checklist.md](./frontend-shell-reuse-checklist.md)

### 技术架构

- 主文档：
  - [enterprise-architecture-spec.md](./enterprise-architecture-spec.md)
- 背景方案稿：
  - [technical-architecture-draft.md](./technical-architecture-draft.md)
- 边界辅助：
  - [boundary-reuse-and-provider-strategy.md](./boundary-reuse-and-provider-strategy.md)
- 持久化与迁移：
  - [database-persistence-and-migration-plan.md](./database-persistence-and-migration-plan.md)

### 合同与 schema

- 主文档：
  - [schema-and-contract-freeze.md](./schema-and-contract-freeze.md)

### 实施阶段和优先级

- 主文档：
  - [implementation-roadmap.md](./implementation-roadmap.md)
- 所有权与审批：
  - [ownership-and-approval-matrix.md](./ownership-and-approval-matrix.md)
- 测试与事故治理：
  - [test-strategy-and-acceptance-matrix.md](./test-strategy-and-acceptance-matrix.md)
  - [incident-response-and-escalation-matrix.md](./incident-response-and-escalation-matrix.md)
- 平台门禁：
  - [repo-ruleset-and-branch-protection-baseline.md](./repo-ruleset-and-branch-protection-baseline.md)
- 主控回锚点：
  - [main-controller-reanchor-prompt.md](./main-controller-reanchor-prompt.md)
- 本地运行：
  - [local-development-runbook.md](./local-development-runbook.md)
- worktree 与分支：
  - [worktree-and-branching-runbook.md](./worktree-and-branching-runbook.md)
- 第一次真实并行演练：
  - [parallel-drill-first-wave.md](./parallel-drill-first-wave.md)
- 并行与上线门槛：
  - [parallel-and-launch-gates.md](./parallel-and-launch-gates.md)

### AI 编程治理

- 主文档：
  - [enterprise-ai-coding-rules.md](./enterprise-ai-coding-rules.md)
- 工程底线：
  - [nfr-and-slo-baseline.md](./nfr-and-slo-baseline.md)
  - [observability-and-alerting-baseline.md](./observability-and-alerting-baseline.md)
- 数据与环境：
  - [data-lifecycle-and-recovery-baseline.md](./data-lifecycle-and-recovery-baseline.md)
  - [environment-promotion-model.md](./environment-promotion-model.md)
- 企业级开工前对齐：
  - [enterprise-prebuild-alignment-gap-analysis.md](./enterprise-prebuild-alignment-gap-analysis.md)
- 操作手册：
  - [enterprise-ai-coding-operating-playbook.md](./enterprise-ai-coding-operating-playbook.md)
- 权限和安全补充：
  - [security/ai-coding-policy-matrix.md](./security/ai-coding-policy-matrix.md)
  - [security/do-not-feed-and-exclusion-list.md](./security/do-not-feed-and-exclusion-list.md)
  - [security/threat-model-and-trust-boundaries.md](./security/threat-model-and-trust-boundaries.md)
  - [security/dependency-and-license-gates.md](./security/dependency-and-license-gates.md)
  - [review/high-risk-change-checklist.md](./review/high-risk-change-checklist.md)
- 发布与回滚：
  - [release-checklist.md](./release-checklist.md)
  - [rollback-runbook.md](./rollback-runbook.md)

## 4. 当前文档体系是否够用

结论是：

`已经足够支撑项目进入持续搭建阶段，但还需要靠少量“文档系统化动作”来避免后期漂移。`

当前最重要的系统化动作包括：

- 保持这份索引更新
- 新增架构或边界变化时补 ADR
- 修改 source-of-truth 文档时同步相关引用

## 5. 后续新增文档规范

以后如果新增文档，建议同时做三件事：

1. 判断它属于哪个层级：
   - 产品
   - 技术
   - 实施
   - 治理
   - 安全 / review
2. 在这份索引里加入口
3. 如果它替换了旧结论，明确标注 source-of-truth 迁移
