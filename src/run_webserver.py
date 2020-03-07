import psycopg2
from database.database_manager import DatabaseManager
from website.webserver import MyHandler, run
from configuration import *


db = DatabaseManager(psycopg2.connect(DB_GAME_PI_LOCAL))

if __name__ == "__main__":
    run(db)