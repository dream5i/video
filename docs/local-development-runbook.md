# 全新项目 本地开发运行手册

更新日期：2026-04-24
状态：Draft v0.1

关联文档：

- [全新项目 README](../README.md)
- [全新项目 实施路线图](./implementation-roadmap.md)
- [全新项目 搭建治理与 Agent 工作模型](./build-governance-and-agent-operating-model.md)

## 1. 这份文档解决什么问题

这份手册只解决一件事：

`让任何一次本地启动、验证、收口都走固定入口，而不是每次临时拼命令。`

## 2. 当前本地前置条件

- `Node.js 22`
- `pnpm 10`
- `Python 3.11+`

## 3. 首次进入仓库

### 3.1 安装 Node 依赖

```bash
pnpm install
```

### 3.2 准备环境变量

```bash
cp .env.example .env
```

当前前端默认读：

- `NEXT_PUBLIC_API_BASE_URL`

当前 API 默认使用：

- `API_HOST`
- `API_PORT`
- `NEW_PROJECT_REPOSITORY_BACKEND`
- `DATABASE_URL`

### 3.3 Python 本地依赖

当前 Python 依赖仍按服务边界管理在各自的 `pyproject.toml` 中。

如果要在本地直接起 API / Worker，一个最小可用方式是先建虚拟环境，再安装当前骨架需要的依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install fastapi pydantic uvicorn dramatiq sqlalchemy alembic
```

说明：

- 这是当前骨架阶段的最小安装方式
- 后续进入持久化和真实任务流后，应收口为统一的 Python 开发安装方案
- 当前默认开发路径已经是 `database`
- 如果要临时退回内存仓库调试，再显式设置 `NEW_PROJECT_REPOSITORY_BACKEND=memory`

## 4. 当前固定命令入口

### 4.1 前端开发

```bash
pnpm dev:web
```

### 4.2 API 开发

```bash
pnpm dev:api
```

说明：

- 这个命令当前会优先使用仓库根目录下的 `.venv`
- 这是为了让数据库默认路径更稳，不依赖你系统 Python 是否刚好装了 `sqlalchemy`

### 4.3 Worker 骨架验证

```bash
pnpm dev:worker
```

### 4.4 仓库统一校验

```bash
pnpm verify
```

当前 `pnpm verify` 会执行：

- `pnpm -r typecheck`
- `pnpm --filter @new-project/web build`
- `python3 -m compileall services/api services/worker`
- `pnpm test:api`

说明：

- `pnpm verify` 当前还不包含浏览器 E2E
- 原因不是它不重要，而是浏览器验收更慢，更适合作为单独一轮“真页面回归”
- 小白版解释：
  - `verify` 像快速质检
  - `test:e2e` 像开真车跑一圈

### 4.5 worktree 环境补齐

如果你在并行开发里新开了一个 worktree，推荐立刻执行：

```bash
pnpm worktree:bootstrap -- .worktrees/parallel-01-api-data
```

这条命令会做两件事：

- 把仓库根目录的 `.venv` 接到这个 worktree
- 在这个 worktree 里执行一次 `CI=1 pnpm install --frozen-lockfile`

小白版解释：

- 这一步是在给新工位发工具箱
- 没做这一步，后面 `pnpm verify` 可能不是代码错，而是环境没接好

### 4.6 主链集成测试

在已经激活 `.venv` 的前提下，当前可以单独跑主链集成测试：

```bash
pnpm test:api
```

如果只想单独跑 migration 冒烟：

```bash
pnpm test:api:migrations
```

这条测试当前覆盖的是：

- 创建项目
- 获取项目
- 生成分析结果
- 生成预填充 workflow
- 创建 render run
- 查询历史
- 覆盖 repository 直连链路
- 覆盖 HTTP API 对外链路
- 覆盖基础异常返回契约（如 `404` / `400`）
- 覆盖 `x-request-id` / `x-trace-id` 响应头
- 覆盖结构化错误返回字段：`message` / `errorCode` / `requestId` / `traceId`
- 覆盖 migration smoke

说明：

- 这条测试已经走真实 SQLite 持久化
- 现在它已经并入仓库默认 `pnpm verify`
- 这意味着主链已经进入统一自动验收

### 4.7 安装浏览器验收依赖

第一次跑页面级 E2E 前，先安装 Playwright 的浏览器：

```bash
pnpm test:e2e:install
```

小白版解释：

- 这一步是在把“自动点页面的浏览器”装到本机
- 不装的话，测试脚本知道要点哪里，但本地没有可用浏览器内核

### 4.8 浏览器主链 E2E

当前已经有第一条真实页面主链验收，可以直接运行：

```bash
pnpm test:e2e
```

这条测试当前会自动启动本地 API 和前端，再从用户视角完成：

- 打开首页
- 新建项目
- 进入项目工作台
- 触发 render run
- 等待结果资产出现
- 进入历史页

说明：

- 这条测试是“真浏览器走真页面”，不是只发 HTTP 请求
- 当前它还没有并入 `pnpm verify`
- 但只要本次改动影响主链页面、API 协作或运行状态流，就建议补跑一轮

## 5. 开发中的默认约束

- 所有改动优先服从共享 contract
- 长任务逻辑不塞进页面请求
- 高风险改动先看 `docs/review/high-risk-change-checklist.md`
- 修改共享锁定区前先看 `AGENTS.md`

## 6. 合并前最低动作

进入主线前，最低要求是：

1. 跑一次 `pnpm verify`
2. 说明本次改动是否触碰共享锁定区
3. 如触碰高风险区域，补独立 review pass
4. 必要时补文档或 ADR

## 7. 当前已知限制

- Python 运行时依赖的安装方式仍是骨架阶段方案
- 真实数据库、真实任务队列和真实对象存储尚未接入
- 浏览器 E2E 已有第一条主链，但还没有扩成完整页面回归套件
- 可观测性第一版字段和错误契约已接入 API，但 dashboard / alerting 平台还没接上
