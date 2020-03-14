import tkinter
from game.login_window import Login
from database.database_manager import DatabaseManager
from database.database_classes import School, Difficulty, Subject, YearGroup, Topic, Teacher, User, Question, Answer, QuestionAnswered
from configuration import *
import psycopg2


db = DatabaseManager(psycopg2.connect(DB_GAME_GLOBAL))

authenticated = None

while not authenticated:

    login = Login(db)
    # login.draw_window()
    login.window.destroy()
    login.username = "rnicholls13"
    login.passcode = "5678"
    login.school_id = 2
    login.subject_id = 'MATHS'
    login.topic_id = 'PERCENTAGE'

    if login.username and login.passcode and login.school_id and login.subject_id and login.topic_id:
        import arcade
        from game.constants import Constants
        from game.falling_man import MyGame

        authenticated = db.auth_user(login.username, login.passcode, login.school_id)
        
        if authenticated:
            print("Successfully authenticated")
            constants = Constants()
            window = MyGame(database_manager=db, login=login)
            # window.setup()

            arcade.run()
        
        else:
            print("Failed to authenticate...")
            continue


    else:
        print("didnt enter details")
