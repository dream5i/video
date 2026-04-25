import Link from "next/link";

import { getObservabilitySummary } from "../../lib/api";
import { formatCost, formatDateTime, formatRunStatusLabel, runToneClass } from "../../lib/format";

export const dynamic = "force-dynamic";

function formatRate(value: number | null) {
  if (value == null) {
    return "-";
  }

  return `${(value * 100).toFixed(1)}%`;
}

function formatLatency(value: number | null) {
  if (value == null) {
    return "待接入";
  }

  return `${Math.round(value)} ms`;
}

function signalToneClass(status: string) {
  if (status === "ok") {
    return "tone-success";
  }

  if (status === "partial" || status === "attention") {
    return "tone-warn";
  }

  return "tone-neutral";
}

function signalLabel(status: string) {
  if (status === "ok") {
    return "已接线";
  }

  if (status === "partial") {
    return "部分接线";
  }

  if (status === "attention") {
    return "需关注";
  }

  return "待补齐";
}

export default async function ObservabilityPage() {
  const summary = await getObservabilitySummary();

  if (!summary) {
    return (
      <main className="page">
        <section className="hero">
          <div className="hero-grid">
            <div>
              <p className="eyebrow">Observability</p>
              <h1>可观测性面板暂时连不上 API</h1>
              <p className="hero-copy">
                页面壳已经准备好，但当前没有拿到后端汇总接口响应。小白版理解：仪表盘装好了，现在等后端电源接通。
              </p>
            </div>
          </div>
        </section>
        <section className="section">
          <div className="empty-state">请先启动 API，再刷新这个页面查看主链健康、任务状态、provider 与风险信号。</div>
        </section>
      </main>
    );
  }

  const mainChain = summary.mainChain;
  const asyncTasks = summary.asyncTasks;

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-grid">
          <div>
            <p className="eyebrow">Observability</p>
            <h1>把系统状态变成主控可以看懂的仪表盘</h1>
            <p className="hero-copy">
              这个页面不是给用户看的宣传页，而是给开发和运维看的“体检表”。它先回答三件事：主链通不通、运行有没有卡住、外部能力有没有风险。
            </p>
            <div className="hero-actions">
              <Link href="/history" className="button-link button-primary">
                查看运行历史
              </Link>
              <Link href="/projects/proj_demo" className="button-link">
                打开演示项目
              </Link>
            </div>
          </div>
          <div className="hero-stat-grid">
            <article className="metric-card">
              <p className="metric-label">生成时间</p>
              <p className="metric-value">{formatDateTime(summary.generatedAt)}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">Render 成功率</p>
              <p className="metric-value">{formatRate(mainChain.renderSuccessRate)}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">活跃任务</p>
              <p className="metric-value">{asyncTasks.activeRuns}</p>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Main Chain</p>
            <h2 className="section-title">主链健康</h2>
          </div>
          <p className="section-copy">小白版：这是项目的“流水线体检”，看输入、分析、工作流、运行、结果这些关键环节有没有断。</p>
        </div>
        <div className="snapshot-grid">
          <article className="card snapshot-card">
            <p className="eyebrow">Projects</p>
            <p className="snapshot-value">{mainChain.projectsTotal}</p>
            <p className="snapshot-copy">当前项目数。后续接租户和权限后，这里会变成按组织维度看。</p>
          </article>
          <article className="card snapshot-card">
            <p className="eyebrow">Analysis</p>
            <p className="snapshot-value">{formatRate(mainChain.analysisSuccessRate)}</p>
            <p className="snapshot-copy">分析成功率。它代表素材理解这一步是否稳定。</p>
            <p className="snapshot-detail">运行数：{mainChain.analysisRunsTotal}</p>
          </article>
          <article className="card snapshot-card">
            <p className="eyebrow">Workflow</p>
            <p className="snapshot-value">{mainChain.workflowDraftsTotal}</p>
            <p className="snapshot-copy">预填充工作流草稿数。低代码能力会从这里继续扩。</p>
          </article>
          <article className="card snapshot-card">
            <p className="eyebrow">Result</p>
            <p className="snapshot-value">{mainChain.resultAssetsTotal}</p>
            <p className="snapshot-copy">已生成的结果资产数，用来判断运行是否真正产出了可交付物。</p>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Async Tasks</p>
            <h2 className="section-title">异步任务状态</h2>
          </div>
          <p className="section-copy">小白版：异步任务就是“后台慢慢跑”的任务。这里主要防止任务排队、卡死、失败没人知道。</p>
        </div>
        <div className="card-grid">
          <article className="card">
            <h3 className="card-title">队列与卡死</h3>
            <div className="meta-list">
              <div className="meta-row">
                <span className="meta-label">排队中</span>
                <span className="meta-value">{asyncTasks.queuedRuns}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">运行中</span>
                <span className="meta-value">{asyncTasks.runningRuns}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">疑似卡住</span>
                <span className="meta-value">{asyncTasks.stuckRuns}</span>
              </div>
            </div>
          </article>
          <article className="card">
            <h3 className="card-title">运行状态分布</h3>
            <div className="tag-list">
              {mainChain.runStatusCounts.map((item) => (
                <span key={item.status} className={`status-pill ${runToneClass(item.status)}`}>
                  {formatRunStatusLabel(item.status)}：{item.count}
                </span>
              ))}
            </div>
            <p className="snapshot-detail">最近更新时间：{formatDateTime(asyncTasks.latestRunUpdatedAt)}</p>
          </article>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Providers</p>
            <h2 className="section-title">Provider 健康</h2>
          </div>
          <p className="section-copy">小白版：provider 就是外部模型或外部生成服务。这里先看调用量、失败量、成本和延迟有没有明显异常。</p>
        </div>
        <div className="card-grid">
          {summary.providers.map((provider) => (
            <article key={`${provider.capability}-${provider.provider}`} className="card">
              <p className="eyebrow">{provider.capability}</p>
              <h3 className="card-title">{provider.provider}</h3>
              <div className="meta-list">
                <div className="meta-row">
                  <span className="meta-label">总运行</span>
                  <span className="meta-value">{provider.totalRuns}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">失败</span>
                  <span className="meta-value">{provider.failedRuns}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">平均延迟</span>
                  <span className="meta-value">{formatLatency(provider.averageLatencyMs)}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">估算成本</span>
                  <span className="meta-value">{formatCost(provider.estimatedCostUsd)}</span>
                </div>
              </div>
              <p className="snapshot-detail">最近事件：{formatDateTime(provider.lastEventAt)}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Signals</p>
            <h2 className="section-title">接线状态与风险信号</h2>
          </div>
        </div>
        <div className="history-list">
          {summary.signals.map((signal) => (
            <article key={signal.id} className="history-item">
              <div className="node-head">
                <div>
                  <h3 className="card-title">{signal.label}</h3>
                  <p className="card-copy">{signal.detail}</p>
                </div>
                <span className={`status-pill ${signalToneClass(signal.status)}`}>{signalLabel(signal.status)}</span>
              </div>
              {signal.evidence ? <p className="snapshot-detail mono">{signal.evidence}</p> : null}
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Recent Failures</p>
            <h2 className="section-title">最近失败</h2>
          </div>
        </div>
        {summary.recentFailures.length > 0 ? (
          <div className="history-list">
            {summary.recentFailures.map((failure) => (
              <article key={`${failure.runType}-${failure.runId}`} className="history-item">
                <Link href={`/projects/${failure.projectId}`} className="history-link">
                  {failure.projectTitle}
                </Link>
                <div className="tag-list">
                  <span className="status-pill tone-warn">{failure.errorCode}</span>
                  <span className="tag">{failure.provider}</span>
                  <span className="tag mono">{failure.traceId}</span>
                </div>
                <p className="small-copy">{failure.errorMessage ?? "暂无错误详情"}</p>
                <p className="snapshot-detail">更新时间：{formatDateTime(failure.updatedAt)}</p>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">当前没有失败记录。小白版：目前仪表盘没有看到红灯。</div>
        )}
      </section>
    </main>
  );
}
