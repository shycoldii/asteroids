import pygame as pg
from pygame.math import Vector2
import pygame.gfxdraw


class Display:

    def __init__(self, width, height):
        pg.display.init()
        pg.mouse.set_cursor(*pg.cursors.tri_left)

        self._size = (width, height)
        self._default_size = (width, height)
        self._full_size = (pg.display.Info().current_w, pg.display.Info().current_h)
        self._display = pg.display.set_mode(self._size)

        self._fullscreen = False

        self.ship_position = Vector2(width//2, height//2)

    def get_width(self):
        return self._size[0]

    def get_height(self):
        return self._size[1]

    def get_size(self):
        return self._size

    def get_full_size(self):
        return self._full_size

    def get_surface(self):
        return self._display.copy()

    def get_rect(self, **kwargs):
        return self._display.get_rect(**kwargs)

    def blit(self, source, dest, area=None, special_flags=0):
        return self._display.blit(source, dest, area, special_flags)

    def fill(self, color, rect=None, special_flags=0):
        return self._display.fill(color, rect, special_flags)

    def resize(self, new_size):
        if self._fullscreen:
            self._display = pg.display.set_mode(new_size, pg.FULLSCREEN)
            self._size = self._full_size
        else:
            self._display = pg.display.set_mode(new_size, pg.RESIZABLE)
            self._size = self._default_size

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self.resize(self._full_size)
        else:
            self.resize(self._default_size)

    def draw(self, obj):
        obj.draw()

    def draw_img(self, img, size, pos):
        """
        Появление картинок на экране
        :param size:
        :param img: картинка, загруженная с помощью pygame.image.load
        :param pos: где хотим разместить (векторный набор)
        """
        self._display.blit(pg.transform.scale(img, size), pos)

    def draw_rect(self, size, color=(0, 0, 0), fill=True, pos=Vector2(0, 0)):
        """
        Рисует прямоугольник
        :param size: размер
        :param color: цвет
        :param fill: закрашивать ли область внутри?
        :param pos: позиция
        :return: None
        """
        rect = pg.Rect(pos, size)
        if fill:
            pg.gfxdraw.box(self._display, rect, color)
        else:
            pg.gfxdraw.rectangle(self._display, rect, color)

    def draw_text(self, text, pos=(0, 0), size=16, color=(255, 255, 255)):
        """
        Рисует текст
        :param text: текст
        :param pos: позиция
        :param size: размер
        :param color: цвет
        :return: None
        """
        font_size = round(size)
        try:
            font_family = "./data/Astrolab.ttf"
        except:
            font_family = "data/Astrolab.ttf"
        font = pg.font.Font(font_family, font_size)
        text = str(text)
        color = [int(color[i]) if color[i] <= 255 else 255 for i in range(len(color))]
        text_surface = font.render(text, True, color)
        if len(color) == 4 and color[3] != 255:
            # если есть прозрачность
            alpha_img = pg.Surface(text_surface.get_size(), pg.SRCALPHA)
            alpha_img.fill((255, 255, 255, color[3]))
            text_surface.blit(alpha_img, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        size = Vector2(text_surface.get_width(), text_surface.get_height())
        pos -= size // 2
        self._display.blit(text_surface, pos)

    def set_ship_position(self, pos):
        self.ship_position = pos

    def get_ship_position(self):
        return self.ship_position