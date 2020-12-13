import configparser

import pygame as pg
from pygame.sprite import Group
import random
from pygame.math import Vector2
from PIL import Image, ImageEnhance
from game.base.base import DynamicObject
from math import sin, cos
import time


class Enemies:

    def __init__(self, display):
        self._display = display
        self._size = self._display.get_size()
        self._asteroids = Group(Asteroid(self._display))
        self.check_time = time.time()  # начало времени отсчета для постепенного спавна астероидов

    def update(self):
        if self._size != self._display.get_size():
            self._size = self._display.get_size()
        if time.time() - self.check_time > 1 and len(self._asteroids) <= 10:  # проверяем прошедшее время
            self._asteroids.add(Asteroid(display=self._display))
            self.check_time = time.time()  # перезаписываем время
        for asteroid in self._asteroids:
            asteroid.update()

    def draw(self, surface=None):
        for asteroid in self._asteroids:
            asteroid.draw(surface)

    @property
    def asteroids(self):
        return self._asteroids


class Asteroid(DynamicObject):
    degrees = [i / 10 for i in range(63)]  # спискок с градусами в радианах для старта в произвольном направлении

    def __init__(self, display, pos=None, *groups):
        config = configparser.ConfigParser()
        config.read('config.ini')
        pos = pos or (random.choice(
            [random.randint(50, display.get_width() // 2 - 100),
             random.randint(display.get_width() // 2 + 100, display.get_width()-50)]), random.choice(
            [random.randint(50, display.get_height() // 2 - 100),
             random.randint(display.get_height() // 2 + 100, display.get_height()-50)]))
        super().__init__(display, pos, *groups)

        self._display_size = self._display.get_size()
        size = int(config["Objects"]["min_ast"]), int(config["Objects"]["max_ast"])
        self._size = (random.randint(size[0], size[1]),) * 2
        speed = float(config["Objects"]["speed_ast"])
        self._speed = Vector2(speed, speed)  # скорость астероидов
        self._angle = random.choice(Asteroid.degrees)  # выбираем рандомный угол

        image = Image.open("./data/ast4.png").resize(self._size)
        image = ImageEnhance.Sharpness(image).enhance(0.4)
        image = ImageEnhance.Brightness(image).enhance(0.7)
        image = ImageEnhance.Contrast(image).enhance(0.85)
        color_key = image.getpixel((0, 0))

        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect(center=self._pos)

    def _move(self):
        # прибавляем к скорости ее проекцию на оси в зависимости от угла
        self._pos.x += self._speed.x * cos(self._angle)
        self._pos.y += self._speed.y * sin(self._angle)
        super()._move()
