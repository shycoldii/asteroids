import configparser

import pygame

from game.display import Display
from game.game import Game


def initialization():
    """Инициализация нужных файлов игры"""
    pygame.init()
    display = Display(int(config["Game"]["WINDOW_WIDTH"]), int(config["Game"]["WINDOW_HEIGHT"]))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    initialization()
    game = Game()
    game.run()
    pygame.quit()
