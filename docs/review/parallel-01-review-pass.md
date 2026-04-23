# Parallel 01 Review Pass

更新日期：2026-04-23
审查分支：`review/parallel-01-review`
基线提交：`17929d2`

## 1. 审查范围

本轮审查覆盖两条功能分支：

- `feat/parallel-01-api-data` (`e1aee0e`)：`/api/history` 增加 `limit` 查询能力
- `feat/parallel-01-web-read` (`e4d2e0e`)：项目详情页增加只读 `Workspace Snapshot` 总览卡片

本轮重点检查：

- 是否超出 MVP 边界
- 是否破坏 contract / repository 接口
- 是否有独立验证证据
- 是否支持独立回滚
- 并行 worktree 流程本身是否暴露治理缺口

## 2. 审查结论

### 2.1 代码结论

本轮没有发现阻塞合并的代码级问题。

判断依据：

- API/Data 线改动范围小，且 contract、内存仓库、SQL 仓库、HTTP 路由、集成测试同步更新
- Web/Read 线只增加项目详情页的只读展示，不改写主链状态，不改 provider 契约，不改工作流写路径
- 两条分支分别可独立回滚，互相之间没有文件级冲突

### 2.2 流程结论

本轮发现 2 类非阻塞但必须补强的流程问题。

这类问题现在不会挡住小规模并行，但会挡住“更大并行”和“稳定上线前的标准化协作”。

## 3. 验证证据

### 3.1 API/Data 线

- 代码审查：
  - `services/api/app/domain/interfaces.py`
  - `services/api/app/domain/repository.py`
  - `services/api/app/domain/sql_repository.py`
  - `services/api/app/routes/projects.py`
  - `tests/integration/test_api_main_flow.py`
  - `tests/integration/test_sql_repository_flow.py`
- diff 检查：`git diff --check 17929d2..e1aee0e`
- 合并兼容性：与 `feat/parallel-01-web-read` 做三方合并模拟，无冲突
- 验证结果：
  - 在 worktree 补齐 `.venv` 后，`pnpm verify` 通过
  - `pnpm test:api` 通过，包含新增 `history limit` 相关用例

### 3.2 Web/Read 线

- 代码审查：
  - `apps/web/app/projects/[projectId]/page.tsx`
  - `apps/web/app/globals.css`
- diff 检查：`git diff --check 17929d2..e4d2e0e`
- 合并兼容性：与 `feat/parallel-01-api-data` 做三方合并模拟，无冲突
- 验证结果：
  - 在 worktree 补齐 `.venv` 后，`pnpm verify` 通过
  - 页面为只读增强，未引入新的写路径

## 4. Findings

### Finding 1

`scripts/worktree/create_parallel_drill.sh` 只负责创建 worktree 和分支，但没有补齐每个 worktree 的本地运行环境，导致新 worktree 直接执行验证时不稳定。

证据：

- [create_parallel_drill.sh](/Users/wangyan/projects/course2/全新项目__误开归档_2026-04-23_1545/scripts/worktree/create_parallel_drill.sh#L1)
- [package.json](/Users/wangyan/projects/course2/全新项目__误开归档_2026-04-23_1545/package.json#L11)
- [package.json](/Users/wangyan/projects/course2/全新项目__误开归档_2026-04-23_1545/package.json#L16)

影响：

- 新 worktree 直接跑 `pnpm verify` 时，`test:api` 会回退到系统 Python
- 如果系统 Python 没装 `sqlalchemy`、`alembic`，验证会失败
- 失败现象会被误判成“代码坏了”，实际上是“环境没接好”

小白版解释：

- 脚本只帮我们把“新工地”搭出来了，但没有把工具箱和电源线一起接过去

建议：

- 在下一轮进入更大并行前，补一个 worktree bootstrap 动作
- 至少自动处理：
  - Python 环境接入策略
  - Node 依赖安装策略
  - 首次验证命令说明

### Finding 2

当前仓库对 worktree 模式下的 Next.js 构建警告没有消音或文档说明，后续大并行时会持续产生噪音。

证据：

- [next.config.mjs](/Users/wangyan/projects/course2/全新项目__误开归档_2026-04-23_1545/apps/web/next.config.mjs#L1)
- [worktree-and-branching-runbook.md](/Users/wangyan/projects/course2/全新项目__误开归档_2026-04-23_1545/docs/worktree-and-branching-runbook.md#L54)

影响：

- `pnpm verify` 虽然能通过，但 `next build` 每次都会提示多 lockfile / root 推断警告
- 当 worktree 数量增加时，审查和 CI 结果会更难分辨“真正错误”和“重复噪音”

小白版解释：

- 现在不是房子塌了，而是每次开工都会响一遍误报警铃

建议：

- 评估在 `apps/web/next.config.mjs` 中显式设置 `turbopack.root`
- 或在 runbook 里明确说明该警告的原因与处理方式

## 5. Merge Judgment

当前建议：

- 可以继续保持“小规模受控并行”
- 可以按功能分支独立评审、独立合并
- 暂不建议直接全面铺开到更大并行

原因：

- 代码层面已经证明“第一轮并行”可行
- 流程层面还没把 worktree bootstrap 做成标准动作
- 噪音警告还没治理，后面分支一多会拉高误判率

## 6. Merge / Rollback 建议

建议合并顺序：

1. `feat/parallel-01-api-data`
2. `feat/parallel-01-web-read`
3. 保留本审查文档作为第一轮并行演练记录

回滚方式：

- 两条功能分支互相隔离，可单独回滚
- `history limit` 出问题时，只回滚 API/Data 线
- Snapshot UI 出问题时，只回滚 Web/Read 线

## 7. 下一步建议

在进入“更大并行”前，先补一个很小但关键的基础动作包：

1. worktree bootstrap 标准化
2. Next worktree 警告治理
3. 把“新 worktree 首次验证步骤”写进 runbook

完成这 3 件事后，再开启第二轮并行会更稳。
