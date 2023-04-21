import math
import random

import pygame

import button
from Enemy import *


class Level:
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level specific info
    """

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.screen = self.game.screen

        self.enemy_sprites = self.game.enemy_sprites
        self.combat_enemy_sprites = self.game.combat_enemy_sprites
        self.background_sprites = self.game.background_sprites
        self.combat_background_sprites = self.game.combat_background_sprites
        self.all_sprites = self.game.all_sprites
        self.player_sprite = self.game.player_sprite
        self.UI_Sprites = self.game.UI_Sprites
        self.combat_UI_Sprites = self.game.combat_UI_Sprites

        # Exits Booleans
        self.north_exit = False
        self.south_exit = False
        self.west_exit = False
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 0

        # Background Image
        self.background = WIN_BG
        self.attackBackground = pygame.image.load(self.game.resource_path('assets/background_attack.png'))
        self.attackBackground = pygame.transform.scale(self.attackBackground, (WIN_WIDTH, WIN_HEIGHT))
        self.Monster1 = None

        # Other Images
        self.tree_image = pygame.image.load(self.game.resource_path('assets/tree.png'))
        self.rock_img = pygame.image.load(self.game.resource_path('assets/large_rock.png'))
        self.building1 = pygame.image.load(self.game.resource_path('assets/Building_1.png'))
        self.wolf_spritesheet = SpriteSheet_Black('assets/Wolfsheet1.png')
        self.character_spritesheet = SpriteSheet('assets/CharacterSpritesheet.png')

        self.milliseconds_delay = 2000  # 1 seconds
        self.CharacterAttackTimer = pygame.USEREVENT + 1
        self.EnemyAttackTimer = pygame.USEREVENT + 2




    def terrainGen(self):
        # Horizontal Rock Walls
        if self.player.isAttackable:
            tempwidthcount = 0
            tempheightcount = 0
            xpos = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
            # Gap in the Middle
            xpos_exit = xpos
            xpos = xpos + BORDER_TILESIZE * 2
            tempwidthcount = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1

            # Vertical Rock Wall
            ypos = 0
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1
            tempheightcount = 0
            ypos_exit = ypos
            # Gap in the Middle
            ypos = ypos + BORDER_TILESIZE * 2
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1

            if not self.east_exit:  # Adds Rocks if East Exit is False
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit + BORDER_TILESIZE, self.rock_img)
            if not self.west_exit:  # Adds Rocks if West Exit is False
                Rock(self, 0, ypos_exit, self.rock_img)
                Rock(self, 0, ypos_exit + BORDER_TILESIZE, self.rock_img)
            if not self.north_exit:  # Adds Rocks if North Exit is False
                Rock(self, xpos_exit, 0, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, 0, self.rock_img)
            if not self.south_exit:  # Adds Rocks if South Exit is False
                Rock(self, xpos_exit, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)

            if self.in_town:
                Building(self, 25, 25, self.building1)
                Tree(self, WIN_WIDTH/2, WIN_HEIGHT/2 + 50, self.tree_image)
                Tree(self, WIN_WIDTH / 2, WIN_HEIGHT / 2 - 150, self.tree_image)
            else:
                for _ in range(random.randint(10, 20)):
                    Tree(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                         random.randint(BORDER_TILESIZE * 2,
                                        WIN_HEIGHT - (BORDER_TILESIZE * 2) - self.tree_image.get_height() / 2),
                         self.tree_image)
                    Rock(self, random.randint(BORDER_TILESIZE * 3, WIN_WIDTH - BORDER_TILESIZE * 3),
                         random.randint(BORDER_TILESIZE * 3, WIN_HEIGHT - BORDER_TILESIZE * 3), self.rock_img)
        else:
            for _ in range(5):
                randomYTop = random.randint(BORDER_TILESIZE, WIN_HEIGHT/2 - 75)
                randomYBottom = random.randint(WIN_HEIGHT / 2 + 75, WIN_HEIGHT - BORDER_TILESIZE * 2)
                Tree(self, random.randint(BORDER_TILESIZE, WIN_WIDTH - BORDER_TILESIZE * 3), random.randint(randomYTop, randomYBottom), self.tree_image)
                randomYTop = random.randint(BORDER_TILESIZE, WIN_HEIGHT / 2 - 75)
                randomYBottom = random.randint(WIN_HEIGHT / 2 + 75, WIN_HEIGHT - BORDER_TILESIZE * 2)
                Rock(self, random.randint(BORDER_TILESIZE, WIN_WIDTH - BORDER_TILESIZE * 3), random.randint(randomYTop, randomYBottom), self.rock_img)


    def GenerateEnemies(self, EnemyName):
        EnemyName = EnemyName
        EnemyList = self.game.EnemyList
        if self.player.isAttackable:
            for _ in range(self.enemy_count):
                RandChoice = random.choice(EnemyList)
                if RandChoice == 'Wolf':
                    Wolf(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                         random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2)))
        else:
            if EnemyName == 'Wolf':
                self.Monster1 = Wolf(self, WIN_WIDTH - BORDER_TILESIZE * 4, WIN_HEIGHT / 2)

    # Update everything on this level
    def update(self):
        self.enemy_sprites.update()
        self.background_sprites.update()
        self.UI_Sprites.update()
        self.combat_UI_Sprites.update()


        # Heal while in Town
        if self.in_town:
            if self.player.hp < self.player.max_hp:
                self.player.changeHealth(.025)

    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen
        self.player = self.game.player

        if not self.player.isAttackable:
            self.screen.blit(self.attackBackground, (0, 0))
            # self.combat_enemy_sprites.draw(self.screen)
            # self.combat_background_sprites.draw(self.screen)
            self.combat_enemy_sprites.draw(self.screen)
            self.combat_background_sprites.draw(self.screen)
            self.combat_UI_Sprites.draw(self.screen)

            self.screen.blit(self.game.enemyHPBarBG, (WIN_WIDTH/3, 10))
            self.screen.blit(self.game.enemyHPBar, (WIN_WIDTH/3, 10))
            # self.screen.blit(pygame.transform.scale(self.game.enemyHPBar, ((self.Monster1.hp/self.Monster1.max_hp*200), 50)), (WIN_WIDTH/3, 10))
            self.screen.blit(self.game.enemyHPBarFGSilver, (WIN_WIDTH, 10))
            self.screen.blit(self.Monster1.HPText, self.Monster1.HPBarTextRect)

            if self.player.canAttack:
                if button.Button(self.game, self.screen, WIN_WIDTH/2-97, WIN_HEIGHT/2, pygame.image.load(self.game.resource_path('assets/button_attack.png')), 195, 50).draw() and self.player.canAttack:
                    self.player.canAttack = False
                    # pygame.time.set_timer(self.CharacterAttackTimer, self.milliseconds_delay)
                    #self.player.Loot()
                    self.player.monsterToAttack = self.game.current_level.Monster1
                    self.player.canAttack = False
                    self.player.AttackMonster()
                if button.Button(self.game, self.screen, WIN_WIDTH / 2 - 97, WIN_HEIGHT / 2 + 60, pygame.image.load(self.game.resource_path('assets/button_flee.png')), 195, 50).draw():
                    self.player.Flee()
            self.player_sprite.draw(screen)
        else:
            # Draw the Background
            self.screen.blit(self.background, (0, 0))
            self.enemy_sprites.draw(self.screen)
            self.player_sprite.draw(screen)
            self.background_sprites.draw(self.screen)
            self.all_sprites.draw(screen)
            # self.enemy_sprites.draw(self.screen)
            # self.background_sprites.draw(self.screen)
        # Draw all the sprite lists we have
        # self.player_sprite.draw(self.screen)
        self.UI_Sprites.draw(self.screen)
        self.screen.blit(self.game.log_surf, (WIN_WIDTH / 2, WIN_HEIGHT))






        # print('--------------------------------------')
        # print('Player Layer:', self.game.player._layer)
        # print('--------------------------------------')


## LEVEL MAP ##
#
# [Town LEVEL]      [LEVEL 4]       [LEVEL 7]
#  [LEVEL 2]        [LEVEL 5]       [LEVEL 8]
#  [LEVEL 3]        [LEVEL 6]       [LEVEL 9]
#
#

class StartLevel(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = False
        self.east_exit = True
        self.in_town = True

        self.enemy_count = 1


class AttackScreen(Level):

    def __init__(self, game, player, ):
        Level.__init__(self, game, player)



class Level_02(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = False
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 2


class Level_03(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = False
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 3


class Level_04(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 2


class Level_05(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 4


class Level_06(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 5


class Level_07(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 5


class Level_08(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 6


class Level_09(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 7
