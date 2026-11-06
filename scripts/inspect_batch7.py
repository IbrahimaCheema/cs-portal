import urllib.request
import ssl
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

urls = {
    "alumni": "https://crescentschool.edu.pk/alumni/",
    "careers": "https://crescentschool.edu.pk/careers/",
    "contact": "https://crescentschool.edu.pk/contact-2/",
    "general_rules": "https://crescentschool.edu.pk/general-rules/"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = {}

for key, url in urls.items():
    print(f"Fetching {key}: {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            soup = BeautifulSoup(resp.read(), 'html.parser')
            title = soup.title.string.strip() if soup.title else ""
            
            # Extract paragraphs / headings
            paragraphs = []
            for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']):
                txt = elem.get_text().strip()
                if len(txt) > 10 and not any(ign in txt for ign in ['Navigation', 'Menu', 'Toggle', 'Copyright']):
                    paragraphs.append(txt)
                    
            # Extract images
            images = []
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') or ''
                if 'wp-content/uploads' in src and 'logo' not in src.lower():
                    images.append(src)
                    
            # Extract forms/inputs
            forms = []
            for f in soup.find_all('form'):
                fields = []
                for inp in f.find_all(['input', 'select', 'textarea']):
                    fields.append({
                        'name': inp.get('name'),
                        'type': inp.get('type', inp.name),
                        'placeholder': inp.get('placeholder'),
                        'options': [opt.get_text().strip() for opt in inp.find_all('option')] if inp.name == 'select' else []
                    })
                forms.append(fields)

            data[key] = {
                'url': url,
                'status': resp.status,
                'title': title,
                'paragraphs': paragraphs[:50],
                'images': list(set(images)),
                'forms': forms
            }
            print(f"  ✓ {key}: HTTP {resp.status} | {len(paragraphs)} paragraphs | {len(images)} images")
    except Exception as e:
        print(f"  ❌ Error {key}: {e}")
        data[key] = {'error': str(e)}

with open('scripts/batch7_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSaved crawl data to scripts/batch7_data.json")
