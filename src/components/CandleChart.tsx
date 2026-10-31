import { useMemo, type CSSProperties } from 'react'

type Candle = { o: number; h: number; l: number; c: number }

// Small seeded PRNG so the chart looks the same on every render.
function rng(seed: number) {
  return () => {
    seed = (seed * 16807) % 2147483647
    return (seed - 1) / 2147483646
  }
}

// Builds a range, a sweep below it, then a continuation leg higher.
function buildCandles(count: number, seed: number): Candle[] {
  const rand = rng(seed)
  const out: Candle[] = []
  let price = 100
  for (let i = 0; i < count; i++) {
    const phase = i / count
    let drift = 0
    if (phase < 0.35) drift = Math.sin(i * 0.9) * 0.6
    else if (phase < 0.45) drift = -1.6
    else if (phase < 0.55) drift = 1.4
    else if (phase < 0.65) drift = -0.5
    else drift = 1.5
    const o = price
    const c = o + drift + (rand() - 0.5) * 2.2
    const h = Math.max(o, c) + rand() * 1.4
    const l = Math.min(o, c) - rand() * 1.4
    out.push({ o, h, l, c })
    price = c
  }
  return out
}

type Props = {
  count?: number
  seed?: number
  height?: number
  annotate?: boolean
}

export function CandleChart({ count = 56, seed = 7, height = 360, annotate = true }: Props) {
  const W = 1000
  const H = height
  const pad = 28
  const candles = useMemo(() => buildCandles(count, seed), [count, seed])

  const lo = Math.min(...candles.map((c) => c.l))
  const hi = Math.max(...candles.map((c) => c.h))
  const y = (v: number) => pad + ((hi - v) / (hi - lo)) * (H - pad * 2)
  const step = (W - pad * 2) / count
  const x = (i: number) => pad + i * step + step / 2

  const sweepIdx = candles.reduce((m, c, i) => (c.l < candles[m].l ? i : m), 0)
  const rangeHigh = Math.max(...candles.slice(0, Math.floor(count * 0.35)).map((c) => c.h))
  const entry = candles[sweepIdx + 3] ?? candles[sweepIdx]
  const last = candles[candles.length - 1]
  const annoDelay = { transitionDelay: `${count * 10 + 600}ms` }
  // The SVG stretches to fit its box, so labels are HTML placed by percentage
  // to keep the text crisp and readable at any size.
  const pct = (v: number, of: number) => `${(v / of) * 100}%`

  return (
    <div className="chart-box">
      <svg className="chart" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img" aria-label="Illustrative gold price chart">
        {[0.2, 0.4, 0.6, 0.8].map((t) => (
          <line key={t} x1={0} x2={W} y1={H * t} y2={H * t} className="chart-grid" />
        ))}

        {annotate && (
          <g className="chart-anno" style={annoDelay}>
            <rect x={pad} width={x(Math.floor(count * 0.35)) - pad} y={y(rangeHigh)} height={y(lo + (hi - lo) * 0.3) - y(rangeHigh)} className="chart-zone" />
            <line x1={pad} x2={W - pad} y1={y(rangeHigh)} y2={y(rangeHigh)} className="chart-level" vectorEffect="non-scaling-stroke" />
            <line x1={x(sweepIdx + 3)} x2={W - pad} y1={y(entry.c)} y2={y(entry.c)} className="chart-entry" vectorEffect="non-scaling-stroke" />
          </g>
        )}

        {candles.map((c, i) => {
          const up = c.c >= c.o
          const bodyTop = y(Math.max(c.o, c.c))
          const bodyH = Math.max(2, Math.abs(y(c.o) - y(c.c)))
          return (
            <g key={i} className={up ? 'candle up' : 'candle down'} style={{ '--c': i } as CSSProperties}>
              <line x1={x(i)} x2={x(i)} y1={y(c.h)} y2={y(c.l)} />
              <rect x={x(i) - step * 0.3} width={step * 0.6} y={bodyTop} height={bodyH} rx={1} />
            </g>
          )
        })}
      </svg>

      {annotate && (
        <div className="chart-anno" style={annoDelay}>
          <span className="chart-label chart-label--above" style={{ left: pct(pad, W), top: pct(y(rangeHigh), H) }}>Range high</span>
          <span className="chart-label chart-label--left" style={{ left: pct(x(sweepIdx), W), top: pct(y(candles[sweepIdx].l), H) }}>Sweep</span>
          <span className="chart-label chart-label--accent chart-label--above" style={{ right: pct(pad, W), top: pct(y(last.h), H) }}>Continuation +2R</span>
        </div>
      )}
    </div>
  )
}
