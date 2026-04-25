# 全新项目 可观测性与告警基线

更新日期：2026-04-25
状态：Active Baseline v0.1

关联文档：

- [全新项目 企业架构定版说明](./enterprise-architecture-spec.md)
- [全新项目 NFR 与 SLO 基线](./nfr-and-slo-baseline.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 企业级 AI 就绪度评估](./enterprise-ai-readiness-assessment.md)

## 1. 这份文档解决什么问题

这份文档回答的是：

`系统出问题时，我们应该看见什么、先看哪里、什么时候要告警。`

专业说法：

- `Observability`
  - 可观测性

小白版解释：

- 不是只写日志
- 而是要让系统“出了问题能被看懂”

## 2. 当前原则

当前先坚持 5 条原则。

1. 每个请求、每个 run、每个 step 都要能被串起来
2. 长任务必须有状态、时间戳和错误分类
3. 外部 provider 不能是黑盒
4. 日志、指标、trace 里不允许裸奔敏感信息
5. 告警要能指向可处理的问题，不能只会吵

## 2.1 当前已落地的第一批接线

截至 `2026-04-24`，代码里已经接上的最小可观测性能力包括：

- API 中间件会生成并回传 `x-request-id` / `x-trace-id`
- API 错误返回已统一包含 `message` / `errorCode` / `requestId` / `traceId`
- render run 的创建、完成、失败和 step 快照已有结构化日志
- integration 测试已经覆盖关键响应头和错误契约

截至 `2026-04-25`，第二批“内部可视化接线”已经落下：

- 新增 `GET /api/observability/summary`
- 新增共享 contract：`ObservabilitySummaryResponse`
- 新增前端页面：`/observability`
- 页面已展示主链健康、异步任务、provider、失败热点和接线状态信号
- integration 测试已覆盖可观测性汇总接口和响应头

小白版解释：

- 这相当于我们先把“每个工单的编号”和“出错时的统一报错格式”接上了
- 这样后面排查问题，不至于每次都像在黑屋里摸
- 现在又加了一块“内部仪表盘”，不用先上外部平台，也能看见主链是否健康

当前还没完成的部分：

- worker / provider 侧 trace 还没完全打通
- 外部 metrics / alerting 平台还没接上
- 还没有做真正的告警演练

## 3. 必须统一的追踪字段

以下字段，当前建议作为最小统一基线：

- `request_id`
- `trace_id`
- `project_id`
- `analysis_run_id`
- `workflow_draft_id`
- `render_run_id`
- `run_step_id`
- `provider`
- `capability`
- `model_name`
- `status`
- `latency_ms`
- `retry_count`
- `estimated_cost`
- `error_code`

小白版解释：

- 后面不管你在页面、API、Worker、日志平台里看，都要能靠这些编号把一整条链串起来

## 4. 必做日志

## 4.1 Web 层

至少记录：

- 页面关键动作提交
- 页面关键失败
- 用户看到的主状态变化

不记录：

- 敏感原文
- 密钥
- 大段未脱敏外部文本

## 4.2 API 层

至少记录：

- 请求进入和结束
- 关键参数摘要
- 领域对象创建
- 任务下发结果
- 错误分类

## 4.3 Worker 层

至少记录：

- 任务开始
- 任务结束
- 步骤开始和结束
- 重试
- 降级
- provider 调用结果摘要

## 4.4 安全与治理事件

至少记录：

- 高风险改动触发
- migration 执行
- retention / deletion 执行
- 配置变更
- 人工审批或阻断

## 5. 必做指标

当前至少要有下面这些指标。

### 5.1 产品主链指标

- 新建项目成功率
- 分析任务成功率
- 从分析进入 workflow 的成功率
- 生成任务成功率
- 历史页可读取率

### 5.2 性能指标

- API 请求延迟
- 长任务总耗时
- 每个 step 耗时
- 队列等待时间
- 状态刷新延迟

### 5.3 稳定性指标

- 5xx 错误率
- worker 失败率
- provider 失败率
- retry 次数
- stuck run 数

### 5.4 成本指标

- 每 provider 调用量
- 每 provider 估算成本
- 每 run 估算成本
- 失败后重复消耗量

## 6. 必做 trace

