import Link from "next/link";

import { createRenderRunAction } from "./actions";
import {
  getHistory,
  getProject,
  getProjectAnalysis,
  getProjectResult,
  getProjectWorkflow,
  getRenderRun
} from "../../../lib/api";
import {
  formatCost,
  formatDateTime,
  formatRunStatusLabel,
  formatSourceTypeLabel,
  formatStageLabel,
  runToneClass,
  stageToneClass
} from "../../../lib/format";

export const dynamic = "force-dynamic";

type Params = Promise<{ projectId: string }>;
type SearchParams = Promise<Record<string, string | string[] | undefined>>;

const stageFlow = [
  "draft",
  "analysis_ready",
  "workflow_ready",
  "render_pending",
  "result_ready"
] as const;

function readSearchValue(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function getStageSummary(stage: (typeof stageFlow)[number] | "analysis_pending" | "failed") {
  switch (stage) {
    case "draft":
      return "项目刚创建完成，下一步是补齐分析结果。";
    case "analysis_ready":
      return "分析已经就绪，可以继续查看脚本和镜头规划。";
    case "workflow_ready":
      return "工作流草稿已经可执行，可以直接发起一次运行。";
    case "render_pending":
      return "最近一次运行已经排队，当前重点是盯住运行状态和结果产出。";
    case "result_ready":
      return "结果资产已经挂上主链，当前可以进入复盘或继续生成下一版。";
    case "analysis_pending":
      return "系统正在分析素材，等待结果回填到工作台。";
    case "failed":
      return "主链在某一步失败了，建议先看最近运行和错误位置。";
    default:
      return "当前主链状态已经记录，可继续沿既有工作台往下走。";
  }
}

function getResultSummary(hasAsset: boolean, currentStage: string) {
  if (hasAsset) {
    return "结果资产已经生成，当前页面可以直接拿到结果锚点。";
  }

  if (currentStage === "render_pending") {
    return "运行已经发起，但结果资产还没挂回来。";
  }

  return "结果资产还没生成，这一层目前只显示稳定占位。";
}

export default async function ProjectDetailPage({
  params,
  searchParams
}: {
  params: Params;
  searchParams: SearchParams;
}) {
  const { projectId } = await params;
  const resolvedSearchParams = await searchParams;
  const errorCode = readSearchValue(resolvedSearchParams.error);

  const initialProjectResponse = await getProject(projectId);

  if (!initialProjectResponse?.project) {
    return (
      <main className="page">
        <section className="hero">
          <p className="eyebrow">Project Missing</p>
          <h1>这个项目还没有被 API 返回出来</h1>
          <p className="hero-copy">如果你刚创建项目但这里看不到，通常是 API 还没启动，或者当前项目 ID 不存在。</p>
          <div className="hero-actions">
            <Link href="/projects/new" className="button-link button-primary">
              返回新建项目
            </Link>
          </div>
        </section>
      </main>
    );
  }

  const [analysisResponse, workflowResponse, resultResponse, historyResponse] = await Promise.all([
    getProjectAnalysis(projectId),
    getProjectWorkflow(projectId),
    getProjectResult(projectId),
    getHistory()
  ]);

  const refreshedProject = (await getProject(projectId))?.project ?? initialProjectResponse.project;
  const latestRunId = refreshedProject.latestRenderRunId;
  const runResponse = latestRunId ? await getRenderRun(projectId, latestRunId) : null;
  const historyItems = historyResponse?.items.filter((item) => item.projectId === projectId) ?? [];
  const latestHistoryItem = historyItems[0] ?? null;
  const workflow = workflowResponse?.workflow ?? null;
  const renderAction = workflow ? createRenderRunAction.bind(null, projectId, workflow.id) : null;
  const latestRunStatus = runResponse?.run.status ?? latestHistoryItem?.status ?? null;
  const latestRunLabel = latestRunStatus ? formatRunStatusLabel(latestRunStatus) : "待发起";
  const latestRunTone = latestRunStatus ? runToneClass(latestRunStatus) : "tone-neutral";
  const latestRunUpdatedAt = runResponse?.run.completedAt ?? runResponse?.run.createdAt ?? latestHistoryItem?.updatedAt ?? null;
  const hasResultAsset = Boolean(resultResponse?.asset);
  const resultTone = hasResultAsset ? "tone-success" : refreshedProject.currentStage === "render_pending" ? "tone-progress" : "tone-neutral";

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-grid">
          <div>
            <div className="breadcrumbs">
              <Link href="/">总览</Link>
              <span>/</span>
              <Link href="/history">历史</Link>
              <span>/</span>
              <span>{refreshedProject.title}</span>
            </div>
            <p className="eyebrow">Project Workspace</p>
            <h1>{refreshedProject.title}</h1>
            <p className="hero-copy">
              这是当前主链的项目工作台。页面按统一 contract 读取项目、分析结果、工作流、运行状态和结果，后续新增节点或 provider 时，都应该在这里沿既有分层接入。
            </p>
            <div className="hero-actions">
              <span className={`status-pill ${stageToneClass(refreshedProject.currentStage)}`}>{formatStageLabel(refreshedProject.currentStage)}</span>
              <span className="tag">{formatSourceTypeLabel(refreshedProject.sourceType)}</span>
              <span className="tag mono">{refreshedProject.id}</span>
            </div>
            {errorCode ? <div className="banner">本次渲染运行没有成功发起，通常是 API 暂时不可用。恢复后重新点击一次即可。</div> : null}
          </div>
          <div className="hero-stat-grid">
            <article className="metric-card">
              <p className="metric-label">当前阶段</p>
              <p className="metric-value">{formatStageLabel(refreshedProject.currentStage)}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">最近更新</p>
              <p className="metric-value">{formatDateTime(refreshedProject.updatedAt)}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Low-Code Graph</p>
              <p className="metric-value">{workflow?.lowCodeGraph.nodes.length ?? 0} nodes</p>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Workspace Snapshot</p>
            <h2 className="section-title">先看总览，再看细节</h2>
            <p className="section-copy">这一层只负责回答 3 个问题：项目现在在哪、最近一次运行到哪、结果资产有没有回来。</p>
          </div>
        </div>
        <div className="snapshot-grid">
          <article className="card snapshot-card">
            <div className="snapshot-head">
              <p className="eyebrow">Current Stage</p>
              <span className={`status-pill ${stageToneClass(refreshedProject.currentStage)}`}>{formatStageLabel(refreshedProject.currentStage)}</span>
            </div>
            <h3 className="snapshot-value">{formatStageLabel(refreshedProject.currentStage)}</h3>
            <p className="snapshot-copy">{getStageSummary(refreshedProject.currentStage)}</p>
            <p className="snapshot-detail">最近更新时间：{formatDateTime(refreshedProject.updatedAt)}</p>
          </article>

          <article className="card snapshot-card">
            <div className="snapshot-head">
              <p className="eyebrow">Latest Run</p>
              <span className={`status-pill ${latestRunTone}`}>{latestRunLabel}</span>
            </div>
            <h3 className="snapshot-value">{runResponse?.run.provider ?? latestHistoryItem?.runType ?? "还没发起运行"}</h3>
            <p className="snapshot-copy">
              {runResponse
                ? "最近一次运行详情已经被工作台捕获，可以继续往下看步骤和成本。"
                : latestHistoryItem
                  ? "历史里已经有最近一次运行，但当前详情还没挂到项目主链上。"
                  : "这个项目还没有独立运行记录，工作流准备好后可以直接发起。"}
            </p>
            <p className="snapshot-detail">
              {latestRunUpdatedAt ? `最近运行时间：${formatDateTime(latestRunUpdatedAt)}` : "最近运行时间：未生成"}
            </p>
          </article>

          <article className="card snapshot-card">
            <div className="snapshot-head">
              <p className="eyebrow">Result Status</p>
              <span className={`status-pill ${resultTone}`}>{hasResultAsset ? "结果已挂载" : "等待结果"}</span>
            </div>
            <h3 className="snapshot-value">{hasResultAsset ? resultResponse?.asset?.assetType : "暂无结果资产"}</h3>
            <p className="snapshot-copy">{getResultSummary(hasResultAsset, refreshedProject.currentStage)}</p>
            <p className="snapshot-detail">
              {resultResponse?.asset?.storageKey ? `结果锚点：${resultResponse.asset.storageKey}` : "结果锚点：等待运行完成后生成"}
            </p>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Stage Flow</p>
            <h2 className="section-title">项目当前所处主链节点</h2>
          </div>
        </div>
        <div className="card">
          <div className="flow-list">
            {stageFlow.map((stage, index) => (
              <div
                key={stage}
                className={`flow-step${stage === refreshedProject.currentStage ? " active" : ""}`}
              >
                <div className="flow-label">
                  <span className="flow-index">{index + 1}</span>
                  <span>{formatStageLabel(stage)}</span>
                </div>
                <span className="small-copy">{stage === refreshedProject.currentStage ? "当前节点" : "已预留"}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Project Metadata</p>
            <h2 className="section-title">项目元信息和运行锚点</h2>
          </div>
        </div>
        <div className="card-grid">
          <article className="card">
            <div className="meta-list">
              <div className="meta-row">
                <span className="meta-label">创建时间</span>
                <span className="meta-value">{formatDateTime(refreshedProject.createdAt)}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">分析 Run</span>
                <span className="meta-value mono">{refreshedProject.latestAnalysisRunId ?? "待生成"}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">工作流 Draft</span>
                <span className="meta-value mono">{refreshedProject.latestWorkflowDraftId ?? "待生成"}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">渲染 Run</span>
                <span className="meta-value mono">{refreshedProject.latestRenderRunId ?? "待发起"}</span>
              </div>
            </div>
          </article>
          <article className="card">
            <p className="eyebrow">Governance</p>
            <h3 className="card-title">当前页面承担的职责</h3>
            <ul className="list">
              <li>消费标准 contract，不直接拼接 provider 细节</li>
              <li>把分析、工作流、运行、结果收束在同一条可追踪主链里</li>
              <li>为后续低代码编辑、版本记录和权限治理保留稳定挂点</li>
            </ul>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Analysis</p>
            <h2 className="section-title">结构化分析结果</h2>
          </div>
        </div>
        {analysisResponse ? (
          <div className="card-grid">
            <article className="card">
              <p className="eyebrow">Target Audience</p>
              <h3 className="card-title">目标人群</h3>
              <div className="tag-list">
                {analysisResponse.insights.targetAudience.map((item) => (
                  <span key={item} className="tag">
                    {item}
                  </span>
                ))}
              </div>
            </article>
            <article className="card">
              <p className="eyebrow">Selling Points</p>
              <h3 className="card-title">核心卖点</h3>
              <div className="tag-list">
                {analysisResponse.insights.sellingPoints.map((item) => (
                  <span key={item} className="tag">
                    {item}
                  </span>
                ))}
              </div>
            </article>
            <article className="card">
              <p className="eyebrow">Hooks</p>
              <h3 className="card-title">前三秒抓手</h3>
              <ul className="list">
                {analysisResponse.insights.hooks.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article className="card">
              <p className="eyebrow">CTA</p>
              <h3 className="card-title">建议行动</h3>
              <p className="card-copy">{analysisResponse.insights.cta}</p>
              <div className="tag-list">
                <span className={`status-pill ${runToneClass(analysisResponse.run.status)}`}>{formatRunStatusLabel(analysisResponse.run.status)}</span>
                <span className="tag">{analysisResponse.run.provider}</span>
                <span className="tag mono">{analysisResponse.run.promptVersion}</span>
              </div>
            </article>
          </div>
        ) : (
          <div className="empty-state">分析结果暂时不可用。API 恢复后，这里会直接显示标准化 insights 和分析 run 元数据。</div>
        )}
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Workflow Draft</p>
            <h2 className="section-title">预填充工作流与低代码图</h2>
          </div>
        </div>
        {workflow ? (
          <div className="panel-stack">
            <div className="split-card">
              <article className="card">
                <p className="eyebrow">Workflow Meta</p>
                <div className="meta-list">
                  <div className="meta-row">
                    <span className="meta-label">Draft 版本</span>
                    <span className="meta-value">v{workflow.version}</span>
                  </div>
                  <div className="meta-row">
                    <span className="meta-label">语言</span>
                    <span className="meta-value">{workflow.meta.language}</span>
                  </div>
                  <div className="meta-row">
                    <span className="meta-label">风格</span>
                    <span className="meta-value">{workflow.meta.style}</span>
                  </div>
                  <div className="meta-row">
                    <span className="meta-label">语气</span>
                    <span className="meta-value">{workflow.meta.tone}</span>
                  </div>
                </div>
              </article>
              <article className="card">
                <p className="eyebrow">Render Entry</p>
                <h3 className="card-title">从工作流直接发起运行</h3>
                <p className="card-copy">当前仍是 stub 运行，但这一步已经按独立 action 和 contract 预留好了，将来接队列、重试、预算与审计时不需要重做入口。</p>
                <div className="button-row">
                  {renderAction ? (
                    <form action={renderAction}>
                      <button type="submit" className="button">
                        发起一次渲染运行
                      </button>
                    </form>
                  ) : null}
                </div>
              </article>
            </div>

            <div className="card-grid">
              {workflow.segments.map((segment) => (
                <article key={segment.id} className="card">
                  <p className="eyebrow">{segment.goal}</p>
                  <h3 className="card-title">{segment.script}</h3>
                  <p className="small-copy">时长：{segment.durationSec}s</p>
                  <div className="tag-list">
                    {segment.shots.map((shot) => (
                      <span key={shot.id} className="tag">
                        {shot.subtitle}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>

            <div className="split-card">
              <article className="card">
                <p className="eyebrow">Low-Code Nodes</p>
                <h3 className="card-title">节点配置</h3>
                <div className="node-list">
                  {workflow.lowCodeGraph.nodes.map((node) => (
                    <div key={node.id} className="node-card">
                      <div className="node-head">
                        <div>
                          <p className="node-kind">{node.kind}</p>
                          <strong>{node.label}</strong>
                        </div>
                        <span className="tag mono">{node.id}</span>
                      </div>
                      <div className="key-value-list">
                        {Object.entries(node.config).map(([key, value]) => (
                          <div key={key} className="key-value-row">
                            <span className="key-label">{key}</span>
                            <span className="key-value mono">{String(value)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </article>
              <article className="card">
                <p className="eyebrow">Graph Edges</p>
                <h3 className="card-title">节点流向</h3>
                <p className="card-copy">首版不做空白画布，但会把 graph 作为可演进的低代码结构保留下来，让后面能平稳接编辑器、模板化和策略编排。</p>
                <div className="edge-list">
                  {workflow.lowCodeGraph.edges.map((edge) => (
                    <span key={edge.id} className="edge-chip">
                      <span className="mono">{edge.from}</span>
                      <span>→</span>
                      <span className="mono">{edge.to}</span>
                    </span>
                  ))}
                </div>
              </article>
            </div>
          </div>
        ) : (
          <div className="empty-state">工作流草稿暂时不可用。当前页面已经按 `WorkflowDraft` contract 和 low-code graph 结构预留完成。</div>
        )}
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Run And Result</p>
            <h2 className="section-title">运行状态、步骤和产出锚点</h2>
          </div>
        </div>
        <div className="split-card">
          <article className="card">
            <p className="eyebrow">Latest Run</p>
            <h3 className="card-title">当前最新运行</h3>
            {runResponse ? (
              <>
                <div className="tag-list">
                  <span className={`status-pill ${runToneClass(runResponse.run.status)}`}>{formatRunStatusLabel(runResponse.run.status)}</span>
                  <span className="tag">{runResponse.run.provider}</span>
                  <span className="tag mono">{runResponse.run.id}</span>
                </div>
                <div className="meta-list">
                  <div className="meta-row">
                    <span className="meta-label">创建时间</span>
                    <span className="meta-value">{formatDateTime(runResponse.run.createdAt)}</span>
                  </div>
                  <div className="meta-row">
                    <span className="meta-label">完成时间</span>
                    <span className="meta-value">{formatDateTime(runResponse.run.completedAt)}</span>
                  </div>
                  <div className="meta-row">
                    <span className="meta-label">估算成本</span>
                    <span className="meta-value">{formatCost(runResponse.run.usage.estimatedCostUsd)}</span>
                  </div>
                </div>
                <div className="node-list">
                  {runResponse.steps.map((step) => (
                    <div key={step.name} className="node-card">
                      <div className="node-head">
                        <strong>{step.name}</strong>
                        <span className={`status-pill ${runToneClass(step.status)}`}>{formatRunStatusLabel(step.status)}</span>
                      </div>
                      <div className="key-value-list">
                        <div className="key-value-row">
                          <span className="key-label">能力</span>
                          <span className="key-value">{step.capability}</span>
                        </div>
                        <div className="key-value-row">
                          <span className="key-label">Provider</span>
                          <span className="key-value">{step.provider ?? "-"}</span>
                        </div>
                        <div className="key-value-row">
                          <span className="key-label">开始时间</span>
                          <span className="key-value">{formatDateTime(step.startedAt)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="empty-state">这个项目还没有最新运行详情。工作流准备好之后，就可以在上方直接发起一次渲染运行。</div>
            )}
          </article>

          <article className="card">
            <p className="eyebrow">Result Asset</p>
            <h3 className="card-title">当前结果锚点</h3>
            {resultResponse?.asset ? (
              <div className="meta-list">
                <div className="meta-row">
                  <span className="meta-label">资产类型</span>
                  <span className="meta-value">{resultResponse.asset.assetType}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">Storage Key</span>
                  <span className="meta-value mono">{resultResponse.asset.storageKey}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">Preview Key</span>
                  <span className="meta-value mono">{resultResponse.asset.previewStorageKey ?? "无"}</span>
                </div>
              </div>
            ) : (
              <div className="empty-state">当前还没有结果资产。后续接真实渲染链路时，这里继续使用同一个 `ProjectResultResponse` contract 收口。</div>
            )}
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">History</p>
            <h2 className="section-title">项目历史与后续治理挂点</h2>
          </div>
        </div>
        {historyItems.length > 0 ? (
          <div className="history-list">
            {historyItems.map((item) => (
              <article key={item.runId} className="history-item">
                <div className="tag-list">
                  <span className={`status-pill ${runToneClass(item.status)}`}>{formatRunStatusLabel(item.status)}</span>
                  <span className="tag">{item.runType}</span>
                  <span className="tag mono">{item.runId}</span>
                </div>
                <p className="small-copy">更新时间：{formatDateTime(item.updatedAt)}</p>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">当前项目还没有独立历史记录，这一层已经接到统一 history contract，可继续承载审计和回放能力。</div>
        )}
      </section>
    </main>
  );
}
