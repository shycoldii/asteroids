from abc import ABC, abstractmethod
from pygame.math import Vector2


class AbstractModule(ABC):

    def __init__(self, space_pos, space_size, space_head, display):
        self._display = display
        self._space_size = space_size
        self._pos = self._calc_position(space_pos, space_head)
        self._started = False

    def started(self):
        return self._started

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    @property
    def position(self):
        return Vector2(self._pos)

    @abstractmethod
    def _calc_position(self, space_pos, space_head):
        pass

    @abstractmethod
    def update(self, space_pos, space_head):
        pass

    @abstractmethod
    def draw(self):
        pass
