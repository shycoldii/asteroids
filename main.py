import configparser
import pygame

from Game.game import Game


def initialization():
    """Инициализация нужных файлов игры"""
    pygame.init()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    initialization()
    game = Game()
    game.run()
    pygame.quit()
