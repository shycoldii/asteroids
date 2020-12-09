import configparser

import pygame

from game.display import Display
from game.game import Game


def initialization():
    """Инициализация нужных файлов игры"""
    pygame.init()
    Display.init(width=int(config["Game"]["WINDOW_WIDTH"]),
                 height=int(config["Game"]["WINDOW_HEIGHT"]))
    pygame.display.set_mode(Display.window_size.totuple())


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    initialization()
    game = Game()
    game.run()
    pygame.quit()