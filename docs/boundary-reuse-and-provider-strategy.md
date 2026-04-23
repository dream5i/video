# 全新项目 边界分层、复用策略与模型接口预留

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 MVP 定义与 PRD 初稿](./product-mvp-prd.md)
- [全新项目 信息架构与页面草图](./information-architecture-and-page-wireframes.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 实施底座方案：仓库结构、Contracts First 与 Provider Registry](./implementation-foundation-plan.md)

## 1. 这份文档解决什么问题

在真正开始搭项目之前，最容易踩坑的不是“技术不会”，而是边界没分清、复用判断失误、接口预留不统一。

这份文档专门回答下面几个问题：

1. 我们的项目边界到底怎么分层。
2. 参考过的这些项目里，哪些只能借鉴产品思路，哪些可以部分复用，哪些不应该直接引入。
3. 哪些能力必须自研，哪些适合基于开源工具或外部服务封装。
4. 模型和供应商接口应该如何预留，才能支持后面换模型、加模型、做 fallback，而不推翻主架构。

## 2. 先给结论

如果先给一个非常明确的结论，我会这么定：

### 2.1 必须自研的部分

- 产品体验层
- 项目、分析、工作流、结果的领域模型
- `storyboard draft` 中间表示
- 任务状态机与步骤追踪
- Provider adapter 抽象层
- 项目历史、版本、重试和可回溯机制

### 2.2 可以复用的部分

- `yt-dlp / FFmpeg / transcript / OCR` 这一类底层工具能力
- OpenShorts 这类 MIT 项目的局部实现思路和部分模块模式
- ComfyUI / OpenMontage 的工作流与管线思想
- Vinci Clips 的 API 拆法和“上传 -> transcript -> clip”链路结构思路

### 2.3 不建议直接拿来当项目骨架的部分

- `ComfyUI` 整体代码
- `OpenMontage` 整体代码
- `Vinci Clips` 整体代码
- 商业闭源产品的任何实现细节假设

原因很简单：

- 有些项目许可证不适合直接嵌入
- 有些项目的产品目标和我们并不完全一致
- 有些项目适合做“侧车服务”或“灵感来源”，但不适合当核心业务骨架

## 3. 项目边界分层

我建议把 `全新项目` 明确拆成 6 层。

### 3.1 产品体验层

包含：

- 首页工作台
- 分析页
- 工作流页
- 运行状态页
- 结果页
- 历史页

这层的职责是：

- 让用户知道现在在做什么
- 让用户知道下一步是什么
- 降低认知负担

这层必须自研，不能依赖外部项目。

原因：

- 这是我们和竞品真正拉开体验差异的地方
- 这里决定了用户是否会像在 `SoraTK` 一样被空白画布劝退

### 3.2 领域与编排层

包含：

- Project
- AnalysisRun
- WorkflowDraft
- RenderRun
- RunStep
- 历史与版本

这层的职责是：

- 决定系统如何理解一次创作流程
- 定义什么叫分析、什么叫工作流、什么叫结果
- 把所有异步长任务组织成可回溯主链路

这层也必须自研。

原因：

- 这是产品的业务内核
- 也是后续做批量、多版本、多模型和计费的基础

### 3.3 中间表示层

包含：

- `storyboard draft JSON`
- analysis output schema
- insight schema
- shot plan schema
- render request schema

这层的职责是：

- 对内统一结构
- 对前端统一编辑模型
- 对后端统一执行快照
- 对外部模型做隔离

这层必须自研，而且要尽早定。

原因：

- 如果没有统一 schema，后面每加一个模型都会把系统搅乱

### 3.4 Provider Adapter 层

包含：

- link parser adapter
- transcript adapter
- OCR adapter
- analysis LLM adapter
- render adapter
- TTS adapter

这层的职责是：

- 把外部能力转换成统一输入输出
- 隔离供应商变化
- 支持 fallback 和灰度切换

这层要自研“接口”，但底层能力可以复用外部工具和服务。

### 3.5 媒体与 AI 执行层

包含：

- 下载
- 抽帧
- 抽音频
- OCR
- transcript
- 合成
- 转码
- 视频生成

这层的职责是：

- 执行真正耗时的媒体和 AI 任务

这层最适合“组合式复用”：

- 不要自己从零发明 FFmpeg
- 不要自己从零造 transcript engine
- 但要自己做编排、封装和状态记录

