import fs from 'fs';
import path from 'path';

const siteUrl = 'https://crescentschool.edu.pk';

const pages = [
  '/',
  // Batch 2: Governance & Institution
  '/about-us/',
  '/mission-values/',
  '/history/',
  '/affiliations/',
  '/principals-message/',
  '/administration/',
  '/message-from-the-chairman-crescent-educational-trust/',
  '/board-of-trustees-2/',
  // Batch 3: Academic Sections & IB/Cambridge
  '/crescent-early-years_primary-section/',
  '/middle-school/',
  '/ib-myp-dp-cp/',
  '/ib-diploma-programme-dp/',
  '/ib-career-related-programme-cp/',
  '/senior-school/',
  '/cambridge-section/',
  '/the-crescent-college/',
  '/facilities/',
  // Batch 4: Schools of Renaissance
  '/school-of-art/',
  '/school-of-music/',
  '/the-finishing-school/',
  '/gentlemens-league/',
  '/the-quran-school/',
  '/robotics/',
  '/school-of-linguistics/',
  // Batch 5: Professional Development (CPD)
  '/professional-development/',
  '/cambridge-professional-development-qualifications/',
  '/cambridge-celta-delta/',
  '/international-certificate-of-learning-and-teaching-icolt/',
  '/futuristic-leaders-and-strategic-headship-flash/',
  // Batch 6: Admissions & Eligibility
  '/am-i-eligible/',
  '/am-i-eligible/early-years/',
  '/am-i-eligible/middle-school/',
  '/am-i-eligible/senior-school/',
  '/am-i-eligible/cambridge/',
  '/am-i-eligible/college/',
  '/am-i-eligible/ib/',
  '/required-documents/',
  '/online-application-form/',
  '/merit-list/',
  '/hall-of-fame/'
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
