from functools import partial  # needed to pass the DB into the handler class
from jinja2 import Template
from os import curdir, sep
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer


tasks = ["Cheese"]


class requestHandler(BaseHTTPRequestHandler):
    def __init__(self, db, *args, directory=None, **kwargs):
        self.db = db
        self.directory = f"{curdir}{sep}website{sep}public{sep}"
        super().__init__(*args, **kwargs)


    def get_content_type(self):
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
        if self.path == "/leaderboard/school/search":
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                self.school_id = fields.get('school_id')
                print(f"SCHOOL ID IS {self.school_id}")

            self.send_response(301)
            self.send_header('Location', "/leaderboard/global")
            self.end_headers()

    
    def do_GET(self):
        try:
            # redirect to the index page
            if self.path == "/":
                self.send_response(301)
                self.send_header("Location", "/index")
                self.end_headers()
                return
            
            if self.path == "/leaderboard":
                self.send_response(301)
                self.send_header("Location", "/leaderboard/index")
                self.end_headers()
                return


            # if the file is html (it wont contain a dot) or another extension (will contain a dot).
            print(self.path)
            if self.path.find(".") == -1:
                f = open(f"{self.directory}{self.path}.html") # open the html file.
                jinja_template = Template(f.read()) # load the web page into the jinja_template engine
            else:
                f = open(f"{self.directory}{self.path}") # open the file.

            
            # WEB PAGE FUNCTIONS
            if self.path == "/index":
                page = jinja_template.render(name='Testing123') # render the web page with all the variables

            if self.path == "/help":
                page = jinja_template.render()
            
            
            if self.path == "/leaderboard/index":
                page = jinja_template.render()

            if self.path == "/leaderboard/global":
                results = self.db.fetch_leaderboard_global()

                page = jinja_template.render(table_entries=results)

            if self.path == "/leaderboard/school":
                schools_list = self.db.fetch_all_schools()

                try:
                    if self.school_id:
                        table_entries = self.db.fetch_leaderboard_school(self.school_id)
                        school_name = self.db.fetch_school(self.school_id)['name']
                        
                        page = jinja_template.render(schools_list=schools_list,
                                                     table_entries=table_entries,
                                                     school_name=school_name)
                
                except:
                    page = jinja_template.render(schools_list=schools_list)



            if self.path == "/analysis/index":
                page = jinja_template.render()




            # SENDING PAGE HEADERS AND CONTENT
            try:
                # if 'page' variable, that means it's a jinja webpage (.html)
                if page:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(page.encode())
            except:
                # else, file must be CSS or other file type.
                if self.get_content_type() == "text/html":
                    # this must someones trying to access the raw .html file
                    self.send_error(403, "Stop trying to access the html file")

                else:
                    f_content = f.read()

                    self.send_response(200)
                    self.send_header('content-type', self.get_content_type())
                    self.end_headers()
                    self.wfile.write(f_content.encode())

            f.close()

        except:
            self.send_error(500, "I don't know what has happened... The server will now explode...")


def run(db):
    PORT_NUMBER = 8000

    try:
        # Create a web server and define the handler to manage the
        # incoming request
        
        handler = partial(requestHandler, db) # allows you to pass argument into the handler class!

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