import pygame
import configparser

from Game.display import Display
from Game.state import State
from pygame.math import Vector2
from Game.map import Map


class Game:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.finished = False
        self.state = State.MENU
        self.display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))
        self.map = Map(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))

    def run(self):
        """Начало игры"""
        pygame.init()
        while not self.finished:
            self.handle_keys()
            mx, my = pygame.mouse.get_pos()
            mouse_pos = Vector2(mx, my)
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if self.state == State.MENU:
                # отрисовываем заставку
                # мониторим щелчок по области заставки
                # если щелчок произошел, то self.state = State.Game
                pass
            elif self.state == State.GAME:
                pass
            elif self.state == State.LOOSE:
                pass
            elif self.state == State.WIN:
                pass

    def handle_keys(self):
        """Функция, взаимодействующая с клавиатурой"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # выход
            self.finished = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:  # полноэкранный
                    self.display.full_screen()
            if event.type == pygame.QUIT:  # выход
                self.finished = False
            # TODO: дописать тут логику игрока

        self.display.update_frame()
        pygame.display.flip()
