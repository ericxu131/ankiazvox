import { BRAND } from '../brand'
import { BrandLogo } from './BrandLogo'

export function MarketingHeader() {
  return (
    <header className="marketing-header">
      <div className="marketing-header-inner home-container">
        <BrandLogo />
        <nav className="marketing-nav" aria-label="页面导航">
          <a href="#features">特性</a>
          <a href="#workflow">流程</a>
          <a href="#install">安装</a>
          <a href={BRAND.github} target="_blank" rel="noreferrer">
            GitHub
          </a>
        </nav>
        <div className="marketing-header-actions">
          <a
            className="btn btn-secondary marketing-cta-secondary"
            href={BRAND.github}
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
          <a className="btn btn-primary marketing-cta" href="#install">
            开始使用
          </a>
        </div>
      </div>
    </header>
  )
}
