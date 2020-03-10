import arcade


class Sounds:
    def __init__(self):
        self.coin_5 = arcade.load_sound("sounds/coin5.wav")
        self.explosion_2 = arcade.load_sound("sounds/explosion2.wav")
        self.gameover_1 = arcade.load_sound("sounds/gameover1.wav")
        self.upgrade_3 = arcade.load_sound("sounds/upgrade3.wav")
        self.fall_3 = arcade.load_sound("sounds/fall3.wav")