### 3.6 基础设施层

包含：

- Postgres
- Redis
- S3-compatible storage
- 日志、监控、任务队列

这层直接用成熟基础设施，不需要自造轮子。

## 4. 参考项目复用判定

这一节不只说“能不能参考”，而是给出更实际的判定：

- `直接复用代码`
- `局部复用思路`
- `作为独立侧车集成`
- `只做灵感参考`

### 4.1 商业产品

### SoraTK

定位：

- 实测竞品

可复用性判断：

- `产品思路可复用`
- `代码不可复用`
- `流程结构值得借鉴`

建议借鉴：

- 去水印 / 链接解析作为入口
- 爆款复刻作为高价值分析环节
- 工作流承接复杂生产链路

不建议直接照抄：

- 空白画布式承接
- 首页 CTA 与实际动作不一致

### Creatify / HeyGen / Arcads

定位：

- 商业闭源产品

可复用性判断：

- `只能复用产品结构思路`
- `不能复用代码`

建议借鉴：

- `Creatify`
  借鉴 `URL -> 广告视频` 和批量变体思路
- `HeyGen`
  借鉴 `URL -> 视频`、批量和 API 自动化思路
- `Arcads`
  借鉴 `AI UGC / 角色资产 / 多语言本地化` 方向

### 4.2 开源项目

### OpenShorts

当前公开信息显示：

- `MIT license`
- 技术栈是 `Python 3.11 + FastAPI + React + Vite + Tailwind`
- 使用 `yt-dlp / faster-whisper / FFmpeg / Gemini / fal.ai / ElevenLabs`

可复用性判断：

- `可以局部复用`
- `可以参考它的技术组合`
- `不建议整个仓库直接作为骨架复制`

适合复用的内容：

- 技术路线
- AI Shorts 管线拆法
- Docker 化本地开发思路
- 媒体处理和 AI 服务拼接方式

适合参考但不建议直接复制的内容：

- 整个 dashboard 结构
- 多工具并列的一体化产品形态
- 直接把客户端存 API key 的做法

我的判断：

`OpenShorts` 是目前最适合拿来做“局部实现参考”的开源项目。

也就是说：

- 可以借它的 pipeline 设计
- 可以借它的工具选型
- 可以借它的一些模块组织方式
- 但不能让我们的核心领域模型围着它转

### ComfyUI

当前公开信息显示：

- `GPL-3.0 license`
- 它是 `graph/nodes/flowchart` 的可视化 AI 引擎

可复用性判断：

- `不建议直接嵌入核心代码`
- `适合做灵感参考`
- `未来可以作为独立外部服务集成`

原因：

- 它非常强，但它的主场是图形化模型工作流，不是我们的电商短视频主业务
- GPL 许可证使得直接代码级复用需要非常谨慎
- 首版如果把 ComfyUI 拉进核心，会把产品带向“先做节点系统”而不是“先做主链路”

我的建议：

- 首版不要把 `ComfyUI` 当骨架
- 如果后续要支持更复杂的视觉生成流程，可以考虑把它作为独立 sidecar service，通过 adapter 调用

### OpenMontage

当前公开信息显示：

- `AGPL-3.0 license`
- 架构强调 `tools + pipeline_defs + skills + schemas + remotion-composer`

可复用性判断：

- `不建议直接复用代码`
- `非常值得复用架构思想`

最值得学的不是代码，而是这几个概念：

- pipeline manifests
- skills / playbooks
- schemas contract
- render 前后验证

我的建议：

- 借鉴它的“声明式 pipeline + schema contract + 质量门”思想
- 不要把它整个拉进我们的服务层

### Vinci Clips

当前公开信息显示：

- `AGPL-3.0 license`
- 结构比较清楚：`backend + frontend`
- API 也很简单直接：上传、查 transcript、生成 clip

可复用性判断：

- `可以借鉴 API 拆法和开发形态`
- `不建议直接复用代码`

原因：

- 许可证同样需要谨慎
- 它的核心问题是“长视频切片”，与我们的“爆款分析 -> 工作流 -> 生成”主链路并不完全同构

我的建议：

- 借鉴它的项目拆分方式和最小 API 路径
- 不要把它当成业务骨架

## 5. 最终复用矩阵

