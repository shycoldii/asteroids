import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite


class Spaceship(Sprite):

    def __init__(self, *groups):
        super(Spaceship, self).__init__(*groups)
        self.image = pg.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(400, 400))

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, -0.1)

    def _boost(self):
        self._speed += self._force

    def _rotate(self):
        pass

    def on_key_press(self, key):
        if key == pg.K_UP:
            self._boost()
        if key == pg.K_LEFT:
            pass
        if key == pg.K_RIGHT:
            pass

    def on_key_release(self, key):
        pass

    def update(self):
        self.rect.x += self._speed.x
        self.rect.y += self._speed.y
        self._speed *= 0.4

    def draw(self, surface):
        surface.blit(self.image, self.rect)
