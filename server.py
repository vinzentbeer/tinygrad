import urllib.parse, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

from tinygrad.runtime.support.hip_comgr import compile_hip

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(b'Hello, World!')

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    code = parsed_data.get('code', [''])[0]
    lib = compile_hip(code)
    asm = subprocess.check_output(["/opt/rocm/llvm/bin/llvm-objdump", '-d', '-'], input=lib)
    asm = '\n'.join([x for x in asm.decode('utf-8').split("\n") if 's_code_end' not in x])

    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    self.wfile.write(asm.encode())

if __name__ == "__main__":
  server_address = ("0.0.0.0", 80)
  httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
  print("Server started on port 80...")
  httpd.serve_forever()
