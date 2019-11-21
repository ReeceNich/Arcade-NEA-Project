import sqlite3
import psycopg2

class Track():
    def __init__(self, title, plays):
        self.title = title
        self.plays = plays

class DB():
    tracks = []

    def insert(self, track):
        self.tracks.append(track)

    def get_all(self):
        return self.tracks

class DB():
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def close(self):
        self.conn.close()

    def setup(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS Tracks;
        """
        )
        self.cursor.execute("""
        CREATE TABLE Tracks (title TEXT, plays INTEGER);
        """)
        self.conn.commit()

    def insert(self, track):
        sqlStatement = f"""
        INSERT INTO Tracks (title, plays) VALUES ( '{track.title}', {track.plays} )
        """
        print(sqlStatement)
        self.cursor.execute(sqlStatement)
        self.conn.commit()

    def query_all_tracks(self):
        self.cursor.execute('SELECT title, plays FROM Tracks')
        # or can use: records = self.cursor.fetchall() and then for row in record: ...
        tracks = []
        for row in self.cursor:
            tracks.append(Track(row[0], row[1]))
        return tracks


def example(conn):
    db = DB(conn)

    db.setup()

    # for track in [Track(), Track(), Track()]:
    #     db.insert(track)
    db.insert(Track("Happy Birthday", 10))
    db.insert(Track("auld lang syne", 12))
    db.insert(Track("Default Dance", 42069))
    tracks = db.query_all_tracks()
    for track in tracks:
        print(f"{track.title} played has been played {track.plays} times")

def sqlite_example():
    conn = sqlite3.connect('music.sqlite3')
    example(conn)

def postgres_example():
    conn = psycopg2.connect("dbname='database1' user=postgres password='password' host='localhost' port= '5432'")
    example(conn)

sqlite_example()
postgres_example()
