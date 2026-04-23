# 全新项目 第一次真实并行演练执行包

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 Worktree 与分支治理手册](./worktree-and-branching-runbook.md)
- [全新项目 大并行与上线门槛](./parallel-and-launch-gates.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)

## 1. 这份文档解决什么问题

这份文档不讲长期原则，只讲：

`第一次真实 worktree 并行演练，到底怎么开始。`

你可以把它理解成一份施工演练单：

- 先检查能不能开工
- 再明确每条线谁干什么
- 最后规定怎么收口

## 2. 先给结论

当前不需要你再补产品资料。

真正开始第一次并行演练前，只需要确认一件事：

`是否先打一个干净的 checkpoint commit。`

原因很简单：

- `git worktree` 是从一个提交点分叉出去的
- 它不会自动带上当前工作区里还没提交的改动
- 如果在脏工作区直接开 worktree，子树会站在旧地基上

小白版解释：

- worktree 像是从“某个存档点”复制出三条施工线
- 不是从“你当前还没存档的桌面状态”复制

## 3. 本次演练的目标

这次演练不是为了追求一次做很多功能。

目标只有 3 个：

1. 验证 worktree 协作规则是不是能真实执行
2. 验证主控收口和 review pass 能不能接住并行改动
3. 验证共享锁定区在并行状态下会不会失控

## 4. 本次演练的默认三条线

### 4.1 线 A：API / Data

分支建议：

- `feat/parallel-01-api-data`

worktree 目录建议：

- `.worktrees/parallel-01-api-data`

职责：

- 只做一个小而完整的 API / 数据层改动
- 允许触碰 `services/api/**`
- 允许触碰 `tests/integration/**`

本轮建议任务：

- 为 `/api/history` 增加可选 `limit` 参数，默认行为不变

为什么选它：

- 它是小改动
- 它能验证 API / repository / 测试这一条线
- 但它不会逼着我们同时改 contracts 和 workflow schema

### 4.2 线 B：Web / Read

分支建议：

- `feat/parallel-01-web-read`

worktree 目录建议：

- `.worktrees/parallel-01-web-read`

职责：

- 只做前端只读展示增强
- 允许触碰 `apps/web/**`
- 不碰 `services/api/**`

本轮建议任务：

- 在项目详情页补一个“当前阶段 / 最近运行 / 结果状态”只读信息区

为什么选它：

- 它直接验证前端是否能稳定消费现有 contract
- 它不需要和 API 线抢同一批文件

### 4.3 线 C：Review Pass

分支建议：

- `review/parallel-01-review`

worktree 目录建议：

- `.worktrees/parallel-01-review`

职责：

- 不做功能实现
- 只负责 review、验证、风险记录和 rollback 说明

本轮要检查：

- 是否越界
- 是否有共享锁定区冲突
- 是否有验证证据
- 是否能安全回退

## 5. 哪些地方本轮不能并行写

本轮默认继续视为共享锁定区：

- `packages/contracts/**`
- `packages/workflow-schema/**`
- `services/api/alembic/**`
- 根配置文件

如果一定要改：

- 先暂停其他写任务
- 由主控串行处理

## 6. 开始前检查清单

满足下面这些条件，才算真的可以开树：

1. `pnpm verify` 通过
2. 当前工作区干净
3. 已有 checkpoint commit
4. 演练任务范围已经写清
5. review pass 责任人已明确

## 7. 固定执行命令

### 7.1 创建演练 worktree

```bash
pnpm worktree:drill:create
```

默认会创建：

- `.worktrees/parallel-01-api-data`
- `.worktrees/parallel-01-web-read`
- `.worktrees/parallel-01-review`

现在默认还会自动补：

- `.venv` 接入
- `pnpm install --frozen-lockfile`

小白版解释：

- 新分支建出来之后，不用你再一条条补环境命令
- 脚本会先把基础开工条件铺好

### 7.2 指定 drill id 或 base ref

```bash
bash scripts/worktree/create_parallel_drill.sh parallel-02 HEAD
```

如果你只想创建树，不想自动补环境，可以这样：

```bash
BOOTSTRAP_WORKTREES=0 bash scripts/worktree/create_parallel_drill.sh parallel-02 HEAD
```

### 7.3 清理演练 worktree

```bash
pnpm worktree:drill:cleanup
```

说明：

- 清理只移除 worktree
- 分支默认保留，不自动删除

## 8. 每条线的最低验收

### API / Data 线

- 有明确功能变化
- 有对应集成测试或验证证据
- 不悄悄改共享 contract

### Web / Read 线

- 页面能跑
- 只读路径不造新后端依赖
- 有截图或 build / typecheck 证据

### Review 线

- 写清风险
- 写清验证命令
- 写清 rollback 说明

## 9. 本轮收口方式

建议顺序：

1. API / Data 线先自测
2. Web / Read 线再自测
3. Review 线做独立检查
4. 主控回主工作区做最终收口
5. 合并前重新跑一次 `pnpm verify`

## 10. 本轮演练结束后要回答的 5 个问题

1. 哪些文件边界还不够清晰
2. 哪些命令入口还不够稳
3. 哪些 review 信息仍然靠人脑记忆
4. 哪些锁定区需要继续收紧
5. 主控是否能承受当前并行密度
