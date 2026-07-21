from .base_strategy import BaseStrategy
import math

class Defender(BaseStrategy):
    def __init__(self):
        self.name = "Defender"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 1.4 + 0.5 * math.cos(t)
        y = 1.3 + 1 * math.sin(t)
        theta = t

        return [x, y, theta]
