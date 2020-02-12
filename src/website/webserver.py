from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
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
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        
        post_data = str(post_data)

        if self.path == "/leaderboard/school.html":
            try:
                s_id = post_data[post_data.find('=')+1:-1] # finds the = sign and assigns value after.
                print(post_data)
                print(s_id)

                self.send_response(301)
                self.send_header("Location", "/leaderboard/school.html")
                self.send_header("Set-Cookie", f"school_id={s_id}") # stores value in a cookie.
                self.end_headers()
            except:
                self.send_response(301)
                self.send_header("Location", "/leaderboard/school.html")
                self.end_headers()
                
        if self.path == "/leaderboard/subject.html":
            try:
                print(post_data)
                school_id = post_data[post_data.find('=')+1:post_data.find("&")] # finds the first = sign and assigns value after but before &.
                post_data = post_data[post_data.find("&"):] # deletes the first part of the data.
                subject_id = post_data[post_data.find('=')+1:-1]

                print(post_data)
                print(f"school id {school_id}")
                print(f"subject id {subject_id}")

                self.send_response(301)
                self.send_header("Location", "/leaderboard/subject.html")
                self.send_header("Set-Cookie", f"school_id={school_id}") # stores value in a cookie.
                self.send_header("Set-Cookie", f"subject_id={subject_id}") # stores value in a cookie.
                self.end_headers()
            except:
                self.send_response(301)
                self.send_header("Location", "/leaderboard/subject.html")
                self.end_headers()

        else:
            self.send_response(301)
            self.send_header("Location", '/')
            self.end_headers()

    # Handler for the GET requests
    def do_GET(self):
        # Open the static file requested and sends it.
        try:
            print(self.path)

            if self.path == "/styles/style.css":
                f = open(f"{curdir}{sep}website{sep}public{sep}{self.path}")

            elif self.path == "/": # this is required as / is actually the homepage.
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
                    table_entries = self.db.fetch_leaderboard_global()
                    print(table_entries)
                    page = jinja_template.render(table_entries=table_entries)
                
                elif self.path == "/leaderboard/school.html":
                    schools_list = self.db.fetch_all_schools()

                    table_entries = None
                    school_name = None
                    try:
                        cookies = SimpleCookie(self.headers.get('Cookie'))
                        s_id = cookies['school_id'].value

                        if s_id:
                            table_entries = self.db.fetch_leaderboard_school(s_id)
                            school_name = self.db.fetch_school_name(s_id)

                    except:
                        pass

                    print(schools_list)
                    print(table_entries)
                    print(school_name)
                    page = jinja_template.render(schools_list=schools_list, table_entries=table_entries, school_name=school_name)
                
                elif self.path == "/leaderboard/subject.html":
                    schools_list = self.db.fetch_all_schools()
                    subjects_list = self.db.fetch_all_subjects()

                    table_entries = None
                    school_name = None
                    subject_name = None
                    try:
                        cookies = SimpleCookie(self.headers.get('Cookie'))
                        school_id = cookies['school_id'].value
                        subject_id = cookies['subject_id'].value
                        print(f"school id {school_id}, subject id {subject_id}")

                        if school_id and subject_id:
                            table_entries = self.db.fetch_leaderboard_school_subject(school_id, subject_id)
                            school_name = self.db.fetch_school_name(school_id)
                            subject_name = self.db.fetch_subject_name(subject_id)

                            print(f"school name, subject name {school_name}, {subject_name}")

                    except:
                        pass

                    print(schools_list)
                    print(table_entries)
                    print(school_name)
                    page = jinja_template.render(schools_list=schools_list, table_entries=table_entries, school_name=school_name, subjects_list=subjects_list, subject_name=subject_name)
                
                
                else:
                    pass

            self.send_response(200)
            self.send_header("Content-type", self.mime_type())
            # self.send_header("Set-Cookie", "user=reece")
            self.end_headers()

            # if page that means its a jinja webpage (html). else, it must be css or other file type.            
            try:
                if page:
                    self.wfile.write(page.encode())
            except:
                f_content = f.read()
                self.wfile.write(f_content.encode())

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