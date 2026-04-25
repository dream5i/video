# 全新项目

这是一个面向电商短视频场景的 AI 工作台骨架仓库。

当前阶段目标不是一次把所有功能做完，而是先把下面这条最短主链路的代码底座搭起来：

`输入爆款链接或商品信息 -> 分析 -> 预填充 workflow draft -> 运行 -> 结果 -> 历史`

当前已经落下来的代码基线包括：

- `packages/contracts`：共享 contract
- `packages/workflow-schema`：workflow / low-code graph schema
- `services/api`：最小 API 编排层，已具备内存仓库和数据库仓库双实现，当前默认走数据库，并已接入 `request_id` / `trace_id`、结构化错误返回与可观测性汇总接口
- `services/worker`：provider / worker 骨架，analysis provider 已接入 started / completed / failed 结构化 trace
- `apps/web`：面向工作台的 Next.js 页面骨架
- `tests/integration`：已覆盖数据库主链、HTTP API 主链、结构化错误契约与 migration smoke
- `tests/e2e`：已落下第一条真实浏览器主链验收，使用 Playwright 跑通“创建项目 -> 运行 -> 历史”

当前可访问的前端路由：

- `/`：项目总览
- `/projects/new`：新建项目入口
- `/projects/proj_demo`：演示项目工作台
- `/history`：运行历史
- `/observability`：内部可观测性面板

## 当前统一命令入口

- `pnpm dev:web`
- `pnpm dev:api`
- `pnpm dev:worker`
- `pnpm test:api`
- `pnpm test:api:migrations`
- `pnpm test:e2e:install`
- `pnpm test:e2e`
- `pnpm worktree:bootstrap -- .worktrees/<name>`
- `pnpm worktree:drill:create`
- `pnpm worktree:drill:cleanup`
- `pnpm verify`

## 文档入口

建议先看：

1. [docs/index.md](./docs/index.md)
2. [docs/main-flow-diagram.md](./docs/main-flow-diagram.md)
3. [docs/implementation-roadmap.md](./docs/implementation-roadmap.md)
4. [docs/project-build-readiness-assessment.md](./docs/project-build-readiness-assessment.md)
5. [docs/version-gate-evidence-ledger.md](./docs/version-gate-evidence-ledger.md)
6. [docs/local-development-runbook.md](./docs/local-development-runbook.md)
7. [docs/parallel-drill-first-wave.md](./docs/parallel-drill-first-wave.md)
8. [docs/parallel-and-launch-gates.md](./docs/parallel-and-launch-gates.md)

## 当前目录

```text
apps/web
services/api
services/worker
packages/contracts
packages/workflow-schema
infra/
docs/
```

## 当前原则

- 前端只吃标准化 contract
- 长任务放到 worker，不塞进页面请求
- provider 先按能力抽象，不按厂商散落
- 先把 contracts 和 workflow schema 定稳，再继续扩功能
- 当前唯一主链：`输入 -> 分析 -> 预填充工作流 -> 运行 -> 结果 -> 历史`
- 默认开发路径已切到 `database`，`memory` 只作为兼容 / 调试兜底

## 下一步

1. 继续把 persistence implementation 从“可用”推进到“更完整可维护”
2. 把 API / Worker 的 stub 运行流继续替换成真实任务流
3. 把第一条浏览器 E2E 扩成更多异常、回退和历史场景
4. 把 worker/provider trace 继续接到 API-to-worker 真实异步链路、外部 metrics 和 alerting
