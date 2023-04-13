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
        self.east_exit = False
        self.in_town = False

        # Background Image
        self.background = None

        # Other Images
        self.tree_image = pygame.image.load('assets/tree.png')
        self.rock_img = pygame.image.load('assets/large_rock.png')

        # Adding Trees and Rocks while not in town
        if not self.in_town:
            tempwidthcount = 0
            tempheightcount = 0
            xpos = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
            ypos = 0
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1

            tempwidthcount = 0
            tempheightcount = 0
            xpos = xpos + BORDER_TILESIZE * 2
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
            ypos = ypos + BORDER_TILESIZE * 2
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1
            if not self.east_exit:
                Rock(self, WIN_WIDTH-BORDER_TILESIZE, WIN_HEIGHT/2-1, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, WIN_HEIGHT / 2 + 1, self.rock_img)





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

        self.east_exit = True
        Level.__init__(self, game, player)


