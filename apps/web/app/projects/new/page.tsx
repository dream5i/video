import { createProjectAction } from "./actions";

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

function readSearchValue(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

export default async function NewProjectPage({ searchParams }: { searchParams: SearchParams }) {
  const resolvedSearchParams = await searchParams;
  const errorCode = readSearchValue(resolvedSearchParams.error);

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-grid">
          <div>
            <p className="eyebrow">Project Intake</p>
            <h1>把输入层做成稳定的企业级项目入口</h1>
            <p className="hero-copy">
              这里不是临时收集字段，而是后续所有分析、工作流生成和运行链路的统一起点。当前支持两种入口：爆款链接和商品信息。主链仍然坚持
              <span className="mono"> 预填充 workflow </span>
              ，不做空白画布。
            </p>
          </div>
          <div className="hero-stat-grid">
            <article className="metric-card">
              <p className="metric-label">输入源类型</p>
              <p className="metric-value">2</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">默认画幅</p>
              <p className="metric-value">9:16</p>
            </article>
            <article className="metric-card">
              <p className="metric-label">当前策略</p>
              <p className="metric-value">Contract First</p>
            </article>
          </div>
        </div>

        {errorCode ? (
          <div className="banner">
            项目创建没有成功，通常是因为 API 还没启动或当前服务不可用。等 API 起好后，重新提交一次即可。
          </div>
        ) : null}
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Two Entry Modes</p>
            <h2 className="section-title">用两个稳定入口换后续整个主链的确定性</h2>
          </div>
          <p className="section-copy">两种模式都直接映射到共享的 `CreateProjectRequest` contract，所以后面无论接真实抓取还是更多自动化，都有统一起点。</p>
        </div>
        <div className="form-grid">
          <form action={createProjectAction} className="card">
            <input type="hidden" name="sourceType" value="video_url" />
            <p className="eyebrow">Mode A</p>
            <h2 className="card-title">爆款链接</h2>
            <p className="card-copy">适合先用一个链接快速起项目，后续由分析层抽取卖点、受众和脚本方向。</p>
            <div className="field">
              <label htmlFor="video-title" className="field-label">
                项目标题
              </label>
              <input id="video-title" className="input" name="title" placeholder="例如：小吊梨汤抖音拆解项目" />
            </div>
            <div className="field">
              <label htmlFor="source-url" className="field-label">
                视频链接
              </label>
              <textarea
                id="source-url"
                className="textarea"
                name="sourceUrl"
                placeholder="粘贴视频链接或完整文案。后续可以在这里继续接解析与清洗逻辑。"
              />
            </div>
            <div className="button-row">
              <button type="submit" className="button">
                以爆款链接创建项目
              </button>
            </div>
          </form>

          <form action={createProjectAction} className="card">
            <input type="hidden" name="sourceType" value="product_brief" />
            <p className="eyebrow">Mode B</p>
            <h2 className="card-title">商品信息</h2>
            <p className="card-copy">适合品牌方或内部运营直接用结构化信息起项，后续最容易接模板化、低代码化和批量化扩展。</p>
            <div className="field">
              <label htmlFor="brief-title" className="field-label">
                项目标题
              </label>
              <input id="brief-title" className="input" name="title" placeholder="例如：新品饮品短视频方案" />
            </div>
            <div className="field">
              <label htmlFor="product-name" className="field-label">
                商品名称
              </label>
              <input id="product-name" className="input" name="productName" placeholder="例如：纯粹计划小吊梨汤" />
            </div>
            <div className="field">
              <label htmlFor="target-audience" className="field-label">
                目标人群
              </label>
              <input id="target-audience" className="input" name="targetAudience" placeholder="例如：家庭囤货人群 / 宝妈" />
            </div>
            <div className="field">
              <label htmlFor="selling-points" className="field-label">
                核心卖点
              </label>
              <textarea
                id="selling-points"
                className="textarea"
                name="sellingPoints"
                placeholder="每行一个，或用逗号分隔。例如：梨香浓郁、配料干净、清甜好喝"
              />
            </div>
            <div className="button-row">
              <button type="submit" className="button">
                以商品信息创建项目
              </button>
            </div>
          </form>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <p className="eyebrow">Contract Mapping</p>
            <h2 className="section-title">当前入口层的治理方式</h2>
          </div>
        </div>
        <div className="card-grid">
          <article className="card">
            <h3 className="card-title">字段先服务共享 contract</h3>
            <p className="card-copy">页面字段不是按“好看”来长，而是按 `CreateProjectRequest` 和 `ProductBrief` 来收口，避免 UI 和 API 各玩各的。</p>
          </article>
          <article className="card">
            <h3 className="card-title">先做稳定 schema，再谈自动化扩展</h3>
            <p className="card-copy">后续如果要接链接解析、商品抓取、模板库或外部导入，都先挂在这个入口层，不直接侵入 workflow 和运行层。</p>
          </article>
          <article className="card">
            <h3 className="card-title">低代码先从预填充开始</h3>
            <p className="card-copy">MVP 不做空白画布，而是让分析结果直接派生出可编辑的 workflow draft 和 graph，让后续改动更可控。</p>
          </article>
        </div>
      </section>
    </main>
  );
}
