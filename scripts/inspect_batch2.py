import os
import sys
import ssl
import json
import urllib.request
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

pages = [
    ("about-us", "https://crescentschool.edu.pk/about-us/"),
    ("mission-values", "https://crescentschool.edu.pk/mission-values/"),
    ("history", "https://crescentschool.edu.pk/history/"),
    ("affiliations", "https://crescentschool.edu.pk/affiliations/"),
    ("principals-message", "https://crescentschool.edu.pk/principals-message/"),
    ("administration", "https://crescentschool.edu.pk/administration/"),
    ("chairman-message", "https://crescentschool.edu.pk/message-from-the-chairman-crescent-educational-trust/"),
    ("board-of-trustees", "https://crescentschool.edu.pk/board-of-trustees-2/")
]

out_data = {}

for slug, url in pages:
    print(f"Fetching {slug} ({url})...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            
            # Title
            title = soup.title.string.strip() if soup.title else slug
            
            # Find entry-content or elementor content
            content_div = soup.find("div", class_=re.compile(r"elementor|entry-content|page-content"))
            
            images = []
            if content_div:
                for img in content_div.find_all("img"):
                    src = img.get("src") or img.get("data-src")
                    if src and not src.startswith("data:"):
                        images.append({"src": src, "alt": img.get("alt", "")})
            
            # Extract text blocks
            headings = []
            if content_div:
                for h in content_div.find_all(["h1", "h2", "h3", "h4"]):
                    headings.append({"tag": h.name, "text": h.get_text(strip=True)})
            
            out_data[slug] = {
                "title": title,
                "url": url,
                "headings": headings,
                "images": images,
                "raw_text_len": len(content_div.get_text()) if content_div else 0
            }
            print(f"✓ {slug}: {len(headings)} headings, {len(images)} images")
    except Exception as e:
        print(f"❌ Error fetching {slug}: {e}")

out_path = r"C:\Projects\antigravity-ide\cs-portal\scripts\batch2_summary.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out_data, f, indent=2)

print(f"\nSaved batch 2 summary to {out_path}")
