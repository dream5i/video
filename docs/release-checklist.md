# 全新项目 发布前检查清单

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)
- [全新项目 回滚 Runbook](./rollback-runbook.md)
- [全新项目 本地开发运行手册](./local-development-runbook.md)

## 1. 适用范围

这份清单用于：

- 合并到主线前的大版本收口
- 进入 staging 前
- 进入正式发布前

## 2. 发布前必须确认

### 2.1 边界与范围

- [ ] 仍在当前 MVP 主链内
- [ ] 没有把冻结的不做项偷偷带进主线
- [ ] 如有边界变化，已补 ADR 或 governing doc 更新

### 2.2 代码与契约

- [ ] `packages/contracts` 与 API / Web / Worker 保持一致
- [ ] 状态枚举没有未说明变化
- [ ] `WorkflowDraft` / `lowCodeGraph` 结构没有静默漂移

### 2.3 校验与测试

- [ ] 已运行 `pnpm verify`
- [ ] 如有额外测试，已附结果
- [ ] 已记录当前未覆盖风险

### 2.4 数据与迁移

- [ ] 如涉及 migration，已做独立 review pass
- [ ] 已说明升级路径
- [ ] 已说明 downgrade 或替代 rollback 方案

### 2.5 安全与依赖

- [ ] 未引入未审查的新外部 provider / MCP / plugin
- [ ] 新依赖已做 license / security 复核
- [ ] 未把敏感数据送入外部模型上下文

### 2.6 发布责任

- [ ] 已指定主控收口人
- [ ] 已指定人工批准人
- [ ] 已链接 rollback runbook 或本次变更专用回滚方案

## 3. 当前阶段的最小发布门槛

在项目还处于骨架阶段时，最低门槛建议为：

1. `pnpm verify` 通过
2. 高风险改动有 review pass
3. 数据改动有 rollback 说明
4. 文档与 README 已回填
