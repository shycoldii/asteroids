import pygame as pg
import math
from pygame.math import Vector2
from pygame.sprite import Sprite
from jet_engine import JetEngine


class Spaceship(Sprite):

    def __init__(self, display=None, *groups):
        super(Spaceship, self).__init__(*groups)

        self._display = display
        self.master_image = pg.transform.scale(pg.image.load("../../data/spaceship.png").convert_alpha(), (30, 30))
        self.image = self.master_image.copy()
        self.rect = self.image.get_rect(center=(self._display.get_width() / 2, self._display.get_height() / 2))

        self._pos = Vector2(*self.rect.center)
        self._head = 0

        self._rotation = 0
        self._rotation_vel = 3

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, 0)
        self._force_vel = 0.2
        self._jet_engine = JetEngine(self._pos, self.master_image.get_size(), self._head, self._display)

    def _move(self):
        self._pos += self._speed
        self._speed *= 0.98

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

    def _toroidal_geometry(self):
        if self.rect.left > self._display.get_width():
            self._pos.x = 0
        elif self.rect.right < 0:
            self._pos.x = self._display.get_width()
        elif self.rect.bottom < 0:
            self._pos.y = self._display.get_height()
        elif self.rect.top > self._display.get_height():
            self._pos.y = 0

    def _fire(self):
        pass

    def on_key_press(self, key):
        if key == pg.K_UP:
            self._jet_engine.start()
        if key == pg.K_LEFT:
            self._rotation = -self._rotation_vel
        if key == pg.K_RIGHT:
            self._rotation = self._rotation_vel
        if key == pg.K_SPACE:
            self._fire()

    def on_key_release(self, key):
        if key == pg.K_LEFT or key == pg.K_RIGHT:
            self._rotation = 0
        if key == pg.K_UP:
            self._jet_engine.stop()

    def update(self):
        if self._jet_engine.started():
            self._boost()
            self._jet_engine.start()

        self._jet_engine.update(self._pos, self._head)
        self._move()
        self._toroidal_geometry()
        self._rotate()

    def draw(self, surface=None):
        if surface is not None:
            surface.blit(self.image, self.rect)
        if self._display is not None:
            self._display.blit(self.image, self.rect)

        self._jet_engine.draw()
