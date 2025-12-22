"""Test HTTP server that returns a fixed JSON response.

WARNING:
    This server is intended for testing purposes only.
    Do not use it in production environments.
"""

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

VALID_RESPONSE = {
    "timestamp": 1761808694,
    "base": "EUR",
    "date": "2025-10-30",
    "rates": {
        "USD": 1.161849,
        "EUR": 1.0,
        "PLN": 4.243909,
        "GTQ": 8.899562,
    },
    "success": True,
}

MAL_RESPONSE = {
    "alert(1)": 1761808694,
    "base": "alert(1)",
    "date": "alert(1)",
    "rates": {
        "USD": 1.161849,
        "EUR": 1.0,
        "PLN": 4.243909,
        "GTQ": 8.899562,
    },
    "success": True,
}

INVALID_RESPONSE = {
    "alert(1)": "alert(1)",
    "base": "alert(1)",
    "date": "alert(1)",
    "rates": {
        "USD": "alert(1)",
        "EUR": "alert(1)",
        "PLN": "alert(1)",
        "GTQ": "alert(1)",
    },
    "success": "alert(1)",
}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    RESPONSE = INVALID_RESPONSE

    def do_GET(self):
        logging.info(f"Received GET request for path: {self.path}")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.RESPONSE).encode())


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting httpd server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8080.")
            port = 8080
    else:
        port = 8080

    run(port=port)
