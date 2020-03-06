import arcade
import random
import psycopg2
import datetime
import os
from .sprites import Player, AnswerSprite, CorrectSprite, IncorrectSprite, CloudSprite
from .constants import Constants
from database.database_classes import QuestionAnswered, Topic


class MyGame(arcade.Window):
    def __init__(self, constants, width, height, title, database_manager, login):
        super().__init__(width, height, title)
        self.constants = constants

        self.db = database_manager
        self.username = login.username
        self.school_id = login.school_id
        self.topic_id = login.topic_id
        self.subject_id = login.subject_id

        # Fetch the users profile
        self.user = self.db.fetch_user(self.username, self.school_id)

        self.user_id = self.user['id']
        self.user_passcode = self.user['passcode']


        arcade.set_background_color(arcade.color.BABY_BLUE)

        self.current_state = self.constants.STATE_INSTRUCTIONS

        # required! this enables the images to load.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


    def setup(self):
        self.data = self.db.fetch_questions_by_topic(Topic(id=self.topic_id, name=None, subject_id=self.subject_id))
        print(f" print data {self.data}")

        # create sprites etc for a my game
        self.player_sprite = Player("images/player_02.png", self.constants.player_scaling)
        self.player_sprite.center_x = self.constants.width / 2
        # self.player_sprite.center_y = self.constants.height - 2
        self.player_sprite.top = self.constants.height - 110

        self.incorrect_sprites_list = arcade.SpriteList()
        self.correct_sprites_list = arcade.SpriteList()

        self.delta_time_elapsed = 0
        self.movement_speed = self.constants.initial_movement_speed

        self.cloud_sprites_list = arcade.SpriteList()

        self.player_lives = 3
        self.current_q_and_a_pointer = -1
        self.current_q_and_a = None
        self.update_next_question()
        
        self.player_score = 0

        self.QuestionsAnswered = []


    def on_draw(self):
        arcade.start_render()
        
        if self.current_state == self.constants.STATE_INSTRUCTIONS:
            self.set_mouse_visible(True)
            self.draw_instructions()

        elif self.current_state == self.constants.STATE_GAME_RUNNING:
            self.set_mouse_visible(True)
            self.draw_game_running()
        
        elif self.current_state == self.constants.STATE_GAME_PAUSED:
            self.set_mouse_visible(True)
            self.draw_paused()
            
        elif self.current_state == self.constants.STATE_GAME_OVER:
            self.set_mouse_visible(True)
            self.draw_game_over()
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
        arcade.draw_rectangle_filled(self.constants.width//2, self.constants.height//2, self.constants.width-100, self.constants.height-100, arcade.color.WHITE)
        arcade.draw_rectangle_outline(self.constants.width//2, self.constants.height//2, self.constants.width-100, self.constants.height-100, arcade.color.BLACK, 5)
        arcade.draw_text("Welcome to Falling Man!", 0, self.constants.height-150, arcade.color.BLACK, 48, self.constants.width, 'center')
        arcade.draw_text("Your character will be falling through the sky.", 0, self.constants.height-250, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text("Direct them using the mouse and collect all the correct answers!", 0, self.constants.height-300, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text("Try and avoid the wrong answers... they hurt you!", 0, self.constants.height-350, arcade.color.BLACK, 18, self.constants.width, 'center')
        
        arcade.draw_text(f"Username: {self.user['username']}", 0, self.constants.height//2, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text(f"Passcode: {self.user['passcode']}", 0, self.constants.height//2 - 50, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text(f"Player ID: {self.user['id']}", 0, self.constants.height//2 - 100, arcade.color.BLACK, 18, self.constants.width, 'center')
        

        arcade.draw_text("Click anywhere to start...", 0, 150, arcade.color.BLACK, 18, self.constants.width, 'center')


    def draw_paused(self):
        arcade.draw_text("Paused", 0, self.constants.height//2, arcade.color.DARK_RED, 96, self.constants.width, 'center')
        arcade.draw_text("(to resume, press Escape)", 0, self.constants.height//2 - 35, arcade.color.DARK_SLATE_GRAY, 14, self.constants.width, 'center')
        arcade.draw_text(f"Lives remaining: {self.player_lives}", 0, self.constants.height//2 - 125, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text(f"Current score: {self.player_score}", 0, self.constants.height//2 - 165, arcade.color.BLACK, 18, self.constants.width, 'center')
    
    def draw_game_over(self):
        arcade.draw_text("Game Over", 0, self.constants.height//2, arcade.color.DARK_RED, 96, self.constants.width, 'center')
        arcade.draw_text(f"Final score: {self.player_score}", 0, self.constants.height//2 - 125, arcade.color.BLACK, 18, self.constants.width, 'center')
        arcade.draw_text("Click anywhere to go back to the start...", 0, 150, arcade.color.BLACK, 18, self.constants.width, 'center')


    def on_mouse_motion(self, x, y, dy, dx):
        # only move the character if the game is 'running'.
        if self.current_state == self.constants.STATE_GAME_RUNNING:
            self.player_sprite.center_x = x

        else:
            pass


    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == self.constants.STATE_INSTRUCTIONS:
            self.current_state = self.constants.STATE_GAME_RUNNING
            # the setup is needed incase the user wants to replay the game again after dying.
            self.setup()

        elif self.current_state == self.constants.STATE_GAME_OVER:
            self.current_state = self.constants.STATE_INSTRUCTIONS

        else:
            pass


    def on_key_press(self, key, modifiers):
        if self.current_state == self.constants.STATE_GAME_RUNNING:
            # pauses the game
            if key == arcade.key.ESCAPE:
                print("game paused")
                self.current_state = self.constants.STATE_GAME_PAUSED
            
            # speed up everything is space is pressed (boost capability)
            if key == arcade.key.SPACE:
                self.movement_speed += 5


        elif self.current_state == self.constants.STATE_GAME_PAUSED:
            # unpauses the game
            if key == arcade.key.ESCAPE:
                print("game running")

                self.current_state = self.constants.STATE_GAME_RUNNING

        elif self.current_state == self.constants.STATE_GAME_OVER:
            pass

        else:
            pass


    def on_key_release(self, key, modifiers):
        if self.current_state == self.constants.STATE_GAME_RUNNING:
            # not really necessary...
            if key == arcade.key.ESCAPE:
                pass

            if key == arcade.key.SPACE:
                self.movement_speed -= 5
        
        if self.current_state == self.constants.STATE_GAME_PAUSED:
            pass

        if self.current_state == self.constants.STATE_GAME_OVER:
            pass


    def update(self, delta_time):
        if self.current_state == self.constants.STATE_GAME_RUNNING:
            self.delta_time_elapsed += delta_time
            self.player_sprite.update()

            self.correct_sprites_list.update()
            self.incorrect_sprites_list.update()

            self.cloud_sprites_list.update()

            #
            # ANSWER SPRITE GENERATION
            #

            # The sprite list(s) may be empty -> error may occur.
            try:
                lowest_correct_sprite = self.correct_sprites_list[-1].center_y
            except:
                # no sprite exists, therefore set a default value that is massive
                lowest_correct_sprite = 9999
            try:
                lowest_incorrect_sprite = self.incorrect_sprites_list[-1].center_y
            except:
                # no sprite exists, therefore set a default value that is massive
                lowest_incorrect_sprite = 9999

            # Creates more sprites if not enough have been spawned or spawned in certain amount of time.
            try:
                # this determines how far up the screen the latest made/lowest down sprite is.
                two_sprite_lists_min_value = min(lowest_correct_sprite, lowest_incorrect_sprite)
                
                if two_sprite_lists_min_value > 150:
                    print("Last sprite on screen is above 150px")
                    self.generate_random_answer_sprite()
                else:
                    if self.delta_time_elapsed > 2:
                        print("its been 2 seconds")
                        self.generate_random_answer_sprite()
            except:
                pass

            


            # TODO: Combine the two FOR loops to remove repetition
            # speeds up each sprite. if off screen -> remove the sprite.
            for sprite in self.incorrect_sprites_list:
                sprite.center_y += self.movement_speed

                if sprite.center_y > (self.constants.height + 50):
                    sprite.remove_from_sprite_lists()
            
            for sprite in self.correct_sprites_list:
                sprite.center_y += self.movement_speed

                if sprite.center_y > (self.constants.height + 50):
                    sprite.remove_from_sprite_lists()


            # speeds up the clouds. if off screen -> remove the sprite.
            for cloud in self.cloud_sprites_list:
                cloud.center_y += self.movement_speed / 2

                if cloud.center_y > (self.constants.height + 50):
                    cloud.remove_from_sprite_lists()


            # check for collisions.
            incorrect_answers_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.incorrect_sprites_list)
            correct_answers_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.correct_sprites_list)

            if incorrect_answers_hit_list:
                for incorrect in incorrect_answers_hit_list:
                    # if true, then player has actually hit the current questions wrong answer 
                    if incorrect.answer_class['question_id'] == self.current_question['id']:
                        # updates QuestionAnswered
                        q_a = QuestionAnswered(self.user_id, incorrect.answer_class['question_id'], incorrect.answer_class['answer_id'], datetime.datetime.now())
                        print(f"JUST ANSWERED AT: {q_a.time}")
                        self.QuestionsAnswered.append(q_a)

                        incorrect.remove_from_sprite_lists()
                        self.update_next_question()
                        self.player_lives -= 1
                    else:
                        # player has answered the previous questions incorrect answer.
                        # assuming this was a mistake on the players behalf, ignoring the error and not storing the result :)
                        print("player has answered the previous questions incorrect answer.")
                        self.update_next_question()
                        incorrect.remove_from_sprite_lists()
                        self.player_lives -= 1

                    
            if correct_answers_hit_list:
                for correct in correct_answers_hit_list:
                    # this is needed because previous correct answers may still be flying up the screen when the next question is displayed.
                    if correct.answer_class['question_id'] == self.current_question['id']:
                        # speeds up the objects (makes the game harder)
                        self.movement_speed += 0.5

                        # updates QuestionAnswered
                        q_a = QuestionAnswered(self.user_id, correct.answer_class['question_id'], correct.answer_class['answer_id'], datetime.datetime.now())
                        print(f"JUST ANSWERED AT: {q_a.time}")
                        self.QuestionsAnswered.append(q_a)

                        # TODO: This player_score should be removed or changed. Dodgey logic, perhaps replace with a questions_answered_correctly score?
                        self.player_score += int(self.current_question['difficulty_id'])
                        
                        correct.remove_from_sprite_lists()
                        self.update_next_question()
                    
                    else:
                        # player has answered the previous questions correct answer.
                        # assuming this was a mistake on the players behalf, ignoring the error and not storing the result :)
                        print("player has answered the previous questions correct answer.")
                        self.update_next_question()
                        correct.remove_from_sprite_lists()
                        self.player_lives -= 1
        
            if self.player_lives == 0:
                self.current_state = self.constants.STATE_GAME_OVER
        

        elif self.current_state == self.constants.STATE_GAME_OVER:
            # update the database
            self.write_questions_answered_to_database()
        
        elif self.current_state == self.constants.STATE_GAME_PAUSED:
            # update the database
            self.write_questions_answered_to_database()

        else:
            pass


    def create_incorrect_sprite(self, answer_class):
        incorrect = IncorrectSprite("images/incorrect_01.png", self.constants.incorrect_scaling, answer_class)
        incorrect.center_x = random.randrange(self.constants.width)
        incorrect.center_y = random.randrange(-100, -50)
        self.incorrect_sprites_list.append(incorrect)
        

    def create_correct_sprite(self, answer_class):
        correct = CorrectSprite("images/incorrect_01.png", self.constants.correct_scaling, answer_class)
        correct.center_x = random.randrange(self.constants.width)
        correct.center_y = random.randrange(-100, -50)
        self.correct_sprites_list.append(correct)

    
    def create_cloud_sprite(self):
        scaling = random.uniform(self.constants.min_cloud_scaling, self.constants.max_cloud_scaling)
        cloud = CloudSprite("images/cloud_01.png", scaling)
        cloud.center_x = random.randrange(self.constants.width)
        cloud.center_y = random.randrange(-100, -50)
        self.cloud_sprites_list.append(cloud)


    def generate_random_answer_sprite(self):
        self.delta_time_elapsed = 0
        random_answer_index = random.randrange(0, len(self.current_answers))

        if self.current_answers[random_answer_index]['correct'] == True:
            self.create_correct_sprite(self.current_answers[random_answer_index])
            print("Created correct sprite")
            
        else:
            self.create_incorrect_sprite(self.current_answers[random_answer_index])
            print("Created incorrect sprite")

        self.create_cloud_sprite()


    def draw_text_on_sprites(self, sprite_list):
        for sprite in sprite_list:
            arcade.draw_text(sprite.text, sprite.left, sprite.center_y, color=arcade.color.WHITE, font_size=self.constants.answer_font_size, width=int(sprite.right-sprite.left), align="center", anchor_y="center")


    def draw_toolbar(self):
        # white bar + difficulty (question)
        arcade.draw_lrtb_rectangle_filled(self.constants.width*0.15, self.constants.width*0.85, self.constants.height, self.constants.height-100, arcade.color.WHITE)
        arcade.draw_text(f"Difficulty: {self.current_question['difficulty_id']}", self.constants.width*0.15, self.constants.height-95, arcade.color.BLACK, font_size=12, width=int(self.constants.width*0.85-self.constants.width*0.15), align="center")

        # lives box (right side)
        arcade.draw_lrtb_rectangle_filled(0, self.constants.width*0.15, self.constants.height, self.constants.height-100, (149, 249, 227))
        arcade.draw_text("Lives", 0, self.constants.height-20, arcade.color.BLACK, font_size=14, width=int(self.constants.width*0.15), align="center")
        arcade.draw_text(str(self.player_lives), 0, self.constants.height-50, arcade.color.BLACK, font_size=18, width=int(self.constants.width*0.15), align="center")

        # score box (left side)
        arcade.draw_lrtb_rectangle_filled(self.constants.width*0.85, self.constants.width, self.constants.height, self.constants.height-100, (231, 200, 221))
        arcade.draw_text("Score", self.constants.width*0.85, self.constants.height-20, arcade.color.BLACK, font_size=14, width=int(self.constants.width-self.constants.width*0.85), align="center")
        arcade.draw_text(str(self.player_score), self.constants.width*0.85, self.constants.height-50, arcade.color.BLACK, font_size=18, width=int(self.constants.width-self.constants.width*0.85), align="center")
    
        # draw the question text
        arcade.draw_text("Question", self.constants.width*0.15, self.constants.height-22, arcade.color.BLACK, font_size=16, width=int(self.constants.width*0.85-self.constants.width*0.15), align="center")
        if len(self.current_question['question']) > 40:
            current_question_string = ""
            line_height_displacement = 50
            for char in self.current_question['question']:
                if len(current_question_string) >= 40:
                    arcade.draw_text(current_question_string, self.constants.width*0.15, self.constants.height-line_height_displacement, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.constants.width*0.85-self.constants.width*0.15), align="center")
                    line_height_displacement += 25
                    current_question_string = char
                else:
                    current_question_string += char
            else:
                arcade.draw_text(current_question_string, self.constants.width*0.15, self.constants.height-line_height_displacement, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.constants.width*0.85-self.constants.width*0.15), align="center")

        else:
            arcade.draw_text(self.current_question['question'], self.constants.width*0.15, self.constants.height-55, arcade.color.DARK_MOSS_GREEN, font_size=20, width=int(self.constants.width*0.85-self.constants.width*0.15), align="center")

    
    # TODO: Fix the current_question logic. It fetches the questions, then fetches them again.
    def update_next_question(self):
        self.current_q_and_a_pointer += 1

        # if it can't fetch the next question (e.g. end of list), default to game over.
        try:
            self.current_question = self.data[self.current_q_and_a_pointer]

            self.current_q_and_a = self.db.fetch_question_and_answers(self.current_question['id'])
            self.current_question = self.current_q_and_a[0]
            self.current_answers = self.current_q_and_a[1]
        
        except:
            print("out of questions, game over")
            self.current_state = self.constants.STATE_GAME_OVER


    def write_questions_answered_to_database(self):
        for entity in self.QuestionsAnswered:
            self.db.insert_question_answered(entity)
            print(f"Inserting entity -> Question ID: {entity.question_id}, Answer ID: {entity.answer_id}, Time: {entity.time}...")
        self.QuestionsAnswered = []


if __name__ == "__main__":
    print("Do not run through this file. Use the run_* file in the root directory.")
    # login = Login()
    # login.draw_window()

    # db = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))
    db = DatabaseManager(psycopg2.connect("dbname='game' user='pi' password='raspberry' host='86.63.31.202' port='5432'"))



    window = MyGame(width, height, title, database_manager=db, user_id=3, user_passcode='5678')
    window.setup()


    # print(login.email)
    # print(login.passcode)

    arcade.run()