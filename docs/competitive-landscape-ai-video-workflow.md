# AI 视频工作流赛道竞品与开源参照完整版

更新日期：2026-04-23

关联文档：

- [SoraTK 竞品分析文档](./competitor-analysis-soratk.md)

## 1. 这份文档解决什么问题

这份文档是在已有 `SoraTK` 实测分析的基础上补做的一份完整版研究，目标不是再重复一遍功能截图，而是回答下面 4 个更关键的问题：

1. `SoraTK` 在整个 AI 视频产品版图里，属于哪一类产品。
2. 市面上相似产品已经把这条链路做到了什么程度。
3. GitHub 上有没有接近这类能力的开源项目，它们通常怎么拆结构。
4. `全新项目` 如果要做这条方向，首版产品和技术结构应该怎么定。

## 2. 研究方法与可信度说明

这份文档混合了三类输入，因此我把信息来源明确分层：

- `实测`
  来自我在登录状态下对 `soratk.com` 的真实操作和流程验证。
- `官方公开信息`
  来自各产品官网、官方帮助中心、官方 API 文档和 GitHub README。
- `结构推断`
  基于公开页面、功能命名、仓库目录结构，对产品架构或系统分层做的归纳判断。

下面文中的结论，如果是我推断出来的，我会直接写成“推断”。

## 3. 一句话总判断

`SoraTK` 不是单一的 AI 视频生成工具，而是一个围绕“电商短视频生产”的流程型平台。

如果把同类产品放在一起看，这个赛道目前大致分成 4 类：

1. `URL / 商品页 -> 广告视频`
   代表：`Creatify`、`HeyGen URL to Video`
2. `AI UGC / AI Actor / 广告批量化`
   代表：`Arcads`、`Creatify`
3. `通用 Agent 式视频生产`
   代表：`InVideo AI`、`OpenMontage`
4. `工作流底座 / 节点编排引擎`
   代表：`ComfyUI`

`SoraTK` 的独特点不在“模型能力本身”，而在于把这几类能力拼成了一条更贴近电商实操的链路：

`去水印/解析 -> 爆款复刻 -> 工作流编排 -> 角色/案例 -> 生成与历史`

## 4. SoraTK 在赛道里的位置

### 4.1 SoraTK 的产品本质

基于实测，`SoraTK` 更像：

`电商短视频 AI 生产操作台`

它不是只做“文字生成视频”，也不是只做“AI 数字人”，而是在做一条围绕爆款复刻和商品内容生产的业务链路。

### 4.2 SoraTK 的核心结构

根据实测，`SoraTK` 的主结构可以拆成 4 层：

#### A. 获客入口层

- 去水印
- 爆款复刻
- 首页工作台

#### B. 生产中枢层

- 工作流画布
- 节点配置
- 全部运行 / 发布

#### C. 资产沉淀层

- 带货案例
- 角色工坊
- 生成历史

#### D. 商业与供应层

- 积分
- 会员
- 配置秘钥
- 第三方模型供应商

### 4.3 SoraTK 的最大问题

实测里最明显的问题仍然是这三个：

1. `首页 CTA 与结果不一致`
   用户点“开始生成”，实际进的是空白工作流，不是直接出片。
2. `高价值能力不够稳`
   爆款复刻确实有价值，但分析链路存在上游失败风险。
3. `默认把认知负担丢给用户`
   用户被带入画布后，如果没有预置模板，接下来的动作不够自然。

## 5. 商业竞品地图

这一节不是简单列名字，而是看它们各自占了哪一段价值链。

### 5.1 竞品全景

| 产品 | 主入口 | 核心价值 | 更像哪类产品 | 与 SoraTK 的关系 |
| --- | --- | --- | --- | --- |
| SoraTK | 链接解析、爆款复刻 | 电商视频生产链路 | 流程型电商视频平台 | 当前核心参照物 |
| Creatify | 商品 URL | 批量广告生成、广告测试 | URL-to-Ad + AI UGC 平台 | 最接近商业闭环 |
| Arcads | AI UGC 广告 | AI 演员、广告批量化 | AI UGC 广告平台 | 偏广告创意生产 |
| HeyGen URL to Video | 网页 URL | 从链接自动生成叙述型视频 | URL-to-Video 工具 | 偏内容转视频 |
| InVideo AI | Prompt / Agent | 通用型 AI 视频生产与编辑 | Agent 式视频工作室 | 覆盖面更广但不够垂直 |

