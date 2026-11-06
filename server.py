# -*- coding: utf-8 -*-
"""Static server with extensionless URL support: /about -> about.html"""
import http.server
import os
import socketserver

PORT = 8000


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # strip query/fragment, decode
        path = path.split('?', 1)[0].split('#', 1)[0]
        orig = super().translate_path(path)

        # directory -> its index.html (root '/' etc.)
        if os.path.isdir(orig):
            idx = os.path.join(orig, 'index.html')
            if os.path.exists(idx):
                return idx
            return orig

        # extensionless path that doesn't exist -> try <path>.html
        if not os.path.exists(orig):
            base = path.rstrip('/')
            if base and not os.path.splitext(base)[1]:
                cand = super().translate_path(base + '.html')
                if os.path.exists(cand):
                    return cand
        return orig

    def log_message(self, fmt, *args):
        pass  # keep console quiet


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), CleanURLHandler) as httpd:
        print(f'Serving on http://127.0.0.1:{PORT} (extensionless URLs supported)')
        httpd.serve_forever()
