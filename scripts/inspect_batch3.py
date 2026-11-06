import os
import sys
import ssl
import json
import urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

pages = [
    ("crescent-early-years_primary-section", "https://crescentschool.edu.pk/crescent-early-years_primary-section/"),
    ("middle-school", "https://crescentschool.edu.pk/middle-school/"),
    ("ib-myp-dp-cp", "https://crescentschool.edu.pk/ib-myp-dp-cp/"),
    ("ib-diploma-programme-dp", "https://crescentschool.edu.pk/ib-diploma-programme-dp/"),
    ("ib-career-related-programme-cp", "https://crescentschool.edu.pk/ib-career-related-programme-cp/"),
    ("senior-school", "https://crescentschool.edu.pk/senior-school/"),
    ("cambridge-section", "https://crescentschool.edu.pk/cambridge-section/"),
    ("the-crescent-college", "https://crescentschool.edu.pk/the-crescent-college/"),
    ("facilities", "https://crescentschool.edu.pk/facilities/")
]

out = {}

for slug, url in pages:
    print(f"Fetching {slug}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        soup = BeautifulSoup(r.read().decode("utf-8", errors="ignore"), "html.parser")
    
    # Strip site header and footer
    for el in soup(["header", "footer", "nav", "script", "style"]):
        el.decompose()

    # Title
    title = soup.title.string.strip() if soup.title else slug
    
    # Collect images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and "wp-content/uploads" in src and not src.startswith("data:"):
            images.append({
                "src": src,
                "alt": img.get("alt", ""),
                "filename": src.split("/")[-1]
            })

    # Collect headings and text
    content_div = soup.find("div", class_="elementor") or soup.find("div", class_="entry-content") or soup.body
    sections = []
    if content_div:
        for tag in content_div.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            txt = tag.get_text(" ", strip=True)
            if txt and len(txt) > 2 and "Skip to content" not in txt:
                sections.append({
                    "tag": tag.name,
                    "text": txt
                })

    out[slug] = {
        "title": title,
        "url": url,
        "images": images,
        "sections": sections
    }
    print(f"✓ {slug}: {len(images)} images, {len(sections)} text items")

out_file = r"C:\Projects\antigravity-ide\cs-portal\scripts\batch3_data.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"\nSaved all Batch 3 data to {out_file}")
