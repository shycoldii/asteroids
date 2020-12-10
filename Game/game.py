import pygame
import configparser
import random

from .display import Display
from .state import State
from pygame.math import Vector2
from .map import Map


class Game:
    alpha, reverse = 255, False  # параметры для рамочки
    pygame.mixer.init()
    menu_sound = pygame.mixer.Sound("data/menu.mp3")
    space_sound = pygame.mixer.Sound("data/space.mp3")
    menu_sound.play()

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.finished = False
        self.list_bkg_aster = []
        self.state = State.MENU
        self.display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))
        self.create_bkg_aster()
        self.map = Map(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]), self.display)

    def create_bkg_aster(self):
        MAX = 60
        SIZE = 10
        for i in range(1, MAX):
            x = self.display.size[0] - i * 12 + SIZE
            y = random.randrange(0, self.display.size[1])

            self.list_bkg_aster.append([x, y])

    def move_bkg_aster(self):
        SIZE = 10
        bkg_aster = pygame.image.load('data/ast2.png').convert()  # передаем картинку
        clock = pygame.time.Clock()

        for i in self.list_bkg_aster:
            i[0] -= 1
            if i[0] < (0 - SIZE):
                i[0] = self.display.size[0]
                clock.tick(30)
            self.display.draw_img(bkg_aster, (SIZE, SIZE), (i[0], i[1]))

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
        x_centered = self.display.size[0] / 2 - x_size / 2
        y_centered = self.display.size[1] / 2 - y_size / 2
        self.display.draw_rect(size=Vector2(x_size, y_size), color=(100, 97, 0, self.alpha)
                               , pos=Vector2(x_centered, y_centered), fill=False)
        self.display.draw_text("Space", pos=Vector2(self.display.size[0] / 2, self.display.size[1] / 2),
                               size=50, color=(100, 74, 0))
        self.display.draw_text("Space", pos=Vector2(self.display.size[0] / 2 - 2,
                                                    self.display.size[1] / 2 - 5), size=50)
        self.display.draw_text("click to start", pos=Vector2(self.display.size[0] / 2,
                                                             self.display.size[1] / 2 + 0.1 * self.display.size[1]),
                               size=15)
        if Game.is_mouse_on(x_centered, y_centered, x_size, y_size, mx, my) and mouse_pressed:
            self.state = State.GAME
            self.menu_sound.stop()
            self.space_sound.play()

    def run(self):
        """Начало игры"""
        while not self.finished:
            self.handle_keys()
            if self.state == State.MENU:
                self.apply_menu()
                self.move_bkg_aster()  # фоновые астероиды
            elif self.state == State.GAME:
                self.move_bkg_aster()
                self.map.update()
                self.map.display()
                if not self.map.alive():  # этот метод пока что под вопросом
                    self.state = State.END
            elif self.state == State.END:
                pass
            self.display.update_frame()

    def handle_keys(self):
        """Функция, взаимодействующая с клавиатурой"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # выход
            self.finished = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:  # полноэкранный
                    self.display.full_screen()
                if event.key == pygame.K_LEFT:
                    print("Влево")
                if event.key == pygame.K_RIGHT:
                    print("Вправо")
                if event.key == pygame.K_UP:
                    print("Ускорение")
                if event.key == pygame.K_SPACE:
                    print("Выстрел")
            if event.type == pygame.QUIT:  # выход
                self.finished = True
