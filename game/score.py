from pygame.font import Font

from game.base.base import StaticObject


class Score(StaticObject):

    def __init__(self, display):
        super().__init__(display)
        self._counter = 0

        # TEMP
        try:
            self._font = Font("./data/Astrolab.ttf", 20)
        except Exception:
            try:
                self._font = Font("...", 20)  # свои пути к файлам сюда
            except Exception:
                self._font = Font("...", 20)

        self._color = (255, 255, 255)
        self.image = self._font.render(str(self._counter), True, self._color)
        self.rect = self.image.get_rect(topleft=(10, 10))

    def update(self):
        self._counter += 1
        self.image = self._font.render(str(self._counter), True, self._color)
        self.rect = self.image.get_rect(topleft=(10, 10))
