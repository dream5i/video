# 全新项目 ADR 索引

更新日期：2026-04-25
状态：Active Baseline v0.1

## 1. 这份文档解决什么问题

ADR 的全称可以理解成：

- `Architecture Decision Record`

小白版解释：

- 它不是普通说明文档
- 它更像“已经拍板的关键决定”
- 后面开发时，如果遇到冲突，先看 ADR，不靠聊天记忆

## 2. 什么时候必须写 ADR

只要改动会影响下面任一项，就要补 ADR：

- 主链范围
- 核心架构拆分
- contract / schema 冻结对象
- provider 策略
- 并行治理规则
- 发布门槛

一句话规则：

`会影响后面很多实现判断的事情，不允许只靠口头约定，必须写成 ADR。`

## 3. 当前有效 ADR

1. [ADR-0001-mvp-main-flow-and-scope-freeze.md](./ADR-0001-mvp-main-flow-and-scope-freeze.md)
   冻结 MVP 主链范围和明确不做项。
2. [ADR-0002-contract-first-layered-async-architecture.md](./ADR-0002-contract-first-layered-async-architecture.md)
   冻结 contract-first、分层拆分和长任务异步化。
3. [ADR-0003-provider-capability-abstraction.md](./ADR-0003-provider-capability-abstraction.md)
   冻结 provider 按能力抽象，不按厂商把产品层写死。
4. [ADR-0004-main-controller-and-bounded-delegation.md](./ADR-0004-main-controller-and-bounded-delegation.md)
   冻结单主控、有限委派、主控终审和受保护主线。

## 4. 使用规则

- ADR 一旦进入 `Accepted`，后续实现默认按它执行。
- 如果要推翻已接受 ADR，不能直接改代码，先补新的 ADR。
- ADR 不替代详细设计文档，它负责定“方向和边界”。
- 详细实现、脚本、测试、运行细节仍然写在对应专题文档里。

## 5. 当前主控提醒

当前后续开发前，优先参考：

1. [README.md](../../README.md)
2. [index.md](../index.md)
3. [enterprise-architecture-spec.md](../enterprise-architecture-spec.md)
4. 本目录下已接受 ADR

如果你对“能不能做、该不该改、要不要并行”有犹豫，先看这里。
