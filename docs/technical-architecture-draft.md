# 全新项目 技术方案与系统架构初稿

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 MVP 定义与 PRD 初稿](./product-mvp-prd.md)
- [全新项目 信息架构与页面草图](./information-architecture-and-page-wireframes.md)
- [AI 视频工作流赛道竞品与开源参照完整版](./competitive-landscape-ai-video-workflow.md)
- [全新项目 实施底座方案：仓库结构、Contracts First 与 Provider Registry](./implementation-foundation-plan.md)

## 1. 这份文档解决什么问题

这份文档把前面的产品文档继续往下落一层，回答下面这些真正会影响开发启动的问题：

1. 首版系统应该怎么拆。
2. 哪些能力应该同步请求，哪些必须走异步任务。
3. 数据应该怎么存，任务状态应该怎么追。
4. 前端、后端、Worker 和外部 AI/媒体供应商之间怎么分工。
5. 首版应该用什么技术栈，哪些地方刻意不要过度设计。

## 2. 总体技术结论

对于 `全新项目` 这条 MVP 主链路，我建议采用：

- 前端：`Next.js`
- API 编排层：`FastAPI`
- 后台任务：`Dramatiq + Redis`
- 数据库：`PostgreSQL`
- 对象存储：`S3-compatible storage`
- 媒体处理：`FFmpeg + Python workers`
- API 合约：`OpenAPI -> TypeScript client`

一句话概括就是：

`Next.js 做交互壳，FastAPI 做编排与领域逻辑，Worker 做媒体和 AI 长任务，Postgres 做事实来源，Redis 做任务队列，S3 做所有中间产物和结果。`

## 3. 架构原则

### 3.1 异步优先

这类产品的关键步骤里，链接解析、转写、OCR、结构分析、镜头规划、视频生成都不是低延迟接口，必须按异步任务来设计，而不是把所有逻辑塞进一次同步请求。

### 3.2 中间产物必须可复用

首版不能把整个流程做成一个黑盒，因为一旦最后一步失败，用户不能接受前面所有工作都白费。

所以系统必须保留：

- 源视频
- 抽帧
- transcript
- OCR 结果
- insight JSON
- 脚本草稿
- 镜头方案
- render 输入快照

### 3.3 供应商适配层独立

外部模型和媒体服务大概率会变，所以和供应商相关的调用不应散落在业务代码里，而应统一放在 adapter 层。

### 3.4 工作流先用结构化 JSON，不先做复杂节点图

首版产品已经决定使用 `prefilled storyboard workflow`，所以技术上也应该先有一个稳定的中间表示层，而不是一上来就实现图数据库式节点系统。

### 3.5 任务状态必须精确到步骤

从 `SoraTK` 实测里我们已经看到，用户最怕的是“像在跑，但不知道是不是卡住了”。所以每个 run 都必须按步骤记录，而不是只有一个总状态。

## 4. 推荐技术栈

### 4.1 前端

推荐：

- `Next.js`
- `TypeScript`
- `React`
- `Tailwind CSS`

原因：

- 页面路由和项目页结构天然适合 `Next.js`
- 结果页、项目页、历史页都需要比较稳定的路由模型
- 后面如果要加鉴权、SSR、SEO 或分享页，`Next.js` 比单纯 Vite 更顺

### 4.2 API 与领域层

推荐：

- `FastAPI`
- `Pydantic`
- `SQLAlchemy 2.x`
- `Alembic`

原因：

- Python 在媒体处理、OCR、转写、LLM 调用、视频管线适配上更自然
- `FastAPI` 非常适合做编排式 API 和内部工具 API
- `Pydantic` 对定义结构化中间产物很有帮助

### 4.3 后台任务

推荐：

- `Dramatiq`
- `Redis`

原因：

- 比 `Celery` 更轻，足够支撑 MVP
- 任务模型清晰，适合“多个步骤串联 + 每一步落库”
- 如果后续管线变得非常复杂，再考虑迁移到更重的工作流引擎

### 4.4 数据存储

推荐：

- `PostgreSQL`
- `S3-compatible storage`
- `Redis`

角色划分：

- `PostgreSQL`
  存结构化事实数据、状态、项目、配置、run、审计信息
- `S3-compatible storage`
  存源文件、中间媒体、结果文件、预览图、JSON 产物
- `Redis`
  存任务队列、短时状态和去重锁

### 4.5 媒体处理

推荐：

- `FFmpeg`
- Python 媒体处理模块

用途：

- 下载和转码
- 抽音频
- 抽帧
- 合成字幕
- 结果封装

## 5. 高层系统结构

### 5.1 逻辑架构图

