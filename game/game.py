import pygame

from display import Display
from state import State
from pygame.math import Vector2

class Game:

    def __init__(self):
        self.finished = False
        self.state = State.MENU
        self.display = Display(800, 600)

    def run(self):
        """Начало игры"""
        pygame.init()
        while not self.finished:
            self.handle_keys()
            mx, my = pygame.mouse.get_pos()
            mouse_pos = Vector2(mx, my)
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if self.state == State.MENU:
                pass
            elif self.state == State.GAME:
                pass
            elif self.state == State.END:
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
