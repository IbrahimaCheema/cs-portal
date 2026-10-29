import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

def test_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGE_ERROR: {err}"))
        page.on("console", lambda msg: errors.append(f"CONSOLE_{msg.type.upper()}: {msg.text}") if msg.type in ["error"] else None)

        print("Navigating to http://localhost:4321/ ...")
        response = page.goto("http://localhost:4321/", wait_until="networkidle")
        
        print(f"HTTP Status: {response.status}")
        print(f"Page Title: {page.title()}")
        
        # Check critical elements
        header_count = page.locator("header.site-header").count()
        footer_count = page.locator("footer.site-footer").count()
        wings_count = page.locator(".wing-card").count()
        stats_count = page.locator(".stat-box").count()
        achieve_count = page.locator(".achievement-card").count()
        partners_count = page.locator(".partner-item").count()
        
        print(f"Header: {header_count}, Footer: {footer_count}")
        print(f"Academic Wings Cards: {wings_count}")
        print(f"Stat Counters: {stats_count}")
        print(f"Achievement Cards: {achieve_count}")
        print(f"Partner Logos: {partners_count}")
        
        # Capture screenshot for verification
        screenshot_path = r"C:\Projects\antigravity-ide\cs-portal\public\test_preview_homepage.png"
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Saved preview screenshot to: {screenshot_path}")
        
        if errors:
            print("\nErrors detected:")
            for err in errors:
                print("  ", err)
        else:
            print("\nZero console/page errors detected! 100% clean render.")
            
        browser.close()

if __name__ == "__main__":
    test_page()
