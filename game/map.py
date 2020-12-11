from pygame.math import Vector2
import time
import random
from .asteroid import Asteroid
import pygame


class Map:

    def __init__(self, width, height, display):
        self.width = width
        self.height = height
        self.disp = display
        self.end = None
        self.asteroids = []
        self.start_time = None
        self.size = Vector2(width, height)
        self.lives = None
        self.hp = None  # тут будет мониторинг жизни игрока
        self.score = None  # не знаю, нужен ли он, но как вообще будет происходить победа?
        self.reset()

    def reset(self):
        """Перезагрузка карты"""
        self.start_time = time.time()
        self.end = False
        self.lives = 3
        self.hp = 1000
        self.score = 0
        self.spawn_asteroid()

    def update(self):
        # проверяем столкновение с астероидом и понижаем хп (или отнимаем жизнь), если необходимо
        # удаляем астероид, в который уже попали или который столкнулся с нами
        # проверяем хп юзера, отнимаем при столкновении с астероидом
        if self.alive():
            for ast in self.asteroids:
                ast.move()
            # обновляем позицию корабля
            # обновляем позицию пульки (ну или ее отсутствие)
        else:
            self.end = True

        pass

    def alive(self):
        if self.lives != 0:
            return True
        else:
            return False

    def display(self):
        for ast in self.asteroids:
            self.disp.draw_img(img=ast.asteroid, size=(ast.size, ast.size), pos=(ast.x, ast.y))
        # рисовка астероидов
        # рисовка пулек (ну или нет, если пулек нет)
        # рисовка корабля
        # рисовка жизнек и хп
        # self.display.draw_text(text=self.hp, pos="позиция под картинкой сердечек")
        pass

    def spawn_asteroid(self):
        for i in range(10):
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            self.asteroids.append(Asteroid(x, y, self.width, self.height))
        #for ast in self.asteroids:
            #self.disp.draw_img(img=ast.asteroid, size=(ast.size, ast.size), pos=(ast.x, ast.y))
