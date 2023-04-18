# Window Settings
import pygame.image

WIN_WIDTH = 800  # Must be Multiple of 32 to look nice
WIN_HEIGHT = 640  # Must be Multiple of 32 to look nice
GAME_HEIGHT = WIN_HEIGHT + 160
# WIN_BG = (17, 102, 24)
WIN_BG = pygame.image.load('assets/background_grass.png')
WIN_BG = pygame.transform.scale(WIN_BG, (WIN_WIDTH, WIN_HEIGHT))
WIN_Attack_BG = pygame.image.load('assets/background_attack.png')
WIN_Attack_BG = pygame.transform.scale(WIN_Attack_BG, (WIN_WIDTH, WIN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TEMPCOLOR = (204, 203, 161)
#

# Clock/Tick Settings
FPS = 30

# Layer Settings
TERRAIN_LAYER = 1  # Not used anymore because of dynamic layering based on y pos
PLAYER_LAYER = TERRAIN_LAYER + 1  # Not used anymore because of dynamic layering based on y pos

# Sprite Settings
CHARACTER_TILESIZE = 32
BORDER_TILESIZE = 32

# Player Settings
PLAYER_SPEED = 10

# Enemy Settings
ENEMY_SPEED = 1
