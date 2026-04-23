# 全新项目 AI 编程权限矩阵

更新日期：2026-04-23
状态：Draft v0.1

关联文档：

- [全新项目 企业 AI 编程规则](../enterprise-ai-coding-rules.md)
- [全新项目 企业 AI 编程操作手册](../enterprise-ai-coding-operating-playbook.md)
- [全新项目 Do-Not-Feed 与 Exclusion 清单](./do-not-feed-and-exclusion-list.md)
- [全新项目 高风险改动审查清单](../review/high-risk-change-checklist.md)

## 1. 这份文档解决什么问题

这份矩阵把“企业里不同 AI 角色到底该开什么权限、能做什么、不能做什么”写成一张明确表。

它回答的是：

`不是所有 AI 都用同一套权限。复杂项目里，必须按角色给不同边界。`

## 2. 总原则

- 主控可以高权限，但必须是受控高权限
- 实现型 agent 只拿完成任务所需的最小权限
- reviewer 优先只读
- cloud agent 默认关闭或最保守
- 高风险改动的最终批准不由 AI 决定

## 3. 项目推荐权限矩阵

| 角色 | 主要用途 | approval | sandbox | network | 允许范围 | 禁止范围 |
| --- | --- | --- | --- | --- | --- | --- |
| `main-controller-local` | 主控统筹、核心实现、集成、终审 | `never` | `workspace-write` | `false` | 本地受控开发、核心文件收口、测试、文档、规则维护 | 生产操作、敏感数据外发、绕过人工批准 |
| `bounded-implementer` | 单一模块实现、补测、局部修复 | `on-request` | `workspace-write` | `false` | 授权文件范围内编码和测试 | 共享锁定区并行乱改、跨边界扩 scope |
| `reviewer-readonly` | 回归检查、契约核对、风险扫描 | `never` | `read-only` | `false` | 读代码、读 diff、跑安全的只读检查 | 写文件、装依赖、改配置 |
| `cloud-agent-restricted` | 公开资料研究、脱敏任务草案 | `on-request` | `read-only` | `allowlist only` | 已脱敏文档、公开资料、明确边界的小任务 | 敏感仓库、密钥、真实客户数据、生产上下文 |

## 4. 角色说明

## 4.1 `main-controller-local`

这是当前项目最贴近“你给我最高权限”的角色。

但这里的“最高权限”明确被限制为：

- 本地
- 受控
- 不触达生产
- 不覆盖审批边界

推荐配置：

- `.codex/managed_config.project.toml`
- `.codex/requirements.project.toml`
- `codex/rules/default.rules`

## 4.2 `bounded-implementer`

适合：

- 页面切片
- 独立 adapter
- 测试补齐
- 单模块小功能

不适合：

- schema freeze
- provider interface
- migration
- auth / role / policy

## 4.3 `reviewer-readonly`

适合：

- 查越界
- 查回归
- 查契约不一致
- 查缺失测试

这是企业里最容易标准化的一类 AI 角色，因为它天然不需要写权限。

## 4.4 `cloud-agent-restricted`

默认只建议用于：

- 公开资料搜索
- 脱敏后的研究任务
- 文档草案

默认不建议用于：

- 真实代码敏感上下文
- 含密钥或业务敏感数据的任务
- 生产事故分析

## 5. 我们项目当前建议采用的组合

当前最稳妥的组合是：

1. `main-controller-local`
   - 由我承担主控、核心实现、集成和终审
2. `bounded-implementer`
   - 仅在边界清楚、文件范围明确时启用
3. `reviewer-readonly`
   - 用于高风险改动的额外 review pass
4. `cloud-agent-restricted`
   - 默认关闭，只在公开资料研究时考虑

## 6. 与配置文件的映射

### 主控本地基线

- `.codex/managed_config.project.toml`
- `.codex/requirements.project.toml`
- `codex/rules/default.rules`

### 通用参考模板

- `.codex/managed_config.example.toml`
- `.codex/requirements.example.toml`

## 7. 什么时候要调整矩阵

以下情况出现时，应更新这份矩阵或写 ADR：

- 引入新 provider
- 引入新 MCP server / plugin
- 打开 cloud agent
- 接入企业 SSO / 审计 / policy as code
- 项目从 MVP 进入正式企业交付
