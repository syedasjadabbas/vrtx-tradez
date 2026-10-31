import { Fragment, useEffect, useRef, useState, type CSSProperties, type MouseEvent } from 'react'
import { CandleChart } from './components/CandleChart'
import { AnalysisMock, CommunityMock, MentorshipMock } from './components/Mocks'
import { ArrowIcon, CheckIcon, DiscordIcon, InstagramIcon, WhatsAppIcon, XIcon } from './components/Icons'
import { daily, faqs, links, nav, partners, pillars, plans, principles, stats, testimonials, trades } from './content'

// Fades sections in as they scroll into view.
function useReveal() {
  useEffect(() => {
    const els = document.querySelectorAll('.reveal')
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('in')
            io.unobserve(e.target)
          }
        }),
      { threshold: 0.12 },
    )
    els.forEach((el) => io.observe(el))
    return () => io.disconnect()
  }, [])
}

function Header() {
  const [open, setOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className={`header${scrolled ? ' scrolled' : ''}${open ? ' open' : ''}`}>
      <div className="container header-inner">
        <a href="#top" className="logo" aria-label="VRTX home">
          <span className="logo-mark"><img src="/vrtx-icon.png" alt="" /></span>
          <span>VRTX</span>
        </a>
        <nav className="nav">
          {nav.map((n) => (
            <a key={n.href} href={n.href} onClick={() => setOpen(false)}>{n.label}</a>
          ))}
        </nav>
        <div className="header-cta">
          <a className="btn btn-ghost" href={links.mentorship} target="_blank" rel="noreferrer">Mentorship</a>
          <a className="btn btn-accent" href={links.discord} target="_blank" rel="noreferrer">Join free</a>
        </div>
        <button className="burger" aria-label="Menu" aria-expanded={open} onClick={() => setOpen(!open)}>
          <span /><span />
        </button>
      </div>
      <div className="mobile-menu">
        {nav.map((n) => (
          <a key={n.href} href={n.href} onClick={() => setOpen(false)}>{n.label}</a>
        ))}
        <a className="btn btn-accent" href={links.discord} target="_blank" rel="noreferrer">Join the Discord</a>
      </div>
    </header>
  )
}

