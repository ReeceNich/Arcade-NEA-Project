import arcade
import random


width = 800
height = 600
title = "Falling Man"
initial_movement_speed = 2
player_scaling = 0.2
incorrect_scaling = 0.1

class Player(arcade.Sprite):
    def update(self):
        pass


class IncorrectSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)
            

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_BROWN)


    def setup(self):
        # create sprites etc for a my game
        self.player_list = arcade.SpriteList()
        player = Player("images/player_01.png", player_scaling)
        player.center_x = width / 2
        player.center_y = height * 0.85
        self.player_list.append(player)

        self.incorrect_sprites_list = arcade.SpriteList()
        self.delta_time_elapsed = 0
        self.movement_speed = initial_movement_speed


    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.incorrect_sprites_list.draw()

    
    def on_mouse_motion(self, x, y, dy, dx):
        for player in self.player_list:
            player.center_x = x


    def on_update(self, delta_time):
        self.delta_time_elapsed += delta_time
        self.movement_speed += 0.002
        self.player_list.update()
        self.incorrect_sprites_list.update()
        
        for sprite in self.incorrect_sprites_list:
            sprite.center_y += self.movement_speed

            if sprite.center_y > (height + 50):
                sprite.remove_from_sprite_lists()

        if len(self.incorrect_sprites_list) <= 5:
            pass
            # self.create_incorrect_object()
        if self.delta_time_elapsed > 2:
            self.create_incorrect_object()
            self.delta_time_elapsed = 0


    def create_incorrect_object(self):
        incorrect = IncorrectSprite("images/incorrect_01.png", incorrect_scaling)
        incorrect.center_x = random.randrange(width)
        incorrect.center_y = random.randrange(-1, 0)
        self.incorrect_sprites_list.append(incorrect)
            
    

if __name__ == "__main__":
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()