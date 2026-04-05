from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import os

PORT = int(os.environ.get('PORT', 8080))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass

def run():
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    server.serve_forever()

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
