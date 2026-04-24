# 全新项目 前端壳复用清单

更新日期：2026-04-24
状态：Active

关联文档：

- [全新项目 信息架构与页面草图](./information-architecture-and-page-wireframes.md)
- [全新项目 技术方案与系统架构初稿](./technical-architecture-draft.md)
- [全新项目 边界分层、复用策略与模型接口预留](./boundary-reuse-and-provider-strategy.md)
- [全新项目 实施路线图](./implementation-roadmap.md)

## 1. 这份文档解决什么问题

这份文档不是讨论“GitHub 上有没有好看的模板”。

它只解决一件事：

`我们现在能不能借别人的前端壳，以及借哪一层最划算。`

小白版解释：

- “前端壳”就是页面骨架
- 例如侧边栏、头部、卡片区、表格区、筛选区、表单区
- 它不是我们的业务主链本身

所以这份清单的重点不是“整套拿来”，而是：

`哪些部分直接借，哪些只参考，哪些现在不要碰。`

## 2. 先给结论

当前建议采用：

`借壳，不换骨架；借布局，不借业务；借组件，不借整套产品逻辑。`

更直白一点：

1. 我们可以复用 GitHub 上成熟的 dashboard 壳和组件层。
2. 但不能把别人的 SaaS、聊天产品、权限系统整套搬进来。
3. 我们当前最该复用的是：
   - dashboard 布局
   - 表格与筛选
   - 组件系统
   - 后续低代码图编辑底座
4. 我们当前不该复用的是：
   - 别人现成的 auth / billing / team / RBAC 整体方案
   - chat-first 的产品壳
   - 与我们主链不一致的业务页面结构

## 3. 选壳标准

当前我用 5 条标准来判断一个仓库值不值得借。

### 3.1 许可证要清楚

优先：

- MIT

原因很简单：

- 企业项目里，许可证不清楚，后面会很麻烦
- MIT 最省心，复用成本最低

### 3.2 技术栈要接近我们

优先：

- Next.js
- React
- TypeScript
- shadcn/ui
- TanStack Table

原因：

- 技术越接近，我们越像是在“搬砖”
- 技术越不接近，我们越像是在“拆房重建”

### 3.3 复用层级要清楚

优先复用：

- layout
- UI blocks
- table/filter
- graph editor shell

谨慎复用：

- auth
- billing
- team workspace
- data model

### 3.4 不能破坏当前主链

当前唯一主链仍然是：

`输入 -> 分析 -> 预填充工作流 -> 运行 -> 结果 -> 历史`

如果一个模板会把页面结构带成：

- 聊天优先
- 空白画布优先
- 组织管理优先
- 营销站优先

那它就不适合作为我们的主壳。

### 3.5 要有明确“借用价值”

如果一个仓库只是“看起来很漂亮”，但不能帮我们减少下面这些工作，就不值得借：

- 布局搭建
- 组件统一
- 表格筛选
- 工作台分区
- 低代码图编辑

## 4. 当前推荐清单

## 4.1 一级推荐：直接纳入复用池

### A. `shadcn-ui/ui`

仓库：

- https://github.com/shadcn-ui/ui

判断：

- 可以直接借

为什么能借：

- MIT
- 它不是一个重业务模板，而是组件底座
- 非常适合做我们自己的长期 UI 基础层

建议借什么：

- button
- dialog
- sheet
- tabs
- dropdown
- table
- form
- badge
- card
- toast

不建议直接借什么：

- 文档里的整套展示页面结构

适合落到我们哪里：

- `apps/web/components/ui/**`
- `apps/web/components/shared/**`

小白版解释：

- 这套东西更像“标准零件库”
- 它不是现成房子，但很适合当我们自己的统一装修材料

### B. `Kiranism/next-shadcn-dashboard-starter`

仓库：

- https://github.com/Kiranism/next-shadcn-dashboard-starter

判断：

- 适合借 dashboard 壳

为什么能借：

