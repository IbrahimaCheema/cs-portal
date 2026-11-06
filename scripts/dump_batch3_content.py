import os
import sys
import ssl
import json
import urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl._create_unverified_context()

slugs = [
    'crescent-early-years_primary-section',
    'middle-school',
    'ib-myp-dp-cp',
    'ib-diploma-programme-dp',
    'ib-career-related-programme-cp',
    'senior-school',
    'cambridge-section',
    'the-crescent-college',
    'facilities'
]

full_data = {}

for s in slugs:
    url = f"https://crescentschool.edu.pk/{s}/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        soup = BeautifulSoup(r.read().decode("utf-8", errors="ignore"), "html.parser")
    for el in soup(["header", "footer", "nav", "script", "style"]): el.decompose()

    # Images
    imgs = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and "wp-content/uploads" in src:
            imgs.append(src)

    # Texts
    texts = []
    # find all headings, paragraphs, and list items in document order
    for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li"]):
        txt = el.get_text(" ", strip=True)
        if txt and len(txt) > 3 and "Skip to content" not in txt and "The Crescent School" not in txt and "BOYS CAMPUS" != txt and "GIRLS CAMPUS" != txt and "At Crescent School, we are inspired by values" not in txt:
            texts.append({"tag": el.name, "text": txt})

    full_data[s] = {
        "url": url,
        "images": list(dict.fromkeys(imgs)),
        "items": texts
    }
    print(f"{s}: {len(imgs)} imgs, {len(texts)} text items")

with open(r"C:\Projects\antigravity-ide\cs-portal\scripts\batch3_full_content.json", "w", encoding="utf-8") as f:
    json.dump(full_data, f, indent=2, ensure_ascii=False)

print("\nDone dumping full content.")
