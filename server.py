import http.server
import json
import os
from urllib.parse import urlparse

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path in ('/save-tareas', '/save-datos', '/save-entregables', '/save-consorcio'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                if parsed_path.path == '/save-entregables':
                    filename = 'entregables.json'
                elif parsed_path.path == '/save-tareas':
                    filename = 'tareas.json'
                elif parsed_path.path == '/save-consorcio':
                    filename = 'consorcioInfo.json'
                else:
                    filename = 'datos.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                message = json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False).encode('utf-8')
                self.wfile.write(message)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"not_found"}')

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    handler_class = RequestHandler
    print(f'Serving HTTP on port {port}...')
    http.server.ThreadingHTTPServer(server_address, handler_class).serve_forever()
