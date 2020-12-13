import configparser

import pygame as pg
import random
from pygame.math import Vector2
from PIL import Image, ImageEnhance
from game.base.base import DynamicObject, StaticObject


class Background(StaticObject):

    def __init__(self, display):
        config = configparser.ConfigParser()
        config.read('config.ini')
        super().__init__(display)
        self._size = self._display.get_size()

        # =======================================

        try:
            self.image = pg.transform.scale(pg.image.load("/Users/13polbr/Desktop/asteroids/data/background.jpg")
                                            .convert(), self._size)
        except Exception:
            try:
                self.image = pg.transform.scale(pg.image.load("./data/background.jpg").convert(), self._size)
            except Exception:
                self.image = pg.transform.scale(pg.image.load("../../data/background.jpg").convert(), self._size)

        # =======================================
        nums = int(config["Objects"]["n_bcg_ast"])
        self.rect = self.image.get_rect(center=(self._size[0] / 2, self._size[1] / 2))
        self._asteroids = [Asteroid(display=self._display) for _ in range(nums)]

    def update(self):
        if self._size != self._display.get_size():
            self.image = pg.transform.scale(self.image, self._display.get_size())
            self._size = self._display.get_size()

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
        self._size = (random.randint(min_ast, max_ast),) * 2
        self._speed = Vector2(random.random(), 0)

        # =======================================

        # Полина
        # image_name = random.choice(["/Users/13polbr/Desktop/asteroids/data/ast5.png",
        #                             "/Users/13polbr/Desktop/asteroids/data/ast3.png",
        #                             "/Users/13polbr/Desktop/asteroids/data/ast1.png",
        #                             "/Users/13polbr/Desktop/asteroids/data/ast4.png",
        #                             "/Users/13polbr/Desktop/asteroids/data/ast2.png",
        #                             "/Users/13polbr/Desktop/asteroids/data/ast6.png"])

        # main
        image_name = random.choice(["./data/ast5.png", "./data/ast3.png",
                                    "./data/ast1.png", "./data/ast4.png",
                                    "./data/ast2.png", "./data/ast6.png"])

        # test_spaceship
        # image_name = random.choice(["../../data/ast5.png", "../../data/ast3.png",
        #                             "../../data/ast1.png", "../../data/ast4.png",
        #                             "../../data/ast2.png", "../../data/ast6.png"])

        # =======================================

        image = Image.open(image_name).resize(self._size)

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

    def update(self):
        eps = self._size[1] / 2
        if 0 - eps < self._pos.y < self._display.get_height() + eps:
            super().update()
