import pygame.sprite

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        # noinspection PyTypeChecker
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.old_rect = self.rect.copy()
