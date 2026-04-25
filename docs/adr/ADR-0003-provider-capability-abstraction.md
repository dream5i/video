# ADR-0003：Provider 按能力抽象，不按厂商硬编码

状态：Accepted
日期：2026-04-25

## 标题

模型和外部 AI / 媒体能力的接入，统一按 capability 抽象，而不是把 OpenAI、Anthropic 等厂商细节直接写进产品层。

## 背景

这个项目后续必然会面对几个现实问题：

- 不同模型擅长的任务不同
- 价格、延迟、稳定性会变化
- 企业阶段可能需要切换供应商或做 fallback
- 如果把厂商名字直接写进页面、路由和领域逻辑，后面会非常难换

我们又不能为了“未来可能很多模型”而过度设计成一个大而空的抽象层。

所以要在“能换供应商”和“不过度抽象”之间找到平衡。

## 决策

我们正式决定：

- Provider 层按能力建接口，例如分析、转写、OCR、生成等
- 具体厂商实现放在 adapter 层，不把供应商细节泄露到 Web 层和领域层
- 编排层只依赖能力接口和标准化返回
- adapter 需要统一记录 latency、retry、cost、failure

当前阶段补充限制：

- MVP 不做 BYOK
- 前端不直接调用模型厂商
- 不在页面或 API 路由里硬编码 `if OpenAI / if Anthropic` 的产品流程判断

保留空间但不提前做满的事项：

- fallback 策略
- provider 灰度
- 多 provider 编排

这些可以预留接口，但不在当前阶段做成大而全平台。

## 备选方案

1. 先直接硬编码单一厂商

优点：

- 上手快
- 早期样例容易打通

缺点：

- 一旦换模型或补第二家，就会把路由、Worker 和页面一起带乱
- 供应商细节会污染产品层

为什么没有采用：

- 这和项目“可维护、可治理、可扩展”的目标冲突

2. 一开始设计成非常通用的大平台抽象

优点：

- 理论上扩展性最好

缺点：

- 很容易过度设计
- 当前阶段会拖慢核心主链推进

为什么没有采用：

- 现在更适合做“刚好够用的能力抽象”，而不是先造一个大平台

## 影响

产品影响：

- 用户看见的是统一能力，不需要知道背后是哪家模型

架构影响：

- Web、API、Worker 和 provider adapter 的边界更清楚
- 将来换供应商时，改动范围更可控

数据 / contract 影响：

- 标准化请求和返回结构会更重要
- provider 级成本、时延、失败信息要有统一记录字段

开发流程影响：

- 新接一家 provider 时，优先补 adapter，而不是直接改上层产品流程
- provider interface 改动仍属于共享锁定区

## 实施与回滚

实施方式：

- 按现有 `providers/interfaces.py` 和 `providers/registry.py` 路径持续扩展
- 新 provider 优先通过 adapter 接入并补测试
- 上层编排逻辑只调用标准能力接口

需要同步的文档：

- `docs/boundary-reuse-and-provider-strategy.md`
- `docs/ai-coding-stack-recommendation.md`
- `docs/schema-and-contract-freeze.md`
- `docs/enterprise-architecture-spec.md`

回滚条件：

- 如果后续业务长期只用单一稳定 provider，且抽象层明显带来过高维护成本

回滚方式：

- 仍需先补新的 ADR
- 再评估哪些接口可以收敛、哪些 contract 需要调整

## 关联文档

- `docs/boundary-reuse-and-provider-strategy.md`
- `docs/ai-coding-stack-recommendation.md`
- `docs/enterprise-architecture-spec.md`
- `services/api/app/providers/interfaces.py`
- `services/api/app/providers/registry.py`
- `services/worker/worker/providers/interfaces.py`
- `services/worker/worker/providers/registry.py`