```text
Browser / Web App
        |
        v
    Next.js Web
        |
        v
    FastAPI API
        |
        +----------------------+
        |                      |
        v                      v
  PostgreSQL              Redis Queue
        |                      |
        |                      v
        |                Worker Cluster
        |                      |
        |          +-----------+-----------+
        |          |           |           |
        v          v           v           v
  S3 Object   Link Parser   AI Analysis   Render Adapters
   Storage      Tools         Tools         / Media Tools
```

### 5.2 组件职责

#### Next.js Web

- 渲染页面
- 处理用户交互
- 拉取项目、分析、结果和 run 状态
- 承载工作流编辑 UI

#### FastAPI API

- 处理同步请求
- 负责领域对象创建
- 负责任务下发
- 负责状态查询
- 统一提供 API 合约

#### Worker Cluster

- 执行所有长耗时任务
- 调用供应商适配器
- 落中间产物
- 更新步骤状态

#### PostgreSQL

- 系统唯一结构化事实来源
- 保存项目、run、工作流草稿、状态流转、错误记录

#### S3 Object Storage

- 保存所有非结构化文件和大 JSON 产物

## 6. 首版核心领域模型

这里尽量和 PRD 保持一致，但更接近真实落库。

### 6.1 User

首版如果还不做正式多租户，也建议保留 `user_id`，避免后面迁移成本。

字段建议：

- id
- email
- display_name
- created_at

### 6.2 Project

一个项目代表一次完整创作上下文。

字段建议：

- id
- user_id
- title
- source_type
- source_url
- product_brief_json
- current_stage
- latest_analysis_run_id
- latest_workflow_draft_id
- latest_render_run_id
- created_at
- updated_at

### 6.3 SourceAsset

源素材及解析结果。

字段建议：

- id
- project_id
- platform
- original_url
- normalized_url
- raw_video_asset_id
- poster_asset_id
- metadata_json
- status

### 6.4 AnalysisRun

每次分析都独立成 run。

字段建议：

- id
- project_id
- status
- transcript_asset_id
- ocr_asset_id
- insight_asset_id
- script_asset_id
- shot_plan_asset_id
- provider_trace_json
- error_message
- created_at
- completed_at

### 6.5 WorkflowDraft

这是首版最重要的领域对象之一。

它不是节点图，而是：

`结构化 storyboard draft`

字段建议：

- id
- project_id
- version
- draft_json
- style_settings_json
- derived_from_analysis_run_id
- created_by
- created_at

### 6.6 RenderRun

每次生成任务。

字段建议：

- id
- project_id
- workflow_draft_id
- status
- provider
- input_snapshot_json
- progress_json
- error_message
- output_asset_id
- created_at
- completed_at

### 6.7 OutputAsset

结果产物。

字段建议：

- id
- project_id
- asset_type
- storage_key
- mime_type
- size_bytes
- duration_ms
- preview_storage_key
- metadata_json

### 6.8 RunStep

为了支持清晰状态页，建议单独建步骤表。

字段建议：

- id
- run_type
- run_id
- step_name
- status
- started_at
- finished_at
- error_message
- detail_json

## 7. 结构化中间表示

这是系统成败的关键之一。首版应该尽快统一内部表示，不要让不同供应商直接穿透到页面层。

### 7.1 Storyboard Draft JSON

建议内部统一为下面这种结构：

```json
{
  "meta": {
    "ratio": "9:16",
    "tone": "friendly",
    "style": "clean-realistic",
    "language": "zh-CN"
  },
  "segments": [
    {
      "id": "seg_1",
      "goal": "hook",
      "script": "第一口就记住的是很浓的梨香",
      "durationSec": 3,
      "shots": [
        {
          "id": "shot_1",
          "visual": "产品近景，暖光，包装与茶汤同框",
          "subtitle": "梨香浓郁，一口记住",
          "durationSec": 3
        }
      ]
    }
  ],
  "cta": {
    "text": "配料干净，家里人喝着更放心"
  }
}
```

### 7.2 为什么它重要

- 前端工作流页围绕它编辑
- RenderRun 基于它快照执行
- 结果页可以回溯它对应的版本
- 后续真要升级成节点图，也可以从这个结构演化

## 8. 核心流程的数据流

### 8.1 爆款链接模式

```text
用户提交链接
  -> API 创建 Project
  -> API 创建 SourceAsset
  -> API 投递 intake/analyze 任务
  -> Worker 解析链接与下载素材
  -> Worker 抽音频 / 抽帧 / OCR / transcript
  -> Worker 生成 insight / script / shot plan
  -> API 生成 WorkflowDraft
  -> 前端展示分析页和工作流页
  -> 用户编辑后发起 RenderRun
  -> Worker 执行 render pipeline
  -> 前端展示结果页
```

