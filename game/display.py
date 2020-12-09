import pygame
import pygame.gfxdraw


class Display:
    background = pygame.image.load("./data/background.jpg")
    all_font = {}

    def __init__(self, width, height):
        """
        Инициализация дисплея
        :param width: ширина
        :param height: высота
        """
        self.user_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)  # размер экрана "компьютера"
        self.size = self.window_size = (width, height)  # заданные настройки
        # Размер окна будет такой, как текущий
        self.is_fullscreen = False
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        # Создание окна с заданными настройками
        self.update_frame()
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    def resize(self, new_size):
        """
        Изменение размера экрана
        :param new_size:
        """
        if self.is_fullscreen:
            self.window = pygame.display.set_mode(new_size, pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(new_size, pygame.RESIZABLE)

    def full_screen(self):
        """Полноэкранный режим"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.resize(*self.user_size)
            # на размер полного "компьютерного" экрана
        else:
            self.resize(self.size)
            # на постоянный размер

    def update_frame(self):
        """Обновление окна"""
        # TODO: потом сюда можно добавлять всякие штуки наподобие ракет и тд
        if self.is_fullscreen:
            self.background = pygame.transform.scale(self.background, self.user_size)
            self.draw_img(self.background, (0, 0))
        else:
            self.background = pygame.transform.scale(self.background, self.size)
            self.draw_img(self.background, (0, 0))

    def draw(self, obj):
        obj.draw(self.window)

    def draw_img(self, img, pos):
        """
        Появление картинок на экране
        :param img: картинка, загруженная с помощью pygame.image.load
        :param pos: где хотим разместить (векторный набор)
        """
        self.window.blit(img, pos)


if __name__ == "__main__":
    pygame.init()
    display = Display(800, 600)
    pygame.display.set_mode(display.window_size)
    c = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    display.full_screen()
        display.update_frame()
        pygame.display.flip()
    pygame.quit()
