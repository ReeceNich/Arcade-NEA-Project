import psycopg2


class DB:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def close(self):
        self.conn.close()


    def setup(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS Questions;
        """)
        self.cursor.execute("""
        CREATE TABLE Questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, wrong_1 TEXT, wrong_2 TEXT, wrong_3 TEXT, subject TEXT, difficulty INTEGER);
        """)
        self.conn.commit()


class Question:
    def __init__(self, question, answer, wrong_1, wrong_2, wrong_3, subject, difficulty):
        self.question = question
        self.answer = answer
        self.wrong_1 = wrong_1
        self.wrong_2 = wrong_2
        self.wrong_3 = wrong_3
        self.subject = subject
        self.difficulty = difficulty


def example(conn):
    db = DB(conn)

    db.setup()

    #db.insert(Track("Happy Birthday", 10))
    
    #tracks = db.query_all_tracks()
    #for track in tracks:
    #    print(f"{track.title} played has been played {track.plays} times")


def postgres_example():
    conn = psycopg2.connect("dbname='database1' user=postgres password='password' host='localhost' port='5432'")
    example(conn)