### 5.2 Creatify

#### 公开结构

根据官方首页和官方文档，`Creatify` 的结构已经非常清楚：

- `URL to Video`
- `AI Avatars`
- `Product Ads`
- `AI Shorts`
- `Batch Generation`
- `Inspiration Library`
- `Ad Cloner`
- API

官方公开信息显示，它把自己定义成“现代广告主的完整工具箱”，并把 `URL to Video`、`Batch Generation`、`Ad Cloner` 和 `Inspiration Library` 放在同一体系下。

#### 它最值得注意的地方

`Creatify` 其实已经把 `SoraTK` 想做的很多东西产品化了：

- 从商品 URL 自动抽取素材
- 自动生成广告脚本
- 批量生成多个广告变体
- 做广告灵感和爆款参照
- 提供 API，便于平台化接入

#### 结构推断

`Creatify` 的真正核心不是“一个视频生成器”，而是：

`商品理解层 + 广告脚本层 + 模板/头像层 + 批量实验层 + API 层`

这比 `SoraTK` 更偏“广告生产系统”，而不是“创作者工具”。

#### 对我们的启发

- `URL -> 多变体广告` 是最强商业闭环之一。
- “批量生成”和“灵感库/Ad Cloner”很关键，因为广告业务天然需要测试而不是只要一条片。
- 如果未来要做 B 端或代理商场景，`API` 和 `Batch` 要尽早考虑。

### 5.3 Arcads

#### 公开结构

根据官网公开页面，`Arcads` 重点强调：

- `1,000+ AI Actors`
- 自建 AI Avatar / AI Actor
- 产品持有、App 展示、服饰展示
- `AI Video Editing`
- `Emotion control`
- `30+ languages` 本地化
- `AI Agent for marketing`

#### 它最值得注意的地方

`Arcads` 的重点不是链接解析，也不是传统工作流，而是：

`AI UGC 广告演员库 + 广告创意批量产能`

这意味着它在“人设感”和“像真人广告”这件事上，明显比通用视频平台更聚焦。

#### 结构推断

`Arcads` 更像：

`角色资产层 + 文案/情绪控制层 + 广告编辑层 + 本地化层 + 批量营销层`

它不像 `SoraTK` 那样强调“先拆爆款再生产”，而是更直接地把广告内容工业化。

#### 对我们的启发

- 如果我们未来偏 `AI UGC 广告`，角色层会比工作流层更先成为用户感知价值。
- “情绪控制”和“多语言本地化”不应该只是附属项，它们直接影响广告转化。
- 广告类产品最终会走向“素材库 + 人物库 + 变体批量化”。

### 5.4 HeyGen URL to Video

#### 公开结构

官方页面显示它的 `URL to Video` 流程是：

`Paste URL -> Choose visual style -> Review script -> Generate and export`

官网还明确提到：

- 自动提取页面内容、图片和元数据
- 自动生成脚本
- 自动配旁白、字幕和音乐
- 支持多语言本地化
- 支持批量和 API 自动化

#### 它最值得注意的地方

`HeyGen` 的这个方向说明一件事：

`URL -> 视频` 已经不是噱头，而是成熟产品功能。

但 `HeyGen` 的落点更偏“内容表达”和“品牌叙述视频”，而不是像 `SoraTK` 那样紧贴电商爆款运营。

#### 对我们的启发

- `URL 输入` 是很强的冷启动入口。
- `脚本可编辑` 很重要，不能只给纯自动结果。
- `批量和 API` 是一条很自然的商业延长线。

### 5.5 InVideo AI

#### 公开结构

官网公开信息表明，`InVideo AI` 的能力更广：

- AI Video Generator
- AI Clip Generator
- UGC Ads
- AI Avatar Generator
- AI Ad Generator
- 多模型接入
- 文字指令式编辑
- Agent 式长视频生成

它的核心卖点是：

