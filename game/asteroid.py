import pygame
import random
from math import sin, cos


class Asteroid:
    degrees = [i / 10 for i in range(63)]  # массив с углами в радианах от 0 до 2П с шагом 0.1

    def __init__(self, x, y, w, h):
        self.display_w = w
        self.display_h = h
        self.size = 55  # размер астероида
        self.x = x
        self.y = y
        self.angle = random.choice(Asteroid.degrees)  # угол, под которым он будет двигаться
        self.speed = 0.5  # скорость астероида (мб сделать выборку из разных маленьких скоростей?)
        # self.asteroid = pygame.image.load("../data/ast1.png").convert_alpha()  # у меня не работало ((
        self.asteroid = pygame.image.load(
            "/Users/13polbr/Desktop/asteroids/data/ast1.png").convert_alpha()  # передаем картинку
        self.asteroid = pygame.transform.scale(self.asteroid, (self.size, self.size))  # задаем размер картинке

    def move(self):
        """
        Функция пересчитывает координаты объекта в зависимости от его скорости и пересечении им границ экрана
        :return:
        """

        # расчитываем новую координату, прибавляя проекции скорости на оси X и Y
        self.y += self.speed * sin(self.angle)
        self.x += self.speed * cos(self.angle)

        # проверка выхода за верхнюю и нижнюю границы
        if self.y > self.display_h:
            self.y = (0 - self.size)
        elif self.y < (0 - self.size):
            self.y = self.display_h

        # проверка выхода за боковые границы
        if self.x > self.display_w:
            self.x = (0 - self.size)
        elif self.x < (0 - self.size):
            self.x = self.display_w
