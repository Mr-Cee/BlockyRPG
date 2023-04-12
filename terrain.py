import pygame
import math
# from SpriteUtilities import *
from config import *


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

        self._layer = self.collision_rect.bottom

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.background_sprites)
