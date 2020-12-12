import pygame
import configparser

from .display import Display
from .state import State
from .map import Map


class Game:
    clock = pygame.time.Clock()
    finished = False

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.state = State.MENU
        self.display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))
        self.map = Map(display=self.display)
        self.fps = 60

    def apply_menu(self):
        """
        Применение состояния MENU
        :return: None
        """
        self.map.update_menu()
        mx, my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        x_size, y_size = 500, 300
        x_centered = self.display.get_width() / 2 - x_size / 2
        y_centered = self.display.get_height() / 2 - y_size / 2
        if Map.is_mouse_on(x_centered, y_centered, x_size, y_size, mx, my) and mouse_pressed:
            self.state = State.GAME
            self.map.menu_sound.stop()
            self.map.space_sound.play(-1)
        self.map.draw_menu(x_size, y_size, x_centered, y_centered)

    def apply_game(self):
        """
        Применения состояния GAME
        :return: None
        """
        self.map.update_game()
        self.map.draw_game()
    def apply_end(self):
         pass

    def run(self):
        """Начало игры"""
        while not self.finished:
            self.handle_keys()
            if self.state == State.MENU:
                self.apply_menu()
            elif self.state == State.GAME:
                self.apply_game()
            elif self.state == State.END:
                pass
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
                    self.map.spaceship.on_key_press(event.key)
            elif event.type == pygame.KEYUP:
                    if self.state == State.GAME:
                        self.map.spaceship.on_key_release(event.key)
            if event.type == pygame.QUIT:  # выход
                self.finished = True
