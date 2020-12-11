import configparser
import pygame

from Game.game import Game


def initialization():
    """Инициализация нужных файлов игры"""
    pygame.init()
    pygame.display.set_icon(pygame.image.load("data/icon.bmp"))
    pygame.display.set_caption('SPACE')


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    initialization()
    game = Game()
    game.run()
    pygame.quit()
