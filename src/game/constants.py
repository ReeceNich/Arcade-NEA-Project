class Constants:
    def __init__(self):
        self.width = 800
        self.height = 1000
        self.title = "Falling Man"
        self.initial_movement_speed = 2
        self.player_scaling = 0.2
        self.incorrect_scaling = 0.1
        self.correct_scaling = 0.1
        self.max_cloud_scaling = 0.2
        self.min_cloud_scaling = 0.05
        self.answer_font_size = 12

        self.STATE_INSTRUCTIONS = 0
        self.STATE_GAME_RUNNING = 1
        self.STATE_GAME_PAUSED = 2
        self.STATE_GAME_OVER = 3
        self.STATE_LOGIN_SCREEN = 4