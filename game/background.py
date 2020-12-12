import pygame as pg
import random
from pygame.math import Vector2
from PIL import Image, ImageEnhance
from game.physical_object import PhysicalObject


class Background:

    def __init__(self, display):
        self._display = display
        self._size = self._display.get_size()

        # =======================================

        # Полина
        # self.image = pg.transform.scale(pg.image.load("/Users/13polbr/Desktop/asteroids/data/background.jpg").convert(), self._size)

        # test_spaceship
        self.image = pg.transform.scale(pg.image.load("./data/background.jpg").convert(), self._size)

        # =======================================

        self.rect = self.image.get_rect(center=(self._size[0] / 2, self._size[1] / 2))
        self._asteroids = [Asteroid(display=self._display) for _ in range(40)]

    def update(self):
        if self._size != self._display.get_size():
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
        pos = pos or (random.randint(0, display._full_size[0]), random.randint(0, display._full_size[1]))
        super().__init__(pos, display, *groups)

        #self._display_size = self._display.get_size()

        self._size = (random.randint(4, 15),) * 2
        self._speed = Vector2(random.random(), 0)

        # =======================================

        # Полина
        # image = Image.open("/Users/13polbr/Desktop/asteroids/data/ast2.png").resize(self._size)

        # test_spaceship
        image_name = random.choice(["./data/ast5.png","./data/ast3.png",
                                    "./data/ast1.png","./data/ast4.png","./data/ast2.png","./data/ast6.png"])
        image = Image.open(image_name).resize(self._size)

        # =======================================

        image = ImageEnhance.Sharpness(image).enhance(0.4)
        image = ImageEnhance.Brightness(image).enhance(0.7)
        image = ImageEnhance.Contrast(image).enhance(0.85)
        color_key = image.getpixel((0, 0))

        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()
        self.image.set_alpha(150)
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect(center=self._pos)

    def _move(self):
        self._pos -= self._speed
        super()._move()

    def _toroidal_geometry(self):
        if self.rect.left > self._display.get_width():
            self._pos.x = 0
        elif self.rect.right < 0:
            self._pos.x = self._display.get_width()
        self.rect.center = self._pos
