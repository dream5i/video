# 全新项目 Worktree 与分支治理手册

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)
- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)

## 1. 这份文档解决什么问题

这份手册把“worktree 要治理”翻译成真实可执行动作。

目标是：

- 主控与子 Agent 不互相覆盖
- 高风险改动有独立 review pass
- 主工作区只做统筹、集成和最终收口

## 2. 当前总规则

- `main` 只用于稳定集成
- 一类任务一个分支
- 一个并行写任务一个 worktree
- 共享锁定区不并行写

## 3. 分支命名

建议统一使用：

- `feat/<scope>`
- `fix/<scope>`
- `chore/<scope>`
- `review/<scope>`
- `docs/<scope>`

示例：

- `feat/web-workspace`
- `feat/persistence-foundation`
- `fix/run-state`
- `review/provider-pass`

## 4. worktree 目录

统一放到仓库根目录下的：

```text
.worktrees/
```

建议结构：

```text
.worktrees/
├── web-workspace/
├── persistence-foundation/
├── worker-render/
└── review-provider-pass/
```

## 5. 常用命令

### 5.1 为一个新任务创建分支和 worktree

```bash
git worktree add .worktrees/feat-web-workspace -b feat/web-workspace main
```

如果是第一次真实并行演练，建议优先使用仓库内置脚本：

```bash
pnpm worktree:drill:create
```

它会一次性创建：

- API / Data 线
- Web / Read 线
- Review pass 线

### 5.2 为 review pass 单独开只读审查树

```bash
git worktree add .worktrees/review-run-state -b review/run-state main
```

### 5.3 查看当前 worktree

```bash
git worktree list
```

### 5.4 清理已完成 worktree

```bash
git worktree remove .worktrees/feat-web-workspace
```

如果是清理第一次真实并行演练，建议使用：

```bash
pnpm worktree:drill:cleanup
```

## 6. 共享锁定区

下面这些目录默认不能并行写：

- `packages/contracts/**`
- `services/api/app/domain/**`
- `services/api/app/providers/interfaces/**`
- `services/api/alembic/**`
- 根配置文件

如果必须改：

- 由主控亲自改
- 或先暂停其他写任务，再串行改

## 7. review pass 的执行方式

以下改动建议单独开一个 `review/*` 分支或 worktree：

- migration
- provider interface
- adapter contract
- 状态机
- 队列 / 重试
- 根配置

review pass 至少检查：

- 是否越界
- 是否破坏 contract / schema
- 是否缺测试或验证证据
- 是否有 rollback 方案

## 8. 合并前固定动作

1. 在任务树里跑完本次需要的验证
2. 主控在主工作区重新拉取并审查
3. 必要时补独立 review pass
4. 合并前至少跑一次 `pnpm verify`

## 9. checkpoint 规则

第一次真实并行演练前，建议增加一条硬规则：

- 当前工作区必须干净
- 必须先打一个 checkpoint commit

原因：

- `git worktree` 是从提交点分出新树
- 不是从当前未提交改动直接复制

小白版解释：

- 没有 checkpoint commit，就像还没存档就想开三个平行世界
- 三个世界会从旧存档出发，不会自动继承你桌面上还没保存的内容

## 10. 当前阶段建议

项目仍处在骨架到最小运行链路阶段。

因此推荐：

- 核心层单线程
- 页面与文档可控并行
- 真正多树并行，等 persistence 和测试底座再稳定一些后再扩大
