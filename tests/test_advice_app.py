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
    expect(page).to_have_title("Cheesy Advice Generator")

    # Check heading
    expect(page.locator("h1")).to_have_text("Cheesy Advice Generator")

    # Check initial instruction text
    expect(page.locator("#advice-text")).to_have_text("Click the button to get some grate advice.")

    # Let's verify the button exists and has correct text
    btn = page.locator("#get-advice-btn")
    expect(btn).to_be_visible()
    expect(btn).to_have_text("Get Some Gouda Advice")

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

    # Verify text matches format: "..." - The Big Cheese
    expect(text).to_contain_text("- The Big Cheese")
    expect(text).to_contain_text('"')

def test_fetch_error(page: Page):
    """Verifies error handling when fetch fails."""
    # Intercept the request to api.adviceslip.com/advice and fail it
    page.route("**/advice", lambda route: route.abort())

    page.goto(f"http://localhost:{PORT}")

    # We must ensure we don't hit the 10% random joke chance which doesn't use the network.
    # To do this reliably, we might need to mock Math.random, but for now,
    # since we can't easily inject JS before load in this setup to mock Math.random perfectly
    # without modifying the source, we will rely on retries or just hope
    # the 10% chance doesn't hit.
    # OR better, we can mock `Math.random` using `page.add_init_script`.

    page.add_init_script("Math.random = () => 0.5;") # Force non-joke path

    btn = page.locator("#get-advice-btn")
    btn.click()

    text = page.locator("#advice-text")
    expect(text).to_contain_text("Failed to load advice")
