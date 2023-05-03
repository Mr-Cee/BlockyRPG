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
                   # Weapon Coords
                   (7, 5): 0,
                   (7, 6): 0,
                   (8, 5): 0,
                   (8, 6): 0,
                   # Shield Coords
                   (10, 5): 1,
                   (10, 6): 1,
                   (11, 5): 1,
                   (11, 6): 1,
                   # Helmet Coords
                   (9, 0): 2,
                   (9, 1): 2,
                   (10, 0): 2,
                   (10, 1): 2,
                   # Chest Coords
                   (9, 2): 3,
                   (10, 2): 3,
                   # Gloves Coords
                   (7, 2): 4,
                   (8, 2): 4,
                   # Legs Coords
                   (9, 3): 5,
                   (9, 4): 5,
                   (10, 3): 5,
                   (10, 4): 5,
                   # Boots Coords
                   (9, 5): 6,
                   (9, 6): 6,
                   (10, 5): 6,
                   (10, 6): 6,
                   # Neck Coords
                   (10, 2): 7,
                   (11, 2): 7
                   }

GEAR_IMG_DICT = {"ID": "Pic",
                 0: pygame.image.load('assets/Weapon_gladius_IMG.png'),
                 1: pygame.image.load('assets/cross-shield.png'),
                 2: pygame.image.load('assets/visored-helm.png'),
                 3: pygame.image.load('assets/breastplate.png'),
                 4: pygame.image.load('assets/gauntlet.png'),
                 5: pygame.image.load('assets/trousers.png'),
                 6: pygame.image.load('assets/steeltoe-boots.png'),
                 7: pygame.image.load('assets/gem-pendant.png'),
                 }

GEAR_DESC_DICT = {"ID": "DESCRIPTION",
                  0: "Short Sword",
                  1: "Full Shield",
                  2: "Helmet",
                  3: "Chest Plate",
                  4: "Gloves",
                  5: "Legs",
                  6: "Boots",
                  7: "Necklace"
                  }

ITEM_TYPE_DICT = {"ID": "TYPE",
                  0: "Weapon",
                  1: "Shield",
                  2: "Helmet",
                  3: "Chest",
                  4: "Gloves",
                  5: "Legs",
                  6: "Boots",
                  7: "Necklace"}

INVENTORY_EQUIPED_REC_DICT = {"ID": "REC",
                              0: (pygame.Rect(449, 212, 33, 33)),  # Weapon
                              1: (pygame.Rect(557, 212, 33, 33)),  # Shield
                              2: (pygame.Rect(503, 42, 33, 33)),  # Helmet
                              3: (pygame.Rect(503, 99, 33, 33)),  # Chest
                              4: (pygame.Rect(447, 99, 33, 33)),  # Gloves
                              5: (pygame.Rect(503, 156, 33, 33)),  # Legs
                              6: (pygame.Rect(503, 214, 33, 33)),  # Boots
                              7: (pygame.Rect(559, 99, 33, 33)),  # Neck
                              }

ITEM_RARITY_DICT = {"ID": "RARITY",
                    0: "Common",
                    1: "Uncommon",
                    2: "Rare",
                    3: "Legendary",
                    4: "Mythical"}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SOFTBROWN = (145, 139, 109)
TEMPCOLOR = (204, 203, 161)

COMMONCOLOR = BLACK
UNCOMMONCOLOR = (54, 128, 40)
RARECOLOR = (5, 21, 122)
LEGENDARYCOLOR = (232, 127, 7)
MYTHICALCOLOR = (198, 3, 252)
RARITY_COLOR_DICT = {"ID": "COLOR",
                     0: COMMONCOLOR,
                     1: UNCOMMONCOLOR,
                     2: RARECOLOR,
                     3: LEGENDARYCOLOR,
                     4: MYTHICALCOLOR}
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
