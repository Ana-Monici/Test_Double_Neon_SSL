# import math
# import numpy as np
# from collections import deque

class Robot(object):

    def __init__(self, game, robot_id, team_color):
        self.game = game
        self.robot_id = robot_id
        self.team_color = team_color
        # self.current_data = {}

        self.strategy = None
        self.kicker = False

        """
        Essas atribuições serão feitas no Coach quando ele existir
        """

        # self._frames = {
        #     'x': deque(maxlen=10),
        #     'y': deque(maxlen=10),
        #     'theta': deque(maxlen=10)
        # }

        self.x, self.y, self.theta = 0, 0, 0

    def start(self):
        # self.strategy.start(self)
        pass

    def get_name(self):
        return 'ROBOT_{}_{}'.format(self.robot_id, self.team_color)

    def update(self, anim_frame):
        new_pos = self.strategy.animate(anim_frame)
        self.x = new_pos[0]
        self.y = new_pos[1]
        self.theta = new_pos[2]
        self.kicker = self.robot_id == 0 and anim_frame % 120 < 60
    
    def set_strategy(self, strategy):
        self.strategy = strategy() if isinstance(strategy, type) else strategy
        print("Robô " + str(self.robot_id) + " iniciado com estratégia " + self.strategy.get_name())

    def get_strategy(self):
        return self.strategy

    # def decide(self):
    #     pass

    # def __getitem__(self, item):
    #     if item == 0:
    #         return self.x

    #     if item == 1:
    #         return self.y

    #     if item == 2:
    #         return self.theta

    #     raise IndexError("Robot only has 3 coordinates")
