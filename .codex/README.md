# Codex Config Templates

这组文件是企业 AI 编程治理的可执行模板与项目基线，不会因为放在仓库里就自动生效。

用途分成两类：

- `.codex/*.example.toml`
  - 作为组织或设备级托管配置的参考模板
  - 需要按官方 Codex 管理方式部署到系统路径、MDM 或云端 managed policy
- `.codex/*.project.toml`
  - 作为当前项目的第一版正式策略草案
  - 用来明确“受控高权限主控”这条线应该怎么配
- `codex/rules/default.rules`
  - 作为仓库级命令规则样例
  - 使用 Codex 原生 `.rules` 语法

建议用法：

1. 先根据 `docs/security/do-not-feed-and-exclusion-list.md` 定好敏感数据边界。
2. 再根据 `docs/review/high-risk-change-checklist.md` 定好审批和证据要求。
3. 先看 `docs/security/ai-coding-policy-matrix.md` 选择角色档位。
4. 最后把这里的 project 或 example 文件部署到你们真实的托管配置体系里，而不是直接假设仓库内文件会自动生效。

关联文档：

- `docs/enterprise-ai-coding-rules.md`
- `docs/enterprise-ai-coding-operating-playbook.md`
- `docs/security/do-not-feed-and-exclusion-list.md`
- `docs/review/high-risk-change-checklist.md`
- `docs/security/ai-coding-policy-matrix.md`
