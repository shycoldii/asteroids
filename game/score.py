import configparser

from pygame.font import Font

from game.base.base import StaticObject


class Score(StaticObject):

    def __init__(self, display):
        super().__init__(display)

        config = configparser.ConfigParser()
        config.read('config.ini')

        self._counter = 0

        self._font = Font("./data/Astrolab.ttf", int(config["score"]["font_size"]))

        self._color = (255, 255, 255)
        self.image = self._font.render(str(self._counter), True, self._color)
        self.rect = self.image.get_rect(topleft=(10, 10))

    def update(self):
        self._counter += 1
        self.image = self._font.render(str(self._counter), True, self._color)
        self.rect = self.image.get_rect(topleft=(10, 10))
