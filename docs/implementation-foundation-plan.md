# 全新项目 实施底座方案：仓库结构、Contracts First 与 Provider Registry

更新日期：2026-04-23  
状态：Draft v0.1

关联文档：

- [全新项目 MVP 定义与 PRD 初稿](./product-mvp-prd.md)
- [全新项目 信息架构与页面草图](./information-architecture-and-page-wireframes.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 边界分层、复用策略与模型接口预留](./boundary-reuse-and-provider-strategy.md)

## 1. 这份文档解决什么问题

前面几份文档已经把“做什么”和“为什么这么做”讲清楚了。  
现在差的是一份能直接指导开工的底座方案。

这份文档只回答 4 个落地问题：

1. 仓库第一天应该怎么建。
2. 首批 contract 到底先定哪些，不先定哪些。
3. provider registry 和 adapter interface 应该长什么样。
4. Phase 0 到 Phase 1 的最小交付清单是什么。

一句话：

> 这不是新 PRD，  
> 这是把前面文档翻译成“可以开搭”的工程起跑稿。

## 2. 先给结论

如果现在就开始搭，我建议固定下面这 6 条：

1. 用 `monorepo`，但先保持轻，别一上来拆十几个服务。
2. 用 `contracts first`，先把 API 输入输出和核心 schema 定下来。
3. provider 先按“能力”注册，不按“厂商名字”散落。
4. 先只接 1 条稳定分析链路和 1 条稳定 render 链路。
5. 所有长任务都必须有 `run + step` 两层状态。
6. 前端永远只吃标准化结果，不直接吃 provider 原始返回。

## 3. 建议的仓库结构

## 3.1 第一版目录

```text
全新项目/
├── apps/
│   └── web/                         Next.js 前端
├── services/
│   ├── api/                         FastAPI 编排层
│   └── worker/                      异步任务与媒体处理
├── packages/
│   ├── contracts/                   OpenAPI client + TS types
│   ├── workflow-schema/             storyboard / analysis / render schema
│   └── config/                      前端可共享的静态配置与枚举
├── infra/
│   ├── docker/
│   ├── scripts/
│   └── env/
├── docs/
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── fixtures/
├── .editorconfig
├── .gitignore
├── docker-compose.yml
├── pnpm-workspace.yaml
└── README.md
```

## 3.2 为什么要多一个 `workflow-schema`

因为这个项目最容易后面崩掉的地方，不是页面，而是：

- analysis 输出结构不统一
- workflow draft 越改越乱
- render request 每家 provider 一个格式

所以建议把下面这些先单独放到一个共享包里：

- `insight schema`
- `script draft schema`
- `shot plan schema`
- `storyboard draft schema`
- `render request schema`
- `run progress schema`

大白话：

> 这包就是“系统内部通用语言”。  
> 没这层，后面每接一个模型都会重新打一架。

## 3.3 为什么 `contracts` 和 `workflow-schema` 要分开

因为它们不是一回事：

- `contracts`
  解决的是前后端接口通信
- `workflow-schema`
  解决的是系统内部的中间表示和执行快照

如果混在一起，后面很容易变成：

- 页面 DTO
- 领域对象
- provider 原始结构

全部搅成一锅。

## 4. Contracts First 应该先定什么

## 4.1 先定 5 组 API，不多做

MVP 第一阶段只建议先定下面 5 组接口：

### A. 项目入口

- `POST /api/projects`
- `GET /api/projects/:projectId`
- `GET /api/projects`

### B. 分析链路

- `POST /api/projects/:projectId/analyze`
- `GET /api/projects/:projectId/analysis`

### C. 工作流

- `GET /api/projects/:projectId/workflow`
- `PATCH /api/projects/:projectId/workflow`

### D. 运行与结果

- `POST /api/projects/:projectId/renders`
- `GET /api/projects/:projectId/runs/:runId`
- `GET /api/projects/:projectId/result`

### E. 历史

- `GET /api/history`

## 4.2 首批必须冻结的 DTO

建议先冻结这些 DTO 名字和边界：

### 项目类

