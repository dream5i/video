# 全新项目 实施路线图

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 文档索引](./index.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 企业 AI 编程规则](./enterprise-ai-coding-rules.md)
- [全新项目 企业 AI 编程操作手册](./enterprise-ai-coding-operating-playbook.md)
- [全新项目 项目搭建就绪度评估](./project-build-readiness-assessment.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 实施底座方案：仓库结构、Contracts First 与 Provider Registry](./implementation-foundation-plan.md)

## 1. 路线图目的

这份文档不是再讨论“做不做”，而是明确：

- 先做什么
- 后做什么
- 哪些阶段必须单线程
- 哪些阶段可以并行
- 哪些里程碑通过后才能进入下一阶段

一句话：

`先冻结主梁，再铺线路，再做页面，再接运行链路。`

## 2. 实施总原则

### 2.1 骨架先于功能

先把仓库结构、合同层、schema、provider interface 定稳，再继续做业务页面和任务编排。

### 2.2 单线程先行

在共享核心层没稳定之前，不做大规模并行开发。

### 2.3 主链路优先

所有实现都必须服务于这条 MVP 主链路：

`输入 -> 分析 -> 预填充工作流 -> 运行 -> 结果 -> 历史`

### 2.4 高风险变更要二次审查

数据库、provider interface、状态机、迁移、共享 contract 改动，必须额外 review pass。

## 3. 阶段拆分

## 3.1 Phase 0：治理与冻结

目标：

- 把后续实现不应漂移的边界先固定下来

任务：

- 补齐 `AGENTS.md`
- 补齐 `implementation-roadmap.md`
- 补齐 `schema-and-contract-freeze.md`
- 补齐 `docs/index.md`
- 补齐 `docs/adr/ADR-TEMPLATE.md`
- 补齐企业 AI 编程规则与操作文档
- 建 `docs/adr/`
- 初始化 git
- 清理运行产物

完成标志：

- 仓库进入可治理状态
- 共享合同层冻结名单可读
- 工作模式不再依赖口头约定
- 企业 AI 编程边界与操作方式可查可复用
- 文档导航与决策模板具备

并行策略：

- 单线程

## 3.2 Phase 1：共享合同层

目标：

- 冻结前后端共同语言

任务：

- 固化 `packages/contracts`
- 固化 `packages/workflow-schema`
- 统一 `Project / AnalysisRun / WorkflowDraft / RenderRun / RunStep` 命名
- 统一状态枚举
- 补 contract 导出结构

完成标志：

- 前端、API、Worker 都可以基于统一类型和 schema 工作

并行策略：

- 单线程

强制 review pass：

- 是

## 3.3 Phase 2：API 骨架

目标：

- 建立最小可运行编排层

任务：

- 补 `services/api` 目录结构
- 建 domain 目录
- 建内存态或 stub repository
- 打通：
  - `POST /api/projects`
  - `GET /api/projects/:projectId`
  - `GET /api/projects/:projectId/analysis`
  - `GET /api/projects/:projectId/workflow`
- API 返回统一 contract

完成标志：

- `web` 可以从 API 获取演示项目、分析和 workflow 数据

并行策略：

- 以主控为主
- 可允许一个只读 Agent 做契约核对

## 3.4 Phase 3：Provider 与 Worker 骨架

目标：

- 把能力抽象和执行层先搭出来

任务：

- 固化 provider interfaces
- 固化 provider registry
- 建 worker 的任务入口
- 建 OpenAI primary adapter stub
- 预留 Anthropic secondary adapter
- 建 run + step 状态模型的最小内存实现

完成标志：

- 任务可以从 API 发起，到 worker 返回 stub 结果

并行策略：

- 允许局部并行
- 但 interface 和 registry 改动仍由主控收口

强制 review pass：

- 是

## 3.5 Phase 4：Web MVP Workspace

目标：

- 把首页、分析页、工作流页连起来

任务：

- 首页接入真实 contract
- 分析页展示结构化结果
- 工作流页展示 storyboard draft
- 运行状态页展示 run + step
- 结果页和历史页先用 stub 数据

完成标志：

- 前端从“宣传页”进入“可操作 workspace”

并行策略：

- 可以分页面并行
- 但共享布局和 contract 层不能并行乱改

## 3.6 Phase 5：最小运行链路

目标：

- 打通一次最小分析与生成运行闭环

任务：

- 从项目创建发起一次 analysis run
- Worker 写回 analysis stub 结果
- WorkflowDraft 从 analysis 派生
- 发起一次 render run
- 结果页可显示 stub 输出

完成标志：

- 项目从输入到结果可以完整走一遍，即使底层是 stubbed provider

并行策略：

- 主控收口

## 3.7 Phase 6：基础设施与测试

目标：

- 让骨架进入稳定推进状态

任务：

- 完善 Docker Compose 使用说明
- 补 `tests/e2e`
- 补 `tests/integration`
- 加最小 lint/typecheck/test 命令
- 准备数据库 migration

完成标志：

- 仓库可以持续演进，而不是一次性脚手架

## 4. 第一阶段任务清单

这是我建议现在立刻执行的最小任务包。

### T1

- 初始化 git 仓库

### T2

- 清理 `__pycache__` 与 `*.pyc`

### T3

- 冻结 schema 与 contract 文档

### T4

- 统一共享目录骨架：
  - `services/api/app/domain/`
  - `services/api/alembic/versions/`
  - `tests/e2e/`
  - `tests/integration/`
  - `tests/fixtures/`
  - `docs/adr/`

### T5

- 让 `README`、`AGENTS.md`、路线图、技术文档保持一致

## 5. 并行与委派策略

### 5.1 现在不应并行的区域

- `packages/contracts/**`
- `packages/workflow-schema/**`
- `services/api/app/providers/interfaces.py`
- `services/api/app/providers/registry.py`
- `services/api/alembic/**`

### 5.2 现阶段可并行的区域

- `apps/web` 的纯展示层页面
- `tests` 的只增不改型用例
- 非共享文档补充

### 5.3 推荐的子 Agent 任务粒度

- 一个 Agent 只拥有一个明确目录或一个明确页面
- 不允许两个 Agent 同时修改共享 contract 层

## 6. 里程碑

### M0

- 治理文件齐备
- git 初始化完成

### M1

- contracts 与 workflow schema 冻结

### M2

- API 可返回统一 stub 数据

### M3

- Web workspace 可读写 workflow draft

### M4

- analysis run / render run 的最小闭环打通

## 7. 当前推荐下一步

如果按这份路线图继续推进，最合适的下一步就是：

1. 初始化 git
2. 清理运行产物
3. 补齐 schema freeze
4. 统一空目录骨架
5. 再进入 contract 与 provider interface 收口
