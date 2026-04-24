# 全新项目 GitHub 平台门禁落地清单

更新日期：2026-04-24
状态：Active Checklist v0.1

关联文档：

- [全新项目 仓库 Ruleset 与 Branch Protection 基线](./repo-ruleset-and-branch-protection-baseline.md)
- [全新项目 企业级对齐缺口优先级总表](./enterprise-alignment-gap-priority-matrix.md)
- [全新项目 所有权与审批矩阵](./ownership-and-approval-matrix.md)
- [全新项目 发布前检查清单](./release-checklist.md)
- [全新项目 高风险改动审查清单](./review/high-risk-change-checklist.md)

## 1. 这份文档解决什么问题

前面的文档已经回答了：

- 平台门禁应该开什么
- 为什么要开

这份清单只解决一件事：

`把 dream5i/video 这个仓库的 GitHub 平台门禁，按可执行步骤真正落下来。`

小白版解释：

- 这不是再讲一次“制度”
- 而是把“平台上到底点哪些开关”写清楚

## 2. 当前仓库的真实状态

截至 `2026-04-24`，当前已确认：

- 仓库：`dream5i/video`
- 可见性：`public`
- 默认分支：`main`
- 当前仓库内已有：
  - [`.github/CODEOWNERS`](../.github/CODEOWNERS)
  - [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
  - [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml)
- 当前本地环境没有 `gh` CLI

已经看到的直接信号：

- 本地曾经直接 `push` 到 `origin/main` 成功

这意味着：

- GitHub 平台门禁当前还没有真正拦住 `main`
- 这件事目前不能只靠仓库内文件解决
- 默认落地路径应按 GitHub Web UI 手动配置

## 2.1 2026-04-25 实际落地结果

截至 `2026-04-25`，这一轮平台门禁已经通过 GitHub API 实际打开。

当前 `main` 上已经生效的规则包括：

- 直接改动 `main` 会被拦住，必须走 pull request
- `verify` 和 `dependency-review` 被列为 required checks
- 禁止 force push
- 禁止删除分支
- 要求 linear history
- 要求 conversation resolution
- 管理员也被纳入保护规则

本轮实际验收结果：

- 通过 GitHub API 构造测试提交，再尝试直接更新 `refs/heads/main`
- GitHub 返回 `422`
- 返回信息包含：
  - `Changes must be made through a pull request`
  - `2 of 2 required status checks are expected`

这说明：

- `main` 已经不是随便能推进去的状态
- 平台门禁已经从“文档计划”变成“真实生效”

## 2.2 当前采用的是“单人阶段安全版”

这里有一个很重要的现实约束：

- 当前仓库仍然是单 owner / 单主控阶段
- GitHub 不会把 PR 作者自己的 approval 当成独立审查

所以如果现在就强行打开：

- `1` 个 approving review
- `Require review from code owners`

在没有第二个正式 reviewer 的情况下，这个仓库会进入：

- `main` 安全了
- 但自己也几乎无法正常合并的死锁状态

因此本轮采用的是：

`单人阶段安全版门禁`

它的核心是：

- 先把直推挡住
- 先把检查挡住
- 先把主分支收紧
- 但暂时不把“必须第二个人审批”锁死

等后面进入多人正式协作，再升级为：

- 至少 `1` 个 approving review
- Require review from code owners

## 3. 这次落地的目标

这次不追求把 GitHub 所有企业功能一次开满。

当前目标只有 1 个：

`把 main 分支从“默认好进”改成“默认难进”。`

落地后，至少做到：

1. 不能直接推送到 `main`
2. 不能 force push 到 `main`
3. 合并前必须跑过自动检查
4. 合并前必须经过 review
5. 共享锁定区改动必须走 code owner review

## 4. 当前推荐路线

### 4.1 首选：Ruleset

如果 GitHub 仓库设置里能看到 `Rules` / `Rulesets`，优先用它。

原因：

- 可见性更强
- 规则更清楚
- 后续更容易扩

### 4.2 兜底：Branch Protection

如果当前账号或 UI 暂时没有合适的 `Ruleset` 入口，就退回到：

- `Settings -> Branches -> Branch protection rules`

小白版解释：

- `Ruleset` 像新一代门禁系统
- `Branch protection` 像老一代门禁系统
- 两者都能拦门，优先用更标准的那套

## 5. 当前建议必须打开的门禁

下面这些是当前阶段必须打开的。

### 5.1 保护对象

- 目标分支：`main`
- Enforcement：`Active`

### 5.2 Push 类限制

- 禁止直接推送到 `main`
- 禁止 force push
- 禁止删除 `main`

### 5.3 Pull Request 合并限制

当前单人阶段实际生效的是：

- Require a pull request before merging
- 当前不强制 `1` 个 approving review
- 当前不强制 code owner review
- Require conversation resolution before merging
- Dismiss stale approvals when new commits are pushed

后续升级到多人协作时，再切换成：

- 至少 `1` 个 approving review
- Require review from code owners

### 5.4 检查类限制

- Require status checks to pass before merging
- 建议开启“分支必须更新到最新后再合并”的严格模式

当前建议列为 required 的检查：

- `verify`
- `dependency-review`

说明：

- GitHub UI 里有时显示的是 job 名
- 有时会显示成 `CI / verify`、`Dependency Review / dependency-review`
- 以实际出现的检查名为准，不要死记字面格式

### 5.5 历史与绕过限制

- Require linear history
- Do not allow bypassing the above settings

如果平台允许更细粒度配置，还建议：

- Restrict who can dismiss reviews
- Restrict who can bypass rules

## 6. 当前阶段故意不建议马上打开的项

下面这些不是永远不用，而是现在先不开。

### 6.1 至少 1 个 approving review

当前不建议立即强制打开。

原因：

- 当前还是单 owner + 主控模式
- GitHub 不会把 PR 作者自己的审批算成独立 review
- 太早打开会让仓库进入“有门禁但无法正常收口”的状态

### 6.2 Require review from code owners

当前不建议立即强制打开。

原因：

- 当前 `CODEOWNERS` 仍是单 owner 形态
- 在没有第二个 reviewer 的情况下，会和上面的问题叠加成死锁

### 6.3 Require approval of the most recent push

当前不建议立即打开。

原因：

- 现在还是单 owner + 主控模式
- 太早打开会让单人阶段的流转明显变卡

### 6.4 Require signed commits

当前不作为第一批必开项。

原因：

- 当前优先级是把 review、checks、code owner gate 先稳定

### 6.5 Merge queue

当前不作为第一批必开项。

原因：

- 现在 PR 量还不高
- 先把基本门禁装好更重要

### 6.6 Require deployments before merging

当前不作为第一批必开项。

原因：

- staging / production 真实环境门槛还没完全落地

## 7. 平台落地步骤

下面按“GitHub Web UI 手动配置”来写。

### Step 1：打开仓库设置

进入：

- `https://github.com/dream5i/video`
- `Settings`

### Step 2：进入规则页

优先看：

- `Rules`

如果能看到：

- `Rulesets`

就继续走 ruleset。

如果没有合适入口，再走：

- `Branches`
- `Add branch protection rule`

### Step 3：创建 main 门禁规则

建议名称：

- `main-protection-baseline`

目标：

- `main`

状态：

- `Active`

### Step 4：打开 push 限制

勾选或开启：

- 禁止直接推送
- 禁止 force push
- 禁止删除目标分支

### Step 5：打开 PR 审查限制

勾选或开启：

- Require a pull request before merging
- Require conversation resolution
- Dismiss stale approvals

如果已经进入多人协作，再继续打开：

- Require approvals：`1`
- Require code owner review

### Step 6：绑定 required checks

先确保仓库最近已有 workflow 成功运行记录。

然后在 required checks 里选择：

- `verify`
- `dependency-review`

如果 UI 里看到的是：

- `CI / verify`
- `Dependency Review / dependency-review`

就选平台实际显示出来的名字。

### Step 7：打开历史与绕过限制

勾选或开启：

- Require linear history
- Do not allow bypassing the above settings

如平台支持更细配置，再继续：

- 限制可 dismiss review 的角色
- 限制可 bypass rules 的角色

### Step 8：保存并立即验证

保存后，不要只看“规则已创建”，还要做一次真验证。

## 8. 落地后的验收方法

这一步非常重要。

企业项目不能只说“我记得已经点了”，而要留验收证据。

### 8.1 最低验收动作

至少做下面 4 个动作：

1. 开一个测试 PR
2. 确认 `verify` 和 `dependency-review` 自动运行
3. 在没有 review 时确认 PR 不能合并
4. 改一个共享锁定区文件，确认 code owner review 被要求

### 8.2 最低验收证据

建议至少留下：

- Ruleset 或 branch protection 截图
- Required checks 截图
- 一个未 review 无法合并的 PR 截图
- 一个涉及共享锁定区的 code owner review 截图

### 8.3 通过标准

下面 5 条都成立，才算平台门禁真正过线：

- `main` 不能直接随手推进去
- PR 没过检查时不能合并
- 规则不是口头的，而是在 GitHub 平台里真实生效
- 当前阶段的门禁和当前协作形态不打架

如果进入多人协作阶段，再追加下面 2 条：

- PR 没过 review 时不能合并
- 共享锁定区会触发 code owner review

## 9. 当前仓库的建议 required checks 对照表

| 来源文件 | Workflow 名 | Job 名 | 平台里优先寻找的检查名 |
| --- | --- | --- | --- |
| [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | `CI` | `verify` | `verify` 或 `CI / verify` |
| [`.github/workflows/dependency-review.yml`](../.github/workflows/dependency-review.yml) | `Dependency Review` | `dependency-review` | `dependency-review` 或 `Dependency Review / dependency-review` |

## 10. 当前阶段的角色分工

### Project Owner

- 决定是否同意把 `main` 彻底收紧

### Main Controller

- 设计门禁组合
- 判断哪些项现在必须开
- 审查是否和当前开发阶段匹配

### 仓库管理员

- 在 GitHub 平台里真正点开这些开关

小白版解释：

- 仓库里的文档和代码是“设计图”
- GitHub 设置页里的开关才是“电闸”

## 11. 当前结论

当前这个仓库，平台门禁真正缺的不是“再写一份规则说明”，而是：

`把 main 的强制规则真正在 GitHub 平台上打开，并留一轮验收证据。`

这一轮已经完成了第一版落地。

当前更准确的说法是：

- `main` 已经被平台规则收紧
- 当前处于“单人阶段安全版门禁”
- 下一次升级点，不是再重配一次平台，而是等第二个正式 reviewer 出现后，把 review / code owner gate 继续抬高
