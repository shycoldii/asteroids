import pygame as pg
import random
from pygame.math import Vector2
from PIL import Image, ImageEnhance
from game.physical_object import PhysicalObject


class Background:

    def __init__(self, display):
        self._display = display
        self._size = self._display.get_size()
        self.image = pg.transform.scale(pg.image.load("./data/background.jpg").convert(), self._size)
        self.rect = self.image.get_rect(center=(self._size[0] / 2, self._size[1] / 2))
        self._asteroids = [Asteroid(display=self._display) for _ in range(22)]

    def update(self):
        if self._size != self._display.get_size():
            print(self._size)
            print(self._display.get_size())
            self.image = pg.transform.scale(self.image, self._display.get_size())
            self._size = self._display.get_size()
        for asteroid in self._asteroids:
            asteroid.update()

    def draw(self, surface=None):
        if surface is not None:
            surface.blit(self.image, self.rect)
        elif self._display is not None:
            self._display.blit(self.image, self.rect)

        for asteroid in self._asteroids:
            asteroid.draw(surface)


class Asteroid(PhysicalObject):

    def __init__(self, pos=None, display=None, *groups):
        pos = pos or (random.randint(0, display.get_width()), random.randint(0, display.get_height()))
        super().__init__(pos, display, *groups)

        self._display_size = self._display.get_size()

        self._size = (random.randint(4, 21), ) * 2
        self._speed = Vector2(random.random(), 0)

        image = Image.open("./data/ast2.png").resize(self._size)
        image = ImageEnhance.Sharpness(image).enhance(0.4)
        image = ImageEnhance.Brightness(image).enhance(0.7)
        image = ImageEnhance.Contrast(image).enhance(0.85)
        color_key = image.getpixel((0, 0))

        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect(center=self._pos)

    def _move(self):
        self._pos += self._speed
        super()._move()

    def update(self):
        super().update()
        if self._size != self._display.get_size():
            self._size = self._display.get_size()
            self.rect = self.image.get_rect(center=(self._size[0], self._size[1]))
