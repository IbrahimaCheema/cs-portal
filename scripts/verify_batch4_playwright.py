import os
import sys
import threading
import http.server
import socketserver
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PORT = 4324
DIST_DIR = r"C:\Projects\antigravity-ide\cs-portal\dist"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        httpd.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

test_routes = [
    ("school-of-art", f"http://localhost:{PORT}/school-of-art/"),
    ("school-of-music", f"http://localhost:{PORT}/school-of-music/"),
    ("the-finishing-school", f"http://localhost:{PORT}/the-finishing-school/"),
    ("gentlemens-league", f"http://localhost:{PORT}/gentlemens-league/"),
    ("the-quran-school", f"http://localhost:{PORT}/the-quran-school/"),
    ("robotics", f"http://localhost:{PORT}/robotics/"),
    ("school-of-linguistics", f"http://localhost:{PORT}/school-of-linguistics/")
]

screenshots_dir = r"C:\Projects\antigravity-ide\cs-portal\public\batch4_evidence"
os.makedirs(screenshots_dir, exist_ok=True)

all_passed = True

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    for slug, url in test_routes:
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGE_ERROR: {err}"))
        page.on("console", lambda msg: errors.append(f"CONSOLE_{msg.type.upper()}: {msg.text}") if msg.type == "error" else None)

        print(f"\n--- Testing route: {slug} ({url}) ---")
        resp = page.goto(url, wait_until="networkidle", timeout=15000)
        status = resp.status if resp else 0
        title = page.title()
        print(f"Status: {status} | Title: {title}")

        hdr = page.locator("header.site-header").count()
        ftr = page.locator("footer.site-footer").count()
        hero = page.locator(".page_hero_banner").count()
        print(f"Elements: Header={hdr}, Footer={ftr}, HeroBanner={hero}")

        if status != 200 or hdr == 0 or ftr == 0 or hero == 0:
            print(f"❌ FAIL on {slug}")
            all_passed = False
        else:
            print(f"✓ PASS on {slug}")

        shot_path = os.path.join(screenshots_dir, f"{slug}.png")
        page.screenshot(path=shot_path, full_page=False)
        print(f"Saved evidence screenshot: {shot_path}")

        if errors:
            print(f"Errors on {slug}:", errors)
            all_passed = False

    browser.close()

if all_passed:
    print("\n=======================================================")
    print("ALL 7 BATCH 4 PAGES VERIFIED WITH 100% SUCCESS & 0 ERRORS!")
    print("=======================================================")
else:
    print("\n⚠️ Some routes failed verification.")
    sys.exit(1)
