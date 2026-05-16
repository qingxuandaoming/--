#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import unquote

PORT = 8090
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)
    
    def do_GET(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0]
        path = unquote(path).lstrip('/\\')
        fs_path = os.path.normpath(os.path.join(ROOT, path))
        
        if not os.path.exists(fs_path) or os.path.isdir(fs_path):
            self.path = '/index.html'
        
        return super().do_GET()

with socketserver.TCPServer(("", PORT), SPAHandler) as httpd:
    print(f"SPA server at port {PORT} from {ROOT}")
    httpd.serve_forever()
