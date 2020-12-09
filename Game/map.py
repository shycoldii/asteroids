from Game.display import Display
from pygame.math import Vector2
import time


class Map:

    def __init__(self, width, height):
        self.display = Display(width, height)
        self.end = None
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

    def update(self):
        # проверяем столкновение с астероидом и понижаем хп (или отнимаем жизнь), если необходимо
        # удаляем астероид, в который уже попали или который столкнулся с нами
        # проверяем хп юзера, отнимаем при столкновении с астероидом
        if self.alive():
            pass
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
        # рисовка астероидов
        # рисовка пулек (ну или нет, если пулек нет)
        # рисовка корабля
        # рисовка жизнек и хп
        self.display.draw_img(img="картинка сердечек", size="размер", pos="коорды какого-нибудь угла")
        self.display.draw_text(text=self.hp, pos="позиция под картинкой сердечек")
        pass