当前最小 trace 要覆盖下面 4 段。

1. 页面发起请求
2. API 创建或读取领域对象
3. Worker 执行各步骤
4. Provider adapter 调外部能力

也就是说，后面排查问题时，至少要能回答：

- 问题发生在页面、API、Worker 还是 provider
- 卡在第几步
- 花了多久
- 是否重试过

## 7. 必做错误分层

当前统一使用下列错误大类：

- `USER_INPUT_ERROR`
- `SOURCE_PARSE_ERROR`
- `TRANSCRIPT_ERROR`
- `OCR_ERROR`
- `ANALYSIS_ERROR`
- `WORKFLOW_ERROR`
- `RENDER_ERROR`
- `STORAGE_ERROR`
- `QUEUE_ERROR`
- `INTERNAL_ERROR`

规则：

- 页面可以展示更友好的文案
- 但底层日志和事件里必须保留统一错误码

## 8. 当前阶段最小仪表盘

专业说法：

- `Dashboard`

小白版解释：

- 就是不同角色最常看的“总览面板”

当前至少规划 4 张；截至 `2026-04-25`，内部页面 `/observability` 已先覆盖前三类的最小版本。

### 8.1 主链健康面板

看什么：

- 新建项目成功率
- 分析成功率
- 生成成功率
- 当前失败热点

当前内部页面已覆盖：

- 项目总数
- analysis 成功率
- render 成功率
- workflow draft 数
- result asset 数
- 最近失败列表

### 8.2 异步任务面板

看什么：

- queue depth
- 当前活跃 run
- stuck run
- retry 分布

当前内部页面已覆盖：

- queued run
- running run
- active run
- stuck run 占位
- 最近运行更新时间

### 8.3 Provider 面板

看什么：

- 各 provider 延迟
- 各 provider 错误率
- fallback 触发情况
- 单次 run 成本异常

当前内部页面已覆盖：

- provider 调用量
- provider 成功 / 失败量
- 平均延迟占位或计算值
- 估算成本
- 最近事件时间

### 8.4 发布与风险面板

看什么：

- 最近部署后错误率变化
- migration 执行结果
- 高风险改动是否带 review pass

## 9. 当前阶段最小告警规则

下面这些告警，当前阶段建议优先实现。

### 9.1 同步接口异常

触发建议：

- `5xx` 错误率连续 `10` 分钟高于 `5%`

### 9.2 主链失败率异常

触发建议：

- 分析或生成在滚动 `30` 分钟窗口里失败率高于 `20%`
- 且样本数不少于 `10`

### 9.3 队列积压

触发建议：

- queue wait time 连续 `10` 分钟高于 `60s`

### 9.4 任务卡死

触发建议：

- analysis run `10` 分钟没有步骤更新时间
- render run `60` 分钟没有步骤更新时间

### 9.5 migration 异常

触发建议：

- 部署后出现 migration 失败，立即告警

### 9.6 成本异常

触发建议：

- 单次 run 估算成本超过预设上限
- 或单日成本显著偏离过去基线

## 10. 日志与 trace 脱敏规则

当前硬规则：

1. 不记录 secrets、token、私钥
2. 不记录未经脱敏的生产数据
3. 不把外部原文整段打进日志
4. stack trace 如涉及敏感字段，必须脱敏
5. provider raw response 不默认全量持久化

小白版解释：

- 监控是为了排查问题
- 不是把敏感信息又复制一份到别处

## 11. 当前阶段的实现优先级

### 第一层：先必须有

- `request_id`
- `trace_id`
- `project_id`
- `run_id`
- `step_id`
- 统一错误码
- 基础请求日志
- step 状态变更日志

### 第二层：主链稳定后补

- provider 调用指标
- retry / fallback 指标
- run 成本指标
- stuck run 告警
- 内部 dashboard 数据接口和页面持续完善

### 第三层：进入更正式交付前补

- 外部 observability 平台集成
- 审计事件统一导出
- 告警分级和值班升级链

## 12. 一句话结论

当前可观测性基线的目标不是“把所有监控平台一次建完”，而是先定住下面这件事：

`以后任何一次主链失败，至少都要能回答它失败在哪一层、哪一步、用了哪个 provider、重试了几次、花了多久。`
