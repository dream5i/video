import Link from "next/link";

import { getHistory, getProject } from "../lib/api";
import {
  formatDateTime,
  formatRunStatusLabel,
  formatSourceTypeLabel,
  formatStageLabel,
  runToneClass,
  stageToneClass
} from "../lib/format";

export const dynamic = "force-dynamic";

const mainFlow = [
  "输入素材或商品信息",
  "结构化分析",
  "预填充工作流",
  "发起运行",
  "查看结果",
  "进入历史"
];

const enterprisePrinciples = [
  {
    title: "可维护",
    copy: "前端只消费标准 contract，页面只做展示和操作， provider、状态机、任务执行从一开始就不散落到 UI。"
  },
  {
    title: "可治理",
    copy: "主链、边界、共享冻结对象、AI 编程规则都已经写进仓库，后续改动有 review 和 ADR 的承接点。"
  },
  {
    title: "可增加新功能",
    copy: "先把能力分层，再补 provider、新节点、新任务类型。后续扩展沿已有接口插入，而不是推倒重来。"
  },
  {
    title: "低代码",
    copy: "首版不用空白画布，而是以预填充 workflow + low-code graph 作为可编辑结构，降低复杂度和治理成本。"
  }
];

export default async function HomePage() {
  const [demoProjectResponse, historyResponse] = await Promise.all([getProject("proj_demo"), getHistory()]);

  const demoProject = demoProjectResponse?.project ?? null;
  const historyItems = historyResponse?.items.slice(0, 4) ?? [];

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-grid">
          <div>
            <p className="eyebrow">Enterprise Build Baseline</p>
            <h1>把 AI 短视频工作台做成一条可长期演进的主链</h1>
            <p className="hero-copy">
              现在这套仓库已经不只是规划稿，而是进入了真正可落地的搭建阶段。主链被冻结为
              <span className="mono"> 输入 - 分析 - 预填充工作流 - 运行 - 结果 - 历史 </span>
              ，并且已经有统一 contract、API 骨架、worker/provider 抽象和低代码 graph 结构可用。
            </p>
            <div className="hero-actions">
              <Link href="/projects/new" className="button-link button-primary">
                新建一个项目
              </Link>
              <Link href="/projects/proj_demo" className="button-link">
                查看演示项目
              </Link>
              <Link href="/history" className="button-link">
                看历史运行
              </Link>
            </div>
          </div>
          <div className="hero-stat-grid">
            <article className="metric-card">
              <p className="metric-label">共享工作语言</p>
              <p className="metric-value">Contracts First</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">低代码承载方式</p>
              <p className="metric-value">Prefilled Graph</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">执行层模式</p>
              <p className="metric-value">API + Worker</p>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Main Flow</p>
            <h2 className="section-title">当前被冻结的主链</h2>
          </div>
          <p className="section-copy">这条链路是接下来所有页面、接口、运行逻辑的唯一优先路径，不围绕它的能力暂时都不进 MVP 主路径。</p>
        </div>
        <div className="card">
          <div className="flow-list">
            {mainFlow.map((step, index) => (
              <div key={step} className={`flow-step${index < 3 ? " active" : ""}`}>
                <div className="flow-label">
                  <span className="flow-index">{index + 1}</span>
                  <span>{step}</span>
                </div>
                <span className="small-copy">{index < 3 ? "已进入代码底座" : "本轮继续打通"}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Demo Project</p>
            <h2 className="section-title">演示项目快照</h2>
          </div>
          <Link href="/projects/proj_demo" className="inline-link">
            进入工作台
          </Link>
        </div>
        {demoProject ? (
          <div className="card-grid">
            <article className="card">
              <p className="eyebrow">Project</p>
              <h3 className="card-title">{demoProject.title}</h3>
              <p className="card-copy">当前用一条演示项目把分析、工作流、结果和历史几个页面都串起来，方便后续边开发边验证主链。</p>
              <div className="tag-list">
                <span className={`status-pill ${stageToneClass(demoProject.currentStage)}`}>{formatStageLabel(demoProject.currentStage)}</span>
                <span className="tag">{formatSourceTypeLabel(demoProject.sourceType)}</span>
              </div>
            </article>
            <article className="card">
              <p className="eyebrow">Metadata</p>
              <div className="meta-list">
                <div className="meta-row">
                  <span className="meta-label">项目 ID</span>
                  <span className="meta-value mono">{demoProject.id}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">最近更新</span>
                  <span className="meta-value">{formatDateTime(demoProject.updatedAt)}</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">最新分析</span>
                  <span className="meta-value mono">{demoProject.latestAnalysisRunId ?? "待生成"}</span>
                </div>
              </div>
            </article>
            <article className="card">
              <p className="eyebrow">Workspace Intent</p>
              <h3 className="card-title">不是宣传页，是可操作工作台</h3>
              <p className="card-copy">下一阶段的所有新增能力都会挂到这个工作台骨架上，而不是继续扩散成彼此割裂的单页原型。</p>
            </article>
          </div>
        ) : (
          <div className="empty-state">当前还没有连上 API 演示数据。前端工作台已经准备好，启动 API 后会自动展示项目快照。</div>
        )}
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Recent Runs</p>
            <h2 className="section-title">最近的运行记录</h2>
          </div>
          <p className="section-copy">历史页是企业级治理的重要观察面。它决定我们之后能不能做回放、排障、审计和版本追踪。</p>
        </div>
        {historyItems.length > 0 ? (
          <div className="history-list">
            {historyItems.map((item) => (
              <article key={item.runId} className="history-item">
                <Link href={`/projects/${item.projectId}`} className="history-link">
                  {item.projectTitle}
                </Link>
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
          <div className="empty-state">历史记录还没有接到 API 响应。这个区域已经预留好统一 contract，不会再走散乱的本地状态。</div>
        )}
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Operating Principles</p>
            <h2 className="section-title">这套底座为什么适合企业级继续往上搭</h2>
          </div>
        </div>
        <div className="card-grid">
          {enterprisePrinciples.map((item) => (
            <article key={item.title} className="card">
              <h3 className="card-title">{item.title}</h3>
              <p className="card-copy">{item.copy}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
