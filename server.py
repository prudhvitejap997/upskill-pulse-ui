import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIR  = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, format, *args):
        print(f"  {args[0]}  {args[1]}  {args[2]}")

print(f"\n  QuizCraft running at  →  http://localhost:{PORT}\n")
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