- `CreateProjectRequest`
- `ProjectSummary`
- `ProjectDetailResponse`
- `ProjectListResponse`

### 分析类

- `StartAnalysisRequest`
- `AnalysisRunSummary`
- `AnalysisResultResponse`

### 工作流类

- `WorkflowDraft`
- `UpdateWorkflowDraftRequest`
- `WorkflowDraftResponse`

### 运行类

- `CreateRenderRunRequest`
- `RenderRunSummary`
- `RunStepSummary`
- `RenderRunDetailResponse`

### 结果类

- `OutputAssetSummary`
- `ProjectResultResponse`

## 4.3 哪些先不要定太细

当前先别把这些做太细：

- 计费 DTO
- 团队协作 DTO
- 多 provider 用户侧选择 DTO
- 批量生成 DTO
- 模板市场 DTO

原因很简单：

> 这些都是真的会做，  
> 但不是现在决定系统能不能跑起来的那根主梁。

## 5. workflow-schema 第一版建议

## 5.1 Analysis Output

```json
{
  "sourceSummary": {
    "platform": "douyin",
    "sourceType": "video_url",
    "title": "string"
  },
  "insights": {
    "targetAudience": ["宝妈"],
    "sellingPoints": ["配料干净", "口感清甜"],
    "hooks": ["第一口就记住的梨香"],
    "cta": "放心喝"
  },
  "scriptDraft": {
    "opening": "string",
    "body": ["string"],
    "ending": "string"
  },
  "shotPlan": {
    "segments": []
  }
}
```

## 5.2 Workflow Draft

```json
{
  "meta": {
    "ratio": "9:16",
    "language": "zh-CN",
    "tone": "friendly",
    "style": "clean-realistic"
  },
  "segments": [
    {
      "id": "seg_1",
      "goal": "hook",
      "script": "string",
      "durationSec": 3,
      "shots": []
    }
  ],
  "cta": {
    "text": "string"
  }
}
```

## 5.3 Render Request Snapshot

```json
{
  "projectId": "proj_xxx",
  "workflowVersion": 3,
  "ratio": "9:16",
  "segments": [],
  "voiceover": {
    "enabled": true,
    "voiceStyle": "warm"
  },
  "music": {
    "mode": "auto"
  }
}
```

## 5.4 Run Progress

```json
{
  "runId": "run_xxx",
  "status": "running",
  "currentStep": "analysis.script_generation",
  "steps": [
    {
      "name": "source.download",
      "status": "succeeded"
    },
    {
      "name": "analysis.transcript",
      "status": "running"
    }
  ]
}
```

## 6. Provider Registry 最小落地方案

## 6.1 先注册能力，不注册 UI 选项

首版 registry 只服务后端，不服务用户 UI。

建议先有这 6 类 capability：

- `link_parse`
- `transcript`
- `ocr`
- `analysis`
- `tts`
- `render`

## 6.2 registry 的最小数据结构

```yaml
capabilities:
  link_parse:
    primary: yt_dlp_parser
    fallback: none
  transcript:
    primary: whisper_primary
    fallback: whisper_backup
  ocr:
    primary: vision_ocr_primary
    fallback: none
  analysis:
    primary: llm_analysis_primary
    fallback: llm_analysis_backup
  render:
    primary: render_primary
    fallback: none
```

## 6.3 provider 配置还要带什么

每个 provider 节点至少带下面这些信息：

- `providerId`
- `capability`
- `transport`
- `timeoutSec`
- `retryPolicy`
- `supportsJsonSchema`
- `supportsAsyncJobs`
- `supportsImageInput`
- `enabled`

## 6.4 建议的 Python 侧抽象

```python
from typing import Protocol


class AnalysisProvider(Protocol):
    async def generate_insight(self, request: "AnalysisRequest") -> "AnalysisResult":
        ...


class RenderProvider(Protocol):
    async def submit(self, request: "RenderRequest") -> "RenderSubmission":
        ...

    async def poll(self, external_job_id: str) -> "RenderJobStatus":
        ...
```

## 6.5 Provider Registry 不负责什么

它不负责：

