from abc import ABC, abstractmethod

class BaseStrategy (ABC):
    @abstractmethod
    def get_name(self):
        pass

    def animate(self, anim_frame):
        pass
