from .base_strategy import BaseStrategy
import math

class Defender2(BaseStrategy):
    def __init__(self):
        self.name = "Defender2"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 2.1 + 1 * math.cos(t)
        y = 3.8 + 0.5 * math.sin(t)
        theta = t

        return [x, y, theta]
