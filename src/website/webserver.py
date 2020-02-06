from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from jinja2 import Template

from http import cookies


class DB():
    def __init__(self):
        pass

    def get_name(self):
        return "Reece"

# This class handles any incoming request from
# the browser
class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.db = DB()
        super().__init__(*args, **kwargs)

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

    def do_POST(self):
        print(self.path)

    # Handler for the GET requests
    def do_GET(self):
        # Open the static file requested and send it
        try:
            if self.path == "/":
                self.path = "/index.html"

                # name = "Reece"
                name = self.db.get_name()

                f = open(f"{curdir}{sep}public{sep}{self.path}")
                jinja_template = Template(f.read())
                page = jinja_template.render(name=name)

            
            # cookies = self.headers.get('Cookie')
            # print(cookies)


            f = open(f"{curdir}{sep}public{sep}{self.path}")
            jinja_template = Template(f.read())

            if self.path == "/help.html":
                print("DIODE")
                page = jinja_template.render()


            self.send_response(200)
            self.send_header("Content-type", self.mime_type())
            # self.send_header("Set-Cookie", "user=reece")
            self.end_headers()
            self.wfile.write(page.encode())    # NEEDED TO USE ENCODE() - TypeError: a bytes-like object is required, not 'str'
            f.close()
            return

        except IOError:
            self.send_error(404, f"File Not Found: {self.path}")


PORT_NUMBER = 8000

try:
    # Create a web server and define the handler to manage the
    # incoming request

    server = HTTPServer(("", PORT_NUMBER), MyHandler)
    print(f"Started httpserver on port {PORT_NUMBER}.")
    print(f"Visit http://localhost:{PORT_NUMBER}/ or press Ctrl + C to exit.")

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()