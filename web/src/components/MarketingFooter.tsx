import { BRAND } from '../brand'

export function MarketingFooter() {
  const year = new Date().getFullYear()

  return (
    <footer className="marketing-footer">
      <div className="marketing-footer-inner home-container">
        <div className="marketing-footer-brand">
          <span className="marketing-footer-name">{BRAND.name}</span>
          <span className="marketing-footer-tagline">为真实生活而造 · 沉浸式学习</span>
        </div>
        <div className="marketing-footer-links">
          <a href="https://apps.pisikeji.com/">Eric&apos;s Apps</a>
          <a href={BRAND.github} target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a href="#features">特性</a>
          <a href="#install">安装</a>
        </div>
        <p className="marketing-footer-copy">
          © {year} pisikeji · v{BRAND.version} · MIT
        </p>
      </div>
    </footer>
  )
}
