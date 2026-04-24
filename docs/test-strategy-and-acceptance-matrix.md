# 全新项目 测试策略与验收矩阵

更新日期：2026-04-24
状态：Active Baseline v0.1

关联文档：

- [全新项目 企业架构定版说明](./enterprise-architecture-spec.md)
- [全新项目 NFR 与 SLO 基线](./nfr-and-slo-baseline.md)
- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)
- [全新项目 发布前检查清单](./release-checklist.md)

## 1. 这份文档解决什么问题

这份文档回答的是：

`改了什么，就至少要测到什么，测成什么样才算能进下一步。`

小白版解释：

- 不是“跑了几个测试就行”
- 而是按改动类型配对应的验收动作

## 2. 当前测试分层

当前统一分 6 层。

### 2.1 Contract / Schema 测试

目标：

- 保证共享 contract、workflow schema、状态枚举不静默漂移

### 2.2 Unit 测试

目标：

- 测单个函数、转换逻辑、适配层输入输出

### 2.3 Integration 测试

目标：

- 测 API、仓储、数据库、任务链路的真实配合

### 2.4 E2E 测试

目标：

- 从用户视角走完整条主链

当前状态：

- 已落地 1 条 Playwright 主链：
  `首页 -> 新建项目 -> 项目工作台 -> 触发 run -> 看到结果 -> 进入历史`

### 2.5 Manual Smoke

目标：

- 在真实页面或真实候选环境里人工确认关键路径没歪

### 2.6 AI Evals

目标：

- 评估分析、脚本、镜头方案这些 AI 结果质量

说明：

- 这一层很重要
- 但当前还是计划内增强，不是已落地的阻断门槛

## 3. 当前阶段的最低必测项

### 3.1 每次进入主线前

- `pnpm verify`
- 本次改动对应的最小必要测试
- 如果改动影响主链页面、页面到 API 的协作、运行状态流，补跑 `pnpm test:e2e`
- 已知未覆盖风险说明

### 3.2 每次高风险改动

- review pass
- 至少一条对应的 integration 或 migration 证明
- 回滚说明

### 3.3 每次准备进入 staging

- 主链人工 smoke
- 至少一条主链 integration
- 至少一条主链浏览器 E2E
- 版本候选说明

## 4. 按改动类型的验收矩阵

| 改动类型 | 最低必测项 | 是否必须 review pass |
| --- | --- | --- |
| 文档或纯说明改动 | 链接和引用自查 | 否 |
| 普通页面 UI 改动 | `pnpm verify` + 页面人工 smoke | 否 |
| Contract / schema 改动 | contract/schema 测试 + integration | 是 |
| API 路由或领域逻辑改动 | integration + 错误路径验证 | 视风险而定 |
| Worker / run step 改动 | integration + 状态流验证 | 视风险而定 |
| Migration 改动 | migration smoke + integration + rollback 说明 | 是 |
| Provider interface / retry / queue 改动 | adapter 测试 + integration + 风险说明 | 是 |
| Auth / role / policy / deletion 改动 | 对应测试 + review pass + 人工批准 | 是 |
| 新依赖 / 新 provider / 新 MCP | 来源与风险审查 + 最小回归验证 | 是 |

## 5. 当前阶段的主链验收定义

当前至少认下面这条链是“主链必须能过”的：

`创建项目 -> 获取项目 -> 生成分析结果 -> 生成预填 workflow -> 创建 render run -> 查询历史`

小白版解释：

- 这不是所有功能都要齐
- 而是最核心的一条用户路径不能断

当前自动化现状：

- API integration 已覆盖这条主链
- 真实浏览器 E2E 已覆盖这条主链的第一版页面路径

## 6. 当前建议的测试覆盖重点

### 6.1 先优先补

- contract / schema
- repository / persistence
- 主链 integration
- migration smoke
- 关键异常返回
- 主链浏览器 E2E 的异常和等待态

### 6.2 再逐步补

- retry / fallback
- provider 失败路径
- 删除与保留策略
- 多浏览器 / 多分辨率页面回归

### 6.3 再往后补

- 性能回归
- 安全专项测试
- AI eval dataset 和 regression suite

## 7. 当前阶段的人工验收插槽

下面这些内容，不应完全依赖自动测试：

- 页面信息架构是否跑偏
- 结果页文案是否和真实能力一致
- AI 输出是否明显不符合业务预期
- 高风险改动是否真的可回滚

## 8. 当前阶段的阻断条件

出现下面任一情况，不进入主线或更高环境：

- `pnpm verify` 不通过
- 主链 integration 断了
- 触碰高风险区却没有 review pass
- migration 没有 rollback 说明
- 明知有高风险未覆盖却没有写出来

## 9. 当前阶段的下一步工程化目标

- `tests/e2e` 从 1 条主链扩成异常、历史和回退场景
- provider failure / retry 场景补 integration
- AI eval fixtures 建第一版样本集
- 验收矩阵逐步写进 PR、发布流程和平台门禁

## 10. 一句话结论

当前测试策略的核心原则是：

`按改动风险决定测试深度，不要求一次把所有测试补满，但必须保证主链不断、高风险有证据、回滚说得清。`
