import os
import sys
import ssl
import json
import urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

pages = [
    ("professional-development", "https://crescentschool.edu.pk/professional-development/"),
    ("cambridge-professional-development-qualifications", "https://crescentschool.edu.pk/cambridge-professional-development-qualifications/"),
    ("cambridge-celta-delta", "https://crescentschool.edu.pk/cambridge-celta-delta/"),
    ("international-certificate-of-learning-and-teaching-icolt", "https://crescentschool.edu.pk/international-certificate-of-learning-and-teaching-icolt/"),
    ("futuristic-leaders-and-strategic-headship-flash", "https://crescentschool.edu.pk/futuristic-leaders-and-strategic-headship-flash/")
]

out = {}

for slug, url in pages:
    print(f"Fetching {slug}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        soup = BeautifulSoup(r.read().decode("utf-8", errors="ignore"), "html.parser")
    
    for el in soup(["header", "footer", "nav", "script", "style"]):
        el.decompose()

    title = soup.title.string.strip() if soup.title else slug
    
    # Images
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and "wp-content/uploads" in src and not src.startswith("data:"):
            images.append({
                "src": src,
                "alt": img.get("alt", ""),
                "filename": src.split("/")[-1]
            })

    # Texts
    texts = []
    for div in soup.find_all(["h1", "h2", "h3", "h4", "p", "div", "li"]):
        if div.name in ["h1", "h2", "h3", "h4", "p", "li"] or "elementor-widget-text-editor" in div.get("class", []):
            txt = div.get_text(" ", strip=True)
            if (txt and len(txt) > 5 and "Skip to content" not in txt 
                and "The Crescent School" not in txt 
                and "BOYS CAMPUS" != txt and "GIRLS CAMPUS" != txt
                and "At Crescent School, we are inspired by values" not in txt):
                if not any(txt == t["text"] for t in texts):
                    texts.append({"tag": div.name, "text": txt})

    out[slug] = {
        "title": title,
        "url": url,
        "images": images,
        "texts": texts
    }
    print(f"✓ {slug}: {len(images)} images, {len(texts)} text blocks")

out_file = r"C:\Projects\antigravity-ide\cs-portal\scripts\batch5_data.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"\nSaved Batch 5 data to {out_file}")
