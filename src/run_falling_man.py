from login_window import Login

login = Login()
login.draw_window()

if login.email and login.passcode:
    from falling_man import *

    window = MyGame(width, height, title, login.email, login.passcode)
    window.setup()

    print(login.email)
    print(login.passcode)

    arcade.run()

else:
    print("didnt enter details")
