from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('http://localhost:4321/', wait_until='networkidle', timeout=15000)
    
    boys_links = page.locator('a[href*="17272449557287959642"]').all()
    print('Boys map links count:', len(boys_links))
    for l in boys_links:
        print('  Boys link text:', repr(l.text_content().strip()))
        
    girls_links = page.locator('a[href*="12619077274026858159"]').all()
    print('Girls map links count:', len(girls_links))
    for l in girls_links:
        print('  Girls link text:', repr(l.text_content().strip()))
        
    title = page.locator('.brand-title').text_content()
    print('Brand title:', title)
    
    iframes = page.locator('.campus-map-card iframe').all()
    print('Map iframes count:', len(iframes))
    
    print('Page errors:', errors)
    browser.close()