- MIT
- Next.js 16 + TypeScript + shadcn/ui
- 自带 sidebar、header、content area、表格、表单、cards

建议借什么：

- 控制台总体布局
- 左侧导航结构
- 顶部信息条
- dashboard 卡片区组织方式
- 页面分区方式

不建议直接借什么：

- Clerk auth
- Organizations
- Billing
- RBAC 导航逻辑

适合落到我们哪里：

- `apps/web/app/layout.tsx`
- `apps/web/app/globals.css`
- `apps/web/components/layout/**`

主控判断：

- 这是当前最像“能借来做工作台外壳”的仓库
- 但只能借壳，不应该整仓 fork 进来

### C. `openstatushq/data-table-filters`

仓库：

- https://github.com/openstatushq/data-table-filters

文档：

- https://data-table.openstatus.dev/docs/quick-start

判断：

- 适合借历史页和运行记录表格能力

为什么能借：

- 它就是专门解决 data table + filters 的
- 很适合我们的 `history`、`run list`、后续审计列表
- 还支持通过 shadcn CLI 安装 block

建议借什么：

- 列表表格骨架
- filter bar
- search
- pagination
- column schema 组织方式

不建议现在借什么：

- AI filter command
- MCP server
- 过重的数据层耦合

适合落到我们哪里：

- `apps/web/app/history/**`
- `apps/web/components/history/**`
- `apps/web/components/data-table/**`

小白版解释：

- 这不是整个工作台模板
- 它更像“高级表格发动机”

### D. `xyflow/xyflow`

仓库：

- https://github.com/xyflow/xyflow

说明页：

- https://xyflow.com/open-source

判断：

- 适合做后续低代码 graph 编辑底座

为什么能借：

- MIT
- 它就是 node-based UI 的成熟开源底座
- 和我们未来的 workflow graph 很匹配

建议借什么：

- graph canvas
- node / edge 基础交互
- viewport、selection、drag
- graph 状态管理思路

不建议现在就借什么：

- 全量拖拽编辑器能力
- 一上来就做复杂节点编排

适合落到我们哪里：

- 后续新增：
  - `apps/web/components/workflow-graph/**`

主控判断：

- 现在先记入“后续确定复用池”
- 不建议在当前运行态收口阶段就引入

## 4.2 二级推荐：可参考，但不作为当前主壳

### E. `nextjs/saas-starter`

仓库：

- https://github.com/nextjs/saas-starter

判断：

- 只适合参考，不适合整套复用

为什么：

- MIT
- 官方系质量不错
- 但它偏 SaaS 业务框架
- 自带 auth、Stripe、team、RBAC、数据库迁移

建议借什么：

- App Router 组织方式
- dashboard 页面拆分思路
- settings / account 这类标准后台页组织方式

不建议直接借什么：

- Postgres + Stripe + auth 整套业务结构
- 它的用户 / 团队 / 计费模型

主控判断：

- 它更像“参考书”
- 不是我们当前阶段该拿来套壳的东西

### F. `shadcnstore/shadcn-dashboard-landing-template`

仓库：

- https://github.com/shadcnstore/shadcn-dashboard-landing-template

判断：

- 适合借视觉层和 marketing/dashboard 分区思路

为什么：

- MIT
- 视觉完成度高
- 适合拿来补强卡片、着陆页、后台视觉表现

建议借什么：

- dashboard 页面排版
- landing 与 dashboard 的视觉分区
- card 和 block 的组合方式

不建议直接借什么：

- 整站样式强行整体复制
- 与我们当前信息架构不匹配的页面模块

主控判断：

- 可作为“视觉灵感仓库”
- 优先级低于 `shadcn-ui/ui` 和 `Kiranism`

## 4.3 当前不推荐作为主壳的方向

### G. 聊天类壳

典型方向：

- Chat-first AI UI

当前不建议原因：

- 它会把主入口带向“聊天”
- 但我们当前产品主链不是聊天主链，而是项目主链

