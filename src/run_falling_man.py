from game.login_window import Login
from database.database_manager import DatabaseManager
from database.database_classes import School, Difficulty, Subject, YearGroup, Topic, Teacher, User, Question, Answer, QuestionAnswered
import psycopg2


# db = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))
db = DatabaseManager(psycopg2.connect("dbname='game' user='pi' password='raspberry' host='pi.local' port='5432'"))

authenticated = None

while not authenticated:

    login = Login()
    # login.draw_window()
    login.window.destroy()
    login.username = "rnicholls13"
    login.passcode = "5678"
    login.school_id = 2

    if login.username and login.passcode and login.school_id:
        import arcade
        from game.constants import Constants
        from game.falling_man import MyGame

        authenticated = db.auth_user(login.username, login.passcode, login.school_id)
        
        if authenticated:
            print("Successfully authenticated")
            constants = Constants()
            window = MyGame(constants, constants.width, constants.height, constants.title, database_manager=db, username=login.username, school_id=login.school_id)
            window.setup()

            arcade.run()
        
        else:
            print("Failed to authenticate...")
            continue


    else:
        print("didnt enter details")
