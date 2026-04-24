# 全新项目 企业架构定版说明

更新日期：2026-04-24
状态：Active Baseline v0.1

关联文档：

- [全新项目 MVP 定义与 PRD 初稿](./product-mvp-prd.md)
- [全新项目 主链图](./main-flow-diagram.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 Schema 与 Contract 冻结清单](./schema-and-contract-freeze.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 NFR 与 SLO 基线](./nfr-and-slo-baseline.md)
- [全新项目 可观测性与告警基线](./observability-and-alerting-baseline.md)

## 1. 这份文档解决什么问题

这份文档把“技术架构初稿”升级成：

`当前阶段真正拿来施工的正式蓝图。`

小白版解释：

- `technical-architecture-draft.md` 更像“方案讨论稿”
- 这份文档更像“当前这版项目就按这个搭”

如果后续文档和这份文档冲突，当前阶段默认以这份文档为准。

## 2. 当前定版范围

当前只为 MVP 主链定版，不为未来所有扩展定版。

当前唯一主链：

`intake -> analysis -> prefilled workflow -> run -> result -> history`

当前明确不纳入首版定版范围的内容：

- 空白节点工作流画布
- BYOK
- 公开 API
- 团队协作
- 多组织权限
- 全时间线视频编辑器
- 模型市场
- Harness 进入核心产品运行路径

## 3. 架构目标

当前定版要同时满足 5 个目标。

### 3.1 主链可持续往前搭

意思是：

- 后面继续开发时，不需要反复推倒重来

### 3.2 边界稳定

意思是：

- 前端、后端、Worker、供应商适配层各管各的
- 不要今天把逻辑塞进页面，明天再拆出来

### 3.3 长任务可追踪

意思是：

- 用户发起分析或生成后，系统要知道它跑到哪一步
- 不能只有一个“正在处理中”

### 3.4 可维护、可替换

意思是：

- 以后换模型、换供应商、换实现方式，不应该把业务层一起重写

### 3.5 为低代码保留空间

意思是：

- 首版先用结构化 workflow draft
- 不先做复杂节点图
- 但中间表示层要为后续增强留下接口

## 4. 定版结论

当前正式采用下面这套拆法：

- Web：`Next.js`
- API 编排层：`FastAPI`
- 后台任务：`Dramatiq + Redis`
- 数据库：`PostgreSQL`
- 对象存储：`S3-compatible storage`
- 媒体处理与外部调用：`Python workers + provider adapters`
- 合同层：`contracts-first`

一句话版本：

`Web 负责交互壳，API 负责同步编排和领域入口，Worker 负责长任务，Postgres 负责结构化事实，S3 负责中间产物和结果，provider adapter 负责外部能力接入。`

## 5. 系统分层

## 5.1 Web 层

职责：

- 页面路由
- 表单输入
- 主工作台展示
- run 状态与结果展示
- 调用标准化 contract

明确不做：

- 直接持有核心业务状态机
- 直接拼供应商请求
- 直接处理长任务

小白版解释：

- 前端是“控制台和展示层”
- 不是“总后台”

## 5.2 API 层

职责：

- 创建项目
- 校验输入
- 创建和读取领域对象
- 下发长任务
- 返回状态和结果
- 统一输出 API contract

明确不做：

- 把所有长任务同步执行完再返回
- 把供应商细节散落在路由里

## 5.3 Worker 层

职责：

- 链接解析
- 转写 / OCR / 结构分析
- workflow 预填充
- 生成链路
- 落中间产物
- 更新 RunStep 状态

明确不做：

- 直接面向页面提供接口
- 绕过 API 自己定义业务真相

## 5.4 Provider Adapter 层

职责：

- 对接 OpenAI、Anthropic 或未来其他供应商
- 按 capability 暴露能力
- 统一记录 latency、retry、cost、failure

明确不做：

- 直接决定产品流程
- 把厂商细节泄露到 Web 层

小白版解释：

