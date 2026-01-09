import pytest
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Define the server port
PORT = 8000

@pytest.fixture(scope="session", autouse=True)
def http_server():
    """Starts a simple HTTP server in a separate thread."""
    server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
