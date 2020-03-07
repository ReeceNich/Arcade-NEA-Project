from database.database_manager import DatabaseManager
from configuration import *
import psycopg2


d = DatabaseManager(psycopg2.connect(DB_GAME_PI_LOCAL))

d.setup()
d.setup_dummy_data()