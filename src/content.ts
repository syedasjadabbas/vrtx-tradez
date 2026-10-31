// All site copy and links live here so the client can update them without touching components.

export const links = {
  discord: 'https://discord.gg/yU9G5sgBHh',
  instagram: 'https://www.instagram.com/mirzatrades_07/',
  x: 'https://x.com/mirzaaaa000',
  linktree: 'https://linktr.ee/Mirza.SMT',
  // 1-on-1 mentorship is booked through Instagram DMs or WhatsApp
  mentorship: 'https://ig.me/m/mirzatrades_07',
  whatsapp: 'https://wa.me/923370333684?text=' + encodeURIComponent("Hi Mirza, I'm interested in 1-on-1 mentorship."),
}

export const nav = [
  { label: 'Approach', href: '#approach' },
  { label: 'Mentor', href: '#mentor' },
  { label: 'Trades', href: '#trades' },
  { label: 'Membership', href: '#membership' },
  { label: 'Results', href: '#results' },
  { label: 'FAQ', href: '#faq' },
]

export const stats = [
  { value: '330+', label: 'Traders in the server' },
  { value: 'XAUUSD', label: 'Primary market' },
  { value: '1-on-1', label: 'Private mentorship' },
  { value: '$0', label: 'To join the community' },
]

// Founder section. Copy is a draft built from Mirza's public profiles. Have him confirm it.
// photo: a 4:5 portrait in public/ (a .webp with the same name is used when present). Leave '' for the branded card.
export const mentor = {
  eyebrow: 'Meet your mentor',
  name: 'Mirza Hammad',
  role: 'Founder, VRTX',
  photo: '/mirza.jpg',
  story: [
    'I trade gold, and I teach it exactly the way I trade it. Every idea starts with time, then price: when the move should happen, where the liquidity sits and which sequence confirms it.',
    'VRTX started as a place to share that process openly. Today it is a free community of 330+ traders, daily XAUUSD analysis and private 1-on-1 mentorship for those who want to go deeper.',
  ],
  points: [
    'XAUUSD focused, with trades shared publicly on X',
    '330+ traders learning together in the VRTX Discord',
    'Students passing prop firm challenges, Phase 1 and Phase 2',
  ],
  quote: 'Time over price. Learn when the market should move, and you stop guessing where.',
}

export const pillars = [
  {
    tag: 'Analysis',
    title: 'See where price is heading before the session opens',
    body: 'Daily bias, key levels and the sequence being watched on gold, shared in the server ahead of the open.',
    points: ['Daily bias on XAUUSD before the session', 'Key levels and time windows marked out', 'The exact sequence being watched for entry'],
  },
  {
    tag: 'Community',
    title: 'Trade alongside traders who take it seriously',
    body: 'A focused Discord built around trade-talk, recaps and honest review, without noise or signal spam.',
    points: ['Live trade-talk with Mirza and members', 'Recaps of wins and losses, explained', 'Process over signals, always'],
  },
  {
    tag: 'Mentorship',
    title: 'Private 1-on-1 sessions built around your trading',
    body: 'Work directly with Mirza on your model, your execution and your psychology, at your pace.',
    points: ['Sessions arranged around your schedule', 'Review of your trades and journal', 'Risk and psychology coaching'],
  },
]

export const principles = [
  { n: '01', title: 'Time before price', body: 'Know when price should move before deciding where. Timing filters out most bad trades.' },
  { n: '02', title: 'Sequence over setups', body: 'Read the continuation sequence and let structure confirm the idea instead of chasing patterns.' },
  { n: '03', title: 'Risk is defined first', body: 'Every position is planned in R. The stop is set before the target, every time.' },
]

// Recent calls pulled from Mirza's X feed. Add new ones at the top.
export const trades = [
  { pair: 'XAUUSD', result: '+2R', note: 'Continuation sequence', date: 'Oct 30, 2026', href: 'https://x.com/mirzaaaa000' },
  { pair: 'XAUUSD', result: '+3R', note: 'Session expansion', date: 'Oct 23, 2026', href: 'https://x.com/mirzaaaa000' },
]

export const daily = [
  { title: 'Read the market through my lens', body: 'Pre-session analysis tells you exactly which levels and times matter that day.' },
  { title: 'Get clarity in the live market', body: 'Ask questions in trade-talk and get your idea checked against the model in real time.' },
  { title: 'Review every trade, win or loss', body: 'Trades are broken down after the fact so you learn the reasoning, not just the entry.' },
  { title: 'Build your own conviction', body: 'The goal is independence. No signals, just a process you can execute yourself.' },
]

