from playwright.sync_api import sync_playwright

URL = "https://www.zaio.io"


def crawl_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")

        text = page.locator("body").inner_text()

        browser.close()

        return text


if __name__ == "__main__":
    content = crawl_website()

    print("Website content extracted!")
    print("Characters:", len(content))
    print()
    print(content[:3000])