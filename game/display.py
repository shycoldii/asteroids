import pygame
import pygame.gfxdraw
from pygame import Vector2


class Display:
    background = pygame.image.load("./data/background.jpg")

    def __init__(self, width, height):
        """
        Инициализация дисплея
        :param width: ширина
        :param height: высота
        """
        self.user_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)  # размер экрана "компьютера"
        self.window_size = (width, height)  # заданные настройки
        self.size = self.window_size
        # Размер окна будет такой, как текущий
        self.is_fullscreen = False
        self.window = pygame.display.set_mode(self.window_size)
        # Создание окна с заданными настройками
        self.update_frame()
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    def resize(self, new_size):
        """
        Изменение размера экрана
        :param new_size: новый размер окна
        """
        if self.is_fullscreen:
            self.window = pygame.display.set_mode(new_size, pygame.FULLSCREEN)
            self.size = self.user_size
        else:
            self.window = pygame.display.set_mode(new_size, pygame.RESIZABLE)
            self.size = self.window_size

    def full_screen(self):
        """Полноэкранный режим"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.resize(self.user_size)
            # на размер полного "компьютерного" экрана
        else:
            self.resize(self.window_size)
            # на постоянный размер

    def update_frame(self):
        """Обновление окна"""
        pygame.display.flip()
        # TODO: потом сюда можно добавлять всякие штуки наподобие ракет и тд
        if self.is_fullscreen:
            self.draw_img(self.background, self.user_size, (0, 0))
        else:
            self.draw_img(self.background, self.window_size, (0, 0))

    def draw(self, obj):
        obj.draw(self.window)

    def draw_img(self, img, size, pos):
        """
        Появление картинок на экране
        :param img: картинка, загруженная с помощью pygame.image.load
        :param pos: где хотим разместить (векторный набор)
        """
        self.window.blit(pygame.transform.scale(img, size), pos)

    def draw_rect(self, size, color=(0,0,0), fill=True, pos=Vector2(0, 0)):
        """
        Рисует прямоугольник
        :param size: размер
        :param color: цвет
        :param fill: закрашивать ли область внутри?
        :param pos: позиция
        :return: None
        """
        rect = pygame.Rect(pos, size)
        if fill:
            pygame.gfxdraw.box(self.window, rect, color)
        else:
            pygame.gfxdraw.rectangle(self.window, rect, color)

    def draw_text(self, text, pos=(0,0), size=16, color=(255, 255, 255)):
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
        font =pygame.font.Font(font_family, font_size)
        text = str(text)
        color = [int(color[i]) if color[i] <= 255 else 255 for i in range(len(color))]
        text_surface = font.render(text, True, color)
        if len(color) == 4 and color[3] != 255:
            # если есть прозрачность
            alpha_img = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, color[3]))
            text_surface.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        size = Vector2(text_surface.get_width(), text_surface.get_height())
        pos -= size // 2
        self.window.blit(text_surface, pos)
