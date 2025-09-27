from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Get the absolute path to the index.html file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # Click the "Get New Advice" button
        page.click('button#get-advice')

        # Take a screenshot
        page.screenshot(path='jules-scratch/verification/screenshot.png')

        browser.close()

run()
