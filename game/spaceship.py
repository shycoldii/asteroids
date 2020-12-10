import pygame as pg
import math
from pygame.math import Vector2
from pygame.sprite import Sprite


class Spaceship(Sprite):

    def __init__(self, display, *groups):
        super(Spaceship, self).__init__(*groups)
        self.display = display
        self.master_image = pg.transform.scale(pg.image.load("../data/spaceship.png").convert_alpha(), (30, 30))
        self.image = self.master_image.copy()
        self.rect = self.image.get_rect(center=(400, 400))

        self._pos = Vector2(400, 400)
        self._head = 0

        self._rotation = 0
        self._rotation_vel = 3

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, 0)
        self._force_vel = 0.2
        self._boosting = False

    def _boost(self):
        self._force = Vector2(math.sin(math.radians(self._head)), -math.cos(math.radians(self._head)))
        self._speed += self._force_vel * self._force

    def _rotate(self):
        self._turn()
        self.image = pg.transform.rotate(self.master_image, -self._head)
        self.rect = self.image.get_rect(center=self._pos)

    def _turn(self):
        self._head += self._rotation
        self._head %= 360

    def on_key_press(self, key):
        if key == pg.K_UP:
            self._boosting = True
        if key == pg.K_LEFT:
            self._rotation = -self._rotation_vel
        if key == pg.K_RIGHT:
            self._rotation = self._rotation_vel

    def on_key_release(self, key):
        if key == pg.K_LEFT or key == pg.K_RIGHT:
            self._rotation = 0
        if key == pg.K_UP:
            self._boosting = False

    def update(self):
        if self._boosting:
            self._boost()

        self._pos += self._speed
        self._speed *= 0.98
        self._rotate()

    def draw(self, surface=None):
        if surface is None:
            self.display.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