- `Turn any idea into videos`
- `Create & edit like you think`
- `Edit with prompts`

#### 它最值得注意的地方

`InVideo AI` 本质上不是电商单点工具，而是一个更通用的 AI 视频工作室。

它值得关注的是两个方向：

1. `Prompt-first`
   用户不是搭流程，而是直接对系统说需求。
2. `Edit-by-command`
   不是传统时间线点点点，而是用文字命令修改视觉、音频、配音和字幕。

#### 结构推断

`InVideo` 的底层结构更像：

`通用生成 Agent + 多模型路由 + 资产库 + 文本编辑代理 + 视频工作室 UI`

#### 对我们的启发

- 长期来看，工作流画布未必是唯一交互方式。
- 对普通用户来说，“直接说需求”和“用自然语言改视频”往往比空白画布更友好。
- 如果我们首版要简单，最好先做“预填充工作流 + 自然语言微调”，不要一上来就强推纯画布。

## 6. GitHub 开源参照

开源侧没有一个项目能 1:1 等于 `SoraTK`，但已经能看到几种非常清晰的结构模板。

### 6.1 ComfyUI

#### 它是什么

`ComfyUI` 是一个图形化工作流底座，不是电商视频产品。

官方 README 明确写到，它是基于 `graph/nodes/flowchart` 的可视化 AI 引擎和应用，并支持离线运行、工作流保存/加载、外部 API 节点等能力。

#### 仓库结构

GitHub 顶层目录能看到这些核心模块：

- `api_server`
- `app`
- `blueprints`
- `comfy`
- `comfy_api`
- `comfy_api_nodes`
- `comfy_execution`
- `custom_nodes`
- `models`
- `tests`

#### 结构判断

它的核心模式是：

`节点系统 + 执行引擎 + 扩展节点生态 + 工作流文件格式`

#### 对我们的启发

- 如果我们以后要做“可组合的视频流程”，节点模型很有价值。
- 但 `ComfyUI` 更像底座，不是直接给业务用户用的完整产品。
- 直接照搬会让产品非常强，但学习门槛也会非常高。

### 6.2 OpenMontage

#### 它是什么

`OpenMontage` 是一个开源的 Agent 式视频生产系统。官方 README 的描述非常激进，但结构确实很有启发。

它的公开主张包括：

- 12 条 production pipelines
- 52 个 tools
- 500+ agent skills
- 研究、写脚本、生成素材、加字幕、渲染成片、做自检

#### 仓库结构

GitHub README 已经把目录结构写得很清楚：

- `pipeline_defs`
- `skills`
- `tools`
- `schemas`
- `styles`
- `remotion-composer`
- `lib`
- `tests`

它还明确提出三层知识结构：

- Layer 1: `tools + pipeline_defs`
- Layer 2: `skills`
- Layer 3: 外部知识包

#### 结构判断

`OpenMontage` 的关键不是 UI，而是：

`管道定义层 + 工具层 + Agent 技能层 + 渲染层 + 合约校验层`

#### 对我们的启发

- 如果未来想做“AI 自动导演式”产品，`pipeline_defs + skills + tools` 这种结构非常值得借鉴。
- 它说明复杂视频产品不一定非要从前端画布开始，也可以先从“管道编排内核”开始。
- 这对我们是一个重要提醒：
  `工作流未必等于可视化节点图，也可以是声明式 pipeline。`

### 6.3 OpenShorts

#### 它是什么

`OpenShorts` 是目前最接近“开源产品形态”的参照之一。

官方 README 明确写它是一个 `3 tools in 1 platform`：

- Clip Generator
- AI Shorts
- YouTube Studio

而且它直接支持：

- 长视频转竖版短视频
- AI 演员营销视频
- YouTube 标题/封面/描述
- 社交平台发布
- UGC Gallery

#### 技术管线

README 把两条核心 pipeline 也写得非常清楚：

- Clip Generator:
  `Ingest -> Transcribe -> Detect -> Analyze -> Extract -> Reframe -> Effects -> Publish`
- AI Shorts:
  `Analyze -> Script -> Actor -> Voice -> Video -> B-roll -> Composite -> Gallery -> Publish`

#### 技术结构