小白版解释：

- 我们现在要做的是“项目工作台”
- 不是“先聊天，再顺手做项目”

## 5. 最终复用结论

当前建议形成下面这套组合。

### 5.1 现在就复用

1. `shadcn-ui/ui`
2. `Kiranism/next-shadcn-dashboard-starter`
3. `openstatushq/data-table-filters`

### 5.2 下一阶段再复用

4. `xyflow/xyflow`

### 5.3 只参考，不整套引入

5. `nextjs/saas-starter`
6. `shadcnstore/shadcn-dashboard-landing-template`

一句话版本：

`组件层用 shadcn，工作台壳借 Kiranism，列表层借 OpenStatus，图编辑底座未来接 xyflow。`

## 6. 落到我们项目里，具体怎么借

## 6.1 第一批直接可做

目标：

- 先把工作台“看起来更像企业级后台”

建议动作：

1. 重构 `apps/web/app/layout.tsx`
   - 引入更稳定的 sidebar + topbar 结构
2. 拆 `apps/web/app/projects/[projectId]/page.tsx`
   - 把页面拆成 snapshot / analysis / workflow / run-result / history 几块组件
3. 重构 `apps/web/app/history/page.tsx`
   - 用 data-table 方案替换当前简单历史列表
4. 补 `apps/web/components/ui/**`
   - 把常用 card / badge / toolbar / table 区块统一下来

## 6.2 第二批再做

目标：

- 把视觉和交互拉齐，但不碰主链逻辑

建议动作：

1. 统一页面工具栏
2. 统一筛选栏和状态条
3. 统一详情页分栏和 tabs
4. 统一空状态 / 错误状态 / loading 状态

## 6.3 第三批才做

目标：

- 引入 workflow graph 真实编辑壳

建议动作：

1. 引入 `xyflow/xyflow`
2. 先只渲染 graph，不开放复杂编辑
3. 等 contract 稳定后再做节点编辑器

## 7. 明确禁止事项

为了避免后面“借着借着把项目借歪”，这里把禁止事项写死。

### 7.1 不整仓 fork 进主线

原因：

- 后续很难维护
- 很难知道哪些是我们自己的代码
- 升级成本会越来越高

### 7.2 不把 auth / billing / team 先带进来

原因：

- 当前 MVP 主链不需要
- 会稀释主链开发资源

### 7.3 不为了图编辑器提前引入复杂前端状态

原因：

- 现在主链重点不是空白编辑器
- 是把现有工作台主链做稳

### 7.4 不让视觉壳反过来决定业务结构

原因：

- 壳应该服务主链
- 不能让“模板长什么样”来决定“我们产品该怎么走”

## 8. 主控建议

如果按企业级最稳的方式推进，我建议下一步不要直接大面积改 UI。

而是按下面顺序推进：

1. 先做 layout 壳升级
2. 再做 history 表格升级
3. 再做项目页区块组件化
4. 最后才接 workflow graph 壳

这样做的好处是：

- 每一步都能独立验收
- 不会因为一次换壳把主链打断
- 后续并行时也更容易切 lane

## 9. 当前最终结论

当前 GitHub 上确实有可复用的前端壳。

但对我们来说，正确做法不是：

`找一个最像的模板，整套搬过来`

而是：

`按层借用最合适的开源底座，再把我们的主链工作台自己收口起来`

这才是企业级项目最稳的复用方式。

## 10. 参考来源

本清单基于 2026-04-24 检查的公开仓库与文档整理：

- https://github.com/shadcn-ui/ui
- https://github.com/Kiranism/next-shadcn-dashboard-starter
- https://github.com/openstatushq/data-table-filters
- https://data-table.openstatus.dev/docs/quick-start
- https://github.com/xyflow/xyflow
- https://xyflow.com/open-source
- https://github.com/nextjs/saas-starter
- https://github.com/shadcnstore/shadcn-dashboard-landing-template
