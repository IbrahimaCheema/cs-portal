# 🏗️ Corporate Website Cloning Architectural Blueprint & Standard Operating Procedures (SOP) — Crescent School (`cs-portal`)

This document defines the exact architecture, technology stack, local-first asset staging strategy, UI design system, and Git workflow guidelines established for cloning **Crescent School (`https://crescentschool.edu.pk/`)** page by page.

---

## 1. 🛠️ Core Technology Stack

- **Framework**: **Astro 4.15+ (Static Site Generator)**
  - Pure static HTML compilation for lightning-fast page loads and zero unnecessary JS overhead.
- **Styling Architecture**: **Vanilla CSS (`src/styles/global.css`)**
  - Modular CSS variables (`--primary-navy: #002147`, `--primary-dark: #001A39`, `--accent-gold: #FDC800`, `--font-heading`, `--font-body`).
  - Responsive CSS Grid and Flexbox layouts, executive academic typography, glassmorphism, and smooth hover transitions.
- **Iconography**: **Crisp Vector SVGs**
  - 100% inline SVG icons for guaranteed render reliability across all browsers and devices (avoiding icon font loading glitches).
- **Media Storage & Staging Strategy**: **Local-First Staging -> Cloudflare R2 Object Storage**
  - **Phase 1 (Local Staging)**: All target website media assets (images, logos, PDFs, banners) are downloaded into `public/images/` and `public/documents/` and resolved locally via `getMediaUrl('/images/...')`.
  - **Phase 2 (Cloudflare R2 & Pages Cutover)**: Upon full website sign-off, all staged assets in `public/` are batch-uploaded to Cloudflare R2 (`cs-uploads`) via `scripts/upload_r2_assets.js`.

---

## 2. 📦 Local Asset Ingestion & R2 Readiness Protocol

During the local staging phase, every page's media assets are downloaded directly from `https://crescentschool.edu.pk/wp-content/uploads/...` into `public/images/` so that the site operates 100% self-contained on localhost without hotlinking the legacy WordPress server.

### Image Component Pattern:
All Astro image tags use `getMediaUrl()` from `src/utils/media.ts` and include a local fallback handler:
```astro
<img 
  src={getMediaUrl('/images/page_feature_1.jpg')} 
  alt="Feature Description" 
  loading="lazy"
  onerror="this.src='/images/cs_logo.png'"
/>
```

---

## 3. 🎨 UI Design System & Component Standardization

> [!IMPORTANT]
> **MANDATORY DESIGN CONTINUITY RULE**: All cloned inner pages MUST automatically inherit the master design system, color palette (`#002147` Oxford Navy & `#FDC800` Crescent Gold), typography (`Roboto Slab` / `Montserrat` headings & `Open Sans` / `Roboto` body), button styles, and card aesthetics established on the Homepage. Do not introduce disconnected or non-standard styles on inner pages.

### Standard Top Page Hero Banner (`.page_hero_banner`)
Every inner page utilizes the standardized academic top page hero banner:

```astro
<section class="page_hero_banner">
  <div class="container">
    <div class="hero_breadcrumbs">
      <a href="/">Home</a>
      <span>/</span>
      <span>Section</span>
      <span>/</span>
      <span class="current">Page Title</span>
    </div>
    <h1 class="hero_page_title">Page Title</h1>
    <p class="hero_subtitle">Concise 1-2 sentence executive summary of the page content.</p>
  </div>
</section>
```

---

## 4. 🔒 Git Commit & Remote Synchronization Protocol

> [!CAUTION]
> **MANDATORY GIT RULE**: NEVER run `git push` autonomously.

- **Local Development**: Format, test, build (`npm run build`), and commit changes locally:
  ```bash
  git add .
  git commit -m "Clone [page-name] with local assets"
  ```
- **Remote Push & Cloudflare Deployment**: Held strictly until all pages are finalized locally and the user explicitly authorizes GitHub & Cloudflare cutover.

---

## 5. 🔄 One-Page-At-A-Time (Iterative) Cloning Workflow

To ensure maximum quality, clean code, and thorough verification, pages are cloned **step-by-step**:
1. **Batch 1 — Core Foundation & Homepage**: Global Header, Mega-Menu/Dropdowns, Footer, and Homepage (`/`).
2. **Batch 2 — About Us & Governance**: About Us, Why Crescent, Mission & Values, History, Affiliations, Principals' Messages, Administration, Chairman's Message, Board of Trustees.
3. **Batch 3 — Academic Sections & IB/Cambridge**: Early Years, Primary, Middle School, Senior School, Cambridge Section, The Crescent College, IB MYP, IB DP, IB CP, Facilities.
4. **Batch 4 — Finishing School & Specialized Academies**: The Finishing School, School of Art, School of Music, Gentlemen's League, The Quran School, Robotics, School of Linguistics, Emerging Technologies Centre.
5. **Batch 5 — Professional Development (CPD)**: Professional Development, Cambridge PDQs, CELTA/Delta, ICOLT, FLASH.
6. **Batch 6 — Admissions & Eligibility**: Am I Eligible (Early Years, Middle, Senior, Cambridge, College), Required Documents (Junior/Middle/Senior/O-Level, College, A-Level), General Rules, Online Application Form.
7. **Batch 7 — Achievements, Community & Contact**: Hall of Fame, Merit List, Events, Gallery, Alumni, Careers, Contact Us.
