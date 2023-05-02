import pygame
from config import *


class Item:
    def __init__(self, game, id, AttackDamage, Armor, HP, MP):
        self.game = game
        self.id = id
        self.image = GEAR_IMG_DICT[self.id].convert_alpha()
        self.image.set_colorkey(WHITE)

        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()
        self.surface = self.image

        self.Description = GEAR_DESC_DICT[self.id]
        self.Type = ITEM_TYPE_DICT[self.id]
        self.AttackDamage = AttackDamage
        self.Armor = Armor
        self.HP = HP
        self.MP = MP

    def resize(self, size):
        return pygame.transform.scale(self.surface, (size, size)).convert_alpha()
