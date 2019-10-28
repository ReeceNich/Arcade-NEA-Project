import arcade
import random


width = 800
height = 600
title = "Falling Man"
initial_movement_speed = 2
player_scaling = 0.2
incorrect_scaling = 0.1
max_cloud_scaling = 0.2
min_cloud_scaling = 0.05

class Player(arcade.Sprite):
    def update(self):
        pass


class IncorrectSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)


class CloudSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)
            

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BABY_BLUE)


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

        self.cloud_sprites_list = arcade.SpriteList()


    def on_draw(self):
        arcade.start_render()
        self.cloud_sprites_list.draw()
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
        self.cloud_sprites_list.update()
        
        # creates more sprites if there are not enough.
        if self.delta_time_elapsed > 2:
            self.create_incorrect_sprite()
            self.create_cloud_sprite()
            self.delta_time_elapsed = 0

        # speeds up each sprite. if off screen -> remove the sprite.
        for sprite in self.incorrect_sprites_list:
            sprite.center_y += self.movement_speed

            if sprite.center_y > (height + 50):
                sprite.remove_from_sprite_lists()


        # speeds up the clouds.
        for cloud in self.cloud_sprites_list:
            cloud.center_y += self.movement_speed / 2

            if cloud.center_y > (height + 50):
                cloud.remove_from_sprite_lists()


    def create_incorrect_sprite(self):
        incorrect = IncorrectSprite("images/incorrect_01.png", incorrect_scaling)
        incorrect.center_x = random.randrange(width)
        incorrect.center_y = random.randrange(-100, -50)
        self.incorrect_sprites_list.append(incorrect)

    
    def create_cloud_sprite(self):
        scaling = random.uniform(min_cloud_scaling, max_cloud_scaling)
        cloud = CloudSprite("images/cloud_01.png", scaling)
        cloud.center_x = random.randrange(width)
        cloud.center_y = random.randrange(-100, -50)
        self.cloud_sprites_list.append(cloud)
            
    

if __name__ == "__main__":
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()