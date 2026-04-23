# 全新项目 本地开发运行手册

更新日期：2026-04-23
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

### 3.3 Python 本地依赖

当前 Python 依赖仍按服务边界管理在各自的 `pyproject.toml` 中。

如果要在本地直接起 API / Worker，一个最小可用方式是先建虚拟环境，再安装当前骨架需要的依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install fastapi pydantic uvicorn dramatiq
```

说明：

- 这是当前骨架阶段的最小安装方式
- 后续进入持久化和真实任务流后，应收口为统一的 Python 开发安装方案

## 4. 当前固定命令入口

### 4.1 前端开发

```bash
pnpm dev:web
```

### 4.2 API 开发

```bash
pnpm dev:api
```

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
- CI 已经覆盖基础校验，但还没有进入完整测试分层
