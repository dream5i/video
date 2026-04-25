# ADR-0002：采用 Contract-First 分层架构与长任务异步化

状态：Accepted
日期：2026-04-25

## 标题

当前正式采用：

- `Web / API / Worker / Data / Provider Adapter` 分层
- `contracts-first`
- 长任务异步化

## 背景

这个项目不是单纯的静态页面项目，而是：

- 有前端工作台
- 有 API 编排
- 有耗时 AI 分析和媒体处理
- 有运行状态追踪
- 未来还会继续扩 provider 和 workflow 能力

如果不先把架构定住，最容易发生的事情是：

- 页面里直接塞业务真相
- API 路由里散落供应商细节
- 耗时任务同步阻塞请求
- 将来想加重试、队列、状态追踪时只能返工

## 决策

我们正式决定：

- Web 负责页面交互和展示，不持有核心业务状态机
- API 负责同步编排、领域入口、标准化 contract 输出
- Worker 负责长任务、媒体处理、AI 调用和步骤追踪
- Provider Adapter 负责对接外部能力，不把厂商细节暴露到上层
- PostgreSQL 保存结构化事实
- S3-compatible storage 保存大对象和中间产物

当前正式采用的技术基线：

- Web：`Next.js`
- API：`FastAPI`
- Worker：`Dramatiq + Redis`
- Database：`PostgreSQL`
- Object Storage：`S3-compatible storage`

当前正式采用的流程原则：

- 先定 contract，再接 Web / API / Worker
- 分析、工作流预填充、生成等长任务按异步任务设计
- 页面不直接等完整长任务跑完才返回

## 备选方案

1. 采用全栈单体，同步执行长任务

优点：

- 初期实现看起来更快
- 服务数量更少

缺点：

- 页面和业务边界容易混掉
- 长任务会拖慢请求
- 后续很难做重试、追踪和故障隔离

为什么没有采用：

- 它更适合轻量 Demo，不适合本项目要走的企业级可维护路线

2. 一开始就上更重的分布式拆分

优点：

- 看起来更“企业级”
- 未来可扩展空间大

缺点：

- 当前阶段复杂度过高
- 团队规模和业务成熟度还不需要这么重

为什么没有采用：

- 现在要的是“够稳的骨架”，不是过早上复杂度

## 影响

产品影响：

- 用户能看到任务状态，而不是只能傻等
- 后续可以更自然地补重试、历史、失败回看

架构影响：

- 代码职责边界更清楚
- 核心层不会频繁在前端和后端之间来回搬家

数据 / contract 影响：

- 合同层会成为前后端共享真相
- `RunStep`、错误契约、请求追踪字段都需要保持稳定

开发流程影响：

- 共享锁定区需要更谨慎修改
- 涉及 contract、domain、provider interface 的改动优先由主控串行整合

## 实施与回滚

实施方式：

- 持续保持 `packages/contracts` 与 `packages/workflow-schema` 为共享真相
- API 继续输出结构化错误和 request / trace 追踪字段
- Worker 继续承接分析、预填充和生成链路

需要同步的文档：

- `docs/enterprise-architecture-spec.md`
- `docs/schema-and-contract-freeze.md`
- `docs/database-persistence-and-migration-plan.md`
- `docs/observability-and-alerting-baseline.md`

回滚条件：

- 如果后续真实业务证明异步队列显著增加复杂度且没有带来可观收益
- 或当前阶段被证实更适合收敛成更简单的单服务模型

回滚方式：

- 必须先补新的 ADR
- 再同步调整架构文档、部署方式和测试策略

## 关联文档

- `docs/enterprise-architecture-spec.md`
- `docs/technical-architecture-draft.md`
- `docs/schema-and-contract-freeze.md`
- `docs/database-persistence-and-migration-plan.md`
- `docs/observability-and-alerting-baseline.md`
