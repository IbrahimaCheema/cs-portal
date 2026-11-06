import urllib.request
import ssl
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

urls = {
    "am_i_eligible_main": "https://crescentschool.edu.pk/am-i-eligible/",
    "am_i_eligible_early_years": "https://crescentschool.edu.pk/am-i-eligible/early-years/",
    "am_i_eligible_middle": "https://crescentschool.edu.pk/am-i-eligible/middle-school/",
    "am_i_eligible_senior": "https://crescentschool.edu.pk/am-i-eligible/senior-school/",
    "am_i_eligible_cambridge": "https://crescentschool.edu.pk/am-i-eligible/cambridge/",
    "am_i_eligible_ib": "https://crescentschool.edu.pk/am-i-eligible/ib/",
    "am_i_eligible_college": "https://crescentschool.edu.pk/am-i-eligible/college/",
    "required_documents": "https://crescentschool.edu.pk/required-documents/",
    "online_application": "https://crescentschool.edu.pk/online-application-form/",
    "merit_list": "https://crescentschool.edu.pk/merit-list/"
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
            
            # Extract main content
            content_div = soup.find('div', class_='elementor') or soup.find('main') or soup.body
            
            # Extract tables
            tables = []
            for t in soup.find_all('table'):
                rows = []
                for tr in t.find_all('tr'):
                    cells = [td.get_text().strip() for td in tr.find_all(['th', 'td'])]
                    if cells:
                        rows.append(cells)
                if rows:
                    tables.append(rows)
                    
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
                    
            # Extract forms/inputs if any
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
                'title': title,
                'tables': tables,
                'paragraphs': paragraphs[:40],
                'images': list(set(images)),
                'forms': forms
            }
            print(f"  ✓ {key}: {len(tables)} tables, {len(paragraphs)} paragraphs, {len(images)} images")
    except Exception as e:
        print(f"  ❌ Error {key}: {e}")
        data[key] = {'error': str(e)}

with open('scripts/batch6_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSaved detailed crawl data to scripts/batch6_data.json")
