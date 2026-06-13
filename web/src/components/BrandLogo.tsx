import { BRAND } from '../brand'

type Props = {
  size?: number
  showWordmark?: boolean
}

export function BrandLogo({ size = 36, showWordmark = true }: Props) {
  return (
    <a className="brand-logo brand-logo-link" href="#top" aria-label={BRAND.name}>
      <svg
        className="brand-mark"
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden
      >
        <defs>
          <linearGradient id="azv-brand-gradient" x1="0" y1="0" x2="40" y2="40">
            <stop stopColor="#38bdf8" />
            <stop offset="1" stopColor="#6366f1" />
          </linearGradient>
        </defs>
        <rect width="40" height="40" rx="10" fill="url(#azv-brand-gradient)" />
        <path
          d="M10 20c0-4 2.5-7 6-7v14c-3.5 0-6-3-6-7z"
          fill="#fff"
          fillOpacity="0.95"
        />
        <path
          d="M18 13c4.5 0 8 3.1 8 7s-3.5 7-8 7V13z"
          fill="#fff"
          fillOpacity="0.75"
        />
        <path
          d="M28 17v6c1.5-.8 2.5-2.2 2.5-3s-1-2.2-2.5-3z"
          fill="#fff"
          fillOpacity="0.95"
        />
      </svg>
      {showWordmark && (
        <div className="brand-wordmark">
          <span className="brand-name">{BRAND.name}</span>
          <span className="brand-tagline">{BRAND.tagline}</span>
        </div>
      )}
    </a>
  )
}
