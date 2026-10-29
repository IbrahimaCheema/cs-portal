from playwright.sync_api import sync_playwright
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('http://localhost:4321/', wait_until='networkidle', timeout=15000)
    page.wait_for_timeout(1000)
    
    # 1. Check initial slide state
    counter_el = page.locator('#currentSlideNum')
    print('Initial counter:', counter_el.text_content())
    
    active_slide = page.locator('.ticker-slide.active')
    print('Active slide 1 text:', repr(active_slide.locator('.notice-text').text_content()))
    
    # 2. Click next button
    next_btn = page.locator('#tickerNextBtn')
    next_btn.click()
    page.wait_for_timeout(600)
    print('After 1st next click, counter:', counter_el.text_content())
    print('Active slide 2 text:', repr(page.locator('.ticker-slide.active .notice-text').text_content()))
    
    # 3. Click next button again to show notice 3 (bookseller advisory)
    next_btn.click()
    page.wait_for_timeout(600)
    print('After 2nd next click, counter:', counter_el.text_content())
    slide3_text = page.locator('.ticker-slide.active .notice-text').text_content()
    print('Active slide 3 text:', repr(slide3_text))
    
    # Capture screenshot of Notice 3 active in the vertical ticker
    page.screenshot(
        path='c:/Projects/antigravity-ide/cs-portal/public/images/verified_vertical_ticker.png',
        clip={'x': 0, 'y': 0, 'width': 1440, 'height': 380}
    )
    shutil.copy(
        'c:/Projects/antigravity-ide/cs-portal/public/images/verified_vertical_ticker.png',
        'C:/Users/ibrah/.gemini/antigravity/brain/5b4cc15f-b0e8-407a-9c57-1129af64cc74/verified_vertical_ticker.png'
    )
    print('Captured verified_vertical_ticker.png!')
    print('Page errors:', errors)
    browser.close()
