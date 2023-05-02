# Window Settings
import os
import sys

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

INVENTORY_DICT = {"ID": "Pic",
                  1: pygame.image.load('assets/Weapon_gladius_IMG.png')}

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
