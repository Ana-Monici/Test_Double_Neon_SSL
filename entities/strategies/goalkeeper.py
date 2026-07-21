from .base_strategy import BaseStrategy
import math

class Goalkeeper(BaseStrategy):
    def __init__(self):
        self.name = "Goalkeeper"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 1 + 0.2 * math.cos(t)
        y = 4 + 1 * math.sin(t)
        theta = t

        return [x, y, theta]
