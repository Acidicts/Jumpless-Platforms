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


class Platform(Sprite):
    def __init__(self, pos, surf, groups, movement=Vector2(0, 0), speed=0):
        super().__init__(pos, surf, groups)

        self.movement = movement
        self.speed = Vector2(0, 0)

        self.start_pos = pos

        if movement.x != 0:
            self.speed.x = movement.x / abs(movement.x) * speed
        if movement.y != 0:
            self.speed.y = movement.y / abs(movement.y) * speed

    def update(self, dt):
        self.old_rect = self.rect.copy()

        self.rect.x += dt * self.speed.x
        self.rect.y += dt * self.speed.y

        if self.rect.y < self.movement.y * TILESIZE:
            self.speed.y = abs(self.speed.y)
        if self.rect.y > self.start_pos[1]:
            self.speed.y = abs(self.speed.y) * -1
