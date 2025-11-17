import pytest
from playwright.sync_api import Page, expect
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Define the server port
PORT = 8000

@pytest.fixture(scope="module", autouse=True)
def http_server():
    """Starts a simple HTTP server in a separate thread."""
    server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()

def test_initial_state(page: Page):
    """Verifies the initial state of the page."""
    page.goto(f"http://localhost:{PORT}")

    # Check title
    expect(page).to_have_title("Questionable Advice")

    # Check heading
    expect(page.locator("h1")).to_have_text("Questionable Advice Generator")

    # Check initial instruction text (it loads fast so it might be "Click the button..." or "Loading advice...")
    # Since we are testing the real app, it fetches advice.json immediately.
    # We can intercept the request to ensure we see "Loading advice..." if we want,
    # but for a general test, we expect the final state or loading state.

    # Let's verify the button exists
    btn = page.locator("#get-advice-btn")
    expect(btn).to_be_visible()

def test_advice_loaded(page: Page):
    """Verifies that advice loads and the button becomes enabled."""
    page.goto(f"http://localhost:{PORT}")

    # Wait for the text to change from "Loading advice..." to the instruction
    text = page.locator("#advice-text")
    btn = page.locator("#get-advice-btn")

    expect(text).to_contain_text("Click the button")
    expect(btn).to_be_enabled()

def test_get_advice(page: Page):
    """Verifies that clicking the button displays advice."""
    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    text = page.locator("#advice-text")

    # Wait for enabled
    expect(btn).to_be_enabled()

    # Click the button
    btn.click()

    # Verify text matches format: "..." ...but idk tho
    expect(text).to_contain_text("...but idk tho")
    expect(text).to_contain_text('"')

def test_fetch_error(page: Page):
    """Verifies error handling when fetch fails."""
    # Intercept the request to advice.json and fail it
    page.route("**/advice.json", lambda route: route.abort())

    page.goto(f"http://localhost:{PORT}")

    text = page.locator("#advice-text")
    expect(text).to_contain_text("Failed to load advice")

def test_empty_advice(page: Page):
    """Verifies behavior when advice list is empty."""
    # Intercept request and return empty array
    page.route("**/advice.json", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body="[]"
    ))

    page.goto(f"http://localhost:{PORT}")

    text = page.locator("#advice-text")
    btn = page.locator("#get-advice-btn")

    expect(text).to_contain_text("There is no advice to give")
    expect(btn).to_be_disabled()
