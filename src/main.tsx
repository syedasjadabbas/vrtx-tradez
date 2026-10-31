import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

// Always open at the top on load or refresh, even if the URL has a #section
// or the browser would normally restore the last scroll position.
if ('scrollRestoration' in history) history.scrollRestoration = 'manual'
if (location.hash) history.replaceState(null, '', location.pathname + location.search)
window.scrollTo(0, 0)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

// The splash screen (inline in index.html) stays for 1.5 seconds from the start of the page load,
// then fades out and lets the page's own entrance animations begin.
const SPLASH_MS = 1500
const splash = document.getElementById('splash')
if (splash) {
  setTimeout(() => {
    splash.classList.add('done')
    document.documentElement.classList.remove('splash-on')
    window.dispatchEvent(new Event('splashdone'))
    setTimeout(() => splash.remove(), 700)
  }, Math.max(0, SPLASH_MS - performance.now()))
}