### 8.2 商品信息模式

```text
用户提交商品 brief
  -> API 创建 Project
  -> API 创建 AnalysisRun
  -> Worker 直接生成 insight / script / shot plan
  -> API 生成 WorkflowDraft
  -> 用户编辑
  -> 发起 RenderRun
```

### 8.3 重新生成模式

```text
已有 WorkflowDraft
  -> 用户修改脚本或风格
  -> 生成新版本 draft
  -> 创建新的 RenderRun
  -> 保留旧结果不覆盖
```

## 9. 服务边界

### 9.1 Web 层边界

Web 层只负责：

- 输入
- 展示
- 编辑
- 发起动作
- 轮询或订阅状态

Web 层不负责：

- 媒体处理
- 供应商逻辑
- 任务编排

### 9.2 API 层边界

API 层负责：

- 参数校验
- 领域对象创建
- 任务启动
- 返回视图模型
- 权限与鉴权

API 层不负责：

- 长时间阻塞处理
- 直接做重媒体任务

### 9.3 Worker 层边界

Worker 层负责：

- 调供应商
- 处理媒体
- 写中间产物
- 更新任务步骤

Worker 层不负责：

- 路由
- 页面逻辑

### 9.4 Adapter 层边界

所有外部服务都必须包成 adapter。

建议至少有这些 adapter：

- `link_parser_adapter`
- `transcript_adapter`
- `ocr_adapter`
- `analysis_llm_adapter`
- `render_adapter`
- `tts_adapter`

后续如果换供应商，只换 adapter，不要改业务流程。

## 10. API 设计建议

首版不需要追求完美 REST，只要边界清晰、前端调用顺手即可。

### 10.1 项目接口

- `POST /api/projects`
  创建项目
- `GET /api/projects/:projectId`
  获取项目总览
- `GET /api/projects/:projectId/history`
  获取项目版本和运行记录

### 10.2 分析接口

- `POST /api/projects/:projectId/analyze`
  发起分析
- `GET /api/projects/:projectId/analysis`
  获取最新分析结果

### 10.3 工作流接口

- `GET /api/projects/:projectId/workflow`
  获取当前工作流
- `PATCH /api/projects/:projectId/workflow`
  更新工作流草稿
- `POST /api/projects/:projectId/workflow/duplicate`
  复制一份草稿版本

### 10.4 运行接口

- `POST /api/projects/:projectId/renders`
  发起生成
- `GET /api/projects/:projectId/renders/:runId`
  获取 run 状态
- `POST /api/projects/:projectId/renders/:runId/retry`
  重试

### 10.5 结果接口

- `GET /api/projects/:projectId/result`
  获取最新结果

### 10.6 历史接口

- `GET /api/history`
  获取项目列表

## 11. 任务编排设计

### 11.1 AnalysisRun 步骤

建议至少拆成这些步骤：

1. `source_prepare`
2. `audio_extract`
3. `frame_extract`
4. `transcript_generate`
5. `ocr_generate`
6. `insight_generate`
7. `script_generate`
8. `shot_plan_generate`
9. `workflow_materialize`

### 11.2 RenderRun 步骤

建议至少拆成这些步骤：

1. `draft_snapshot`
2. `render_request_prepare`
3. `provider_render_start`
4. `provider_render_poll`
5. `post_process`
6. `preview_generate`
7. `result_finalize`

### 11.3 状态枚举建议

统一使用：

- `pending`
- `running`
- `succeeded`
- `failed`
- `canceled`

### 11.4 为什么要单独记步骤

- 页面需要显示清楚进度
- 失败时要定位在第几步
- 后面做重试时，才能只从失败点恢复

## 12. 供应商适配策略

这部分非常重要，因为外部能力最不稳定。

### 12.1 首版策略

首版建议每类能力只主打一个主供应商，并允许有限 fallback：

- 链接解析：1 个主解析器
- transcript：1 个主服务
- OCR：1 个主服务
- LLM 分析：1 个主模型
- render：1 条主渲染链路

### 12.2 不建议首版做的事情

- 不要把多个模型选项暴露给最终用户
- 不要把 `BYOK` 做进首版
- 不要让页面直接感知供应商差异

### 12.3 fallback 原则

只有当 fallback 不会显著改变结果语义时，才允许自动切换。

例如：

- transcript provider 切换，可以
- 核心 render provider 切换，要谨慎

## 13. 文件与对象存储设计

建议对象存储采用清晰路径命名，方便追踪和清理：

