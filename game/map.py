from PIL import Image
from pygame.math import Vector2
import time
from .asteroid import Asteroid, Enemies
import pygame
from .background import Background
from .spaceship.spaceship import Spaceship


class Map:
    alpha,reverse = 255,False
    def __init__(self, display):
        pygame.mixer.init()
        self.space_sound = pygame.mixer.Sound("data/space.mp3")
        self.menu_sound =  pygame.mixer.Sound("data/menu.mp3")
        self.menu_sound.play(-1)
        self.display = display
        self.spaceship = Spaceship(display=self.display)
        self.enemies = Enemies(display=self.display)
        self.background = Background(display=self.display)

        self.end = None
        self.first_spawn = True
        self.start_time = None

        self.lives = None
        self.hp = None  # тут будет мониторинг жизни игрока
        self.score = None  # не знаю, нужен ли он, но как вообще будет происходить победа?
        self.collision = True
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None

        self.init_lives()
        self.reset()

    def reset(self):
        """Перезагрузка карты"""
        self.start_time = time.time()
        self.end = False
        self.lives = 3
        self.hp = 1000
        self.score = 0
        self.init_lives()

    def update_menu(self):
        """
        Обновление состояния MENU
        :return: None
        """
        self.change_alpha()
        self.background.update()

    def update_game(self):
        """
        Обновление состояния GAME
        :return: None
        """
        # проверяем столкновение с астероидом и понижаем хп (или отнимаем жизнь), если необходимо
        # удаляем астероид, в который уже попали или который столкнулся с нами
        # проверяем хп юзера, отнимаем при столкновении с астероидом
        if self.first_spawn:
            self.first_spawn = False
        self.background.update()
        self.spaceship.update()
        self.enemies.update()
        if self.lives != 0:
              pass
                # обновляем позицию корабля
                # обновляем позицию пульки (ну или ее отсутствие)
        else:
                self.end = True

    @staticmethod
    def is_mouse_on(x_centered, y_centered, x_size, y_size, mx, my):
        """
        :param x_centered: координата х централизации (с учетом прямоугольника)
        :param y_centered: координата у централизации (с учетом прямоугольника)
        :param x_size: размер объекта (прямоугольника)
        :param y_size: размер объекта (прямоугольника)
        :param mx: координата мышки х
        :param my: координата мышки у
        :return: True, если мышь находится внутри области
        """
        if x_centered <= mx <= x_centered + x_size and y_centered <= my <= y_centered + y_size:
            return True
        return False
    def change_alpha(self):
        """
                Вспомогательная функция для изменения видимости рамки в начале игры
                :return: None
                """
        if self.reverse:
            self.alpha += 0.5
        else:
            self.alpha -= 0.5
        if self.alpha == 0:
            self.reverse = True
        if self.alpha == 255:
            self.reverse = False

    def draw_menu(self,x_size,y_size,x_centered,y_centered):
        """
        Отображение на экране состояния МЕНЮ
        :param x_size: вспомогательный параметр лого
        :param y_size: вспомогательный параметр лого
        :param x_centered: вспомогательный параметр лого
        :param y_centered: вспомогательный параметр лого
        :return: None
        """
        self.background.draw()
        self.display.draw_rect(size=Vector2(x_size, y_size), color=(100, 97, 0, self.alpha)
                               , pos=Vector2(x_centered, y_centered), fill=False)
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2, self.display.get_height() / 2),
                               size=50, color=(100, 74, 0))
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2 - 2,
                                                    self.display.get_height() / 2 - 5), size=50)
        self.display.draw_text("click to start", pos=Vector2(self.display.get_width() / 2,
                                                             self.display.get_height() / 2 + 0.1 * self.display.get_height()),
                               size=15)

    def draw_game(self):
        """
        Отображение состояния GAME
        :return: None
        """
        self.background.draw()
        self.spaceship.draw()
        self.enemies.draw()
        self.display_lives()
        self.display_points()
        # рисовка астероидов
        # рисовка пулек (ну или нет, если пулек нет)
        # рисовка корабля
        # рисовка жизнек и хп
        # self.display.draw_text(text=self.hp, pos="позиция под картинкой сердечек")

#==========эти ф-и видимо потеряют свой смысл или изменятся
    def display_lives(self):
        length = 115
        height = 40
        _size = (30,) * 2
        # вместо self.alfa надо подобрвть нормальный фон для сердечек )))
        # self.display.draw_rect(size=Vector2(length, height), color=(255, 255, 255,100)
        # , pos=Vector2(self.display.get_width() - length, 0), fill=True)
        for i in range(3):
            if i < self.spaceship._health:
                self.display.draw_img(img=self.image4, size=(40, 40),
                                      pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
            else:
                if self.collision:
                    self.display.draw_img(img=self.image3, size=(40, 40),
                                          pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
                    # реализовать анимацию уменьшения жизни
                    """for l in range(4):
                        if l != 3:
                            if l == 0:
                                self.display.draw_img(img=self.image3, size=(30, 30),
                                                      pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
                            elif l == 1:
                                self.display.draw_img(img=self.image2, size=(30, 30),
                                                      pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
                            else:
                                self.display.draw_img(img=self.image1, size=(30, 30),
                                                      pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
                            # time.sleep(0.5)
                        else:
                            self.display.draw_img(img=self.image5, size=(30, 30),
                                                  pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
                    self.collision = False"""
                else:
                    self.display.draw_img(img=self.image5, size=(30, 30),
                                          pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))

    def display_points(self):
        length = 120 + len(str(self.spaceship.score)) * 10
        if length < 130:
            length = 130
        self.display.draw_text(text="POINTS:  " + str(self.spaceship.score), pos=(length // 2, 20), size=11,
                               color=(255, 255, 255))

    def init_lives(self):
        _size = (30,) * 2
        self.image1 = Image.open("./data/1.png").resize(_size)
        color_key = self.image1.getpixel((0, 0))
        self.image1 = pygame.image.fromstring(self.image1.tobytes(), self.image1.size, self.image1.mode).convert()
        self.image1.set_colorkey(color_key)
        self.image2 = Image.open("./data/2.png").resize(_size)
        color_key = self.image2.getpixel((0, 0))
        self.image2 = pygame.image.fromstring(self.image2.tobytes(), self.image2.size, self.image2.mode).convert()
        self.image2.set_colorkey(color_key)
        self.image3 = Image.open("./data/3.png").resize(_size)
        color_key = self.image3.getpixel((0, 0))
        self.image3 = pygame.image.fromstring(self.image3.tobytes(), self.image3.size, self.image3.mode).convert()
        self.image3.set_colorkey(color_key)
        self.image4 = Image.open("./data/4.png").resize(_size)
        color_key = self.image4.getpixel((0, 0))
        self.image4 = pygame.image.fromstring(self.image4.tobytes(), self.image4.size, self.image4.mode).convert()
        self.image4.set_colorkey(color_key)
        self.image5 = Image.open("./data/5.png").resize(_size)
        color_key = self.image5.getpixel((0, 0))
        self.image5 = pygame.image.fromstring(self.image5.tobytes(), self.image5.size, self.image5.mode).convert()
        self.image5.set_colorkey(color_key)


