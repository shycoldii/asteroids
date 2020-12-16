import configparser
import random
import time
from math import sin, cos, fabs

import pygame as pg
from PIL import Image, ImageEnhance
from pygame.math import Vector2
from pygame.sprite import Group

from game.base.base import DynamicObject, StaticObject


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
        if not pos:
            x = random.choice([0, random.randint(1, display.get_width() - 2), display.get_width()])
            if x != 0 and x != display.get_width():
                y = random.choice([0, display.get_height()])
            else:
                y = random.randint(0, display.get_height())
            pos = Vector2(x, y)
        else:
            pos = pos
        while fabs(pos.x - display.get_ship_position().x) < 35 or fabs(pos.y - display.get_ship_position().y) < 35:
            pos.x = random.choice([0, random.randint(1, display.get_width() - 2), display.get_width()])
            if pos.x != 0 and pos.x != display.get_width():
                pos.y = random.choice([0, display.get_height()])
            else:
                pos.y = random.randint(0, display.get_height())
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

        self._preloaded_image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
        self._preloaded_image.set_colorkey(color_key)

        self.image = self._preloaded_image.copy()
        self.rect = self.image.get_rect(center=self._pos)

    def _load_image(self):
        self.image = self._preloaded_image.copy()

    def _resize(self):
        x_factor = self._display.get_size()[0] / self._display_size[0]
        y_factor = self._display.get_size()[1] / self._display_size[1]

        self._load_image()
        self._size = (round(self._size[0] * x_factor), round(self._size[1] * y_factor))

        self.image = pg.transform.scale(self.image, self._size)
        self.rect = self.image.get_rect(center=(round(self.rect.centerx * x_factor),
                                                round(self.rect.centery * y_factor)))
        self._pos = Vector2(self.rect.center)

        self._display_size = self._display.get_size()

    def _move(self):
        # прибавляем к скорости ее проекцию на оси в зависимости от угла
        self._pos.x += self._speed.x * cos(self._angle)
        self._pos.y += self._speed.y * sin(self._angle)
        super()._move()

    def update(self):
        if self._display_size != self._display.get_size():
            self._resize()

        super().update()


class Explosion(StaticObject):
    _source_images = ["./data/exp/11.png", "./data/exp/10.png", "./data/exp/9.png",
                      "./data/exp/8.png", "./data/exp/7.png", "./data/exp/6.png",
                      "./data/exp/5.png", "./data/exp/4.png", "./data/exp/3.png",
                      "./data/exp/2.png", "./data/exp/1.png", "./data/exp/0.png"]

    def __init__(self, display):
        super().__init__(display)

        self._images = []
        for i in range(len(self._source_images)):
            image = pg.transform.scale(pg.image.load(self._source_images[i]).convert_alpha(), (100, 100))
            image.set_colorkey((0, 0, 0))
            self._images.append(image)
        self._current = self._images[-1]  # текущая для анимации картинка (начало взрыва)
        self.pos = Vector2(0, 0)  # позиция взрыва
        self._reset_animation()

    def _place(self):
        self.image = self._current
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))  # делаем по картике прямоугольник

    def _reset_animation(self):
        self._animated = False
        self._current_image = len(self._images) - 1  # устанавливаем первую картинку анимации
        self._current_frame = self._current_image * 10  # устанавливаем максимальное количество фреймов

    def _animate(self):
        if self._current_frame >= 0 and self._current_image >= 0:
            if self._current_frame % 10 == 0:  # каждый 10 фреймов
                self._current = self._images[self._current_image]  # изменяем текущую картинку
                self._current_image -= 1  # уменьшаем индекс текущей картинки (продвижение по анимации)
            self._current_frame -= 1
        else:
            self._reset_animation()

    def update(self):
        if self._animated:
            self._animate()

    def draw(self, surface=None):
        if self._animated:
            self._place()
            super().draw(surface)
