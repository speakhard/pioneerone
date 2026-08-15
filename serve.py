"""Serve the built site for local checking.

    python serve.py [port]

Threaded on purpose. The single-threaded default queues requests, and a page
with six lazily-loaded stills plus three fonts hits it hard enough that images
appear to fail when in fact they were merely waiting — which then gets
mistaken for a bug in the site. Binds loopback only.
"""
from __future__ import annotations

import functools
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent / "site"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8791


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # noqa: D102 - quiet by default
        pass

    def end_headers(self):
        # Never serve a stale page while iterating on the design.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> int:
    if not ROOT.is_dir():
        print("site/ does not exist — run: python builder.py", file=sys.stderr)
        return 1
    handler = functools.partial(Handler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"serving {ROOT} at http://127.0.0.1:{PORT}/  (ctrl-c to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
