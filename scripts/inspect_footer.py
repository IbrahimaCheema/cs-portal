import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

url = 'https://crescentschool.edu.pk/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    footer_match = re.search(r'(<footer[\s\S]*?</footer>)', html, re.I)
    if footer_match:
        f_html = footer_match.group(1)
        print('Footer length:', len(f_html))
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', f_html)
        print('Footer images:', imgs)
        links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', f_html)
        print('Total links in footer:', len(links))
        for href, text in links[:20]:
            clean_text = re.sub(r'<[^>]+>', '', text).strip()
            print(f'  {clean_text} -> {href}')
    else:
        # Check for footer-like div
        f_div = re.findall(r'(<div[^>]+class=["\'][^"\']*footer[^"\']*["\'][\s\S]*?</div>)', html, re.I)
        print('Footer divs found:', len(f_div))
except Exception as e:
    print('Error:', e)
