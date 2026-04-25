# 全新项目 版本门槛证据总表

更新日期：2026-04-25
状态：Active Baseline v0.1

关联文档：

- [全新项目 大并行与上线门槛](./parallel-and-launch-gates.md)
- [全新项目 企业级对齐缺口优先级总表](./enterprise-alignment-gap-priority-matrix.md)
- [全新项目 GitHub 平台门禁落地检查单](./github-platform-gates-rollout-checklist.md)
- [全新项目 测试策略与验收矩阵](./test-strategy-and-acceptance-matrix.md)
- [全新项目 可观测性与告警基线](./observability-and-alerting-baseline.md)
- [全新项目 回滚 Runbook](./rollback-runbook.md)
- [全新项目 ADR 索引](./adr/README.md)

## 1. 这份文档解决什么问题

前面我们已经有：

- 门槛文档
- 治理文档
- 测试文档
- 平台门禁文档

但企业项目真正做版本判断时，不能只说：

- 我感觉现在能继续开发
- 我感觉现在还不能上线

企业更看重的是：

`你拿什么证据证明这个判断是成立的。`

小白版解释：

- 这份文档像项目当前阶段的“验收表”
- 它不替代详细文档
- 它负责把“当前到哪一步了”用证据串起来

## 2. 当前主控快照

截至 `2026-04-25`，当前主控判断是：

- `Gate A：可持续开发` -> `已达到`
- `Gate B：可控大并行` -> `部分达到，只适合小范围并行`
- `Gate C：可上线` -> `未达到`

同日已核验的实时信号包括：

- GitHub `main` 保护规则仍然生效
- GitHub open Dependabot alerts 为 `0`
- GitHub open PR 为 `0`
- 本地 `pnpm verify` 通过
- 旧的并行 worktree 已清理，主工作区重新回到单主线收口状态

## 3. 使用规则

- 每次主控重新判断 Gate 状态时，优先更新这份总表。
- 每条判断都尽量带上日期、来源和证据类型。
- 证据来源分 3 类：
  - `文档证据`
  - `平台证据`
  - `运行证据`
- 如果 Gate 结论变了，但这份文档没更新，默认以这份文档“未更新”为风险信号。

## 4. Gate A 证据

Gate A 的意思是：

- 可以沿主链继续开发
- 但不代表已经可以全面大并行或上线

| 项目 | 当前状态 | 证据 | 主控判断 | 后续动作 |
| --- | --- | --- | --- | --- |
| 主链范围冻结 | 已完成 | [ADR-0001](./adr/ADR-0001-mvp-main-flow-and-scope-freeze.md)、[README.md](../README.md)、[main-flow-diagram.md](./main-flow-diagram.md) | 当前没有主链漂移 | 后续任何扩边界改动先补 ADR |
| 架构与治理冻结 | 已完成 | [ADR-0002](./adr/ADR-0002-contract-first-layered-async-architecture.md)、[ADR-0003](./adr/ADR-0003-provider-capability-abstraction.md)、[ADR-0004](./adr/ADR-0004-main-controller-and-bounded-delegation.md) | 分层、provider 抽象、主控治理已经有正式拍板 | 后续重大变化继续按 ADR 沉淀 |
| GitHub 平台门禁 | 已完成第一版 | `2026-04-25` 主控实时核验：`main` 必须走 PR，required checks 为 `verify` / `dependency-review`，`strict=true`，`enforce_admins=true`，禁止 force push 和删除；参考 [github-platform-gates-rollout-checklist.md](./github-platform-gates-rollout-checklist.md) | 门禁已经从“文档规则”变成“平台真拦” | 等第二个真实 reviewer 稳定进入后，再升级为多人强审版 |
| 本地主链校验 | 已完成 | `2026-04-25` 本地执行 `pnpm verify` 通过，覆盖 typecheck、web build、Python compileall、integration tests | 当前代码底座和文档判断一致，没有“说能开发但一跑就坏” | 后续高风险改动继续保持合并前必跑 |
| 安全基线 | 已完成第一版 | `2026-04-25` GitHub open Dependabot alerts 为 `0`；上一轮已修复 `postcss` 漏洞并合入 `main` | 当前没有挂着未处理的已知 Dependabot 告警 | 后续继续保持依赖门禁和漏洞闭环 |
| 主工作区治理 | 已完成当前收口 | `2026-04-25` 已清理过期并行 worktree，本地主工作区重新只保留 `main` | 当前不会因为旧树残留导致主控误判上下文 | 后续每轮并行结束后立即收树 |

## 5. Gate B 证据

Gate B 的意思是：

- 可以更大胆地开并行 lane
- 但前提是主控还能稳住共享核心层和验收节奏

