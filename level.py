import pygame.sprite

from settings import *
from sprites import Sprite
from pytmx.util_pygame import load_pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collider_sprites):
        # noinspection PyTypeChecker
        super().__init__(groups)

        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_frect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hitbox = self.rect.copy()

        self.direction = Vector2(0, 0)
        self.speed = 100
        self.gravity = 5

        self.sprite_collider = [sprites.rect for sprites in collider_sprites]

        self.colliders = {
            'top': False,
            'bottom': False,
            'left': False,
            'right': False
        }

    def collide(self):
        self.colliders = {
            'top': False,
            'bottom': False,
            'left': False,
            'right': False
        }

        colliders = {
            'top': pygame.Rect(self.rect.midtop, (1, 1)),
            'bottom': pygame.Rect(self.rect.midbottom, (1, 1)),
            'left': pygame.Rect(self.rect.midleft, (1, 1)),
            'right': pygame.Rect(self.rect.midright, (1, 1))
        }

        for rect in colliders.values():
            if rect.collidelist(self.sprite_collider) > 0:
                self.colliders[list(colliders.keys())[list(colliders.values()).index(rect)]] = True

    def collisions(self, direction):
        if direction == 'x':
            for sprite in self.sprite_collider:
                if self.hitbox.colliderect(sprite):

                    if self.hitbox.right > sprite.left:
                        self.hitbox.right = sprite.left

                    elif self.hitbox.left < sprite.right:
                        self.hitbox.left = sprite.right

        elif direction == 'y':
            for sprite in self.sprite_collider:
                if self.hitbox.colliderect(sprite):

                    if self.rect.bottom > sprite.top:
                        self.hitbox.bottom = sprite.top

                    elif self.rect.top > sprite.bottom:
                        self.hitbox.top = sprite.bottom
                        self.direction.y = 0

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if not self.colliders['bottom']:
            self.direction.y += 1
        else:
            self.direction.y = 0

    def move(self, pos):
        self.rect.center = pos
        self.hitbox.center = pos

    def update(self, dt):
        self.collide()
        self.input()

        self.hitbox.x += self.direction.x * self.speed * dt
        self.collisions('x')

        self.hitbox.y += self.direction.y * dt * self.gravity
        self.collisions('y')

        self.rect.center = self.hitbox.center


class Level:
    def __init__(self, game):
        self.game = game
        self.running = True

        self.all_sprites = AllSprites()
        self.colliders_sprites = pygame.sprite.Group()
        self.player = None

        self.setup()

        self.map = 'map/0.tmx'

    def setup(self):
        tmx_data = load_pygame('map/0.tmx')  # Corrected this line

        for x, y, surf in tmx_data.get_layer_by_name('Colliders').tiles():
            Sprite((x * TILESIZE, y * TILESIZE), surf, (self.all_sprites, self.colliders_sprites))

        for obj in tmx_data.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.colliders_sprites)

    def run(self, dt):

        self.game.screen.fill((0, 0, 0))

        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.player)

        pygame.display.flip()


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

        self.offset = Vector2(0, 0)
        self.display = pygame.display.get_surface()

        self.debug = False

    def custom_draw(self, player):
        self.offset.x = player.hitbox.x - WIDTH / 2
        self.offset.y = player.hitbox.y - HEIGHT / 2

        for sprite in self:
            offset_rect = Vector2()

            offset_rect.x = sprite.rect.x - self.offset.x
            offset_rect.y = sprite.rect.y - self.offset.y

            self.display.blit(sprite.image, offset_rect)

            if self.debug:
                if hasattr(sprite, 'colliders'):
                    pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (offset_rect, (32, 32)), 1)
                else:
                    pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (offset_rect, (32, 32)), 1)
