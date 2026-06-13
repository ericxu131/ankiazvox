const VERSION = '0.6.0'

export const GITHUB_URL = 'https://github.com/ericxu131/ankiazvox'

export const BRAND = {
  name: 'azv',
  tagline: '让 Anki 卡片听见自然语音',
  version: VERSION,
  github: GITHUB_URL,
} as const

export const FEATURES = [
  {
    icon: '◉',
    title: '神经网络语音',
    desc: 'Azure Neural TTS，接近真人的发音与韵律，让听 card 像听母语者朗读。',
  },
  {
    icon: '↻',
    title: '批量同步',
    desc: '按 Anki 搜索条件一键生成音频，多字段映射，并发加速大批量 deck。',
  },
  {
    icon: '♪',
    title: '韵律可控',
    desc: '语速、音高可调——复杂句式放慢听清，关键词略提音调加深印象。',
  },
  {
    icon: '▤',
    title: 'SSML 友好',
    desc: '自动清理 HTML、保留换行停顿；高级用户可直接写 SSML 精细控制。',
  },
] as const

export const STEPS = [
  { num: '1', title: '初始化', desc: 'azv init 连接 Azure 与 AnkiConnect，选好默认音色。' },
  { num: '2', title: '试听', desc: 'azv sample 预览不同 neural voice，找到最适合的语言材料。' },
  { num: '3', title: '同步', desc: 'azv sync 批量写入 [sound:...] 标签，卡片即刻可听。' },
] as const

export const INSTALL_SNIPPET = 'pip install ankiazvox'

export const SYNC_SNIPPET = `azv sync -q "deck:English::Vocabulary" \\
  -s "Front" -t "Audio"`
