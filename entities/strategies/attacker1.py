from .base_strategy import BaseStrategy
import math

class MainAttacker(BaseStrategy):
    def __init__(self):
        self.name = "MainAttacker"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 5.4 + 1 * math.cos(t) * 0.1
        y = 3.47 + 2 * math.sin(t) * 0.1
        theta = t

        return [x, y, theta]
