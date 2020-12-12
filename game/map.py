from PIL import Image
import time
from .asteroid import Enemies
import pygame
from .spaceship.spaceship import Spaceship


class Map:
    def __init__(self, display):
        self.space_sound = pygame.mixer.Sound("data/space.mp3")
        self.display = display
        self.spaceship = Spaceship(display=self.display)
        self.enemies = Enemies(display=self.display)

        self.end = None
        self.first_spawn = True
        self.start_time = None
        self.respawn = time.time()

        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None

        self.explosion_pics = [pygame.image.load(filename).convert_alpha() for filename in
                               ["data/e1.png", "data/e2.png", "data/e3.png",
                                "data/e4.png", "data/e5.png", "data/e6.png"]]
        self.init_lives()
        self.reset()

    def reset(self):
        """Перезагрузка карты"""
        self.start_time = time.time()
        self.end = False
        self.init_lives()

    def update_game(self):
        """
        Обновление состояния GAME
        :return: None
        """
        if self.first_spawn:
            self.first_spawn = False
        self.enemies.update()
        if self.spaceship.health != 0:
            self.spaceship.update()
            self.ship_collision()
            self.cannon_colision()
        else:
            self.end = True

    def draw_game(self):
        """
        Отображение состояния GAME
        :return: None
        """
        self.display_lives()
        self.display_points()
        if not self.end:
            self.enemies.draw()
            self.spaceship.draw()

    # ==========эти ф-и видимо потеряют свой смысл или изменятся
    def display_lives(self):
        length = 140
        _size = (40,) * 2
        for i in range(3):
            if i < self.spaceship.health:
                self.display.draw_img(img=self.image5, size=(40, 40),
                                      pos=(self.display.get_width() - length + 5 + i * 40 + i * 5, 5))
            else:
                self.display.draw_img(img=self.image1, size=(40, 40),
                                      pos=(self.display.get_width() - length + 5 + i * 40 + i * 5, 5))

    def display_points(self):
        length = 120 + len(str(self.spaceship.score)) * 10
        if length < 130:
            length = 130
        self.display.draw_text(text="POINTS:  " + str(self.spaceship.score), pos=(length // 2, 20), size=11,
                               color=(255, 255, 255))

    def init_lives(self):
        _size = (30,) * 2
        self.image1 = Image.open("./data/0.png").resize(_size)
        color_key = self.image1.getpixel((0, 0))
        self.image1 = pygame.image.fromstring(self.image1.tobytes(), self.image1.size, self.image1.mode).convert()
        self.image1.set_colorkey(color_key)
        self.image2 = Image.open("./data/1.png").resize(_size)
        color_key = self.image2.getpixel((0, 0))
        self.image2 = pygame.image.fromstring(self.image2.tobytes(), self.image2.size, self.image2.mode).convert()
        self.image2.set_colorkey(color_key)
        self.image3 = Image.open("./data/2.png").resize(_size)
        color_key = self.image3.getpixel((0, 0))
        self.image3 = pygame.image.fromstring(self.image3.tobytes(), self.image3.size, self.image3.mode).convert()
        self.image3.set_colorkey(color_key)
        self.image4 = Image.open("./data/3.png").resize(_size)
        color_key = self.image4.getpixel((0, 0))
        self.image4 = pygame.image.fromstring(self.image4.tobytes(), self.image4.size, self.image4.mode).convert()
        self.image4.set_colorkey(color_key)
        self.image5 = Image.open("./data/4.png").resize(_size)
        color_key = self.image5.getpixel((0, 0))
        self.image5 = pygame.image.fromstring(self.image5.tobytes(), self.image5.size, self.image5.mode).convert()
        self.image5.set_colorkey(color_key)

    def cannon_colision(self):
        for missle in self.spaceship.cannon.missiles:
            for ast in self.enemies.asteroids:
                exp = pygame.sprite.collide_mask(missle, ast)
                if exp:
                    self.enemies.asteroids.remove(ast)
                    self.spaceship.cannon.missiles.remove(missle)
                    # сделать добавление очков игроку

    def ship_collision(self):
        if time.time() - self.respawn > 1:
            for ast in self.enemies.asteroids:
                if pygame.sprite.collide_mask(self.spaceship, ast):
                    self.enemies.asteroids.remove(ast)  # удаляем булыжник, в который врезались
                    # анимация взрыва
                    self.spaceship.collision(True)
                    # анимация потери хп
                    self.spaceship._pos = (self.display.get_width() // 2,
                                           self.display.get_height() // 2)  # переносим в середину
                    self.respawn = time.time()
