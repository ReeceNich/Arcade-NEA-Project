from database.database_manager import DatabaseManager
import psycopg2


d = DatabaseManager(psycopg2.connect("dbname='game' user='pi' password='raspberry' host='pi.local' port='5432'"))

d.setup()
d.setup_dummy_data()