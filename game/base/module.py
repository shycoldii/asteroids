from pygame.math import Vector2

from game.base.base import BasicObject


class AbstractModule(BasicObject):

    def __init__(self, display, space_pos, space_size, space_head):
        super().__init__(display)
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

    def _calc_position(self, space_pos, space_head):
        pass

    def update(self, space_pos, space_head):
        pass

    def draw(self, surface):
        pass
