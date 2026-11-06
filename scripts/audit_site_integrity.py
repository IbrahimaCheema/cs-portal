import os
import sys
import threading
import http.server
import socketserver
import time
import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PORT = 4328
DIST_DIR = r"C:\Projects\antigravity-ide\cs-portal\dist"
PUBLIC_DIR = r"C:\Projects\antigravity-ide\cs-portal\public"

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

print(f"🚀 Started Static Audit Server on http://localhost:{PORT}")

visited_urls = set()
to_visit = [f"http://localhost:{PORT}/"]
broken_links = []
broken_images = []
hotlinked_images = []
page_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    while to_visit:
        current_url = to_visit.pop(0)
        parsed = urllib.parse.urlparse(current_url)
        clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
        
        if clean_url in visited_urls:
            continue
        visited_urls.add(clean_url)
        page_count += 1

        print(f"[{page_count}] Auditing: {parsed.path or '/'}")
        try:
            resp = page.goto(clean_url, wait_until="domcontentloaded", timeout=10000)
            status = resp.status if resp else 0
            if status != 200:
                broken_links.append((clean_url, f"HTTP {status}"))
                continue
        except Exception as e:
            broken_links.append((clean_url, str(e)))
            continue

        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Check all internal links
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:'):
                continue
            
            full_href = urllib.parse.urljoin(clean_url, href)
            p_href = urllib.parse.urlparse(full_href)

            # If it's an internal link
            if p_href.netloc == f"localhost:{PORT}":
                clean_target = urllib.parse.urlunparse((p_href.scheme, p_href.netloc, p_href.path, '', '', ''))
                if clean_target not in visited_urls and clean_target not in to_visit:
                    to_visit.append(clean_target)

        # Check all images
        for img in soup.find_all('img'):
            src = img.get('src') or ''
            if not src:
                continue
            
            # Check for legacy hotlinks
            if 'crescentschool.edu.pk' in src:
                hotlinked_images.append((clean_url, src))
                continue

            # Check if local image exists
            if src.startswith('/'):
                local_file = os.path.join(DIST_DIR, src.lstrip('/'))
                if not os.path.exists(local_file):
                    # also check in public/
                    pub_file = os.path.join(PUBLIC_DIR, src.lstrip('/'))
                    if not os.path.exists(pub_file):
                        broken_images.append((clean_url, src))

    browser.close()

print("\n" + "=" * 60)
print(f"🎯 SITE INTEGRITY AUDIT COMPLETE")
print("=" * 60)
print(f"Total Unique Pages Crawled: {page_count}")
print(f"Broken Links Detected: {len(broken_links)}")
for u, err in broken_links:
    print(f"  ❌ Link: {u} -> {err}")

print(f"Broken Local Images: {len(broken_images)}")
for u, src in broken_images:
    print(f"  ❌ Image: {src} on {u}")

print(f"Legacy Hotlinked Images: {len(hotlinked_images)}")
for u, src in hotlinked_images:
    print(f"  ⚠️ Hotlink: {src} on {u}")

if len(broken_links) == 0 and len(broken_images) == 0 and len(hotlinked_images) == 0:
    print("\n🌟 100% PERFECT SCORE! ZERO BROKEN LINKS, ZERO BROKEN IMAGES, ZERO HOTLINKS!")
    sys.exit(0)
else:
    print("\n⚠️ Issues found that require attention.")
    sys.exit(1)
