import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    code = parsed_data.get('code', [''])[0]
    print("code: {}", code)

    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    self.wfile.write(b"Code recieved")

if __name__ == "__main__":
  server_address = ("", 80)
  httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
  print("Server started on port 80...")
  httpd.serve_forever()