```text
projects/{projectId}/source/raw.mp4
projects/{projectId}/source/poster.jpg
projects/{projectId}/analysis/{analysisRunId}/transcript.json
projects/{projectId}/analysis/{analysisRunId}/ocr.json
projects/{projectId}/analysis/{analysisRunId}/insight.json
projects/{projectId}/analysis/{analysisRunId}/script.json
projects/{projectId}/analysis/{analysisRunId}/shot-plan.json
projects/{projectId}/renders/{renderRunId}/output.mp4
projects/{projectId}/renders/{renderRunId}/preview.jpg
projects/{projectId}/renders/{renderRunId}/metadata.json
```

## 14. 建议的仓库结构

当前仓库还是空骨架，所以这里直接给一个建议结构。

```text
全新项目/
├── apps/
│   └── web/                  Next.js
├── services/
│   ├── api/                  FastAPI
│   └── worker/               Dramatiq workers
├── packages/
│   └── contracts/            OpenAPI generated TS client / shared schemas
├── infra/
│   ├── docker/
│   └── scripts/
├── docs/
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
└── README.md
```

### 14.1 为什么这样拆

- `web` 和 `api/worker` 生命周期不同
- 媒体任务和页面代码不该混在一起
- `contracts` 有助于前后端统一接口

## 15. 本地开发与部署建议

### 15.1 本地开发

推荐使用：

- `Docker Compose`
- 本地 `Postgres`
- 本地 `Redis`
- 本地 `MinIO` 作为 S3 替代

本地最小组成：

- web
- api
- worker
- postgres
- redis
- minio

### 15.2 Staging / Production

可以按下面方式部署：

- `web`
  独立前端服务
- `api`
  独立应用服务
- `worker`
  独立 worker 服务
- `postgres`
  托管数据库
- `redis`
  托管 Redis
- `object storage`
  托管对象存储

### 15.3 不建议首版使用的部署形态

- 全部做成 serverless
- 把媒体处理塞进前端函数
- 把长任务绑死在 HTTP 请求生命周期里

## 16. 鉴权与权限

### 16.1 MVP 建议

首版可以采用轻量鉴权：

- 邮箱登录
  或
- 邀请制账号

### 16.2 设计建议

即使首版不做复杂权限，也建议所有核心表都带：

- `user_id`
- `created_by`

这样后续要支持团队协作时不至于推翻。

## 17. 可观测性与错误处理

### 17.1 必做日志

- API 请求日志
- 外部供应商请求日志
- RunStep 状态变更日志
- 关键异常日志

### 17.2 必做追踪

- 每个项目有 project id
- 每个分析 run 有 analysis run id
- 每个生成任务有 render run id

页面上也应该展示这些状态映射，而不是只在后端可见。

### 17.3 错误分层

建议把错误至少分成：

- `USER_INPUT_ERROR`
- `SOURCE_PARSE_ERROR`
- `TRANSCRIPT_ERROR`
- `OCR_ERROR`
- `ANALYSIS_ERROR`
- `RENDER_ERROR`
- `STORAGE_ERROR`
- `INTERNAL_ERROR`

## 18. 测试策略

### 18.1 单元测试

覆盖：

- JSON schema
- workflow draft 转换逻辑
- provider adapter 输入输出

### 18.2 集成测试

覆盖：

- 项目创建到分析完成
- draft 更新到 render run 创建
- 错误重试路径

### 18.3 E2E 测试

覆盖 2 条主链路：

1. `爆款链接 -> 分析 -> 工作流 -> 生成`
2. `商品信息 -> 工作流 -> 生成`

### 18.4 测试原则

不要让 E2E 直接依赖真实昂贵供应商。
应优先 mock adapter 或使用 sandbox 环境。

## 19. 建议的开发顺序

### Phase 0：架构落地准备

- 建仓库结构
- 建数据库迁移
- 建对象存储封装
- 建 adapter 接口

### Phase 1：项目与分析链路

- 新建项目
- 链接解析
- 分析 run
- 分析结果页

### Phase 2：工作流链路

- WorkflowDraft schema
- 工作流页
- 草稿保存与版本

### Phase 3：生成链路

- RenderRun
- RunStep
- 结果页
- 重试机制

### Phase 4：稳定性与运营能力

- 历史页
- 错误可观测性
- 清理任务
- 配额或额度

## 20. 当前最重要的技术决策

如果只保留 5 个最重要决定，就是：

1. `用结构化 storyboard draft 作为核心中间表示`
2. `用 FastAPI + Worker，而不是把一切塞进 Next.js`
3. `所有长任务异步化，并且步骤级落库`
4. `所有外部能力走 adapter 层`
5. `先做 prefilled workflow，不做空白节点系统`

## 21. 下一步建议

基于这份技术文档，最适合马上进入的动作是：

1. 建立仓库目录和基础脚手架
2. 定义数据库 schema 与迁移
3. 定义首批 API contract
