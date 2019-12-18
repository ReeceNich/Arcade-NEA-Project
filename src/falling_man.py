import arcade
import random
from database_manager import *


width = 800
height = 1000
title = "Falling Man"
initial_movement_speed = 2
player_scaling = 0.2
incorrect_scaling = 0.1
correct_scaling = 0.1
max_cloud_scaling = 0.2
min_cloud_scaling = 0.05
answer_font_size = 12

STATE_INSTRUCTIONS = 0
STATE_GAME_RUNNNG = 1
STATE_GAME_PAUSED = 2
STATE_GAME_OVER = 3


db = DB(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))
data = db.fetch_all()


class Player(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)


class IncorrectSprite(arcade.Sprite):
    def __init__(self, img, scale, question_id, incorrect_answer_text):
        super().__init__(img, scale)
        self.question_id = question_id
        self.text = incorrect_answer_text.replace(' ', '\n')


class CorrectSprite(arcade.Sprite):
    def __init__(self, img, scale, question_id, correct_answer_text):
        super().__init__(img, scale)
        self.question_id = question_id
        self.text = correct_answer_text.replace(' ', '\n')


class CloudSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)
            

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        arcade.set_background_color(arcade.color.BABY_BLUE)

        self.current_state = STATE_INSTRUCTIONS


    def setup(self):
        # create sprites etc for a my game
        self.player_sprite = Player("images/player_01.png", player_scaling)
        self.player_sprite.center_x = self.width / 2
        # self.player_sprite.center_y = self.height - 2
        self.player_sprite.top = self.height - 110

        self.incorrect_sprites_list = arcade.SpriteList()
        self.correct_sprites_list = arcade.SpriteList()

        self.delta_time_elapsed = 0
        self.movement_speed = initial_movement_speed

        self.cloud_sprites_list = arcade.SpriteList()

        self.player_lives = 3
        self.current_q_and_a_pointer = 0
        self.current_q_and_a = data[self.current_q_and_a_pointer]
        self.player_score = 0


    def on_draw(self):
        arcade.start_render()
        
        if self.current_state == STATE_INSTRUCTIONS:
            self.draw_instructions()

        elif self.current_state == STATE_GAME_RUNNNG:
            self.draw_game_running()
        
        elif self.current_state == STATE_GAME_PAUSED:
            self.draw_paused()
            
        elif self.current_state == STATE_GAME_OVER:
            pass
        else:
            # default to game over here.
            pass
    
    def draw_game_running(self):
        self.cloud_sprites_list.draw()
        self.player_sprite.draw()

        self.correct_sprites_list.draw()
        self.incorrect_sprites_list.draw()

        self.draw_text_on_sprites(self.correct_sprites_list)
        self.draw_text_on_sprites(self.incorrect_sprites_list)

        self.draw_toolbar()


    def draw_instructions(self):
        arcade.draw_rectangle_filled(self.width//2, self.height//2, self.width-100, self.height-100, arcade.color.WHITE)
        arcade.draw_rectangle_outline(self.width//2, self.height//2, self.width-100, self.height-100, arcade.color.BLACK, 5)
        arcade.draw_text("Welcome to Falling Man!", 0, self.height-150, arcade.color.BLACK, 48, self.width, 'center')
        arcade.draw_text("Your character will be falling through the sky.", 0, self.height-250, arcade.color.BLACK, 18, self.width, 'center')
        arcade.draw_text("Direct them using the mouse and collect all the correct answers!", 0, self.height-300, arcade.color.BLACK, 18, self.width, 'center')
        arcade.draw_text("Try and avoid the wrong answers... they hurt you!", 0, self.height-350, arcade.color.BLACK, 18, self.width, 'center',)
        arcade.draw_text("Click anywhere to start...", 0, 150, arcade.color.BLACK, 18, self.width, 'center')


    def draw_paused(self):
        arcade.draw_text("Paused", 0, self.height//2, arcade.color.DARK_RED, 96, self.width, 'center')
        arcade.draw_text("(to resume, press Escape)", 0, self.height//2 - 35, arcade.color.DARK_SLATE_GRAY, 14, self.width, 'center')
        arcade.draw_text(f"Lives remaining: {self.player_lives}", 0, self.height//2 - 125, arcade.color.BLACK, 18, self.width, 'center')
        arcade.draw_text(f"Current score: {self.player_score}", 0, self.height//2 - 165, arcade.color.BLACK, 18, self.width, 'center')
    
    def on_mouse_motion(self, x, y, dy, dx):
        # only move the character if the game is 'running'.
        if self.current_state == STATE_GAME_RUNNNG:
            self.player_sprite.center_x = x

        else:
            pass


    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == STATE_INSTRUCTIONS:
            self.current_state = STATE_GAME_RUNNNG
        elif self.current_state == STATE_GAME_OVER:
            pass
        else:
            pass


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # pauses/unpaused the game
            if self.current_state == STATE_GAME_RUNNNG:
                self.current_state = STATE_GAME_PAUSED
            elif self.current_state == STATE_GAME_PAUSED:
                self.current_state = STATE_GAME_RUNNNG
            else:
                pass
        else:
            pass

    def on_key_release(self, key, modifiers):
        # not really necessary...
        if key == arcade.key.ESCAPE:
            pass


    def update(self, delta_time):
        if self.current_state == STATE_GAME_RUNNNG:
            self.delta_time_elapsed += delta_time
            self.movement_speed += 0.001
            self.player_sprite.update()

            self.correct_sprites_list.update()
            self.incorrect_sprites_list.update()

            self.cloud_sprites_list.update()
            
            # creates more sprites if there are not enough.
            if self.delta_time_elapsed > 1:
                if random.randrange(0, 3) == 0:
                    print("Create correct sprite")
                    self.create_correct_sprite(self.current_q_and_a.id, self.current_q_and_a.answer)
                    
                else:
                    print("Create incorrect sprite")
                    # Need to generate an incorrect answer, append to list of the wrong answers (should mirror index of
                    # incorrect sprites on screen), then draw sprite.

                    wrong_answers = [self.current_q_and_a.wrong_1, self.current_q_and_a.wrong_2, self.current_q_and_a.wrong_3]
                    wrong_text = wrong_answers[random.randrange(0, 2)]
                    self.create_incorrect_sprite(self.current_q_and_a.id, wrong_text)

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


            # speeds up the clouds. if off screen -> remove the sprite.
            for cloud in self.cloud_sprites_list:
                cloud.center_y += self.movement_speed / 2

                if cloud.center_y > (self.height + 50):
                    cloud.remove_from_sprite_lists()


            # check for collisions.
            incorrect_answers_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.incorrect_sprites_list)
            correct_answers_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.correct_sprites_list)

            if incorrect_answers_hit_list:
                for incorrect in incorrect_answers_hit_list:
                    incorrect.remove_from_sprite_lists()
                    self.player_lives -= 1
                    
            if correct_answers_hit_list:
                for correct in correct_answers_hit_list:
                    print(f"{correct.question_id}, {self.current_q_and_a.id}")
                    if correct.question_id == self.current_q_and_a.id:
                        correct.remove_from_sprite_lists()
                        self.player_score += int(self.current_q_and_a.difficulty)
                        self.update_next_question()
                    else:
                        correct.remove_from_sprite_lists()
                        self.player_lives -= 1
        
        else:
            pass


    def create_incorrect_sprite(self, question_id, incorrect_answer_text):
        incorrect = IncorrectSprite("images/incorrect_01.png", incorrect_scaling, question_id, incorrect_answer_text)
        incorrect.center_x = random.randrange(self.width)
        incorrect.center_y = random.randrange(-100, -50)
        self.incorrect_sprites_list.append(incorrect)
        

    def create_correct_sprite(self, question_id, correct_answer_text):
        correct = CorrectSprite("images/correct_01.png", correct_scaling, question_id, correct_answer_text)
        correct.center_x = random.randrange(self.width)
        correct.center_y = random.randrange(-100, -50)
        self.correct_sprites_list.append(correct)

    
    def create_cloud_sprite(self):
        scaling = random.uniform(min_cloud_scaling, max_cloud_scaling)
        cloud = CloudSprite("images/cloud_01.png", scaling)
        cloud.center_x = random.randrange(self.width)
        cloud.center_y = random.randrange(-100, -50)
        self.cloud_sprites_list.append(cloud)


    def draw_text_on_sprites(self, sprite_list):
        for sprite in sprite_list:
            arcade.draw_text(sprite.text, sprite.left, sprite.center_y, color=arcade.color.BLACK, font_size=answer_font_size, width=int(sprite.right-sprite.left), align="center", anchor_y="center")


    def draw_toolbar(self):
        # white bar + difficulty (question)
        arcade.draw_lrtb_rectangle_filled(self.width*0.15, self.width*0.85, self.height, self.height-100, arcade.color.WHITE)
        arcade.draw_text(f"Difficulty: {self.current_q_and_a.difficulty}", self.width*0.15, self.height-95, arcade.color.BLACK, font_size=12, width=int(self.width*0.85-self.width*0.15), align="center")

        # lives box (right side)
        arcade.draw_lrtb_rectangle_filled(0, self.width*0.15, self.height, self.height-100, (149, 249, 227))
        arcade.draw_text("Lives", 0, self.height-20, arcade.color.BLACK, font_size=14, width=int(self.width*0.15), align="center")
        arcade.draw_text(str(self.player_lives), 0, self.height-50, arcade.color.BLACK, font_size=14, width=int(self.width*0.15), align="center")

        # score box (left side)
        arcade.draw_lrtb_rectangle_filled(self.width*0.85, self.width, self.height, self.height-100, (231, 200, 221))
        arcade.draw_text("Score", self.width*0.85, self.height-20, arcade.color.BLACK, font_size=14, width=int(self.width-self.width*0.85), align="center")
        arcade.draw_text(str(self.player_score), self.width*0.85, self.height-50, arcade.color.BLACK, font_size=14, width=int(self.width-self.width*0.85), align="center")
    
        # draw the question
        arcade.draw_text("Question", self.width*0.15, self.height-22, arcade.color.BLACK, font_size=16, width=int(self.width*0.85-self.width*0.15), align="center")
        if len(self.current_q_and_a.question) > 40:
            current_question_string = ""
            line_height_displacement = 50
            for char in self.current_q_and_a.question:
                if len(current_question_string) >= 40:
                    arcade.draw_text(current_question_string, self.width*0.15, self.height-line_height_displacement, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.width*0.85-self.width*0.15), align="center")
                    line_height_displacement += 25
                    current_question_string = char
                else:
                    current_question_string += char
            else:
                arcade.draw_text(current_question_string, self.width*0.15, self.height-line_height_displacement, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.width*0.85-self.width*0.15), align="center")

        else:
            arcade.draw_text(self.current_q_and_a.question, self.width*0.15, self.height-55, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.width*0.85-self.width*0.15), align="center")

    def update_next_question(self):
        self.current_q_and_a_pointer += 1
        self.current_q_and_a = data[self.current_q_and_a_pointer]


if __name__ == "__main__":
    window = MyGame(width, height, title)
    window.setup()
    arcade.run()