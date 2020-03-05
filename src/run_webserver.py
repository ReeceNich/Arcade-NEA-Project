import psycopg2
from database.database_manager import DatabaseManager
from website.webserver import MyHandler, run

# db = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))
db = DatabaseManager(psycopg2.connect("dbname='game' user='pi' password='raspberry' host='pi.local' port='5432'"))

if __name__ == "__main__":
    run(db)