| 项目 | 当前状态 | 证据 | 主控判断 | 过线条件 |
| --- | --- | --- | --- | --- |
| 小范围并行演练 | 已做过第一轮 | [parallel-drill-first-wave.md](./parallel-drill-first-wave.md)、[review/parallel-01-review-pass.md](./review/parallel-01-review-pass.md) | 说明并行不是纯纸面规则 | 还需要第二轮更完整的并行闭环 |
| worktree / review 流程 | 已执行过且当前已收树 | [worktree-and-branching-runbook.md](./worktree-and-branching-runbook.md)；`2026-04-25` 主控已清理旧 worktree | 当前具备可控并行基础，但还不适合“全面放大” | 再做 1 轮真实并行并顺利收口 |
| 集成测试深度 | 部分完成 | [README.md](../README.md)、[test-strategy-and-acceptance-matrix.md](./test-strategy-and-acceptance-matrix.md)、`tests/integration`、`tests/e2e` | 已有主链测试，但异常覆盖仍不够深 | 扩关键异常、失败、回退场景 |
| 主控收口压力 | 当前可承受 | 当前 open PR 为 `0`，主线干净，最近治理收口顺利 | 现在的小范围并行是可控的 | 真正放大前，需要再验证 1 轮多 lane 收口 |
| 共享核心层稳定度 | 部分达到 | [parallel-and-launch-gates.md](./parallel-and-launch-gates.md)、[schema-and-contract-freeze.md](./schema-and-contract-freeze.md) | 当前够支撑小并行，不够支撑全面大并行 | contracts / schema / provider interface 再稳定一段时间 |

## 6. Gate C 证据

Gate C 的意思是：

- 不是“能演示”
- 而是“已经接近外部交付和上线准备”

当前这层还没有达到，主要卡在下面这些点。

| 项目 | 当前状态 | 证据 | 主控判断 | 补齐动作 |
| --- | --- | --- | --- | --- |
| 真实 AI 分析能力 | 未达到 | `services/worker/worker/adapters/openai_analysis.py`、`services/worker/worker/adapters/anthropic_analysis.py` 当前仍返回 `stubbed` | 这是当前最大的产品真实性风险 | 把 analysis stub 替换成真实 provider 调用链 |
| 真实渲染运行链 | 未达到 | [page.tsx](../apps/web/app/projects/[projectId]/page.tsx) 当前页面仍明确提示“stub 运行” | 现在能演示流程，不能误判成真实生产链路 | 把 render queue / retry / result chain 接成真实流 |
| 可观测平台接线 | 未达到 | [observability-and-alerting-baseline.md](./observability-and-alerting-baseline.md) 已有基线，但 dashboard / alerting 还未落平台 | 当前仍偏“日志可看”，还不是“告警可用” | 接 dashboard、metrics、alerting |
| 恢复与事故演练 | 未达到 | [rollback-runbook.md](./rollback-runbook.md)、[incident-response-and-escalation-matrix.md](./incident-response-and-escalation-matrix.md) 仍停留在文档层 | 现在有预案，还没有真实演练证据 | 做一次 backup/restore drill 和 incident drill |
| AI 输出验收底线 | 未达到 | [enterprise-alignment-gap-priority-matrix.md](./enterprise-alignment-gap-priority-matrix.md) 已明确这是必补项 | 现在更像“代码可验”，不是“结果可验” | 定义 analysis / workflow / render 的最小 AI 质量验收标准 |
| 环境晋级与外部上线 | 未达到 | [environment-promotion-model.md](./environment-promotion-model.md) 有文档，但还没有 staging / production 的真实发布节奏 | 现在还在企业级地基期，不在上线准备期 | 等真实 provider、观测和演练补齐后再推进 |

## 7. 当前风险清单

截至 `2026-04-25`，当前主控认为最值得盯住的风险是：

1. `真实性风险`
   当前主链已经能跑，但 AI 分析和渲染链仍有 stub 成分，不能把“演示可跑”误判成“产品可上线”。
2. `观测闭环风险`
   已有 request / trace / 结构化错误和关键日志，但还没有真正的平台告警和 dashboard。
3. `演练缺口风险`
   现在有回滚和事故响应文档，但没有真实 drill 证据。
4. `AI 验收缺口风险`
   代码验证在变强，但 AI 输出结果的验收底线还没固定。

## 8. 下一步主控优先级

这份证据总表落地后，下一项主控优先级切到：

`第 4 项：可观测性平台接线`

原因：

- 证据总表已经把“当前为什么还能继续开发、为什么还不能上线”说清楚了
- 下一步最缺的不是再讲判断，而是把运行闭环真正接到平台

## 9. 更新触发条件

以后出现下面任一情况，就要更新这份文档：

- Gate A / Gate B / Gate C 结论发生变化
- 新增或移除平台门禁
- `pnpm verify` 基线变化
- AI 主链从 stub 切到真实 provider
- 发生真实恢复演练或事故演练
- AI 结果验收标准正式落版
