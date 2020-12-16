import configparser
import math

import pygame as pg
from pygame.math import Vector2

from game.base.base import DynamicObject, StaticObject
from game.spaceship.cannon import Cannon
from game.spaceship.jet_engine import JetEngine


class Spaceship(DynamicObject):

    def __init__(self, display, pos=None, *groups):
        config = configparser.ConfigParser()
        config.read('config.ini')
        pos = pos or Vector2(display.get_width() / 2, display.get_height() / 2)
        super().__init__(display, pos, *groups)

        self._display_size = self._display.get_size()
        self._size = (round(self._display_size[0] / int(config["Objects-spaceship"]["size_factor"])),
                      round(self._display_size[0] / int(config["Objects-spaceship"]["size_factor"])))

        self._sprite = "./data/spaceship3.png"
        self._preloaded_image = pg.image.load(self._sprite).convert_alpha()

        self._master_image = pg.transform.scale(self._preloaded_image,
                                                self._size)  # поверхность, которая будет вращаться

        self.image = self._master_image.copy()  # sprite на подвижной поверхности
        self.rect = self.image.get_rect(center=self._pos)

        self._head = 0  # направление движения
        self._rotation = 0  # текущее направление поворота
        self._rotation_vel = float(config["Objects-spaceship"]["rotation_vel"])  # скорость поворота

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, 0)
        self._force_vel = float(config["Objects-spaceship"]["force_vel"])

        self._jet_engine = JetEngine(self._display, self._pos, self._master_image.get_size(), self._head)  # двигатель
        self._cannon = Cannon(self._display, self._pos, self._master_image.get_size(), self._head)  # пушка
        self._hp = Health(display)  # hp бар
        self._reset_animation()

    def _load_image(self):
        self._master_image = self._preloaded_image.copy()

    def _resize(self):
        x_factor = self._display.get_size()[0] / self._display_size[0]  # коэфф. масштабирования по x
        y_factor = self._display.get_size()[1] / self._display_size[1]  # коэфф. масштабирования по y

        self._load_image()
        self._size = (round(self._size[0] * x_factor), round(self._size[0] * x_factor))

        self._master_image = pg.transform.scale(self._master_image, self._size)
        self.image = self._master_image.copy()
        self.rect = self.image.get_rect(center=(round(self.rect.centerx * x_factor),
                                                round(self.rect.centery * y_factor)))
        self._pos = Vector2(self.rect.center)

        self._display_size = self._display.get_size()

    def _move(self):
        self._pos += self._speed
        self._speed *= 0.98  # плавное замедление движения
        super()._move()

    def _boost(self):
        """Ускорение"""
        self._jet_engine.start()
        self._force = Vector2(math.sin(math.radians(self._head)), -math.cos(math.radians(self._head)))
        self._speed += self._force_vel * self._force

    def _rotate(self):
        self._turn()
        self.image = pg.transform.rotate(self._master_image, -self._head)
        self.rect = self.image.get_rect(center=self._pos)

    def _turn(self):
        """Вычисление угла поворота"""
        self._head += self._rotation
        self._head %= 360

    def _reset_animation(self):
        self._animated = False
        self._current_frame = 90
        self._master_image.set_alpha(255)

    def _animate(self):
        if self._current_frame >= 0:
            step = self._current_frame % 22
            if step == 10 or step == 0:
                self._master_image.set_alpha(255 if step == 0 else 80)
            self._current_frame -= 1
        else:
            self._reset_animation()

    def _on_damage(self):
        """Определяет поведени при получении урона"""
        if not self._animated:
            self._hp.damage()
            self._animated = True

    def _on_key_press(self, key):
        if key == pg.K_UP:
            self._jet_engine.start()  # усорение
        if key == pg.K_LEFT:
            self._rotation = -self._rotation_vel  # поворот против секундной стрелки
        if key == pg.K_RIGHT:
            self._rotation = self._rotation_vel  # поворот по секундной стрелки
        if key == pg.K_SPACE:
            self._cannon.start()  # активация пушки, выстрелы

    def _on_key_release(self, key):
        if key == pg.K_LEFT or key == pg.K_RIGHT:
            self._rotation = 0  # остановка вращения
        if key == pg.K_UP:
            self._jet_engine.stop()  # выключение ускорения
        if key == pg.K_SPACE:
            self._cannon.stop()  # деактивация пушки

    @property
    def cannon(self):
        return self._cannon

    def is_alive(self):
        return self._hp.hp != 0

    def is_damaged(self):
        return self._animated

    def on_collision(self, damage=True):
        if damage:
            self._on_damage()

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            self._on_key_press(event.key)
        elif event.type == pg.KEYUP:
            self._on_key_release(event.key)

    def update(self):
        if self._jet_engine.started():
            self._boost()  # ускорить
        if self._animated:
            self._animate()  # проиграть анимацию

        if self._display_size != self._display.get_size():
            self._resize()  # масштабировать

        self._jet_engine.update(self._pos, self._head)
        self._cannon.update(self._pos, self._head)
        self._hp.update()

        self._rotate()
        super().update()

    def draw(self, surface=None):
        super().draw(surface)
        self._hp.draw()
        self._jet_engine.draw()
        self._cannon.draw()


class Health(StaticObject):

    def __init__(self, display, val=None):
        super().__init__(display)
        config = configparser.ConfigParser()
        config.read('config.ini')

        self._display_size = self._display.get_size()
        self._size = (int(config["Objects-spaceship-health"]["size"]),) * 2

        self._sprites = ["./data/01.png", "./data/10.png", "./data/12.png",
                         "./data/13.png", "./data/14.png"]  # спрайты кадров анимации
        self._preloaded_images = []  # предзагруженные изоображения кадров анимации
        for i in range(len(self._sprites)):
            image = pg.transform.scale(pg.image.load(self._sprites[i]).convert_alpha(), self._size)
            image.set_colorkey((0, 0, 0))
            self._preloaded_images.append(image)

        self._max_hp = self._hp = val or 3  # стартовое, максимальное значение hp
        self._current = [self._preloaded_images[-1] for _ in range(self._max_hp)]  # текущая позиция hp
        self._place()

        self._reset_animation()

    def _place(self):
        """Перерасчет расположения, размеров, состояния"""
        self.image = pg.Surface((self._preloaded_images[1].get_width() * self._max_hp,
                                 self._preloaded_images[1].get_height()), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self._display.get_width() - (self.image.get_width() + 10), 10))

        for i in range(len(self._current)):
            image = self._current[i]
            rect = image.get_rect(topleft=(i * image.get_width(), 0))
            self.image.blit(image, rect)

    def _reset_animation(self):
        self._animated = False
        self._current_image = len(self._preloaded_images) - 1
        self._current_frame = self._current_image * 10

    def _animate(self):
        if self._current_frame >= 0 and self._current_image >= 0:
            if self._current_frame % 10 == 0:  # каждый 10-ый кадр
                # обновить картинку текущей позиции
                self._current[self._hp] = self._preloaded_images[self._current_image]
                self._current_image -= 1
            self._current_frame -= 1
        else:
            self._reset_animation()

    @property
    def hp(self):
        return self._hp

    def damage(self):
        if self._hp > 0:
            self._hp -= 1
            self._animated = True

    def update(self):
        if self._animated:
            self._animate()

    def draw(self, surface=None):
        self._place()
        super().draw(surface)