- 这一层像“翻译层”
- 上层只说“我要分析”或“我要生成”
- 这一层再去处理到底找哪家、怎么调

## 5.5 Data 层

职责分两类：

- `PostgreSQL`
  - 保存结构化事实
  - 项目、草稿、run、step、审计元数据都在这里
- `S3-compatible storage`
  - 保存大文件和中间产物
  - 例如视频、预览图、JSON 产物

定版原则：

- `PostgreSQL` 是结构化事实来源
- 大对象不塞进数据库
- run 的状态不能只靠内存

## 6. 当前正式冻结的关键决策

以下内容，当前阶段视为正式冻结。

### 6.1 Contract-first

先定 contract，再接 Web / API / Worker。

原因：

- 避免三边越写越散

### 6.2 长任务异步化

分析、预填 workflow、生成都按异步任务设计。

原因：

- 这类任务天然不稳定、耗时长
- 同步请求会让页面卡死，也很难做重试和状态追踪

### 6.3 Workflow 先用结构化 JSON

首版工作流以 `WorkflowDraft` / `StoryboardDraftSchema` 为核心中间表示。

原因：

- 先把低代码骨架做稳
- 不一上来做复杂节点图

### 6.4 Provider 按能力抽象，不按厂商硬编码

原因：

- 以后换模型时，不要把产品层一起推倒

### 6.5 共享锁定区由主控串行治理

包含：

- `packages/contracts/**`
- `services/api/app/domain/**`
- `services/api/app/providers/interfaces/**`
- `services/api/alembic/**`
- 根配置文件

原因：

- 这些地方一乱，整条主线都容易漂

## 7. 当前版本的质量属性

专业说法：

- `Quality Attributes`

小白版解释：

- 就是这套系统最看重的“工程性格”

当前优先级按顺序是：

1. `主链稳定`
2. `边界稳定`
3. `可维护`
4. `可观测`
5. `成本可控`
6. `性能逐步增强`

这意味着：

- 当前阶段不追求最炫的架构
- 先追求主链跑通、结构不乱、后面好加功能

## 8. 当前阶段明确不追求的东西

当前不把下面这些当首版硬目标：

- 复杂多租户
- 企业 SSO / SCIM
- 大规模多区域部署
- 全自动策略引擎
- 复杂事件总线
- 通用型节点编排平台
- 大而全 DevOps 平台整合

原因很简单：

- 这些都很重要
- 但现在先做，会明显拖慢主链落地

## 9. 组件边界与目录归属

## 9.1 Web

- `apps/web/**`

## 9.2 API

- `services/api/**`

## 9.3 Worker

- `services/worker/**`

## 9.4 Shared contracts

- `packages/contracts/**`
- `packages/workflow-schema/**`

## 9.5 Infra / scripts / docs

- `infra/**`
- `scripts/**`
- `docs/**`

## 10. 决策边界

以下情况必须补 ADR 或更新治理文档后再做：

- 主链改变
- 核心领域对象改名或改语义
- workflow 中间表示层大改
- provider strategy 改成 vendor-specific
- 引入新外部执行平台
- 打开 cloud agent 或未批准 MCP / plugin
- 引入会改变部署模型的基础设施

## 11. 当前架构风险

### 11.1 现在的强项

- 主链清晰
- 共享边界清晰
- 适合继续往下开发

### 11.2 现在的风险

- 观测和告警还没工程化
- NFR 还只是第一版基线
- 权限、审批、环境晋级还没完全平台化
- 真正大并行还没经过多轮实战验证

## 12. 下一阶段的最小技术收口

从这份定版文档往下，下一阶段最应该补的是：

1. 所有权和审批矩阵
2. NFR / SLO 基线
3. 可观测性与告警基线
4. 数据生命周期与环境晋级规则

## 13. 一句话结论

当前企业级架构定版可以概括成：

`以 contracts-first 为骨架，以 Web/API/Worker 分层为主体，以异步长任务和结构化 workflow 为主线，以主控串行治理共享核心区来保证项目长期可维护。`
