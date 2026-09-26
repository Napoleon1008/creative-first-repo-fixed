from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = sys.argv[2] if len(sys.argv) > 2 else "build/web"

if not Path(DIRECTORY).is_dir():
    raise SystemExit(f"Directory not found: {DIRECTORY}")


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


handler = partial(NoCacheHandler, directory=DIRECTORY)
server = ThreadingHTTPServer(("0.0.0.0", PORT), handler)

print(f"Serving {DIRECTORY} on port {PORT}", flush=True)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
