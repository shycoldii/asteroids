import pygame
import pygame as pg
import math
from pygame.math import Vector2
from pygame.sprite import Group

from game.base.base import DynamicObject
from game.base.module import AbstractModule


class Cannon(AbstractModule):
    pygame.mixer.init()
    missile_sound = pygame.mixer.Sound("data/missile.mp3")
    missile_sound.set_volume(missile_sound.get_volume()-0.7)
    def __init__(self, display, space_pos, space_size, space_head):
        super(Cannon, self).__init__(display, space_pos, space_size, space_head)

        self._missiles = Group()
        self._frequency = 60

    def _calc_position(self, space_pos, space_head):
        return space_pos - Vector2(0, self._space_size[1] / 2).rotate(space_head % 360)

    def _add_missile(self, pos, space_head):
        self.missile_sound.play()
        speed = Vector2(math.sin(math.radians(space_head)), -math.cos(math.radians(space_head)))
        self._missiles.add(Missile(self._display, pos, speed))
        self._pos = Vector2(pos)


    @property
    def missiles(self):
        return self._missiles

    def update(self, space_pos, space_head):
        if self.started():
            pos = self._calc_position(space_pos, space_head)
            if len(self._missiles) == 0:
                self._add_missile(pos, space_head)
            else:
                distance = pos.distance_to(list(self._missiles)[-1].position)
                if distance > self._frequency:
                    if min(self._display.get_size()) - distance > self._frequency:
                        self._add_missile(pos, space_head)

        for p in self._missiles:
            p.update()
            if p.done():
                self._missiles.remove(p)

    def draw(self):
        for p in self._missiles:
            p.draw()


class Missile(DynamicObject):

    def __init__(self, display, pos, speed, *groups):
        super().__init__(display, pos, *groups)

        self._start_pos = Vector2(pos)
        self._pos = Vector2(pos)
        self._radius = 3

        self.image = pg.Surface((2 * self._radius, 2 * self._radius), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self._pos)

        self._opacity = 255
        self._color = (255, 0, 0)
        self._done = False

        self._speed = speed
        self._speed_vel = 7

        self._lifetime = int(0.63 * min((self._display.get_size())) / self._speed_vel)

    def _move(self):
        self._pos += self._speed_vel * self._speed
        super()._move()

    def _live(self):
        if self._lifetime > 0:
            if self._lifetime < 25:
                if self._opacity > 11:
                    self._opacity -= 11
                else:
                    self._opacity = 0
                self.image.set_alpha(self._opacity)

            self._lifetime -= 1
        else:
            self._done = True

    def done(self):
        return self._done

    def update(self):
        super().update()
        self._live()

    def draw(self, surface=None):
        pg.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)
        super().draw(surface)
