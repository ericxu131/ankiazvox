import { BRAND, FEATURES, INSTALL_SNIPPET, STEPS, SYNC_SNIPPET } from './brand'
import { MarketingFooter } from './components/MarketingFooter'
import { MarketingHeader } from './components/MarketingHeader'
import './App.css'

function CodeBlock({ code }: { code: string }) {
  return (
    <pre className="code-block">
      <code>{code}</code>
    </pre>
  )
}

export default function App() {
  return (
    <div className="home-page" id="top">
      <MarketingHeader />

      <main>
        <section className="home-hero">
          <div className="home-hero-glow" aria-hidden />
          <div className="home-container home-hero-inner">
            <div className="home-hero-copy">
              <span className="home-badge">CLI · AnkiConnect · Azure Neural TTS</span>
              <h1 className="home-hero-title">
                让 Anki 卡片
                <span className="home-hero-title-accent"> 听见自然语音</span>
              </h1>
              <p className="home-hero-subtitle">
                批量为笔记生成高质量朗读音频，把纯文字 deck 变成可听可记的学习伴侣——自己学语言时在用的工具。
              </p>
              <div className="home-hero-actions">
                <a className="btn btn-primary btn-lg" href="#install">
                  安装并开始
                </a>
                <a className="btn btn-secondary btn-lg" href="#features">
                  了解特性
                </a>
              </div>
            </div>

            <div className="home-hero-visual" aria-hidden>
              <div className="home-mock-card float-a">
                <div className="home-mock-card-label">Anki 卡片</div>
                <p className="home-mock-card-front">serendipity</p>
                <div className="home-mock-card-audio">
                  <span className="home-mock-play" />
                  <span className="home-mock-wave">
                    <i /><i /><i /><i /><i />
                  </span>
                </div>
              </div>
              <div className="home-mock-terminal float-b">
                <div className="home-mock-terminal-bar">
                  <span /><span /><span />
                </div>
                <pre className="home-mock-terminal-body">
                  <span className="prompt">$</span> azv sync -q deck:English
                  {'\n'}
                  <span className="ok">✓ 128 notes · 128 audio</span>
                </pre>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="home-section">
          <div className="home-container">
            <div className="home-section-head">
              <h2>为沉浸式学习而设计</h2>
              <p>不是炫技的 TTS 封装——每一条能力都服务于「听 card、记单词」的真实流程。</p>
            </div>
            <div className="home-feature-grid">
              {FEATURES.map((item) => (
                <article key={item.title} className="home-feature-card">
                  <span className="home-feature-icon" aria-hidden>
                    {item.icon}
                  </span>
                  <h3>{item.title}</h3>
                  <p>{item.desc}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="workflow" className="home-section home-section--muted">
          <div className="home-container">
            <div className="home-section-head">
              <h2>三步上手</h2>
              <p>从配置到批量同步，流程克制、可预期。</p>
            </div>
            <ol className="home-steps">
              {STEPS.map((step) => (
                <li key={step.num}>
                  <span className="home-step-num">{step.num}</span>
                  <div className="home-step-body">
                    <strong>{step.title}</strong>
                    <span>{step.desc}</span>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section id="install" className="home-section">
          <div className="home-container home-install">
            <div className="home-section-head home-section-head--left">
              <h2>安装与快速开始</h2>
              <p>
                需要 Anki Desktop + AnkiConnect 插件，以及 Azure Speech 订阅（有免费额度）。
              </p>
            </div>
            <div className="home-install-grid">
              <div className="home-install-block">
                <h3>安装</h3>
                <CodeBlock code={INSTALL_SNIPPET} />
                <p className="home-install-hint">然后运行 <code>azv init</code> 完成交互式配置。</p>
              </div>
              <div className="home-install-block">
                <h3>同步示例</h3>
                <CodeBlock code={SYNC_SNIPPET} />
                <p className="home-install-hint">
                  多字段、语速、并发等用法见{' '}
                  <a href={BRAND.github} target="_blank" rel="noreferrer">
                    GitHub README
                  </a>
                  。
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="home-cta-band">
          <div className="home-container home-cta-inner">
            <h2>把 deck 变成可听可记</h2>
            <p>{BRAND.tagline} — 为真实生活而造的学习工具。</p>
            <a className="btn btn-primary btn-lg" href="#install">
              查看安装步骤
            </a>
          </div>
        </section>
      </main>

      <MarketingFooter />
    </div>
  )
}
