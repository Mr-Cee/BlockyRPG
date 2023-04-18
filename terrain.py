import pygame
from character import *
import math
# from SpriteUtilities import *
from config import *
#

class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game

        self.image = image
        self.image.set_colorkey(WHITE)

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # self.rect = self.image.get_rect()
        self.rect = (self.x, self.y, self.width, self.height)
        self.collision_rect = pygame.Rect(self.x + 5, self.y + self.height - 5, self.width - 10, self.height / 4)

        self._layer = self.y + self.height

        if self.game.player.isAttackable:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.background_sprites)
        else:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_background_sprites)


class Rock(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game

        self.image = image
        self.image.set_colorkey(WHITE)

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision_rect = self.rect

        self._layer = self.y + self.height

        if self.game.player.isAttackable:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.background_sprites)
        else:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_background_sprites)

class Building(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game

        self.image = image
        self.image.set_colorkey(WHITE)

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collision_rect = self.rect

        self._layer = self.y + self.height

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.background_sprites)
