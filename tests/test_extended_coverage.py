import pytest
from playwright.sync_api import Page, expect

PORT = 8000

def test_malformed_json_handling(page: Page):
    """Verifies that the app handles malformed JSON response from the API."""
    # Force non-joke path
    page.add_init_script("Math.random = () => 0.5;")

    # Mock the API to return invalid JSON
    page.route("**/advice", lambda route: route.fulfill(
        status=200,
        body="This is not JSON"
    ))

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    btn.click()

    text = page.locator("#advice-text")
    # Should display the load error message
    expect(text).to_contain_text("Failed to load advice")

def test_regex_word_boundaries(page: Page):
    """Verifies that cheeseify respects word boundaries."""
    # Force non-joke path
    page.add_init_script("Math.random = () => 0.5;")

    # Mock API with words that contain pun keys but shouldn't be replaced
    # "good" is a key -> "gouda"
    # "goodness" contains "good" but shouldn't match
    # "agood" contains "good" but shouldn't match
    page.route("**/advice", lambda route: route.fulfill(
        status=200,
        body='{"slip": { "id": 1, "advice": "The goodness of agood thing." }}'
    ))

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    btn.click()

    text = page.locator("#advice-text")
    # "thing" -> "thing... or string cheese"
    expect(text).to_contain_text("The goodness of agood thing... or string cheese.")

def test_case_insensitivity_behavior(page: Page):
    """Verifies that cheeseify handles mixed case input."""
    # Force non-joke path
    page.add_init_script("Math.random = () => 0.5;")

    # Mock API with uppercase words
    # "GOOD" should be replaced by "gouda"
    # "FRIEND" should be replaced by "friend-cheese"
    page.route("**/advice", lambda route: route.fulfill(
        status=200,
        body='{"slip": { "id": 1, "advice": "GOOD FRIEND" }}'
    ))

    page.goto(f"http://localhost:{PORT}")

    btn = page.locator("#get-advice-btn")
    btn.click()

    text = page.locator("#advice-text")
    # Current implementation replaces matched text with the value from map (which is lowercase)
    # So "GOOD" -> "gouda", "FRIEND" -> "friend-cheese"
    expect(text).to_contain_text("gouda friend-cheese")
