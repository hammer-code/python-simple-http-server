import socketserver
import http.server 
import os
from urllib.parse import parse_qs

PORT = 5050

result = "hey"

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        file_to_open = ""
        try:
            file_to_open = open(self.path[1:], 'r').read();
            self.send_response(200)
        except:
            file_to_open = "File Not Found"
            self.send_response(404)
        
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])        
        post_data = self.rfile.read(content_length)
        res = parse_qs(post_data.decode('utf-8'))

        name = "-" 
        age = "-"
        if 'name' in res: name = res['name'][0]
        if 'age' in res: age = res['age'][0]
        
        text = 'My name is {}. My age is {}'.format(name, age)

        self.wfile.write(bytes(text, 'utf-8'))


httpd = socketserver.TCPServer(("localhost", PORT), RequestHandler)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()