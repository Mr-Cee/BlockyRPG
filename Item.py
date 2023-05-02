import pygame
from config import *


class Item:
    def __init__(self, game, id):
        self.game = game
        self.id = id
        self.image = INVENTORY_DICT[self.id].convert_alpha()
        self.image.set_colorkey(WHITE)

        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()
        self.surface = self.image



    def resize(self, size):
        return pygame.transform.scale(self.surface, (size, size))
