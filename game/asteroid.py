import pygame as pg
import random
from pygame.math import Vector2
from PIL import Image, ImageEnhance
from Game.physical_object import PhysicalObject
from math import sin, cos


class Enemies:

    def __init__(self, display):
        self._display = display
        self._size = self._display.get_size()
        self._asteroids = [Asteroid(display=self._display) for _ in range(10)]

    def update(self):
        if self._size != self._display.get_size():
            self._size = self._display.get_size()
        for asteroid in self._asteroids:
            asteroid.update()

    def draw(self, surface=None):
        for asteroid in self._asteroids:
            asteroid.draw(surface)


class Asteroid(PhysicalObject):
    degrees = [i/10 for i in range(63)]

    def __init__(self, pos=None, display=None, *groups):
        pos = pos or (random.randint(0, display.get_width()), random.randint(0, display.get_height()))
        super().__init__(pos, display, *groups)

        self._display_size = self._display.get_size()

        self._size = (random.randint(35, 55), ) * 2
        self._speed = Vector2(0.5, 0.5)
        self._angle = random.choice(Asteroid.degrees)

        image = Image.open("./data/ast1.png").resize(self._size)
        image = ImageEnhance.Sharpness(image).enhance(0.4)
        image = ImageEnhance.Brightness(image).enhance(0.7)
        image = ImageEnhance.Contrast(image).enhance(0.85)
        color_key = image.getpixel((0, 0))

        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect(center=self._pos)

    def _move(self):
        self._pos.x += self._speed.x * cos(self._angle)
        self._pos.y += self._speed.y * sin(self._angle)
        super()._move()

    def update(self):
        super().update()
        if self._size != self._display.get_size():
            self._size = self._display.get_size()
            self.rect = self.image.get_rect(center=(self._size[0], self._size[1]))
