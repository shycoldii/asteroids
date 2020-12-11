import pygame
import random
import sys
import time

W = 800  # ось x
H = 600  # ось y
SIZE = 55  # размер картинки
MAX = 15  # максимальное количество астероидов на экране


class Asteroid:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.asteroid = pygame.image.load('../data/ast1.png').convert_alpha()  # передаем картинку
        self.asteroid = pygame.transform.scale(self.asteroid, (SIZE, SIZE))  # задаем размер картинке

    # движение астероидов
    def move(self):
        self.speed = random.randrange(1, 2)  # задаем скорость
        self.y += self.speed

        if self.y > H:
            self.y = (0 - SIZE)  # выход за рамки

        place = random.randrange(1, 3)
        if place == 1:  # движение вправо
            self.x += 1
            if self.x > W:
                self.x = (0 - SIZE)

        elif place == 2:  # движение влево
            self.x -= 1
            if self.x < (0 - SIZE):
                self.x = W

    # рисуем астероиды на экране
    def showing(self):
        screen.blit(self.asteroid, (self.x, self.y))


all_asteroid = []

# создание астеройдов в рандомных местах(случайное положение x, y)


def init_aster(MAX, all_asteroid):

    for _ in range(1, MAX):
        x = random.randrange(0, W)
        y = random.randrange(0, H)
        all_asteroid.append(Asteroid(x, y))


pygame.init()
screen = pygame.display.set_mode((W, H))
init_aster(MAX, all_asteroid)

game = True
# при нажатии любой кнопки игра прекращается
while game:
    screen.fill((0, 51, 102))  # закрашиваем, чтобы не оставалось следов передвижения
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            sys.exit()
    for i in all_asteroid:
        i.move()
        i.showing()

    time.sleep(0.001)
    pygame.display.flip()
