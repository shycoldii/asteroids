import pygame as pg
from pygame.sprite import Sprite


class Particle(Sprite):

    def __init__(self, pos, speed, display=None, *groups):
        super().__init__(*groups)
        self._display = display

        self._pos = pos
        self._radius = 2
        self.image = pg.Surface((2 * self._radius, 2 * self._radius), pg.SRCALPHA)

        self._opacity = 255
        self._color = (255, 0, 0)
        self._done = False

        self._speed = speed

        self._updated = 0

    def _move(self):
        self._pos += self._speed
        self._speed *= 0.98

    def _live(self):
        if self._updated % 4 == 0:

            if self._radius > 0:
                self._radius -= 0.05

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
        self._move()
        self._live()

    def draw(self, surface=None):
        pg.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)

        if surface is not None:
            surface.blit(self.image, self._pos)
        if self._display is not None:
            self._display.blit(self.image, self._pos)
