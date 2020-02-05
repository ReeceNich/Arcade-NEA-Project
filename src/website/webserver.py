#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

# This class handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    def mime_type(self):
        for ext in [
            # html, js and css
            (".html", "text/html"),
            (".js", "application/javascript"),
            (".css", "text/css"),
            # images
            (".jpg", "image/jpg"),
            (".png", "image/png"),
            (".gif", "image/gif"),
        ]:
            if self.path.endswith(ext[0]):
                return ext[1]

        raise ValueError("unknown file extension")

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:
            # Open the static file requested and send it
            f = open(f"{curdir}{sep}{self.path}")
            self.send_response(200)
            self.send_header("Content-type", self.mime_type())
            self.end_headers()
            self.wfile.write(f.read().encode())    # NEEDED TO USE ENCODE() - TypeError: a bytes-like object is required, not 'str'
            f.close()
            return

        except IOError:
            self.send_error(404, f"File Not Found: {self.path}")


PORT_NUMBER = 8000

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(("", PORT_NUMBER), myHandler)
    print(f"Started httpserver on port {PORT_NUMBER}.")
    print(f"Visit http://localhost:{PORT_NUMBER}/ or press Ctrl + C to exit.")

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()