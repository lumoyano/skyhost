# $ python -m http.server 8000 # Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

handler = http.server.SimpleHTTPResquestHandler
with socketserver.TCPServer(('0.0.0.0', 8000), handler)