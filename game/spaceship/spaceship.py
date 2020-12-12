import pygame as pg
import math
from pygame.math import Vector2

from game.physical_object import PhysicalObject
from game.spaceship.jet_engine import JetEngine
from game.spaceship.cannon import Cannon


class Spaceship(PhysicalObject):

    def __init__(self, pos=None, display=None, *groups):
        pos = pos or Vector2(display.get_width() / 2, display.get_height() / 2)
        super().__init__(pos, display, *groups)

        # =======================================

        # Полина
        # self._master_image = pg.transform.scale(pg.image.load("/Users/13polbr/Desktop/asteroids/data/spaceship.png").convert_alpha(), (30, 30))

        # test_spaceship
        self._master_image = pg.transform.scale(pg.image.load("../../data/spaceship.png").convert_alpha(), (30, 30))

        # =======================================

        self.image = self._master_image.copy()
        self.rect = self.image.get_rect(center=self._pos)

        self._head = 0
        self._rotation = 0
        self._rotation_vel = 3

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, 0)
        self._force_vel = 0.2

        self._jet_engine = JetEngine(self._pos, self._master_image.get_size(), self._head, self._display)
        self._cannon = Cannon(self._pos, self._master_image.get_size(), self._head, self._display)

        self._health = 2
        self.score = 0  # TODO: убрать

    def _move(self):
        self._pos += self._speed
        # self._speed *= 0.85
        self._speed *= 0.98
        super()._move()

    def _boost(self):
        self._jet_engine.start()
        self._force = Vector2(math.sin(math.radians(self._head)), -math.cos(math.radians(self._head)))
        self._speed += self._force_vel * self._force

    def _rotate(self):
        self._turn()
        self.image = pg.transform.rotate(self._master_image, -self._head)
        self.rect = self.image.get_rect(center=self._pos)

    def _turn(self):
        self._head += self._rotation
        self._head %= 360

    @property
    def cannon(self):
        return self._cannon

    def is_alive(self):
        return self._health != 0

    def collision(self, damage=True):
        if damage:
            if self._health > 1:
                self._health -= 1
            else:
                self._health = 0

    def on_key_press(self, key):
        if key == pg.K_UP:
            self._jet_engine.start()
        if key == pg.K_LEFT:
            self._rotation = -self._rotation_vel
        if key == pg.K_RIGHT:
            self._rotation = self._rotation_vel
        if key == pg.K_SPACE:
            self._cannon.start()

    def on_key_release(self, key):
        if key == pg.K_LEFT or key == pg.K_RIGHT:
            self._rotation = 0
        if key == pg.K_UP:
            self._jet_engine.stop()
        if key == pg.K_SPACE:
            self._cannon.stop()

    def update(self):
        super().update()
        if self._jet_engine.started():
            self._boost()

        self._jet_engine.update(self._pos, self._head)
        self._cannon.update(self._pos, self._head)

        self._rotate()

    def draw(self, surface=None):
        super().draw(surface)
        self._jet_engine.draw()
        self._cannon.draw()
