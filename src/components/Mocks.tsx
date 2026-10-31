import type { CSSProperties } from 'react'
import { CandleChart } from './CandleChart'

// Visual mock-ups for the numbered "Approach" section.
// Children with --i animate in one after another once the parent is revealed.

const at = (i: number) => ({ '--i': i }) as CSSProperties

export function AnalysisMock() {
  return (
    <div className="mock">
      <div className="mock-head">
        <span className="mock-pill">XAUUSD · 15m</span>
        <span className="mock-muted">Pre-session plan</span>
      </div>
      <div className="mock-chart">
        <CandleChart count={44} seed={21} height={300} />
      </div>
      <div className="mock-row stagger stagger--after-chart">
        <div style={at(0)}><span className="mock-muted">Bias</span><strong className="accent">Bullish</strong></div>
        <div style={at(1)}><span className="mock-muted">Window</span><strong>NY open</strong></div>
        <div style={at(2)}><span className="mock-muted">Model</span><strong>Continuation</strong></div>
      </div>
    </div>
  )
}

const channels = ['announcements', 'analysis', 'trade-talk', 'trade-recaps', 'wins', 'education']

const messages = [
  { mentor: true, name: 'M I R Z A', text: 'Gold swept the Asia low into the NY window. Watching for the continuation sequence above the range.' },
  { mentor: false, name: 'member', text: 'Is the displacement candle enough confirmation here?' },
  { mentor: true, name: 'M I R Z A', text: 'Wait for the time. Price can go anywhere, timing tells you when it matters.' },
]

export function CommunityMock() {
  return (
    <div className="mock mock--discord">
      <aside className="dc-side stagger">
        <div className="dc-server">
          <img src="/vrtx-icon.png" alt="" />
          <span>V R T X</span>
        </div>
        {channels.map((c, i) => (
          <div key={c} style={at(i)} className={c === 'trade-talk' ? 'dc-ch active' : 'dc-ch'}># {c}</div>
        ))}
      </aside>
      <div className="dc-main">
        <div className="dc-title"># trade-talk</div>
        <div className="dc-feed">
          {messages.map((m, i) => (
            <div key={i} className="dc-msg" style={at(i)}>
              <span className={m.mentor ? 'dc-av accent-bg' : 'dc-av'}>{m.name[0]}</span>
              <div>
                <b>{m.name}</b> {m.mentor && <span className="dc-tag">VRTX</span>}
                <p>{m.text}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="dc-typing" style={at(messages.length)}>
          <span className="dots-typing"><i /><i /><i /></span> member is typing…
        </div>
        <div className="dc-input">Message #trade-talk</div>
      </div>
    </div>
  )
}

const sessions = [
  { day: 'Mon', topic: 'Model review', done: true },
  { day: 'Wed', topic: 'Live execution', done: true },
  { day: 'Fri', topic: 'Journal and risk', done: false },
]

export function MentorshipMock() {
  const done = sessions.filter((s) => s.done).length
  return (
    <div className="mock">
      <div className="mock-head">
        <span className="mock-pill">1-on-1</span>
        <span className="mock-muted">This week · {done}/{sessions.length}</span>
      </div>
      <div className="mm-progress" style={{ '--w': done / sessions.length } as CSSProperties}><span /></div>
      <ul className="mm-list stagger">
        {sessions.map((s, i) => (
          <li key={s.day} style={at(i)} className={s.done ? 'done' : ''}>
            <span className="mm-day">{s.day}</span>
            <span>{s.topic}</span>
            <span className="mm-state">
              {s.done && <svg className="mm-check" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2"><path d="m3 8.5 3 3 7-7" /></svg>}
              {s.done ? 'Completed' : 'Upcoming'}
            </span>
          </li>
        ))}
      </ul>
      <div className="mm-note">
        <span className="mock-muted">Mentor note</span>
        <p>Entries are clean. Stop moving the stop to breakeven before the sequence completes. Let the trade breathe.</p>
      </div>
    </div>
  )
}
