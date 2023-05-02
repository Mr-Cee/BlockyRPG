# Window Settings
import os
import sys

import pygame as pygame
import pygame.image


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


WIN_WIDTH = 800  # Must be Multiple of 32 to look nice
WIN_HEIGHT = 500  # Must be Multiple of 32 to look nice
GAME_HEIGHT = WIN_HEIGHT + 160
# WIN_BG = (17, 102, 24)
WIN_BG = pygame.image.load('assets/background_grass.png')
WIN_BG = pygame.transform.scale(WIN_BG, (WIN_WIDTH, WIN_HEIGHT))
WIN_Attack_BG = pygame.image.load('assets/background_attack.png')
WIN_Attack_BG = pygame.transform.scale(WIN_Attack_BG, (WIN_WIDTH, WIN_HEIGHT))

EquipedPOS_Dict = {"POS": "Slot#",
                   (8, 5): 0,
                   (11, 5): 1,
                   (9, 0): 2,
                   (9, 1): 2,
                   (10, 0): 2,
                   (10, 1): 2,
                   }

GEAR_IMG_DICT = {"ID": "Pic",
                 0: pygame.image.load('assets/Weapon_gladius_IMG.png'),
                 1: pygame.image.load('assets/cross-shield.png'),
                 2: pygame.image.load('assets/visored-helm.png')
                 }

GEAR_DESC_DICT = {"ID": "DESCRIPTION",
                  0: "A Short Sword",
                  1: "A Full Shield",
                  2: "A Common Helmet"}

ITEM_TYPE_DICT = {"ID": "TYPE",
                  0: "Weapon",
                  1: "Shield",
                  2: "Helmet"}

INVENTORY_EQUIPED_REC_DICT = {"ID": "REC",
                              0: (pygame.Rect(449, 212, 33, 33)),
                              1: (pygame.Rect(557, 212, 33, 33)),
                              2: (pygame.Rect(503, 42, 33, 33))
                              }

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SOFTBROWN = (145, 139, 109)
TEMPCOLOR = (204, 203, 161)
#

# Clock/Tick Settings
FPS = 30

# Layer Settings
TERRAIN_LAYER = 1  # Not used anymore because of dynamic layering based on y pos
PLAYER_LAYER = TERRAIN_LAYER + 1  # Not used anymore because of dynamic layering based on y pos

# Sprite Settings
CHARACTER_TILESIZE = 64
BORDER_TILESIZE = 32

# Player Settings
PLAYER_SPEED = 5
PROJECTILE_SPEED = 10

# Enemy Settings
ENEMY_SPEED = 1
