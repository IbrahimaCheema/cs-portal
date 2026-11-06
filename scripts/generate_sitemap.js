import fs from 'fs';
import path from 'path';

const siteUrl = 'https://crescentschool.edu.pk';

const pages = [
  '/',
  '/about-us/',
  '/mission-values/',
  '/history/',
  '/affiliations/',
  '/principals-message/',
  '/administration/',
  '/message-from-the-chairman-crescent-educational-trust/',
  '/board-of-trustees-2/'
];

function generateSitemap() {
  const lastmod = new Date().toISOString().split('T')[0];

  const xmlUrls = pages.map(page => `  <url>
    <loc>${siteUrl}${page}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${page === '/' ? 'weekly' : 'monthly'}</changefreq>
    <priority>${page === '/' ? '1.0' : '0.8'}</priority>
  </url>`).join('\n');

  const sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${xmlUrls}
</urlset>`;

  const indexContent = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>${siteUrl}/sitemap-0.xml</loc>
    <lastmod>${lastmod}</lastmod>
  </sitemap>
</sitemapindex>`;

  const publicDir = path.resolve('public');
  if (!fs.existsSync(publicDir)) fs.mkdirSync(publicDir, { recursive: true });
  fs.writeFileSync(path.join(publicDir, 'sitemap-0.xml'), sitemapContent, 'utf-8');
  fs.writeFileSync(path.join(publicDir, 'sitemap-index.xml'), indexContent, 'utf-8');

  console.log(`✅ Generated XML Sitemaps in public/: sitemap-0.xml & sitemap-index.xml (${pages.length} URLs)`);
}

generateSitemap();
