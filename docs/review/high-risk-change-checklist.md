# 全新项目 高风险改动审查清单

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 搭建治理与 Agent 工作模型](../build-governance-and-agent-operating-model.md)
- [全新项目 企业 AI 编程规则](../enterprise-ai-coding-rules.md)
- [全新项目 企业 AI 编程操作手册](../enterprise-ai-coding-operating-playbook.md)

## 1. 这份文档解决什么问题

这份清单用来回答：

`哪些改动算高风险，进入主线前必须补哪些证据、哪些检查、哪些批准。`

它的目标不是拖慢开发，而是让下面这些风险有统一门槛：

- 越界
- 状态不一致
- 数据损坏
- 权限失控
- 成本失控
- 审计缺口

## 2. 哪些改动默认算高风险

以下改动默认进入高风险审查：

- auth / role / tenant
- provider interface
- prompt registry
- 数据库 schema / migration
- queue / retry / state machine
- retention / audit / tracing policy
- deletion logic
- 新外部 provider
- 新 MCP server / plugin / external tool
- 新依赖且带许可证或供应链风险
- 任何会触碰生产数据、成本或权限边界的改动

## 3. 进入审查前必须附带的证据包

### 所有高风险改动都要有

- 改动目的
- 影响范围
- 涉及文件
- 测试结果
- 已知未覆盖风险
- 回滚思路

### 涉及 AI 生成或 AI 协助的，再补

- 使用了哪个 agent
- model / provider
- prompt / instruction / policy 版本
- 关键命令记录
- reviewer 结论

## 4. 审查问题清单

### 4.1 边界检查

- 有没有超出当前 MVP 主链？
- 有没有改到共享锁定区以外不该动的地方？
- 有没有把实验性扩展偷偷带进主线？

### 4.2 正确性检查

- contract / schema / API 返回是否仍一致？
- 状态机有没有引入不可达或不一致状态？
- 错误处理、超时、重试是否完整？

### 4.3 安全与数据检查

- 有没有读到或外发不该进入模型的内容？
- 有没有新增敏感日志或 trace 泄露点？
- 权限、审批、删除、审计边界是否仍有效？

### 4.4 依赖与供应链检查

- 有没有新增依赖？
- 新依赖的许可证和维护状态是否可接受？
- 有没有来源不明的大段代码？

### 4.5 可运维性检查

- 是否有观测点？
- 是否有失败回滚路径？
- 是否会显著增加成本、重试或人工接管次数？

## 5. 最低批准要求

### 普通高风险改动

- 主控自审
- 一轮独立 review pass

### 安全、权限、删除、生产边界相关改动

- 主控自审
- 一轮独立 review pass
- 人工批准

### 新外部能力接入

- 主控自审
- 一轮独立 review pass
- license / security 复核
- 人工批准

## 6. 不通过时怎么处理

如果审查未通过，不直接“继续试试”，而是：

1. 先记录阻断原因
2. 再缩小改动范围或补证据
3. 必要时拆成更小任务重新进入审查

以下情况应直接阻断，不进入主线：

- 无法说明数据边界
- 无法说明回滚路径
- 无法说明依赖来源或许可证
- 破坏共享 contract / schema 且无配套迁移说明
- 试图绕过人工批准

## 7. 与仓库规则的关系

这份清单和下面这些文件一起使用：

- `AGENTS.md`
- `docs/security/do-not-feed-and-exclusion-list.md`
- `.codex/requirements.example.toml`
- `codex/rules/default.rules`