它公开的技术栈是：

- Backend: `Python 3.11 + FastAPI`
- Frontend: `React 18 + Vite + Tailwind`
- AI APIs: `Gemini / fal.ai / ElevenLabs`
- Infra: `Docker + AWS S3`

#### 对我们的启发

- 这是离 `SoraTK` 最近的开源参照，因为它已经把“短视频生产 + AI UGC + 发布”连起来了。
- 它证明这类产品的主结构完全可以按“业务流水线”来设计，而不是先按模型能力拆。
- 如果我们未来要做 MVP，`OpenShorts` 是最值得借鉴的开源产品结构。

### 6.4 Vinci Clips

#### 它是什么

`Vinci Clips` 更聚焦在一个单点能力：

`长视频 -> AI 分析 -> 自动切片 -> 短视频分发`

#### 仓库结构

README 直接给出了项目结构：

- `backend/src/models`
- `backend/src/routes`
- `frontend/src/app`
- `frontend/src/components`
- `frontend/src/lib`

它的架构是很标准的双层：

- Frontend: `Next.js`
- Backend: `Express`
- Data: `MongoDB`
- AI: `Gemini`
- Media: `FFmpeg`

#### 对我们的启发

- 如果只聚焦一个闭环，系统结构可以很轻，不需要一上来就做大而全平台。
- 对 MVP 来说，这种“前后端清晰分层 + 单一强闭环”的做法非常适合快速验证。

## 7. 从这些产品里抽出来的共同结构

把 `SoraTK + Creatify + Arcads + HeyGen + InVideo + OpenShorts + OpenMontage + ComfyUI` 放在一起看，可以归纳出一个很稳定的行业结构。

### 7.1 产品层共同结构

#### 第一层：需求入口

用户通常不会先想“我要配一个工作流”。
用户的真实入口通常是下面几类之一：

- 给你一个链接
- 给你一个商品页
- 给你一个产品描述
- 给你一个长视频
- 给你一个脚本

#### 第二层：理解与拆解

这一层的核心不是生成，而是理解：

- 抓取商品信息
- 解析链接素材
- 转写音视频
- 分析爆款结构
- 提取卖点和脚本骨架

#### 第三层：创意生成

这一层才开始出现：

- 脚本生成
- 角色/头像选择
- 视觉模板选择
- 情绪与语言风格控制
- B-roll 和字幕方案

#### 第四层：编排与渲染

这里才是工作流、节点、组合、导出。

#### 第五层：资产与分发

- 历史记录
- 案例库
- 角色库
- 模板库
- 社交平台发布
- SEO/公开 gallery

### 7.2 技术层共同结构

从开源项目结构看，几乎都能还原成下面 6 层：

1. `Frontend`
   输入、配置、预览、历史、案例、工作流 UI
2. `Orchestration`
   任务编排、状态机、队列、重试、步骤跟踪
3. `Media/AI Workers`
   抓取、转写、分析、生成、字幕、合成、渲染
4. `Provider Adapters`
   Gemini、OpenAI、fal.ai、ElevenLabs、视频模型供应商
5. `Storage`
   文件、缩略图、产物、角色素材、模板、日志
6. `Data & Control`
   用户、积分、权限、项目、历史、评估、监控

### 7.3 行业已经验证的关键设计原则

1. `入口必须简单`
   URL、链接、脚本、上传文件，是最自然的入口。
2. `中间步骤必须可见`
   自动生成不代表全黑盒，用户需要能看到脚本、角色、镜头方案。
3. `最终一定会走向批量化`
   单条视频只是起点，广告业务最终要做多变体。
4. `角色和模板会成为资产`
   一旦产品做深，就不只是“生成一次”，而是“沉淀可复用资产”。
5. `供应商稳定性是核心风险`
   商业产品都高度依赖外部模型，所以容错和回退很关键。

## 8. 对全新项目的产品建议

### 8.1 我建议我们不要照搬 SoraTK

`SoraTK` 值得参考，但不适合直接照抄。原因很简单：

- 它已经开始平台化，首版范围偏大
- 它的工作流入口对新用户不够友好
- 它的高价值能力依赖上游稳定性

