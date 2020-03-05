import arcade

class Player(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)


class AnswerSprite(arcade.Sprite):
    def __init__(self, img, scale, answer_class):
        super().__init__(img, scale)
        self.answer_class = answer_class
        
        # This exists for now because the text 'may' not fit into the sprite box on screen.
        self.text = answer_class['answer'].replace(' ', '\n')


class IncorrectSprite(AnswerSprite):
    def __init__(self, img, scale, answer_class):
        super().__init__(img, scale, answer_class)


class CorrectSprite(AnswerSprite):
    def __init__(self, img, scale, answer_class):
        super().__init__(img, scale, answer_class)


class CloudSprite(arcade.Sprite):
    def __init__(self, img, scale):
        super().__init__(img, scale)