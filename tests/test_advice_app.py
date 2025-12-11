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

    # Force non-joke path to trigger fetch
    page.add_init_script("Math.random = () => 0.5;")

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    btn.click()

    text = page.locator("#advice-text")
    expect(text).to_contain_text("Failed to load advice")

def test_cheeseify_logic(page: Page):
    """Verifies that advice text is correctly 'cheeseified'."""
    # Mock the API response with specific text to test replacements
    page.route("**/advice", lambda route: route.fulfill(
        status=200,
        body='{"slip": { "id": 1, "advice": "Hello friend, I believe this is good." }}'
    ))

    # Force non-joke path
    page.add_init_script("Math.random = () => 0.5;")

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    text = page.locator("#advice-text")

    btn.click()

    # Expected replacements:
    # "Hello" -> "hallo-umi"
    # "friend" -> "friend-cheese"
    # "believe" -> "brie-lieve"
    # "good" -> "gouda"
    expect(text).to_contain_text("hallo-umi friend-cheese, I brie-lieve this is gouda.")

def test_random_cheese_joke(page: Page):
    """Verifies the 10% chance of getting a pure cheese joke."""
    # Force joke path (Math.random < 0.1)
    # Return 0.05. Logic: Math.floor(0.05 * 10) = 0 => First joke.
    page.add_init_script("Math.random = () => 0.05;")

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    text = page.locator("#advice-text")

    btn.click()

    expected_joke = "What cheese can be used to hide a horse? Mascarpone."

    expect(text).to_contain_text(expected_joke)
    expect(text).to_contain_text("- The Big Cheese")

def test_loading_state(page: Page):
    """Verifies the loading spinner and button state during fetch."""

    route_container = []

    def handler(route):
        route_container.append(route)
        # Do not fulfill here to keep request pending

    page.route("**/advice", handler)

    # Force non-joke path so it fetches advice
    page.add_init_script("Math.random = () => 0.5;")
    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    spinner = page.locator("#loading-spinner")

    btn.click()

    # Check state while request is pending (intercepted but not fulfilled)
    # The spinner should become visible
    expect(spinner).to_be_visible()
    expect(btn).to_be_disabled()

    # Fulfill the request
    # We expect the route to be captured
    assert len(route_container) > 0, "Request was not captured"
    route = route_container[0]
    route.fulfill(
        status=200,
        body='{"slip": { "id": 123, "advice": "Patience is a virtue." }}'
    )

    # Verify final state
    expect(spinner).not_to_be_visible()
    expect(btn).to_be_enabled()
    expect(page.locator("#advice-text")).to_contain_text("Patience is a virtue")