| 参考对象 | 许可证 / 性质 | 能否直接复用代码 | 适合复用什么 | 最终判定 |
| --- | --- | --- | --- | --- |
| SoraTK | 商业闭源 | 否 | 产品流程、用户路径、问题清单 | 只借鉴产品 |
| Creatify | 商业闭源 | 否 | URL-to-Video、Batch、API 方向 | 只借鉴产品 |
| HeyGen | 商业闭源 | 否 | URL-to-Video、批量和本地化思路 | 只借鉴产品 |
| Arcads | 商业闭源 | 否 | AI UGC、角色资产、多语言方向 | 只借鉴产品 |
| OpenShorts | MIT | 有条件地少量可行 | pipeline 设计、技术栈、局部实现思路 | 局部复用 |
| ComfyUI | GPL-3.0 | 不建议 | 节点与工作流思想、独立 sidecar 可能性 | 思想参考 / 侧车候选 |
| OpenMontage | AGPL-3.0 | 不建议 | 声明式 pipeline、schema、质量门 | 架构参考 |
| Vinci Clips | AGPL-3.0 | 不建议 | 最小 API 路径、前后端拆法 | 结构参考 |

说明：

这里的许可证判断只是工程决策建议，不是正式法律意见。如果后面要做商业化分发，涉及 GPL / AGPL 的代码级复用，最好单独做许可证审查。

## 6. 哪些必须自己开发

以下能力我建议明确归为“核心自研”。

### 6.1 Storyboard Draft Schema

这是我们的核心内部语言，必须自己定。

原因：

- 前端工作流依赖它
- 生成链路依赖它
- 历史回溯依赖它
- 未来接更多模型也依赖它

### 6.2 项目与 Run 状态机

必须自己做：

- 项目阶段
- 分析 run
- render run
- step 级状态
- 重试与回放

原因：

- 这是可观测性和用户信任的基础

### 6.3 工作流编辑体验

必须自己做：

- 脚本卡片
- 镜头卡片
- 风格设置
- 版本保存

原因：

- 这是用户真正感知“好不好用”的地方

### 6.4 Provider Adapter 抽象

必须自己做：

- 统一请求格式
- 统一响应格式
- provider registry
- fallback 规则

原因：

- 这是系统长期稳定性的底座

### 6.5 领域级 Prompt / Planning 逻辑

虽然底层模型可以换，但下面这些逻辑最好自己掌握：

- 爆款分析 prompt 模板
- 卖点提炼规则
- 脚本生成框架
- 镜头规划框架

原因：

- 这部分才是业务 know-how
- 也是将来效果迭代最关键的杠杆

## 7. 哪些适合基于现成工具封装

### 7.1 链接解析与下载

适合：

- 复用成熟下载器和解析工具
- 自己包一层 `link_parser_adapter`

不要做：

- 自己从零写各个平台下载器

### 7.2 Transcript

适合：

- 接 Whisper 系列或外部 transcript provider
- 自己统一 timestamps、speaker、language 结构

不要做：

- 把 transcript provider 的原始输出直接透给业务层

### 7.3 OCR

适合：

- 接现成 OCR 服务或模型
- 自己统一 frame_text schema

### 7.4 视频处理

适合：

- 复用 FFmpeg
- 自己封装任务步骤、参数和存储路径

不要做：

- 自己重造媒体处理底座

### 7.5 Render

适合：

- 首版先接 1 条稳定 render 路径
- 把它包成 `render_adapter`

不要做：

- 一上来支持一堆用户可选模型

## 8. 模型接口怎么预留

这里是这份文档最关键的一节。

我的建议是：

### 8.1 不按“厂商”抽象，按“能力”抽象

不要写成：

- OpenAIAdapter
- GeminiAdapter
- FalAdapter

然后让业务层直接依赖这些名字。

应该写成：

- `TranscriptProvider`
- `OCRProvider`
- `InsightProvider`
- `ScriptProvider`
- `ShotPlanProvider`
- `TTSProvider`
- `RenderProvider`

也就是说，业务层只知道“我要这种能力”，不知道具体是哪个厂商。

### 8.2 建一个统一的请求信封

建议所有模型型调用都走统一 envelope：

```json
{
  "requestId": "req_xxx",
  "projectId": "proj_xxx",
  "runId": "run_xxx",
  "capability": "insight_generation",
  "provider": "primary",
  "model": "default",
  "locale": "zh-CN",
  "inputs": {},
  "constraints": {},
  "fallbackPolicy": {
    "allowed": true,
    "maxAttempts": 2
  },
  "metadata": {}
}
```