export const plans = [
  {
    name: 'Community',
    price: 'Free',
    period: 'forever',
    cta: 'Join the Discord',
    href: links.discord,
    featured: false,
    features: ['Access to the VRTX server', 'Trade-talk with other members', 'Shared market analysis', 'Trade recaps and breakdowns', 'Announcements and events'],
  },
  {
    name: '1-on-1 Mentorship',
    price: 'DM',
    period: 'for availability',
    cta: 'Message on Instagram',
    href: links.mentorship,
    secondary: { cta: 'Message on WhatsApp', href: links.whatsapp },
    featured: true,
    features: ['Everything in Community', 'Private sessions with Mirza', 'Model built around your schedule', 'Trade journal and execution review', 'Direct access for questions', 'Risk and psychology coaching'],
  },
]

// Real messages from the VRTX Discord. `image` is the original screenshot in public/testimonials.
export const testimonials = [
  {
    title: 'Phase 1 & 2 in 5 days',
    quote: 'Joined VRTX 10 days ago. Your mentorship has been an extraordinary journey of my learning and growth. Thank you for being such a remarkable guide and supporter. I am very glad that I passed my phase 1 in 3 days and phase 2 in 2 days.',
    name: 'Shahid',
    date: 'Mar 16, 2026',
    image: '/testimonials/shahid.jpg',
  },
  {
    title: 'First 10K account passed',
    quote: "Alhumdulillah passed my first ever 10k account, didn't even know what MT5 was. I only traded the dead London session for 1 hour daily. There were losses and profits, I just stayed consistent following my rules. Started trading only 4 months back. If I can do it, you can too. This started with strangers, now I have brothers here, a whole family.",
    name: 'DEAD',
    date: 'Apr 18, 2026',
    image: '/testimonials/dead.jpg',
  },
  {
    title: 'Phase 1 cleared',
    quote: 'The knowledge and insights you shared have been extremely valuable, and I have implemented your strategies exactly as you taught them. Alhamdulillah, I have successfully cleared Phase 1 of my account, and this achievement would not have been possible without your mentorship.',
    name: 'hollowpixel',
    date: 'Mar 19, 2026',
    image: '/testimonials/hollowpixel.jpg',
  },
  {
    title: 'It finally clicked',
    quote: "I've joined courses before, but this is the first time I actually understood what I'm doing in the market. You didn't just teach strategies, you changed the way I look at trading, risk, and discipline.",
    name: 'Abdullah Trades',
    date: 'Jan 11, 2026',
    image: '/testimonials/abdullah.jpg',
  },
  {
    title: 'Recovered a −8% drawdown',
    quote: 'I learned how to approach the market with a proper systematic framework instead of trading based on emotions or random setups. My trading psychology improved significantly, and I was able to recover my account from an −8% drawdown back to breakeven.',
    name: 'IRTAZA',
    date: 'Feb 26, 2026',
    image: '/testimonials/irtaza.jpg',
  },
  {
    title: '5 TP, zero SL',
    quote: "I had basic knowledge of price action but was confused about market bias. Hammad Bhai explained trading in a very clear and structured way, with practical knowledge you can't easily find on YouTube or TikTok. I followed his strategies and achieved 5 TP with zero SL in the first week of January.",
    name: 'Ali.fx',
    date: 'Jan 11, 2026',
    image: '/testimonials/alifx.jpg',
  },
]

// Prop firms Mirza partners with. `href` is the affiliate link with his code applied.
export const partners = [
  {
    name: 'Atlas Funded',
    code: 'MIRZAA',
    blurb: 'Transparent payout decisions, daily payout plans and a 90% profit split.',
    href: 'https://app.atlasfunded.com/?afmc=MIRZAA',
  },
  {
    name: 'Blue Guardian',
    code: 'MIRZA25',
    blurb: 'Instant funding and challenge accounts for traders ready to scale.',
    href: 'https://blueguardian.com/?afmc=MIRZA25',
  },
]

export const faqs = [
  {
    q: 'Is the VRTX Discord really free?',
    a: 'Yes. Anyone can join the server and access the community, trade-talk and shared analysis without paying anything.',
  },
  {
    q: 'What markets do you trade?',
    a: 'The main focus is gold (XAUUSD). The same time-and-price framework can be applied to other liquid markets once you understand it.',
  },
  {
    q: 'Do you give trade signals?',
    a: 'No. Analysis and trades are shared with the reasoning behind them so you build the skill to make your own decisions.',
  },
  {
    q: 'How does 1-on-1 mentorship work?',
    a: 'Send a DM on Instagram. Sessions are arranged around your schedule and focus on your model, execution, risk and psychology.',
  },
  {
    q: 'What experience level do I need?',
    a: 'None in particular. Newer traders get a clear starting point and experienced traders get a sharper process.',
  },
  {
    q: 'Can I trade this with a prop firm?',
    a: 'Yes. Many members trade funded accounts. Mirza partners with Atlas Funded (code MIRZAA) and Blue Guardian (code MIRZA25) for discounted accounts.',
  },
]
