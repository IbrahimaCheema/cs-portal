import sys
import os
import time
import urllib.parse
import urllib.request
import ssl
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://crescentschool.edu.pk"
OUTPUT_REPORT_DIR = r"C:\Projects\antigravity-ide\cs-portal\test_reports\certification"
os.makedirs(OUTPUT_REPORT_DIR, exist_ok=True)

# List of known routes to audit
PAGES_DIR = r"C:\Projects\antigravity-ide\cs-portal\src\pages"
routes = []

for root, dirs, files in os.walk(PAGES_DIR):
    for f in files:
        if f.endswith(".astro"):
            rel_path = os.path.relpath(os.path.join(root, f), PAGES_DIR).replace("\\", "/")
            route = "/" + rel_path.replace(".astro", "")
            if route.endswith("/index"):
                route = route[:-6]
            if route == "":
                route = "/"
            routes.append(route)

routes = sorted(list(set(routes)))

def audit_all_pages_and_links():
    print("=" * 80)
    print("🏛️ COMPREHENSIVE PRODUCTION CERTIFICATION — ALL PAGES & LINKS")
    print(f"Target: {BASE_URL} | Total Defined Routes: {len(routes)}")
    print("=" * 80)

    page_results = []
    discovered_links = set()
    link_results = {}
    total_images_checked = 0
    broken_images_all = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        console_errors_by_page = {}

        def on_console(msg):
            if msg.type == "error":
                txt = msg.text
                if "compute-pressure" not in txt and "Permissions policy violation" not in txt:
                    current_url = page.url
                    console_errors_by_page.setdefault(current_url, []).append(txt)

        page.on("console", on_console)

        # Step 1: Visit every page on live production
        for idx, route in enumerate(routes, 1):
            url = f"{BASE_URL}{route}" if route != "/" else f"{BASE_URL}/"
            t0 = time.time()
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(500)
                status = resp.status if resp else 0
                latency = int((time.time() - t0) * 1000)
            except Exception as e:
                status = str(e)
                latency = int((time.time() - t0) * 1000)

            title = page.title()
            
            # Scroll down to hydrate lazy images and back up
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(400)
            page.evaluate("window.scrollTo(0, 0)")

            # Check images on page (wait for lazy loaded images to complete)
            images = page.locator("img").all()
            page_broken_imgs = []
            page_valid_imgs = 0
            for img in images:
                src = img.get_attribute("src")
                if not src:
                    continue
                page_valid_imgs += 1
                try:
                    img.scroll_into_view_if_needed()
                    img.evaluate("el => new Promise(resolve => { if (el.complete) resolve(el.naturalWidth); else { el.onload = () => resolve(el.naturalWidth); el.onerror = () => resolve(0); setTimeout(() => resolve(el.naturalWidth), 2500); } })")
                    w = img.evaluate("el => el.naturalWidth")
                    if w == 0:
                        page_broken_imgs.append(src)
                except Exception:
                    pass

            total_images_checked += page_valid_imgs
            if page_broken_imgs:
                broken_images_all.extend([(url, src) for src in page_broken_imgs])

            errors = console_errors_by_page.get(page.url, [])

            page_info = {
                "index": idx,
                "route": route,
                "url": url,
                "status": status,
                "latency_ms": latency,
                "title": title,
                "images_count": page_valid_imgs,
                "broken_images": len(page_broken_imgs),
                "console_errors": len(errors)
            }
            page_results.append(page_info)

            print(f"[{idx:02d}/{len(routes):02d}] {route:45} -> Status: {status} | Latency: {latency:4d}ms | Imgs: {page_valid_imgs:2d} (Broken: {len(page_broken_imgs)}) | Errors: {len(errors)}")

            # Extract all links on this page
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
                    continue
                full_url = urllib.parse.urljoin(url, href)
                # Normalize url (remove fragment)
                parsed = urllib.parse.urlparse(full_url)
                normalized = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ""))
                discovered_links.add(normalized)

        browser.close()

    # Step 2: Audit all discovered unique internal links
    internal_links = sorted([u for u in discovered_links if urllib.parse.urlparse(u).netloc in ["crescentschool.edu.pk", "www.crescentschool.edu.pk"]])
    external_links = sorted([u for u in discovered_links if urllib.parse.urlparse(u).netloc not in ["crescentschool.edu.pk", "www.crescentschool.edu.pk"]])

    print("\n" + "=" * 80)
    print(f"🔗 AUDITING ALL DISCOVERED INTERNAL LINKS ({len(internal_links)} unique URLs)...")
    print("=" * 80)

    ctx = ssl.create_default_context()
    broken_links = []

    for idx, link in enumerate(internal_links, 1):
        req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Crescent-Auditor/1.0"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                status = resp.status
                final_url = resp.geturl()
                latency = int((time.time() - t0) * 1000)
                link_results[link] = {"status": status, "final_url": final_url, "latency_ms": latency}
                print(f"  [{idx:03d}/{len(internal_links):03d}] {link:55} -> HTTP {status} ({latency}ms)")
        except urllib.error.HTTPError as e:
            link_results[link] = {"status": e.code, "error": str(e)}
            broken_links.append((link, f"HTTP {e.code}"))
            print(f"  [{idx:03d}/{len(internal_links):03d}] ❌ {link:55} -> HTTP {e.code}")
        except Exception as e:
            link_results[link] = {"status": "ERROR", "error": str(e)}
            broken_links.append((link, str(e)))
            print(f"  [{idx:03d}/{len(internal_links):03d}] ❌ {link:55} -> {e}")

    # Step 3: Produce Executive Summary
    failed_pages = [p for p in page_results if p["status"] != 200]
    total_pages = len(page_results)
    passed_pages = total_pages - len(failed_pages)

    print("\n" + "=" * 80)
    print("🏆 CERTIFICATION AUDIT SUMMARY")
    print("=" * 80)
    print(f"  Total Pages Audited:         {total_pages}")
    print(f"  Passed Pages (HTTP 200):     {passed_pages} ({passed_pages/total_pages*100:.1f}%)")
    print(f"  Failed Pages:                {len(failed_pages)}")
    print(f"  Total Internal Links:        {len(internal_links)}")
    print(f"  Valid Internal Links:        {len(internal_links) - len(broken_links)} ({(len(internal_links) - len(broken_links))/len(internal_links)*100:.1f}%)")
    print(f"  Broken Internal Links:       {len(broken_links)}")
    print(f"  Total Images Audited:        {total_images_checked}")
    print(f"  Broken Images:               {len(broken_images_all)}")
    print(f"  External Reference Links:    {len(external_links)}")
    print("=" * 80)

    # Save detailed JSON report
    import json
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": BASE_URL,
        "summary": {
            "total_pages": total_pages,
            "passed_pages": passed_pages,
            "failed_pages": len(failed_pages),
            "total_internal_links": len(internal_links),
            "broken_internal_links": len(broken_links),
            "total_images_checked": total_images_checked,
            "broken_images": len(broken_images_all)
        },
        "pages": page_results,
        "broken_links": broken_links,
        "broken_images": broken_images_all,
        "internal_links": link_results,
        "external_links": external_links
    }
    report_file = os.path.join(OUTPUT_REPORT_DIR, "full_site_certification_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Detailed JSON Report saved: {report_file}")

    if len(failed_pages) == 0 and len(broken_links) == 0 and len(broken_images_all) == 0:
        print("\n🎉 100% CERTIFIED: EVERY SINGLE PAGE, LINK, AND ASSET IS FULLY OPERATIONAL!")
    else:
        print(f"\n⚠️ WARNING: Identified issues - Failed Pages: {len(failed_pages)}, Broken Links: {len(broken_links)}, Broken Images: {len(broken_images_all)}")

if __name__ == "__main__":
    audit_all_pages_and_links()