### 8.2 我建议我们先做哪条闭环

如果要做首版，我建议只做这一条：

`短视频链接 / 商品链接输入 -> 内容分析 -> 自动生成脚本与镜头方案 -> 进入预填充工作流 -> 一键生成结果`

这个方案有几个好处：

- 它保留了强入口价值
- 它保留了高价值分析环节
- 它让工作流存在，但不是空白画布
- 它足够接近未来平台形态，又不会一开始太重

### 8.3 MVP 模块建议

#### Phase 1: 必做

- 链接输入与解析
- 商品/视频内容抽取
- 脚本与镜头拆解
- 预填充工作流
- 基础生成结果页
- 历史记录

#### Phase 2: 很快会需要

- 案例库
- 模板库
- 角色库
- 多语言
- 多变体生成

#### Phase 3: 平台化能力

- 批量生成
- API
- 发布分发
- 团队协作
- 实验与效果评估

### 8.4 我建议我们先别做什么

1. 不要首版就把用户扔进空白节点画布。
2. 不要首版就做过于泛化的“什么视频都能做”。
3. 不要首版就做太多模型入口和供应商暴露给用户。
4. 不要先做“展示型案例库”，而忽略真正的闭环产出。

## 9. 对全新项目的技术结构建议

如果基于这次调研来反推一个更稳的技术结构，我会建议按下面方式拆：

### 9.1 前端层

- `workspace`
  工作区、项目、历史、模板入口
- `intake`
  链接输入、文件上传、商品信息确认
- `analysis`
  爆款拆解、脚本、卖点、镜头方案
- `workflow`
  预填充流程，而不是默认空白
- `result`
  预览、下载、版本对比

### 9.2 编排层

- job orchestration
- step state
- retry / fallback
- provider routing
- credit / quota accounting

### 9.3 能力层

- link parser
- transcript / OCR / ASR
- script planner
- shot planner
- avatar / voice / subtitle
- renderer / compositor

### 9.4 数据层

- projects
- assets
- templates
- characters
- runs
- logs
- billing / credits

### 9.5 为什么这样拆

因为这次调研已经很清楚地告诉我们：

- 商业竞品最终都在做“流程编排”
- 开源项目最终都在做“能力解耦”
- 真正的产品差异，不在某一个模型，而在入口、编排、资产和稳定性

## 10. 最终结论

如果只看 `SoraTK`，我们容易以为自己要做的是一个“爆款复刻网站”。

但把全网产品和 GitHub 开源项目一起看完以后，更准确的判断是：

`我们真正要做的，不是一个单点工具，而是一条 AI 视频生产主链路。`

这条主链路里，最值得先做出来的不是“最多功能”，而是：

- 一个强入口
- 一个强分析
- 一个不让用户迷路的工作流承接
- 一个能沉淀资产的结果系统

如果后面继续推进，我建议下一份文档直接进入：

`全新项目 MVP 定义 + PRD 初稿`

## 11. 参考来源

### SoraTK 实测

- `soratk.com` 登录态手动实测，覆盖首页、去水印、爆款复刻、工作流画布、带货案例、历史、角色工坊、会员与配置秘钥。

### 商业产品官方资料

- [Creatify 官方首页](https://creatify.ai/)
- [Creatify API Introduction](https://docs.creatify.ai/introduction)
- [Creatify URL to Video 用例文档](https://docs.creatify.ai/use-case/url-to-video)
- [Creatify Batch Mode](https://creatify.ai/features/batch-mode)
- [Arcads 官方首页](https://www.arcads.ai/)
- [HeyGen URL to Video](https://www.heygen.com/tool/url-to-video)
- [InVideo 官方首页](https://invideo.io/)
- [InVideo AI Video Generator](https://invideo.io/make/ai-video-generator/)

### GitHub 开源项目

- [ComfyUI](https://github.com/Comfy-Org/ComfyUI)
- [ComfyUI workflow templates](https://github.com/Comfy-Org/workflow_templates)
- [OpenMontage](https://github.com/calesthio/OpenMontage)
- [OpenShorts](https://github.com/mutonby/openshorts)
- [Vinci Clips](https://github.com/tryvinci/vinci-clips)
