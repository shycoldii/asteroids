import pygame
import pygame.gfxdraw

from vector_utils import vector

class Display:
    background = pygame.image.load("D:/it_projects/asteroids/data/background.jpg")
    height = None
    width = None
    user_size = None
    size = None
    window_size = None
    is_fullscreen= False
    all_font = {}
    window = None
    end = False

    @classmethod
    def init(cls, width, height):
        """
        Инициализация дисплея
        :param width: ширина
        :param height: высота
        """
        cls.set_cursor()
        cls.user_size = vector(pygame.display.Info().current_w,  # размер экрана "компьютера"
                               pygame.display.Info().current_h)
        cls.size = vector(width, height)  # заданные настройки
        cls.window_size = cls.size.copy()
        # Размер окна будет такой, как текущий
        cls.resize(cls.size.x, cls.size.y)
        # Создание окна с заданными настройками
        cls.update_frame()
        cls.width = width
        cls.height = height

    @classmethod
    def set_cursor(cls):
        """Курсор вида треугольник"""
        try:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        except:
            pass

    @classmethod
    def resize(cls, w, h):
        """
        Изменение размера экрана
        :param w: ширина
        :param h: высота
        """
        if cls.is_fullscreen:
            cls.window = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            cls.window = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    @classmethod
    def full_screen(cls):
        """Полноэкранный режим"""
        cls.is_fullscreen = not cls.is_fullscreen
        if cls.is_fullscreen:
            cls.resize(cls.user_size.x, cls.user_size.y)
            # на размер полного "компьютерного" экрана
        else:
            cls.resize(cls.width, cls.height)
            # на постоянный размер

    @classmethod
    def update_frame(cls):
        """Обновление окна"""
        #TODO: потом сюда можно добавлять всякие штуки наподобие ракет и тд
        if cls.is_fullscreen:
            cls.draw_img(cls.background,vector(0,0),(cls.user_size.x,cls.user_size.y))
        else:
            cls.draw_img(cls.background, vector(0, 0), (cls.size.x,cls.size.y))

    @classmethod
    def draw_img(cls, img, pos,size):
        """
        Появление картинок на экране
        :param img: картинка, загруженная с помощью pygame.image.load
        :param pos: где хотим разместить (векторный набор)
        :param size: какого размера
        """
        cls.window.blit(pygame.transform.scale(img, size), pos.totuple())


if __name__ == "__main__":
    pygame.init()
    Display.init(800,600) #потом это заменит
    pygame.display.set_mode(Display.window_size.totuple())
    c=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    Display.full_screen()
        Display.update_frame()
        pygame.display.flip()
    pygame.quit()