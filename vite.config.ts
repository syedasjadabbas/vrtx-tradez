import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'

// The public URL used in canonical, Open Graph and sitemap links.
// Set SITE_URL for a custom domain; on Vercel it falls back to the production domain,
// then to the current deployment's URL.
function siteUrl() {
  const env = process.env
  const url =
    env.SITE_URL ||
    (env.VERCEL_PROJECT_PRODUCTION_URL && `https://${env.VERCEL_PROJECT_PRODUCTION_URL}`) ||
    (env.VERCEL_URL && `https://${env.VERCEL_URL}`) ||
    'http://localhost:5173'
  return url.replace(/\/+$/, '')
}

// Fills %SITE_URL% in index.html and writes robots.txt + sitemap.xml at build time.
function seo(): Plugin {
  const url = siteUrl()
  return {
    name: 'vrtx-seo',
    // 'pre' so the placeholder is replaced before Vite parses the HTML (it isn't a valid URL escape)
    transformIndexHtml: { order: 'pre', handler: (html) => html.replaceAll('%SITE_URL%', url) },
    generateBundle() {
      this.emitFile({ type: 'asset', fileName: 'robots.txt', source: `User-agent: *\nAllow: /\n\nSitemap: ${url}/sitemap.xml\n` })
      this.emitFile({
        type: 'asset',
        fileName: 'sitemap.xml',
        source:
          `<?xml version="1.0" encoding="UTF-8"?>\n` +
          `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
          `  <url><loc>${url}/</loc><lastmod>${new Date().toISOString().slice(0, 10)}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n` +
          `</urlset>\n`,
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), seo()],
})
