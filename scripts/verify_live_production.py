import sys
import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://crescentschool.edu.pk"
SAMPLE_ROUTES = [
    "/",
    "/about-us",
    "/admissions",
    "/cambridge-section",
    "/the-crescent-college",
    "/the-finishing-school",
    "/robotics",
    "/professional-development",
    "/am-i-eligible",
    "/required-documents",
    "/hall-of-fame",
    "/contact"
]

def verify_live_production():
    print("=" * 70)
    print("🚀 LIVE PRODUCTION PLAYWRIGHT VERIFICATION — https://crescentschool.edu.pk/")
    print("=" * 70)

    output_dir = r"C:\Projects\antigravity-ide\cs-portal\test_reports\live_production"
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for route in SAMPLE_ROUTES:
            url = f"{BASE_URL}{route}"
            print(f"\n🔍 Testing Live Route: {url} ...")

            console_errors = []
            def handle_console(msg):
                txt = msg.text
                if msg.type == "error":
                    if "compute-pressure" not in txt and "Permissions policy violation" not in txt:
                        console_errors.append(txt)
            page.on("console", handle_console)

            t0 = time.time()
            response = page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            latency = int((time.time() - t0) * 1000)

            status = response.status if response else 0
            title = page.title()
            print(f"  Status: {status} | Title: '{title}' | Latency: {latency}ms")
            assert status == 200, f"Expected 200, got {status}"

            # Scroll to trigger lazy loading and wait for images to load
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)

            # Check images
            images = page.locator("img").all()
            broken = []
            valid_count = 0
            for img in images:
                src = img.get_attribute("src")
                if not src:
                    continue
                valid_count += 1
                img.scroll_into_view_if_needed()
                try:
                    img.evaluate("el => new Promise(resolve => { if (el.complete) resolve(el.naturalWidth); else { el.onload = () => resolve(el.naturalWidth); el.onerror = () => resolve(0); } })")
                except:
                    pass
                w = img.evaluate("el => el.naturalWidth")
                if w == 0:
                    broken.append(src)

            print(f"  Valid Images: {valid_count} | Broken Images: {len(broken)} | Console Errors: {len(console_errors)}")
            assert len(broken) == 0, f"Broken images: {broken}"
            assert len(console_errors) == 0, f"Console errors: {console_errors}"

            # Capture screenshot
            slug = "home" if route == "/" else route.replace("/", "_")
            shot_path = os.path.join(output_dir, f"live_{slug}_1440.png")
            page.screenshot(path=shot_path, full_page=True)
            print(f"  Saved Live Screenshot: {shot_path}")

        browser.close()

    print("\n" + "=" * 70)
    print("🏆 100% PASS: LIVE PRODUCTION DOMAIN https://crescentschool.edu.pk/ FULLY OPERATIONAL!")
    print("=" * 70)

if __name__ == "__main__":
    verify_live_production()
