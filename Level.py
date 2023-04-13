import math
import random
from config import *
from terrain import *
from SpriteUtilities import *


class Level(object):
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level specific info
    """

    def __init__(self, game, player):
        self.game = game
        self.enemy_list = self.game.enemy_sprites
        self.terrain_list = self.game.background_sprites

        # Exits Booleans
        self.north_exit = False
        self.south_exit = False
        self.west_exit = False
        self.in_town = False

        # Background Image
        self.background = None

        # Other Images
        tree_image = pygame.image.load('assets/tree.png')
        rock_img = pygame.image.load('assets/large_rock.png')

        # Adding Trees and Rocks while not in town
        if not self.in_town:
            for _ in range(10):
                Tree(self, random.randint(0+BORDER_TILESIZE, WIN_WIDTH-BORDER_TILESIZE), random.randint(0+BORDER_TILESIZE, WIN_HEIGHT-BORDER_TILESIZE), tree_image)
            tempwidthcount = 0
            tempheightcount = WIN_HEIGHT/BORDER_TILESIZE
            while tempwidthcount < WIN_WIDTH/BORDER_TILESIZE:
                Tree(self, random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), tree_image)



    # Update everything on this level
    def update(self):
        self.enemy_list.update()
        self.terrain_list.update()

    def draw(self):
        # Draw everyone on this level

        # Draw the Background
        self.game.screen.fill(WIN_BG)

        # Draw all the sprite lists we have
        self.terrain_list.draw(self.game.screen)
        self.enemy_list.draw(self.game.screen)


class Level_01(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)
