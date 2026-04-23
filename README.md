# 全新项目

这是一个面向电商短视频场景的 AI 工作台骨架仓库。

当前阶段目标不是一次把所有功能做完，而是先把下面这条最短主链路的代码底座搭起来：

`输入爆款链接或商品信息 -> 分析 -> 预填充 workflow draft -> 运行 -> 结果 -> 历史`

当前已经落下来的代码基线包括：

- `packages/contracts`：共享 contract
- `packages/workflow-schema`：workflow / low-code graph schema
- `services/api`：最小 API 编排层与内存仓库
- `services/worker`：provider / worker 骨架
- `apps/web`：面向工作台的 Next.js 页面骨架

当前可访问的前端路由：

- `/`：项目总览
- `/projects/new`：新建项目入口
- `/projects/proj_demo`：演示项目工作台
- `/history`：运行历史

## 当前统一命令入口

- `pnpm dev:web`
- `pnpm dev:api`
- `pnpm dev:worker`
- `pnpm verify`

## 文档入口

建议先看：

1. [docs/index.md](./docs/index.md)
2. [docs/main-flow-diagram.md](./docs/main-flow-diagram.md)
3. [docs/implementation-roadmap.md](./docs/implementation-roadmap.md)
4. [docs/project-build-readiness-assessment.md](./docs/project-build-readiness-assessment.md)
5. [docs/local-development-runbook.md](./docs/local-development-runbook.md)

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

## 下一步

1. 把数据库初稿和 migration skeleton继续落成真实 persistence implementation
2. 把 API / Worker 的 stub 运行流继续替换成真实任务流
3. 把最小测试从“基础校验”推进到“单元 / 集成 / E2E”
