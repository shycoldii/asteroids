from pygame.sprite import Sprite
from pygame.math import Vector2


class PhysicalObject(Sprite):

    def __init__(self, pos, display=None, *groups):
        super(PhysicalObject, self).__init__(*groups)
        self._display = display
        self._pos = Vector2(pos)

    def _toroidal_geometry(self):
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
        self.rect.center = self._pos

    def get_position(self):
        return self._pos

    def update(self):
        self._move()
        self._toroidal_geometry()

    def draw(self, surface=None):
        if surface is not None:
            surface.blit(self.image, self.rect)
        elif self._display is not None:
            self._display.blit(self.image, self.rect)
