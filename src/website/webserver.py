from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from jinja2 import Template, Environment, FileSystemLoader
#from database_manager import DatabaseManager


from http import cookies


# This class handles any incoming request from
# the browser
class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, db, *args, directory=None, **kwargs):
        self.db = db
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
            (".gif", "image/gif")
        ]:
            if self.path.endswith(ext[0]):
                return ext[1]

        raise ValueError("unknown file extension")

    def do_POST(self):
        print(self.path)
        print("HUZZZAHHHHH")

    # Handler for the GET requests
    def do_GET(self):
        # Open the static file requested and send it.
        print(f"{curdir}{sep}website{sep}public{sep}{self.path}")
        try:
            # cookies = self.headers.get('Cookie')
            # print(cookies)

            if self.path == "/": # this is required as / is actually the homepage.
                self.path = "/index.html"

                name = "Reece"
                # name = self.db.get_name()

                f = open(f"{curdir}{sep}website{sep}public{sep}{self.path}") # open the web page file
                jinja_template = Template(f.read()) # load the web page into the jinja_template engine
                page = jinja_template.render(name=name) # render the web page with all the variables

            else:
                f = open(f"{curdir}{sep}website{sep}public{sep}{self.path}")
                jinja_template = Template(f.read())

                if self.path == "/help.html":
                    page = jinja_template.render()

                elif self.path == "/leaderboard/index.html":
                    self.path = "/leaderboard/index.html"
                    page = jinja_template.render()
                
                elif self.path == "/leaderboard/global.html":
                    table_entries = [
                        {
                            'name': 'Reece',
                            'score': 420
                        },
                        {
                            'name': 'Louis',
                            'score': 69
                        },
                        {
                            'name': 'Olly',
                            'score': 1
                        },
                        {
                            'name': 'Treeve',
                            'score': -999
                        }
                    ]

                    table_entries = self.db.fetch_leaderboard_global()
                    print(table_entries)
                    page = jinja_template.render(table_entries=table_entries)


            self.send_response(200)
            self.send_header("Content-type", self.mime_type())
            # self.send_header("Set-Cookie", "user=reece")
            self.end_headers()
            self.wfile.write(page.encode())    # NEEDED TO USE ENCODE() - TypeError: a bytes-like object is required, not 'str'
            f.close()
            return

        except IOError:
            self.send_error(404, f"File Not Found: {self.path}")


def run(db):
    PORT_NUMBER = 8000

    try:
        # Create a web server and define the handler to manage the
        # incoming request
        
        handler = partial(MyHandler, db) # allows you to pass argument into the handler class!

        server = HTTPServer(("", PORT_NUMBER), handler)
        print(f"Started httpserver on port {PORT_NUMBER}.")
        print(f"Visit http://localhost:{PORT_NUMBER}/ or press Ctrl + C to exit.")

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C received, shutting down the web server")
        server.socket.close()

if __name__ == "__main__":
    print("Please run using the other run_webserver.py")