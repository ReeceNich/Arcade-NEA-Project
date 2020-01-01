from login_window import Login

login = Login()
login.draw_window()

from falling_man import *

window = MyGame(width, height, title, login.username, login.passcode)
window.setup()

print(login.username)
print(login.passcode)

arcade.run()
