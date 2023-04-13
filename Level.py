import math
import random
from config import *
from terrain import *
from SpriteUtilities import *


class Level:
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level specific info
    """

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.enemy_sprites = self.game.enemy_sprites
        self.background_sprites = self.game.background_sprites
        self.all_sprites = self.game.all_sprites

        # Exits Booleans
        self.north_exit = False
        self.south_exit = False
        self.west_exit = False
        self.east_exit = False
        self.in_town = False

        # Background Image
        self.background = WIN_BG

        # Other Images
        self.tree_image = pygame.image.load('assets/tree.png')
        self.rock_img = pygame.image.load('assets/large_rock.png')

    def terrainGen(self):
        # Adding Trees and Rocks while not in town
        if not self.in_town:
            # Horizontal Rock Walls
            tempwidthcount = 0
            tempheightcount = 0
            xpos = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
                print(xpos)
            # Gap in the Middle
            xpos_exit = xpos
            xpos = xpos_exit + BORDER_TILESIZE * 2
            tempwidthcount = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
                print(xpos)

            # Vertical Rock Wall
            ypos = 0
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1
            tempheightcount = 0
            ypos_exit = ypos
            # Gap in the Middle
            ypos = ypos_exit + BORDER_TILESIZE * 2
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1

            if not self.east_exit:  # Adds Rocks if East Exit is False
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit + BORDER_TILESIZE, self.rock_img)
                print('place rocks in east')
                print(self.east_exit)
            if not self.west_exit:  # Adds Rocks if West Exit is False
                Rock(self, 0, ypos_exit, self.rock_img)
                Rock(self, 0, ypos_exit + BORDER_TILESIZE, self.rock_img)
            if not self.north_exit:  # Adds Rocks if North Exit is False
                Rock(self, xpos_exit, 0, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, 0, self.rock_img)
            if not self.south_exit:  # Adds Rocks if South Exit is False
                Rock(self, xpos_exit, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)

            for _ in range(int(WIN_WIDTH / BORDER_TILESIZE)):
                Tree(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                     random.randint(BORDER_TILESIZE * 2,
                                    WIN_HEIGHT - (BORDER_TILESIZE * 2) - self.tree_image.get_height() / 2),
                     self.tree_image)
                Rock(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                     random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - BORDER_TILESIZE * 2), self.rock_img)

    # Update everything on this level
    def update(self):
        self.enemy_sprites.update()
        self.background_sprites.update()


    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen

        # Draw the Background
        self.screen.fill(self.background)

        # Draw all the sprite lists we have
        self.background_sprites.draw(self.screen)

        self.enemy_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)


class Level_01(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = False
        self.west_exit = False
        self.east_exit = True
        self.in_town = False

        Level.terrainGen(self)

class Level_02(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = False
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        if game.current_level_no == 1:
            self.terrainGen()



