from .base_strategy import BaseStrategy
import math

class SideAttacker(BaseStrategy):
    def __init__(self):
        self.name = "SideAttacker"
    
    def get_name(self):
        return self.name
    
    def animate(self, anim_frame):
        t = math.radians(anim_frame)

        # Movimento circular
        x = 7.5 + 1 * math.cos(t) * 0.1
        y = 4.3 + 2 * math.sin(t) * 0.1
        theta = t

        return [x, y, theta]
