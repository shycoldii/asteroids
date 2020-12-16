import configparser
import math

import pygame as pg
from pygame.math import Vector2

from game.base.base import DynamicObject
from game.spaceship.module import AbstractModule


class JetEngine(AbstractModule):

    def __init__(self, display, space_pos, space_size, space_head):
        super(JetEngine, self).__init__(display, space_pos, space_size, space_head)

        config = configparser.ConfigParser()
        config.read('config.ini')

        self._particles = []
        self._frequency = int(config["Objects-jet_engine"]["frequency"])

    def _calc_position(self, space_pos, space_head):
        return space_pos - Vector2(0, self._space_size[1] / 2).rotate((space_head + 180) % 360)

    def _add_particle(self, pos, space_head):
        speed = -1 * Vector2(math.sin(math.radians(space_head)), -math.cos(math.radians(space_head)))
        self._particles.append(Particle(self._display, pos, speed))
        self._pos = Vector2(pos)

    def update(self, space_pos, space_head):
        if self.started():
            pos = self._calc_position(space_pos, space_head)
            if self._pos.distance_to(pos) > self._frequency:
                self._add_particle(pos, space_head)

        for p in self._particles:
            p.update()
            if p.done():
                self._particles.remove(p)

    def draw(self):
        for p in self._particles:
            p.draw()


class Particle(DynamicObject):

    def __init__(self, display, pos, speed, *groups):
        super().__init__(display, pos, *groups)

        config = configparser.ConfigParser()
        config.read('config.ini')

        self._pos = Vector2(pos)
        self._radius = int(config["Objects-jet_engine-particle"]["radius"])

        self.image = pg.Surface((2 * self._radius, 2 * self._radius), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self._pos)

        self._opacity = 255
        self._color = (int(config["Objects-jet_engine-particle"]["color_r"]),
                       int(config["Objects-jet_engine-particle"]["color_g"]),
                       int(config["Objects-jet_engine-particle"]["color_b"]))
        self._done = False

        self._speed = speed
        self._speed_vel = 1

        self._updated = 0

    def _move(self):
        self._pos += self._speed_vel * self._speed
        self._speed *= 0.98
        super()._move()

    def _live(self):
        if self._updated % 4 == 0:

            if self._opacity > 22:
                self._opacity -= 22
            else:
                self._opacity = 0
                self._done = True
            self.image.set_alpha(self._opacity)

        self._updated += 1

    def done(self):
        return self._done

    def update(self):
        super().update()
        self._live()

    def draw(self, surface=None):
        pg.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)
        super().draw(surface)
