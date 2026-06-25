from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

def analyze_url(url: str) -> Path:
    """Runs the given url in multiple browsers and saves the collected data."""

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs")/run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    browsers = ["chromium", "firefox"] # webkit, brave

    with sync_playwright() as p:

        browser_types = {
            "chromium": p.chromium,
            "firefox": p.firefox,
        }

        for browser_name, browser_type in browser_types.items():
            browser_dir = run_dir / browser_name
            browser_dir.mkdir(parents=True, exist_ok=True)

            print(f"OPENING {url} IN {browser_name}...")

            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="load", timeout=30000)
            except Exception as e:
                print(f"FAILED IN {browser_name}: {e}")
                browser.close()
                continue
            page.screenshot(path=browser_dir/"screenshot.png", full_page=True,)

            html = page.content()
            (browser_dir/"page.html").write_text(html, encoding="utf-8")

            browser.close()

            print(f"SAVED {browser_name} ARTIFACTS")

    return run_dir


