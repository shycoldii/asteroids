import pygame

from game.display import Display
from game.state import State
from vector_utils import vector


class Game:
    finished = False
    state = State.MENU

    @classmethod
    def run(cls):
        """Начало игры"""
        pygame.init()
        while not cls.finished:
            cls.handle_keys()
            mx, my = pygame.mouse.get_pos()
            mouse_pos = vector(mx,my)
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if cls.state == State.MENU:
                pass
            elif cls.state == State.GAME:
                pass
            elif cls.state == State.END:
                pass

    @classmethod
    def handle_keys(cls):
        """Функция, взаимодействующая с клавиатурой"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: #выход
            cls.finished = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12: #полноэкранный
                    Display.full_screen()
            if event.type == pygame.QUIT: #выход
                    cls.finished = False
            #TODO: дописать тут логику игрока

        Display.update_frame()
        pygame.display.flip()