import arcade
import random


width = 800
height = 1000
title = "Falling Man"
initial_movement_speed = 2
player_scaling = 0.2
incorrect_scaling = 0.1
correct_scaling = 0.1
max_cloud_scaling = 0.2
min_cloud_scaling = 0.05


data = [
    {
        'question': 'What is 10x10?',
        'answer': '100',
        'wrong_1': '20',
        'wrong_2': '1000',
        'wrong_3': '1010'
    }, {
        'question': 'What colour is the sky?',
        'answer': 'Blue',
        'wrong_1': 'Red',
        'wrong_2': 'Green',
        'wrong_3': 'Yellow'
    }, {
        'question': 'Who is the Queen?',
        'answer': 'Elizabeth',
        'wrong_1': 'Victoria',
        'wrong_2': 'Louis',
        'wrong_3': 'Jane'
    }
]


class Player(arcade.Sprite):
    def update(self):
        pass


class IncorrectSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)


class CorrectSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)


class CloudSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)
            

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        arcade.set_background_color(arcade.color.BABY_BLUE)


    def setup(self):
        # create sprites etc for a my game
        self.player_list = arcade.SpriteList()
        player = Player("images/player_01.png", player_scaling)
        player.center_x = self.width / 2
        # player.center_y = self.height - 2
        player.top = self.height - 110
        self.player_list.append(player)

        self.incorrect_sprites_list = arcade.SpriteList()
        self.correct_sprites_list = arcade.SpriteList()
        self.delta_time_elapsed = 0
        self.movement_speed = initial_movement_speed

        self.cloud_sprites_list = arcade.SpriteList()

        self.player_lives = 3
        self.current_q_and_a = data[0]
        self.player_score = 0


    def on_draw(self):
        arcade.start_render()
        self.cloud_sprites_list.draw()
        self.player_list.draw()

        self.correct_sprites_list.draw()
        self.incorrect_sprites_list.draw()

        self.draw_text_on_correct_sprites(self.correct_sprites_list)
        self.draw_text_on_incorrect_sprites(self.incorrect_sprites_list)

        self.draw_toolbar()

    
    def on_mouse_motion(self, x, y, dy, dx):
        for player in self.player_list:
            player.center_x = x


    def on_update(self, delta_time):
        self.delta_time_elapsed += delta_time
        self.movement_speed += 0.001
        self.player_list.update()

        self.correct_sprites_list.update()
        self.incorrect_sprites_list.update()

        self.cloud_sprites_list.update()
        
        # creates more sprites if there are not enough.
        if self.delta_time_elapsed > 2:
            if random.randrange(0, 3) == 0:
                print("Create correct sprite")
                self.create_correct_sprite()
            else:
                print("Creat incorrect sprite")
                self.create_incorrect_sprite()

            self.create_cloud_sprite()
            self.delta_time_elapsed = 0

        # speeds up each sprite. if off screen -> remove the sprite.
        for sprite in self.incorrect_sprites_list:
            sprite.center_y += self.movement_speed

            if sprite.center_y > (self.height + 50):
                sprite.remove_from_sprite_lists()
        
        for sprite in self.correct_sprites_list:
            sprite.center_y += self.movement_speed

            if sprite.center_y > (self.height + 50):
                sprite.remove_from_sprite_lists()


        # speeds up the clouds.
        for cloud in self.cloud_sprites_list:
            cloud.center_y += self.movement_speed / 2

            if cloud.center_y > (self.height + 50):
                cloud.remove_from_sprite_lists()


    def create_incorrect_sprite(self):
        incorrect = IncorrectSprite("images/incorrect_01.png", incorrect_scaling)
        incorrect.center_x = random.randrange(self.width)
        incorrect.center_y = random.randrange(-100, -50)
        self.incorrect_sprites_list.append(incorrect)
        

    def create_correct_sprite(self):
        correct = CorrectSprite("images/correct_01.png", correct_scaling)
        correct.center_x = random.randrange(self.width)
        correct.center_y = random.randrange(-100, -50)
        self.correct_sprites_list.append(correct)

    
    def create_cloud_sprite(self):
        scaling = random.uniform(min_cloud_scaling, max_cloud_scaling)
        cloud = CloudSprite("images/cloud_01.png", scaling)
        cloud.center_x = random.randrange(self.width)
        cloud.center_y = random.randrange(-100, -50)
        self.cloud_sprites_list.append(cloud)

    
    def draw_text_on_correct_sprites(self, sprite_list):
        # draw the text onto the sprites.
        for sprite in sprite_list:
            arcade.draw_text(self.current_q_and_a['answer'], sprite.left, sprite.center_y, color=arcade.color.BLACK, font_size=12, width=int(sprite.right-sprite.left), align="center")
            #print(f"CORRECT!: {self.current_q_and_a['answer']}")

    def draw_text_on_incorrect_sprites(self, sprite_list):
        # draw the text onto the sprites.
        for sprite in sprite_list:
            try:
                if sprite.already_chosen_answer:
                    arcade.draw_text(wrong_text, sprite.left, sprite.center_y, color=arcade.color.BLACK, font_size=12, width=int(sprite.right-sprite.left), align="center")
                else:
                    wrong_answers = [self.current_q_and_a['wrong_1'], self.current_q_and_a['wrong_2'], self.current_q_and_a['wrong_3']]
                    wrong_text = wrong_answers[random.randrange(0, 2)]
                    sprite.already_chosen_answer = True
            except:
                #print("TRY FAILED")
                sprite.already_chosen_answer = True
            
            #print(f"INCORRECT!: {wrong_answers[random.randrange(0, 2)]}")

    def draw_toolbar(self):
        # white bar (question)
        arcade.draw_lrtb_rectangle_filled(self.width*0.15, self.width*0.85, self.height, self.height-100, arcade.color.WHITE)
        arcade.draw_text("QUESTION", self.width*0.15, self.height-20, arcade.color.BLACK, font_size=14, width=int(self.width*0.85-self.width*0.15), align="center")
        arcade.draw_text(self.current_q_and_a['question'], self.width*0.15, self.height-50, arcade.color.BLACK, font_size=12, width=int(self.width*0.85-self.width*0.15), align="center")

        # lives box (right side)
        arcade.draw_lrtb_rectangle_filled(0, self.width*0.15, self.height, self.height-100, (149, 249, 227))
        arcade.draw_text("Lives", 0, self.height-20, arcade.color.BLACK, font_size=14, width=int(self.width*0.15), align="center")
        arcade.draw_text(str(self.player_lives), 0, self.height-50, arcade.color.BLACK, font_size=14, width=int(self.width*0.15), align="center")

        # score box (left side)
        arcade.draw_lrtb_rectangle_filled(self.width*0.85, self.width, self.height, self.height-100, (231, 200, 221))
        arcade.draw_text("Score", self.width*0.85, self.height-20, arcade.color.BLACK, font_size=14, width=int(self.width-self.width*0.85), align="center")
        arcade.draw_text(str(self.player_score), self.width*0.85, self.height-50, arcade.color.BLACK, font_size=14, width=int(self.width-self.width*0.85), align="center")


if __name__ == "__main__":
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()