- 页面展示什么模型名
- 用户权限判断
- 商业计费逻辑
- 工作流编排

它只负责：

- 这类能力现在该走谁
- 失败后允不允许 fallback
- 哪些 provider 当前可用

## 7. MVP 推荐的 provider 策略

## 7.1 首版不要做“模型广场”

这条一定要写死：

> MVP 不是给用户选模型的，  
> MVP 是让用户稳定拿到结果的。

所以首版建议：

- 用户侧不展示 provider 品牌
- 用户侧不展示模型列表
- 用户侧只展示“风格、节奏、输出偏好”

## 7.2 首版推荐的真实策略

### 分析侧

- 只保留 `1` 个主分析 provider
- 最多保留 `1` 个 fallback
- transcript / OCR 最好各自也只保留 `1+1`

### render 侧

- 只保留 `1` 条稳定 render 路径
- 如果 fallback 不成熟，宁可先不做 render fallback

大白话：

> 分析侧出错还能重试，  
> render 侧一旦乱切 provider，结果风格和质量可能直接飘。

## 7.3 建议的失败策略

### 可自动 fallback 的

- transcript 超时
- OCR 单次失败
- analysis provider 短暂失败

### 先不自动 fallback 的

- render 风格引擎切换
- TTS 音色系统切换
- 链接解析平台策略切换

因为这些切换很容易导致结果体验断层。

## 8. Phase 0 到 Phase 1 的最小交付清单

## 8.1 Phase 0：骨架搭建

必须交付：

- monorepo 初始化
- `apps/web` 可启动
- `services/api` 可启动
- `services/worker` 可启动
- `packages/contracts` 可生成
- `packages/workflow-schema` 有首版 schema
- Docker Compose 跑起 `postgres + redis + minio`

## 8.2 Phase 0：工程规则

必须交付：

- `.env.example`
- 统一 lint / format
- API 错误码约定
- run/step 状态枚举
- provider registry 配置文件

## 8.3 Phase 1：最短主链

必须交付：

1. 新建项目
2. 提交链接或商品信息
3. 创建分析任务
4. 页面能看到 run step 状态
5. 页面能看到分析结果
6. 页面能看到预填充 workflow draft

注意：

> Phase 1 先不要求真的出视频，  
> 先把“输入 -> 分析 -> workflow draft” 跑通。

这样成功率更高，也更容易验证用户是否真的认可这套入口和承接方式。

## 9. 开发顺序建议

## 9.1 第一周

- 建仓库
- 建 docker
- 建数据库连接
- 建第一版 contracts
- 建 workflow schema

## 9.2 第二周

- 建项目接口
- 建分析任务接口
- 建 run / step 表
- 建最小前端页面骨架

## 9.3 第三周

- 打通分析链路
- 落 analysis output
- 生成 workflow draft
- 前端展示分析页和工作流页

## 9.4 第四周

- 补历史页
- 补错误态
- 补重试
- 再评估是否接 render 第一条链

## 10. 当前最容易犯的错

### 错误 1

一开始就做复杂节点工作流。

后果：

- 开发重
- 用户更懵
- MVP 主链变慢

### 错误 2

接口不先定，前后端各写各的。

后果：

- 页面会很快跑起来
- 但第二周就开始反复返工

### 错误 3

把 provider 细节直接暴露到页面层。

后果：

- UI 复杂
- 用户看不懂
- 后面切 provider 要连 UI 一起改

### 错误 4

把 render 当成 MVP 第一阶段唯一验收点。

后果：

- 很容易被最长、最不稳定的环节拖死

## 11. 最终执行建议

如果现在就开工，我建议真正的开始顺序是：

1. 先建 `packages/contracts`
2. 再建 `packages/workflow-schema`
3. 再建 `services/api` 的项目、分析、workflow 三组接口
4. 再建 `services/worker` 的 analysis pipeline
5. 最后才评估是否把 render 接进第一阶段

一句话收口：

> 先把“结构”和“状态”搭对，  
> 再把“生成能力”接进来。  
> 不然会很快做成一个看起来功能多、实际很难稳定推进的系统。
