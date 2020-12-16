from pygame.math import Vector2
from pygame.sprite import Sprite


class BasicObject(Sprite):
    """Базовый объект"""

    def __init__(self, display=None, *groups):
        self._display = display
        super().__init__(*groups)

    def update(self):
        """Обновляет состояние объекта"""
        pass

    def draw(self, surface=None):
        """Отрисовывает объект на surface или display"""
        if surface is not None:
            surface.blit(self.image, self.rect)
        elif self._display is not None:
            self._display.blit(self.image, self.rect)


class DynamicObject(BasicObject):
    """Базовый класс для подвижных объектов"""

    def __init__(self, display, pos, *groups):
        super().__init__(display, *groups)
        self._pos = Vector2(pos)

    def _toroidal_geometry(self):
        """Определяет поведение объекта согласно тороидальной геометрии"""
        if self.rect.left > self._display.get_width():
            self._pos.x = 0
        elif self.rect.right < 0:
            self._pos.x = self._display.get_width()
        elif self.rect.bottom < 0:
            self._pos.y = self._display.get_height()
        elif self.rect.top > self._display.get_height():
            self._pos.y = 0
        self.rect.center = self._pos

    def _move(self):
        """Определяет поведение объекта при его движении"""
        self.rect.center = self._pos

    @property
    def position(self):
        """Копия текущей позиции модуля"""
        return Vector2(self._pos)

    def on_collision(self):
        """Определяет поведение объекта при столкновении с другим"""
        pass

    def on_event(self, event):
        """Определяет реакцию объекта на pygame.event экземпляр"""
        pass

    def update(self):
        """Обновляет состояние объекта"""
        self._move()
        self._toroidal_geometry()


class StaticObject(BasicObject):
    """Базовый класс для неподвижных объектов"""

    def __init__(self, display, *groups):
        super().__init__(display, *groups)

    def update(self):
        """Обновляет состояние объекта"""
        pass
