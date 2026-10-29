import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://crescentschool.edu.pk/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

idx = html.find('bookseller')
s_open = html.rfind('<script', 0, idx)
s_close = html.find('</script>', idx)
script_content = html[s_open:s_close]

# Let's inspect display settings, speed, transition, styles
displays = re.findall(r'"ditty-display-[^"]+":\{[\s\S]*?\}', script_content)
for d in displays[:3]:
    print('Display:', d[:300])

# CSS of ditty
css_matches = re.findall(r'"css":"([^"]+)"', script_content)
for c in css_matches:
    print('CSS:', c.replace('\\/', '/').replace('\\"', '"'))
