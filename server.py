#!/usr/bin/env python3
"""
Bejaw Store - Local PKG install server for jailbroken PS4
Binds to 0.0.0.0 so it works on every IP of the host.
"""

import http.server
import socketserver
import json
import os
import sys
import socket
from urllib.parse import urlparse

PORT = 8000
HOST = "0.0.0.0"
STORE_DIR = os.path.dirname(os.path.abspath(__file__))


def local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if ":" not in ip and not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return sorted(set(ips))


class BejawHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STORE_DIR, **kwargs)

    def end_headers(self):
        try:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            if self.path.endswith(".json"):
                self.send_header("Cache-Control", "no-store")
            super().end_headers()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.end_headers()
        except Exception:
            pass

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                payload = {"status": "ok", "store": "Bejaw Store"}
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            self.close_connection = True
        except Exception:
            self.close_connection = True

    def log_message(self, fmt, *args):
        sys.stderr.write("[bejaw] " + (fmt % args) + "\n")


def main():
    os.chdir(STORE_DIR)
    with socketserver.ThreadingTCPServer((HOST, PORT), BejawHandler) as httpd:
        httpd.allow_reuse_address = True
        httpd.daemon_threads = True
        print("=" * 60)
        print("  Bejaw Store - PKG installer server")
        print("=" * 60)
        print(f"  Bound to : {HOST}:{PORT}")
        print("  Open in PS4 browser:")
        for ip in local_ips():
            print(f"      http://{ip}:{PORT}/")
        print("  Local:")
        print(f"      http://127.0.0.1:{PORT}/")
        print("=" * 60)
        print("  Ctrl+C to stop")
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[bejaw] stopped.")


if __name__ == "__main__":
    main()
