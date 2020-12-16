import configparser
import random

import pygame as pg
from PIL import Image, ImageEnhance
from pygame.math import Vector2

from game.base.base import DynamicObject, StaticObject


class Background(StaticObject):

    def __init__(self, display):
        config = configparser.ConfigParser()
        config.read('config.ini')
        super().__init__(display)

        self._display_size = self._display.get_size()
        self._sprite = "./data/background.jpg"
        self._preloaded_image = pg.image.load(self._sprite).convert()  # предзагруженный исходный спрайт

        self.image = pg.transform.scale(self._preloaded_image, self._display_size)
        self.rect = self.image.get_rect(center=(self._display_size[0] // 2, self._display_size[1] // 2))

        nums = int(config["Objects"]["n_bcg_ast"])
        self._asteroids = [Asteroid(display=self._display) for _ in range(nums)]

    def _load_image(self):
        """Сброс состояния картинки"""
        self.image = self._preloaded_image.copy()

    def _resize(self):
        x_factor = self._display.get_size()[0] / self._display_size[0]  # коэфф. масштабирования по x
        y_factor = self._display.get_size()[1] / self._display_size[1]  # коэфф. масштабирования по y

        self._load_image()
        self.image = pg.transform.scale(self.image, self._display.get_size())
        self.rect = self.image.get_rect(center=(round(self.rect.centerx * x_factor),
                                                round(self.rect.centery * y_factor)))

        self._display_size = self._display.get_size()

    def update(self):
        if self._display_size != self._display.get_size():
            self._resize()

        for asteroid in self._asteroids:
            asteroid.update()

    def draw(self, surface=None):
        super().draw(surface)

        for asteroid in self._asteroids:
            asteroid.draw()


class Asteroid(DynamicObject):

    def __init__(self, display, pos=None, *groups):
        config = configparser.ConfigParser()
        config.read('config.ini')
        pos = pos or (random.randint(0, display.get_full_size()[0]),
                      random.randint(0, display.get_full_size()[1]))
        super().__init__(display, pos, *groups)
        min_ast = int(config["Objects"]["min_bcg_ast"])
        max_ast = int(config["Objects"]["min_bcg_ast"])

        self._display_size = self._display.get_size()

        self._speed = Vector2(random.random(), 0)
        self._size = (random.randint(min_ast, max_ast),) * 2

        self._sprite = random.choice(["./data/ast5.png", "./data/ast3.png",
                                      "./data/ast1.png", "./data/ast4.png",
                                      "./data/ast2.png", "./data/ast6.png"])
        # предобработка изоображения
        image = Image.open(self._sprite)
        image = ImageEnhance.Sharpness(image).enhance(0.4)
        image = ImageEnhance.Brightness(image).enhance(0.7)
        image = ImageEnhance.Contrast(image).enhance(0.85)
        color_key = image.getpixel((0, 0))
        self._preloaded_image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()
        self._preloaded_image.set_alpha(150)
        self._preloaded_image.set_colorkey(color_key)

        self._load_image()
        self.image = pg.transform.scale(self.image, self._size)
        self.rect = self.image.get_rect(center=self._pos)

    def _load_image(self):
        """Сброс состояния картинки"""
        self.image = self._preloaded_image.copy()

    def _resize(self):
        x_factor = self._display.get_size()[0] / self._display_size[0]  # коэфф. масштабирования по x
        y_factor = self._display.get_size()[1] / self._display_size[1]  # коэфф. масштабирования по y

        self._load_image()
        self._size = (round(self._size[0] * x_factor), round(self._size[1] * y_factor))

        self.image = pg.transform.scale(self.image, self._size)
        self.rect = self.image.get_rect(center=(round(self.rect.centerx * x_factor),
                                                round(self.rect.centery * y_factor)))
        self._pos = Vector2(self.rect.center)

        self._display_size = self._display.get_size()

    def _move(self):
        self._pos -= self._speed
        super()._move()

    def _toroidal_geometry(self):
        if self.rect.left > self._display.get_width():
            self._pos.x = 0
        elif self.rect.right < 0:
            self._pos.x = self._display.get_width()
        self.rect.center = self._pos

    def update(self):
        if self._display_size != self._display.get_size():
            self._resize()

        eps = self._size[1] / 2
        if 0 - eps < self._pos.y < self._display.get_height() + eps:
            super().update()
