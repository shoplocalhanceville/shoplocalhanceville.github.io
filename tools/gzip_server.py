#!/usr/bin/env python3
"""gzip_server.py: a small static file server for the Lighthouse CI gate.

Raw Python, standard library only, no dependencies. It serves a directory
read-only, like python3 -m http.server, with one deliberate difference:
text responses are gzip compressed when the client offers
Accept-Encoding: gzip, the way GitHub Pages serves the deployed site.
The gate measures the site through this server so its numbers reflect
the delivery mode real visitors get, instead of the uncompressed
delivery of the plain test server.

Usage:
    python3 tools/gzip_server.py [port] [--directory DIR] [--bind ADDR]

Defaults: port 8080, directory = current working directory,
bind = all interfaces (same as python3 -m http.server).
Only GET and HEAD are supported. There is no upload, no CGI, and no
write path of any kind.
"""

import argparse
import gzip
import io
import mimetypes
import os
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Response bodies at or above this size are candidates for compression.
MIN_COMPRESS_BYTES = 256

# Types worth compressing. Everything else (images, fonts, archives)
# is already compressed or binary and is sent as stored.
COMPRESSIBLE_TYPES = {
    "text/html",
    "text/css",
    "text/javascript",
    "application/javascript",
    "application/json",
    "application/manifest+json",
    "image/svg+xml",
    "application/xml",
    "text/xml",
    "text/plain",
    "text/csv",
    "application/rss+xml",
    "application/atom+xml",
}

EXTRA_TYPES = {
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".json": "application/json",
    ".map": "application/json",
    ".svg": "image/svg+xml",
    ".webmanifest": "application/manifest+json",
    ".wasm": "application/wasm",
}


def guess_content_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in EXTRA_TYPES:
        return EXTRA_TYPES[ext]
    ctype, _ = mimetypes.guess_type(path)
    return ctype or "application/octet-stream"


def gzip_bytes(data):
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=6, mtime=0) as fh:
        fh.write(data)
    return buf.getvalue()


class GzipHandler(SimpleHTTPRequestHandler):
    server_version = "GzipStatic/1.0"
    # Match the cache header GitHub Pages sends for site files.
    cache_control = "max-age=600"

    def do_GET(self):
        self._serve(send_body=True)

    def do_HEAD(self):
        self._serve(send_body=False)

    def _serve(self, send_body):
        # translate_path (inherited) normalizes the URL path and keeps
        # the request inside the served directory.
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            parts = self.path.split("?", 1)
            if not parts[0].endswith("/"):
                parts[0] += "/"
                location = "?".join(parts) if len(parts) > 1 else parts[0]
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", location)
                self.end_headers()
                return
            index = os.path.join(path, "index.html")
            if os.path.isfile(index):
                path = index
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "No index file and directory listings are off")
                return
        if not os.path.isfile(path):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        try:
            mtime = os.path.getmtime(path)
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return

        if self._not_modified(mtime):
            self.send_response(HTTPStatus.NOT_MODIFIED)
            self.end_headers()
            return

        ctype = guess_content_type(path)
        body = data
        encoding = None
        if (
            ctype in COMPRESSIBLE_TYPES
            and len(data) >= MIN_COMPRESS_BYTES
            and "gzip" in self.headers.get("Accept-Encoding", "")
        ):
            body = gzip_bytes(data)
            encoding = "gzip"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if encoding:
            self.send_header("Content-Encoding", encoding)
        if ctype in COMPRESSIBLE_TYPES:
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Cache-Control", self.cache_control)
        self.send_header("Last-Modified", self.date_time_string(mtime))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _not_modified(self, mtime):
        header = self.headers.get("If-Modified-Since")
        if not header:
            return False
        try:
            from email.utils import parsedate_to_datetime

            since = parsedate_to_datetime(header).timestamp()
        except (TypeError, ValueError):
            return False
        return int(mtime) <= int(since)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Static file server with gzip, for the Lighthouse CI gate.")
    parser.add_argument("port", nargs="?", type=int, default=8080, help="port to listen on (default 8080)")
    parser.add_argument("--directory", default=os.getcwd(), help="directory to serve (default: current directory)")
    parser.add_argument("--bind", default=None, help="address to bind (default: all interfaces)")
    args = parser.parse_args(argv)

    handler = lambda *a, **kw: GzipHandler(*a, directory=args.directory, **kw)
    server = ThreadingHTTPServer((args.bind or "", args.port), handler)
    print(
        "Serving HTTP on port {port} from directory {dir} ...".format(
            port=args.port, dir=os.path.abspath(args.directory)
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
