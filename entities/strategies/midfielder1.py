from .base_strategy import BaseStrategy
import math

class Midfielder(BaseStrategy):
    def __init__(self):
        self.name = "Midfielder"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 4.9 + 1 * math.cos(t) * 0.2
        y = 3.6 + 2 * math.sin(t) * 0.2
        theta = t

        return [x, y, theta]
