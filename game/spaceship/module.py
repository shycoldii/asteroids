from pygame.math import Vector2

from game.base.base import BasicObject


class AbstractModule(BasicObject):
    """Абстрактный модуль, гаджет, навес для spaceship"""

    def __init__(self, display, space_pos, space_size, space_head):
        super().__init__(display)
        self._space_size = space_size
        self._pos = self._calc_position(space_pos, space_head)
        self._started = False

    def started(self):
        """Статус: включен-выключен"""
        return self._started

    def start(self):
        """Включает модуль"""
        self._started = True

    def stop(self):
        """Выключает модуль"""
        self._started = False

    @property
    def position(self):
        """Копия текущей позиции модуля"""
        return Vector2(self._pos)

    def _calc_position(self, space_pos, space_head):
        """Расчитать позицию относительно spaceship"""
        pass

    def update(self, space_pos, space_head):
        """Обновляет расположение, состояние"""
        pass

    def draw(self):
        """Отображает модуль"""
        pass