function Hero() {
  return (
    <section className="hero" id="top">
      <div className="hero-glow" aria-hidden="true" />
      <div className="container hero-inner">
        <a className="proof reveal" href="#results">
          <span className="proof-avatars" aria-hidden="true">
            {testimonials.slice(0, 4).map((t) => (
              <span key={t.name}>{t.name[0].toUpperCase()}</span>
            ))}
          </span>
          <span>Trusted by <strong>330+ traders</strong><span className="proof-extra"> in the VRTX community</span></span>
        </a>
        <h1 className="reveal">In pursuit of price.<br /><span className="muted">Guided by time.</span></h1>
        <p className="lead reveal">
          Learn the gold trading process refined by Mirza, with daily analysis, honest trade breakdowns and a
          community built for traders who want consistency over noise.
        </p>
        <div className="hero-ctas reveal">
          <a className="btn btn-accent btn-lg" href={links.discord} target="_blank" rel="noreferrer">
            <DiscordIcon /> Join the Discord
          </a>
          <a className="btn btn-ghost btn-lg" href={links.mentorship} target="_blank" rel="noreferrer">
            1-on-1 mentorship
          </a>
        </div>
      </div>

      <div className="container">
        <div className="window reveal">
          <div className="window-bar">
            <span className="dots"><i /><i /><i /></span>
            <span className="window-url">vrtx · XAUUSD · 5m</span>
            <span className="window-live"><span className="dot" /> Live</span>
          </div>
          <div className="window-body">
            <CandleChart />
          </div>
        </div>
      </div>

      <div className="container stats reveal">
        {stats.map((s) => (
          <div key={s.label} className="stat">
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
    </section>
  )
}

// Splits a heading into words that slide up one after another.
function SplitWords({ text }: { text: string }) {
  return (
    <>
      {text.split(' ').map((w, i) => (
        <Fragment key={i}>
          <span className="w"><span style={{ '--i': i } as CSSProperties}>{w}</span></span>{' '}
        </Fragment>
      ))}
    </>
  )
}

// Moves a soft highlight under the cursor on the mock-ups.
function spotlight(e: MouseEvent<HTMLDivElement>) {
  const r = e.currentTarget.getBoundingClientRect()
  e.currentTarget.style.setProperty('--mx', `${e.clientX - r.left}px`)
  e.currentTarget.style.setProperty('--my', `${e.clientY - r.top}px`)
}

function Approach() {
  const mocks = [<AnalysisMock />, <CommunityMock />, <MentorshipMock />]
  const refs = useRef<(HTMLElement | null)[]>([])

  // Writes into --q how far the next card has slid over each card (0 to 1),
  // which CSS uses to push the covered card back.
  useEffect(() => {
    let raf = 0
    const update = () => {
      raf = 0
      const vh = window.innerHeight
      const cards = refs.current
      cards.forEach((el, i) => {
        const next = cards[i + 1]
        if (!el) return
        if (!next) return el.style.setProperty('--q', '0')
        const stickTop = parseFloat(getComputedStyle(next).top) || 0
        const top = next.getBoundingClientRect().top
        const q = Math.min(1, Math.max(0, (vh - top) / (vh - stickTop)))
        el.style.setProperty('--q', q.toFixed(3))
      })
    }
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(update)
    }
    update()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
    }
  }, [])

  return (
    <section id="approach" className="approach">
      <div className="container">
        <h2 className="center reveal">Three ways to<br /><span className="muted">grow with VRTX.</span></h2>
        <div className="stack">
          {pillars.map((p, i) => (
            <article
              key={p.tag}
              className="stack-card"
              style={{ '--i': i } as CSSProperties}
              ref={(el) => { refs.current[i] = el }}
            >
              <div className="stack-info">
                <div className="pillar-num reveal">
                  <span className="big-mask"><span className="big">{i + 1}</span></span>
                  <span className="tag">({p.tag})</span>
                </div>
                <div>
                  <h3 className="split reveal"><SplitWords text={p.title} /></h3>
                  <p className="reveal reveal--late">{p.body}</p>
                </div>
                <span className="stack-count">0{i + 1} / 0{pillars.length}</span>
              </div>
              <div className="mock-wrap reveal" onMouseMove={spotlight}>{mocks[i]}</div>
            </article>
          ))}
        </div>
      </div>
      <div className="container next-step reveal">
        <h3>Take the next step.</h3>
        <div className="row">
          <a className="btn btn-ghost" href={links.discord} target="_blank" rel="noreferrer">Join free</a>
          <a className="btn btn-ghost" href={links.mentorship} target="_blank" rel="noreferrer">I want more</a>
        </div>
      </div>
    </section>
  )
}

function Philosophy() {
  return (
    <section className="philosophy">
      <div className="container">
        <h2 className="display reveal">Time <span className="accent">&gt;</span> Price</h2>
        <p className="lead center reveal">The idea everything at VRTX is built on.</p>
        <div className="principles">
          {principles.map((p) => (
            <div key={p.n} className="principle reveal">
              <span className="n">{p.n}</span>
              <h4>{p.title}</h4>
              <p>{p.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Trades() {
  return (
    <section id="trades" className="section">
      <div className="container">
        <div className="section-head">
          <h2 className="reveal">Recent trades,<br /><span className="muted">shared in public.</span></h2>
          <a className="link reveal" href={links.x} target="_blank" rel="noreferrer">Follow on X <ArrowIcon /></a>
        </div>
        <div className="trades">
          {trades.map((t) => (
            <a key={t.date} className="trade reveal" href={t.href} target="_blank" rel="noreferrer">
              <div className="trade-top">
                <span className="mock-pill">{t.pair}</span>
                <span className="mock-muted">{t.date}</span>
              </div>
              <strong className="trade-r">{t.result}</strong>
              <span className="trade-note">{t.note}</span>
              <div className="trade-chart"><CandleChart count={28} seed={t.date.length * 13 + 3} height={120} annotate={false} /></div>
            </a>
          ))}
          <a className="trade trade--more reveal" href={links.discord} target="_blank" rel="noreferrer">
            <DiscordIcon size={28} />
            <strong>Every trade is broken down inside the server</strong>
            <span className="link">Join free <ArrowIcon /></span>
          </a>
        </div>
      </div>
    </section>
  )
}

function Daily() {
  return (
    <section className="section">
      <div className="container daily">
        <h2 className="reveal">Trade alongside<br /><span className="muted">me every day.</span></h2>
        <div className="daily-list">
          {daily.map((d, i) => (
            <div key={d.title} className="daily-item reveal">
              <span className="n">{i + 1}</span>
              <div>
                <h4>{d.title}</h4>
                <p>{d.body}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Membership() {
  return (
    <section id="membership" className="section">
      <div className="container">
        <h2 className="center reveal">Start your path to<br /><span className="muted">consistent trading.</span></h2>
        <div className="plans">
          {plans.map((p) => (
            <div key={p.name} className={`plan reveal${p.featured ? ' featured' : ''}`}>
              {p.featured && <span className="badge">Most hands-on</span>}
              <h4>{p.name}</h4>
              <div className="price">
                <strong>{p.price}</strong>
                <span>{p.period}</span>
              </div>
              <ul>
                {p.features.map((f) => (
                  <li key={f}><CheckIcon /> {f}</li>
                ))}
              </ul>
              <div className="plan-ctas">
                <a className={`btn ${p.featured ? 'btn-accent' : 'btn-ghost'} btn-block`} href={p.href} target="_blank" rel="noreferrer">
                  {p.secondary && <InstagramIcon />}{p.cta}
                </a>
                {p.secondary && (
                  <a className="btn btn-ghost btn-block" href={p.secondary.href} target="_blank" rel="noreferrer">
                    <WhatsAppIcon />{p.secondary.cta}
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Results() {
  return (
    <section id="results" className="section">
      <div className="container">
        <h2 className="center reveal">What members<br /><span className="muted">have to say.</span></h2>
        <div className="testimonials">
          {testimonials.map((t) => (
            <figure key={t.name} className="testimonial reveal">
              <h4>{t.title}</h4>
              <blockquote>“{t.quote}”</blockquote>
              <figcaption>
                <span className="dc-av">{t.name[0].toUpperCase()}</span>
                <span className="who">
                  {t.name}
                  <span className="mock-muted">{t.date}</span>
                </span>
                <a className="verified" href={t.image} target="_blank" rel="noreferrer">View screenshot <ArrowIcon size={11} /></a>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  )
}

function Partners() {
  const [copied, setCopied] = useState<string | null>(null)
  const copy = (code: string) => {
    navigator.clipboard?.writeText(code)
    setCopied(code)
    setTimeout(() => setCopied(null), 1600)
  }
  return (
    <section className="section">
      <div className="container">
        <h2 className="center reveal">Get funded with<br /><span className="muted">our partners.</span></h2>
        <div className="partners">
          {partners.map((p) => (
            <div key={p.name} className="partner reveal">
              <div>
                <span className="tag">Funding partner</span>
                <h3>{p.name}</h3>
                <p>{p.blurb}</p>
              </div>
              <div className="partner-actions">
                <button className="code" onClick={() => copy(p.code)}>
                  <span className="mock-muted">Use code</span>
                  <strong>{p.code}</strong>
                  <span className="copy">{copied === p.code ? 'Copied' : 'Click to copy'}</span>
                </button>
                <a className="btn btn-accent btn-block" href={p.href} target="_blank" rel="noreferrer">
                  Get funded <ArrowIcon />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Faq() {
  const [open, setOpen] = useState<number | null>(0)
  return (
    <section id="faq" className="section">
      <div className="container narrow">
        <h2 className="center reveal">Answers to<br /><span className="muted">your questions.</span></h2>
        <div className="faq">
          {faqs.map((f, i) => (
            <div key={f.q} className={`faq-item reveal${open === i ? ' open' : ''}`}>
              <button onClick={() => setOpen(open === i ? null : i)} aria-expanded={open === i}>
                {f.q}
                <span className="plus" />
              </button>
              <div className="faq-a"><p>{f.a}</p></div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer>
      <div className="container final-cta reveal">
        <img src="/vrtx-icon.png" alt="" className="final-logo" />
        <h2>Get started today.</h2>
        <div className="hero-ctas">
          <a className="btn btn-accent btn-lg" href={links.discord} target="_blank" rel="noreferrer"><DiscordIcon /> Join the Discord</a>
          <a className="btn btn-ghost btn-lg" href={links.mentorship} target="_blank" rel="noreferrer">Book mentorship</a>
        </div>
      </div>
      <div className="container footer-grid">
        <div>
          <a href="#top" className="logo"><span className="logo-mark"><img src="/vrtx-icon.png" alt="" /></span><span>VRTX</span></a>
          <p className="mock-muted">I intersect the candles.</p>
          <div className="socials">
            <a href={links.discord} target="_blank" rel="noreferrer" aria-label="Discord"><DiscordIcon /></a>
            <a href={links.instagram} target="_blank" rel="noreferrer" aria-label="Instagram"><InstagramIcon /></a>
            <a href={links.x} target="_blank" rel="noreferrer" aria-label="X"><XIcon /></a>
          </div>
        </div>
        <div>
          <h5>Explore</h5>
          {nav.map((n) => <a key={n.href} href={n.href}>{n.label}</a>)}
        </div>
        <div>
          <h5>Connect</h5>
          <a href={links.discord} target="_blank" rel="noreferrer">Discord</a>
          <a href={links.instagram} target="_blank" rel="noreferrer">Instagram</a>
          <a href={links.x} target="_blank" rel="noreferrer">X / Twitter</a>
          <a href={links.linktree} target="_blank" rel="noreferrer">Linktree</a>
        </div>
      </div>
      <div className="container disclaimer">
        <p>
          Trading foreign exchange, commodities and derivatives carries a high level of risk and may not be suitable for
          all investors. Content shared by VRTX is for educational purposes only and is not financial advice. Past
          performance does not guarantee future results.
        </p>
        <p>© {new Date().getFullYear()} VRTX. All rights reserved.</p>
      </div>
    </footer>
  )
}

export default function App() {
  useReveal()
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Approach />
        <Philosophy />
        <Trades />
        <Daily />
        <Membership />
        <Results />
        <Partners />
        <Faq />
      </main>
      <Footer />
    </>
  )
}
