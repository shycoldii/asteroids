import time
from .asteroid import Enemies
import pygame

from .score import Score
from .spaceship.spaceship import Spaceship


class Map:
    def __init__(self, display):
        pygame.mixer.init()
        self.space_sound = pygame.mixer.Sound("data/space.mp3")
        self.ast_exp = pygame.mixer.Sound("data/ast_exp.mp3")
        self.ship_exp = pygame.mixer.Sound("data/ship_exp.mp3")
        self.display = display
        self.best_score = False
        self.score = Score(self.display)
        self.spaceship = Spaceship(self.display)
        self.enemies = Enemies(self.display)
        self.end = None
        self.start_time = None
        self.respawn = time.time()

        self.explosion_pics = [pygame.image.load(filename).convert_alpha() for filename in
                               ["data/e1.png", "data/e2.png", "data/e3.png",
                                "data/e4.png", "data/e5.png", "data/e6.png"]]
        self.reset()

    def reset(self):
        """Перезагрузка карты"""
        self.score = Score(self.display)
        self.spaceship = Spaceship(self.display)
        self.enemies = Enemies(self.display)
        self.end = None
        self.start_time = None
        self.best_score = False
        self.start_time = time.time()
        self.end = False

    def update_game(self):
        """
        Обновление состояния GAME
        :return: None
        """
        self.enemies.update()
        if self.spaceship.is_alive():
            self.ship_collision()
            self.cannon_colision()
            self.spaceship.update()
        else:
            self.spaceship.update()
            self.end = True
            self.update_best_score()


    def draw_game(self):
        """
        Отображение состояния GAME
        :return: None
        """
        if not self.end:
            self.enemies.draw()
            self.spaceship.draw()
        self.score.draw(self.display)

    def cannon_colision(self):
        for missle in self.spaceship.cannon.missiles:
            for ast in self.enemies.asteroids:
                exp = pygame.sprite.collide_mask(missle, ast)
                if exp:
                    self.ast_exp.play()
                    self.enemies.asteroids.remove(ast)
                    self.spaceship.cannon.missiles.remove(missle)
                    self.score.update()

    def ship_collision(self):
        if time.time() - self.respawn > 1:
            for ast in self.enemies.asteroids:
                if pygame.sprite.collide_mask(self.spaceship, ast):
                    self.ship_exp.play()
                    self.enemies.asteroids.remove(ast)  # удаляем булыжник, в который врезались
                    # анимация взрыва
                    self.spaceship.on_collision(True)
                    # анимация потери хп
                    self.spaceship._pos = (self.display.get_width() // 2,
                                           self.display.get_height() // 2)  # переносим в середину
                    self.respawn = time.time()
    def update_best_score(self):
        f = open("best_score.txt","r")
        if int(f.readline().split()[0]) < self.score._counter:
            f.close()
            f = open("best_score.txt","w+")
            f.write(str(self.score._counter))
            f.close()
            self.best_score = True