这样做的好处：

- 页面层永远不需要知道供应商细节
- 后面加 provider 很轻
- 可以统一记录日志、成本和失败原因

### 8.3 统一响应结构

建议所有 provider 返回统一结果：

```json
{
  "status": "succeeded",
  "provider": "xxx",
  "model": "xxx",
  "usage": {
    "inputTokens": 0,
    "outputTokens": 0,
    "estimatedCostUsd": 0
  },
  "output": {},
  "artifacts": [],
  "trace": {
    "latencyMs": 0
  },
  "error": null
}
```

### 8.4 业务层只消费“标准化输出”

例如：

- transcript 统一成 `segments[]`
- OCR 统一成 `frameTexts[]`
- insight 统一成 `angles[] / hooks[] / cta`
- shot plan 统一成 `segments[] / shots[]`

不要让前端或领域层直接吃 provider 原始 JSON。

### 8.5 Provider Registry

建议内部保留一个 provider registry 配置层。

例如：

```text
capability: transcript
  primary: whisper_local
  fallback: cloud_transcript_a

capability: analysis
  primary: llm_a
  fallback: llm_b

capability: render
  primary: render_path_a
  fallback: disabled
```

这样后面切换供应商，不需要改业务代码。

### 8.6 预留“特性能力”而不是只预留模型名

建议每个 provider 声明 capability flags，例如：

- supports_image_input
- supports_json_schema
- supports_streaming
- supports_long_context
- supports_async_jobs
- supports_webhook
- supports_voice_clone

原因：

- 后面做策略路由时，不会只靠字符串判断模型

### 8.7 不把供应商选择暴露给 MVP 用户

MVP 阶段建议：

- 页面不展示模型下拉
- 页面不展示 provider 品牌
- 页面只展示用户能理解的“风格 / 速度 / 结果偏好”

技术上可以预留 provider，但产品上不要先暴露。

## 9. 推荐的代码抽象方式

### 9.1 Python 侧接口

建议以 protocol 或 abstract base class 定义能力接口：

```python
from typing import Protocol


class InsightProvider(Protocol):
    async def generate(self, request: "InsightRequest") -> "InsightResult":
        ...


class RenderProvider(Protocol):
    async def submit(self, request: "RenderRequest") -> "RenderSubmission":
        ...

    async def poll(self, run_id: str) -> "RenderStatus":
        ...
```

### 9.2 Domain Service 侧调用

Domain service 不直接 import 某个厂商实现，而是依赖 registry：

```python
provider = provider_registry.get_insight_provider()
result = await provider.generate(request)
```

### 9.3 前端侧

前端只认 API contract：

- analysis result
- workflow draft
- render run
- output asset

前端不认 provider response。

## 10. 现在就应该预留的扩展点

### 10.1 输入扩展点

当前：

- 短视频链接
- 商品信息

未来可加：

- 商品 URL
- 图片包
- 竞品视频合集

### 10.2 分析扩展点

当前：

- transcript
- OCR
- insight

未来可加：

- 评论区分析
- 品类知识库增强
- 多视频对比分析

### 10.3 生成扩展点

当前：

- 单一路径 render

未来可加：

- UGC avatar 模式
- 图像生成镜头模式
- 模板化成片模式

### 10.4 平台扩展点

未来可加：

- batch generation
- team workspace
- billing / quota
- API

## 11. 最终判定

如果把这次判断浓缩成一句真正能指导搭建的话，就是：

`把产品内核、领域模型、状态机和 provider 抽象牢牢抓在自己手里，把底层媒体和模型能力尽量做成可替换的外部执行层。`

进一步展开就是：

- 页面体验自己做
- 业务对象自己定
- schema 自己定
- run 状态自己控
- adapter 自己写
- 底层工具尽量复用
- 对 GPL / AGPL 项目只借鉴思想，不轻易直接嵌入
- 对 MIT 项目可以有选择地吸收实现方式，但不要让项目骨架被外部项目反向定义

## 12. 下一步建议

基于这份文档，最适合立刻推进的事情是：

1. 建仓库骨架
2. 先把 `packages/contracts` 和 `services/api` 的 schema 定下来
3. 先定义 provider registry 与 adapter interface
