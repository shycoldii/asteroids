import configparser

import pygame
from pygame.math import Vector2

from .background import Background
from .display import Display
from .map import Map
from .state import State


class Game:
    clock = pygame.time.Clock()
    finished = False
    alpha, reverse = 255, False
    pygame.mixer.init()
    menu_sound = pygame.mixer.Sound("data/menu.mp3")
    menu_sound.play(-1)
    trigger = False

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.state = State.MENU
        self.display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))
        self.background = Background(self.display)
        self.map = Map(self.display)
        self.fps = int(config["Game"]["FPS"])

    def apply_menu(self):
        """
        Применение состояния MENU
        :return: None
        """
        self.change_alpha()
        mx, my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        x_size, y_size = 500, 300
        x_centered = self.display.get_width() / 2 - x_size / 2
        y_centered = self.display.get_height() / 2 - y_size / 2
        if x_centered <= mx <= x_centered + x_size and y_centered <= my <= y_centered + y_size and mouse_pressed:
            self.state = State.GAME
            self.menu_sound.stop()
            self.map.space_sound.play(-1)
        self.display.draw_rect(size=Vector2(x_size, y_size), color=(100, 97, 0, self.alpha)
                               , pos=Vector2(x_centered, y_centered), fill=False)
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2, self.display.get_height() / 2),
                               size=50, color=(100, 74, 0))
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2 - 2,
                                                    self.display.get_height() / 2 - 5), size=50)
        self.display.draw_text("click to start", pos=Vector2(self.display.get_width() / 2,
                                                             self.display.get_height() / 2 + 0.1 * self.display
                                                             .get_height()),
                               size=15, color=(255, 255, 255, self.alpha))

    def apply_game(self):
        """
        Применения состояния GAME
        :return: None
        """
        self.map.update_game()
        self.map.draw_game()
        if self.map.end:
            self.apply_end()
            self.state = State.END

    def apply_end(self):
        self.map.space_sound.stop()
        if not self.trigger:
            self.trigger = True
            self.menu_sound.play(-1)
        self.map.spaceship._hp.update()
        self.map.spaceship._hp.draw()
        self.map.score.draw()
        self.change_alpha()
        mx, my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        x_size, y_size = 500, 300
        x_centered = self.display.get_width() / 2 - x_size / 2
        y_centered = self.display.get_height() / 2 - y_size / 2
        if self.map.best_score:
            color1 = (198, 169, 207, self.alpha)
            color2 = (119, 93, 128)
            self.display.draw_text(f"new record: {self.map.score._counter}",
                                   pos=Vector2(self.display.get_width() / 2,
                                               self.display.get_height() / 2 -
                                               0.1 * self.display.get_height()),
                                   size=15, color=color1)
        else:
            color1 = (209, 100, 100, self.alpha)
            color2 = (107, 51, 64)

        self.display.draw_rect(size=Vector2(x_size, y_size), color=color1,
                               pos=Vector2(x_centered, y_centered), fill=False)
        self.display.draw_text("replay", pos=Vector2(self.display.get_width() / 2,
                                                     self.display.get_height() / 2 + 0.1 * self.display.get_height()),
                               size=15, color=color1)
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2, self.display.get_height() / 2),
                               size=50, color=color2)
        self.display.draw_text("Space", pos=Vector2(self.display.get_width() / 2 - 2,
                                                    self.display.get_height() / 2 - 5), size=50)

        if x_centered <= mx <= x_centered + x_size and y_centered <= my <= y_centered + y_size and mouse_pressed:
            self.state = State.GAME
            self.trigger = False
            self.menu_sound.stop()
            self.map.reset()
            self.map.space_sound.play(-1)

    def run(self):
        """Начало игры"""
        while not self.finished:
            self.background.update()
            self.background.draw()
            self.handle_keys()
            if self.state == State.MENU:
                self.apply_menu()
            elif self.state == State.GAME:
                self.apply_game()
            elif self.state == State.END:
                self.apply_end()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_keys(self):
        """Функция, взаимодействующая с клавиатурой"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # выход
            self.finished = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:  # полноэкранный
                    self.display.toggle_fullscreen()
                if self.state == State.GAME:
                    self.map.spaceship.on_event(event)
            elif event.type == pygame.KEYUP:
                if self.state == State.GAME:
                    self.map.spaceship.on_event(event)
            if event.type == pygame.QUIT:  # выход
                self.finished = True

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
