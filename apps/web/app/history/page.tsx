import Link from "next/link";

import { getHistory } from "../../lib/api";
import { formatDateTime, formatRunStatusLabel, runToneClass } from "../../lib/format";

export const dynamic = "force-dynamic";

export default async function HistoryPage() {
  const historyResponse = await getHistory();
  const items = historyResponse?.items ?? [];

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-grid">
          <div>
            <p className="eyebrow">History</p>
            <h1>把运行记录做成后续治理和审计的支点</h1>
            <p className="hero-copy">
              历史页现在先展示最小运行记录，但 contract 已经收口。后续不管接重试、版本追踪、预算、审计还是批量运行，都会沿这层继续扩。
            </p>
          </div>
          <div className="hero-stat-grid">
            <article className="metric-card">
              <p className="metric-label">当前记录数</p>
              <p className="metric-value">{items.length}</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">统一 contract</p>
              <p className="metric-value">History DTO</p>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Run Timeline</p>
            <h2 className="section-title">最近运行</h2>
          </div>
        </div>
        {items.length > 0 ? (
          <div className="history-list">
            {items.map((item) => (
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
          <div className="empty-state">当前还没有 API 历史返回。等 API 启动后，这里会直接显示统一的历史记录列表。</div>
        )}
      </section>
    </main>
  );
}
