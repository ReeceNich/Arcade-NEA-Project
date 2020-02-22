from login_window import Login

authenticated = None

while not authenticated:

    login = Login()
    login.draw_window()

    if login.email and login.passcode:
        from falling_man import *

        authenticated = db.auth_user(login.email, login.passcode)
        
        if authenticated:
            print("Successfully authenticated")
            window = MyGame(width, height, title, login.email, login.passcode)
            window.setup()

            print(login.email)
            print(login.passcode)

            arcade.run()
        
        else:
            print("Failed to authenticate...")
            continue


    else:
        print("didnt enter details")
