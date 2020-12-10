import pygame as pg
from pygame.sprite import Sprite


class Missile(Sprite):

    def __init__(self, *groups):
        super(Missile, self).__init__(*groups)
