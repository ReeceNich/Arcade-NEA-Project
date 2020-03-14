from functools import partial  # needed to pass the DB into the handler class
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, db, *args, directory=None, **kwargs):
        self.db = db
        super().__init__(*args, **kwargs)

    
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.path.encode())


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
    print("Run using the run script in the root directory")