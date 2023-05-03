import random
import math

import pygame
from config import *


class Item:
    def __init__(self, game, id, AttackDamage, Armor, HP, MP, CritChance, CritBonus):
        self.game = game
        self.id = id
        self.image = GEAR_IMG_DICT[self.id].convert_alpha()
        self.image.set_colorkey(WHITE)

        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()
        self.surface = self.image

        QualityRand = random.randint(1, 100)
        ItemRarity = 0

        if 1 <= QualityRand <= 60:  # 60%
            ItemRarity = 0

        elif 61 <= QualityRand <= 80:  # 20%
            ItemRarity = 1

        elif 81 <= QualityRand <= 90:  # 10%
            ItemRarity = 2

        elif 91 <= QualityRand <= 98:  # 8%
            ItemRarity = 3

        else:  # 2%
            ItemRarity = 4

        self.Description = (str(ITEM_RARITY_DICT[ItemRarity]) + " " + str(GEAR_DESC_DICT[self.id]) + " ")
        self.Type = ITEM_TYPE_DICT[self.id]
        if self.id == 0:
            self.AttackDamage = AttackDamage + (3 * ItemRarity)
        else:
            self.AttackDamage = 0

        if 0 < self.id <= 6:
            self.Armor = Armor + (3 * ItemRarity)
        else:
            self.Armor = 0

        if self.id == 7:
            self.CritChance = CritChance
            self.CritBonus = CritBonus
        else:
            self.CritChance = 0
            self.CritBonus = 0

        self.HP = HP + (3 * ItemRarity)
        self.MP = MP + (3 * ItemRarity)
        self.Rarity = ItemRarity



    def resize(self, size):
        return pygame.transform.scale(self.surface, (size, size)).convert_alpha()
