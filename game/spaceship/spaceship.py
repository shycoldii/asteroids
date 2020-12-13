import configparser

import pygame as pg
import math
from pygame.math import Vector2

from game.base.base import DynamicObject, StaticObject
from game.spaceship.jet_engine import JetEngine
from game.spaceship.cannon import Cannon


class Spaceship(DynamicObject):

    def __init__(self, display, pos=None, *groups):
        config = configparser.ConfigParser()
        config.read('config.ini')
        pos = pos or Vector2(display.get_width() / 2, display.get_height() / 2)
        super().__init__(display, pos, *groups)

        # =======================================
        try:
            self._master_image = pg.transform.scale(
                pg.image.load("/Users/13polbr/Desktop/asteroids/data/spaceship.png").convert_alpha(), (30, 30))
        except Exception:
            try:
                self._master_image = pg.transform.scale(pg.image.load("./data/spaceship3.png").convert_alpha(),
                                                        (60, 60))
            except Exception:
                self._master_image = pg.transform.scale(pg.image.load("../../data/spaceship3.png").convert_alpha(),
                                                        (60, 60))
        # =======================================

        self.image = self._master_image.copy()
        self.rect = self.image.get_rect(center=self._pos)

        self._head = 0
        self._rotation = 0
        self._rotation_vel = 3

        self._speed = Vector2(0, 0)
        self._force = Vector2(0, 0)
        self._force_vel = 0.2

        self._jet_engine = JetEngine(self._display, self._pos, self._master_image.get_size(), self._head)
        self._cannon = Cannon(self._display, self._pos, self._master_image.get_size(), self._head)
        self._hp = Health(display)
        self._reset_animation()

    def _move(self):
        self._pos += self._speed
        self._speed *= 0.98
        super()._move()

    def _boost(self):
        self._jet_engine.start()
        self._force = Vector2(math.sin(math.radians(self._head)), -math.cos(math.radians(self._head)))
        self._speed += self._force_vel * self._force

    def _rotate(self):
        self._turn()
        self.image = pg.transform.rotate(self._master_image, -self._head)
        self.rect = self.image.get_rect(center=self._pos)

    def _turn(self):
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
        if not self._animated:
            self._hp.damage()
            self._animated = True

    def _on_key_press(self, key):
        if key == pg.K_UP:
            self._jet_engine.start()
        if key == pg.K_LEFT:
            self._rotation = -self._rotation_vel
        if key == pg.K_RIGHT:
            self._rotation = self._rotation_vel
        if key == pg.K_SPACE:
            self._cannon.start()

    def _on_key_release(self, key):
        if key == pg.K_LEFT or key == pg.K_RIGHT:
            self._rotation = 0
        if key == pg.K_UP:
            self._jet_engine.stop()
        if key == pg.K_SPACE:
            self._cannon.stop()

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
        super().update()
        if self._jet_engine.started():
            self._boost()
        if self._animated:
            self._animate()

        self._jet_engine.update(self._pos, self._head)
        self._cannon.update(self._pos, self._head)
        self._hp.update()

        self._rotate()

    def draw(self, surface=None):
        super().draw(surface)
        self._hp.draw()
        self._jet_engine.draw()
        self._cannon.draw()


class Health(StaticObject):
    # _source_images = ["../../data/0.png", "../../data/1.png", "../../data/2.png",
    #                   "../../data/3.png", "../../data/4.png"]
    _source_images = ["./data/0.png", "./data/1.png", "./data/2.png",
                      "./data/3.png", "./data/4.png"]

    def __init__(self, display, val=None):
        super().__init__(display)

        self._images = []
        for i in range(len(self._source_images)):
            image = pg.transform.scale(pg.image.load(self._source_images[i]).convert(), (40, 40))
            image.set_colorkey((0, 0, 0))
            self._images.append(image)

        self._max_hp = self._hp = val or 3
        self._current = [self._images[-1] for _ in range(self._max_hp)]
        self._place()

        self._reset_animation()

    def _place(self):
        self.image = pg.Surface((self._images[1].get_width() * self._max_hp,
                                 self._images[1].get_height()), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self._display.get_width() - (self.image.get_width() + 10),
                                                 10))

        for i in range(len(self._current)):
            image = self._current[i]
            rect = image.get_rect(topleft=(i * image.get_width(), 0))
            self.image.blit(image, rect)

    def _reset_animation(self):
        self._animated = False
        self._current_image = len(self._images) - 1
        self._current_frame = self._current_image * 10

    def _animate(self):
        if self._current_frame >= 0 and self._current_image >= 0:
            if self._current_frame % 10 == 0:
                self._current[self._hp] = self._images[self._current_image]
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
