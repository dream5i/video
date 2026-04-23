# 全新项目 数据库、持久化与 Migration 初稿

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 Schema 与 Contract 冻结清单](./schema-and-contract-freeze.md)
- [全新项目 实施路线图](./implementation-roadmap.md)

## 1. 这份文档解决什么问题

这份文档用于回答：

`在真正把内存仓库换成持久化实现之前，数据库应该先定哪些边界、表和 migration 规则。`

它的目标不是一次定完所有后期表，而是把 MVP 主链需要的第一批事实来源先压稳。

## 2. 当前持久化原则

### 2.1 数据库只存结构化事实

数据库负责：

- 主项目记录
- 各类 run 状态
- workflow draft 版本
- 输出资产引用
- 审计事件

### 2.2 大对象不直接塞数据库

下面这些内容默认放对象存储，数据库只存引用：

- 原始视频
- 抽帧图
- 大体积 transcript 文件
- render 中间产物
- 最终视频

### 2.3 默认不持久化原始 provider response

首版默认只持久化：

- 标准化输出
- provider 标识
- prompt version
- token / cost / trace 信息

原始大响应、调试片段、第三方返回包不默认入库，避免：

- 数据边界失控
- 迁移困难
- 审计噪音过高

## 3. MVP 第一批表建议

## 3.1 `projects`

作用：

- 承接项目主身份与当前阶段

建议字段：

- `id`
- `org_id`
- `owner_id`
- `title`
- `source_type`
- `source_url`
- `source_payload_json`
- `current_stage`
- `latest_analysis_run_id`
- `latest_workflow_draft_id`
- `latest_render_run_id`
- `created_at`
- `updated_at`

说明：

- `source_payload_json` 当前用于承接 `product_brief`
- 等输入层稳定后，再决定是否拆成单独表

## 3.2 `analysis_runs`

作用：

- 记录一次分析执行

建议字段：

- `id`
- `project_id`
- `status`
- `capability`
- `provider`
- `prompt_version`
- `trace_id`
- `usage_json`
- `error_message`
- `created_at`
- `completed_at`

## 3.3 `analysis_outputs`

作用：

- 存结构化分析结果

建议字段：

- `id`
- `project_id`
- `analysis_run_id`
- `source_summary_json`
- `insights_json`
- `script_draft_json`
- `shot_plan_json`
- `created_at`

## 3.4 `workflow_drafts`

作用：

- 存 prefilled workflow 的版本化结果

建议字段：

- `id`
- `project_id`
- `version`
- `meta_json`
- `segments_json`
- `cta_json`
- `low_code_graph_json`
- `created_from_analysis_run_id`
- `created_at`
- `updated_at`

## 3.5 `render_runs`

作用：

- 记录一次渲染或生成执行

建议字段：

- `id`
- `project_id`
- `workflow_draft_id`
- `status`
- `provider`
- `trace_id`
- `usage_json`
- `error_message`
- `created_at`
- `completed_at`

## 3.6 `run_steps`

作用：

- 记录步骤级状态与回溯点

建议字段：

- `id`
- `run_id`
- `run_type`
- `name`
- `status`
- `capability`
- `provider`
- `started_at`
- `finished_at`
- `error_message`
- `step_payload_json`

## 3.7 `output_assets`

作用：

- 存结果资产引用

建议字段：

- `id`
- `project_id`
- `render_run_id`
- `asset_type`
- `storage_key`
- `preview_storage_key`
- `created_at`

## 3.8 `audit_events`

作用：

- 存关键动作审计记录

建议字段：

- `id`
- `category`
- `action`
- `actor_id`
- `org_id`
- `project_id`
- `run_id`
- `occurred_at`
- `metadata_json`

## 3.9 `prompt_registry`

作用：

- 固定 prompt / policy / version 的引用点

建议字段：

- `id`
- `capability`
- `version`
- `status`
- `model_family`
- `updated_at`

## 4. 当前第一批索引建议

- `projects(updated_at desc)`
- `analysis_runs(project_id, created_at desc)`
- `workflow_drafts(project_id, version desc)`
- `render_runs(project_id, created_at desc)`
- `run_steps(run_id, name)`
- `audit_events(project_id, occurred_at desc)`

## 5. 首个 migration 的边界

第一版 migration 只建议做下面这些：

- 建 MVP 第一批表
- 建核心外键
- 建主查询索引
- 不做复杂数据回填
- 不做软删体系
- 不做团队 / 权限 / billing 相关表

## 6. Migration 规则

### 6.1 一次 migration 只做一个逻辑焦点

不要把下面这些混在一个 revision 里：

- schema 重构
- 数据回填
- 行为逻辑变更

### 6.2 默认要求可回滚

每个 revision 都必须能说明：

- 如何 downgrade
- 如果不能安全 downgrade，为什么
- 数据损失边界是什么

### 6.3 不允许静默 schema 漂移

禁止：

- 手工改线上表结构但不补 migration
- 先改 ORM / model 再补 revision 却不说明差异

### 6.4 高风险 migration 必须额外 review pass

尤其是：

- 重命名列
- 删除列
- 改枚举
- 改外键
- 大表回填

## 7. 当前不建议现在就做的事

- 多团队权限表
- 模板市场相关表
- 批量运行与配额体系
- 大而全的通用节点引擎表
- 原始 provider response 全量留存

## 8. 下一步可执行动作

1. 先按这份文档补首个 Alembic revision skeleton
2. 再决定 SQLAlchemy model 的第一版映射
3. 再把 API repository 从 in-memory 逐步切到 persistence adapter
