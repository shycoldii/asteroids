import pygame
import configparser

from .background import Background
from .spaceship.spaceship import Spaceship
from .asteroid import Enemies
from .display import Display
from .state import State
from pygame.math import Vector2
from PIL import Image
import time


class Game:
    alpha, reverse = 255, False  # параметры для рамочки
    pygame.mixer.init()
    menu_sound = pygame.mixer.Sound("data/menu.mp3")
    space_sound = pygame.mixer.Sound("data/space.mp3")
    menu_sound.play(-1)
    finished = False

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.state = State.MENU
        self.display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))
        self.background = Background(display=self.display)
        self.enemies = Enemies(display=self.display)
        self.spaceship = Spaceship(display=self.display)
        self.first_spawn = True
        self.collision = True
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None
        self.init_lives()


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

    def apply_menu(self):
        """
        Применение настроек старта игры
        :return: None
        """
        self.change_alpha()
        mx, my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        x_size, y_size = 500, 300
        x_centered = self.display.get_width() / 2 - x_size / 2
        y_centered = self.display.get_height() / 2 - y_size / 2
        self.display.draw_rect(size=Vector2(x_size, y_size), color=(100, 97, 0, self.alpha)
                               , pos=Vector2(x_centered, y_centered), fill=False)
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2, self.display.get_height() / 2),
                               size=50, color=(100, 74, 0))
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2 - 2,
                                                    self.display.get_height() / 2 - 5), size=50)
        self.display.draw_text("click to start", pos=Vector2(self.display.get_width() / 2,
                                                             self.display.get_height() / 2 + 0.1 * self.display.get_height()),
                               size=15)
        if Game.is_mouse_on(x_centered, y_centered, x_size, y_size, mx, my) and mouse_pressed:
            self.state = State.GAME
            self.menu_sound.stop()
            self.space_sound.play(-1)

    def run(self):
        """Начало игры"""
        while not self.finished:
            self.background.draw()
            self.background.update()
            self.handle_keys()
            if self.state == State.MENU:
                self.apply_menu()
            elif self.state == State.GAME:
                self.spaceship.draw()
                self.spaceship.update()
                self.enemies.draw()
                self.enemies.update()
                self.display_lives()
                self.display_points()
                if self.first_spawn:
                    self.first_spawn = False
            elif self.state == State.END:
                pass

            pygame.display.flip()

    def handle_keys(self):
        """Функция, взаимодействующая с клавиатурой"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # выход
            self.finished = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:  # полноэкранный
                    self.display.toggle_fullscreen()
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE]:
                    self.spaceship.on_key_press(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE]:
                    self.spaceship.on_key_release(event.key)
            if event.type == pygame.QUIT:  # выход
                self.finished = True

    def display_lives(self):
        length = 115
        height = 40
        _size = (30,) * 2
        # вместо self.alfa надо подобрвть нормальный фон для сердечек )))
        self.display.draw_rect(size=Vector2(length, height), color=(255, 255, 255, 100)
                               , pos=Vector2(self.display.get_width() - length, 0), fill=True)
        for i in range(3):
            if i < self.spaceship._health:
                self.display.draw_img(img=self.image4, size=(30, 30),
                                      pos=(self.display.get_width() - length + 5 + i * 30 + i * 5, 5))
            else:
                if self.collision:
                    self.display.draw_img(img=self.image5, size=(30, 30),
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
        self.image1 = Image.open("/Users/13polbr/Desktop/asteroids/data/1.png").resize(_size)
        color_key = self.image1.getpixel((0, 0))
        self.image1 = pygame.image.fromstring(self.image1.tobytes(), self.image1.size, self.image1.mode).convert()
        self.image1.set_colorkey(color_key)
        self.image2 = Image.open("/Users/13polbr/Desktop/asteroids/data/2.png").resize(_size)
        color_key = self.image2.getpixel((0, 0))
        self.image2 = pygame.image.fromstring(self.image2.tobytes(), self.image2.size, self.image2.mode).convert()
        self.image2.set_colorkey(color_key)
        self.image3 = Image.open("/Users/13polbr/Desktop/asteroids/data/3.png").resize(_size)
        color_key = self.image3.getpixel((0, 0))
        self.image3 = pygame.image.fromstring(self.image3.tobytes(), self.image3.size, self.image3.mode).convert()
        self.image3.set_colorkey(color_key)
        self.image4 = Image.open("/Users/13polbr/Desktop/asteroids/data/4.png").resize(_size)
        color_key = self.image4.getpixel((0, 0))
        self.image4 = pygame.image.fromstring(self.image4.tobytes(), self.image4.size, self.image4.mode).convert()
        self.image4.set_colorkey(color_key)
        self.image5 = Image.open("/Users/13polbr/Desktop/asteroids/data/5.png").resize(_size)
        color_key = self.image5.getpixel((0, 0))
        self.image5 = pygame.image.fromstring(self.image5.tobytes(), self.image5.size, self.image5.mode).convert()
        self.image5.set_colorkey(color_key)