import arcade
import random


width = 800
height = 600
title = "Falling Man"
movement_speed = 2
player_scaling = 0.1
incorrect_scaling = 0.1

class Player(arcade.Sprite):

    def update(self):
        pass


class IncorrectSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)
        self.upper_bound = 2
        self.change_x = self.upper_bound


    def update(self):
        self.center_y += movement_speed
        self.center_x += self.change_x

        if self.center_x <= 0:
            self.change_x = abs(self.change_x)
        elif self.center_x >= width:
            self.change_x = -abs(self.change_x)
        else:
            pass
            

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_BROWN)


    def setup(self):
        # create sprites etc for a my game
        self.player_list = arcade.SpriteList()
        player = Player("images/player_01.png", player_scaling)
        player.center_x = width / 2
        player.center_y = height *0.75
        self.player_list.append(player)

        self.incorrect_sprites_list = arcade.SpriteList()
        for _ in range(5):
            incorrect = IncorrectSprite("images/incorrect_01.png", incorrect_scaling)
            self.incorrect_sprites_list.append(incorrect)


    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.incorrect_sprites_list.draw()

    
    def on_mouse_motion(self, x, y, dy, dx):
        """
        for player in self.player_list:
            player.center_x = x
            player.center_y = y
        """
        pass


    def update(self, delta_time):
        self.player_list.update()
        self.incorrect_sprites_list.update()
    

if __name__ == "__main__":
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()