import math

class Ball(object):

    def __init__(self, game):
        self.game = game
        self.x, self.y = 0, 0

    def get_name(self):
        return 'BALL'

    def update(self, anim_frame):
        t = math.radians(anim_frame)

        # Exemplo de movimento circular
        self.x = 7.12 + 0.1 * math.cos(t)
        self.y = 3.12 + 1 * math.sin(t)

    def __getitem__(self, item):
        if item == 0:
            return self.x

        if item == 1:
            return self.y

        raise IndexError("Ball only has 2 coordinates")
