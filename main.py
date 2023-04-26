import logging
import os
import random
import sys
from math import floor

import pygame
from config import *
from character import *
from terrain import *
from Enemy import *
from Level import *
from UI import *


class Game:
    def __init__(self):
        pygame.init()
        self.DEBUGMOD = 1
        self.DEBUGGING = False
        self.screen = pygame.display.set_mode((WIN_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.characterList = []

        self.font = pygame.font.Font(self.resource_path('assets/BKANT.TTF'), 10)

        self.character_spritesheet = SpriteSheet('assets/CharacterWalkingSpritesheet.png')
        self.WeaponsAndMagicSpritesheet = SpriteSheet('assets/Weapons&Magic.png')

        # self.BottomPanel_IMG = pygame.image.load('assets/BottomUI.png')
        self.BottomPanel_IMG = pygame.image.load(self.resource_path('assets/BottomUI.png'))
        self.hpbar_empty_img = pygame.image.load(self.resource_path('assets/EmptyHPBar.png'))
        self.hpbar_inside_img = pygame.image.load(self.resource_path('assets/HPBarInside.png'))
        self.textboxIMG = pygame.image.load(self.resource_path('assets/textbox.png'))
        self.textboxIMG = pygame.transform.scale(self.textboxIMG, (WIN_WIDTH / 2, 160))

        self.font = pygame.font.Font('assets/BKANT.TTF', 15)
        self.DEBUGText = 'DEBUGGING/TESTING'
        self.DEBUGText = self.font.render(str(self.DEBUGText), True, RED, None)
        self.DEBUGTextRect = self.DEBUGText.get_rect()
        self.DEBUGTextRect.topright = (WIN_WIDTH - 10, 5)

        self.enemyHPBar = pygame.image.load(self.resource_path('assets/enemy_health_bar.png'))
        self.enemyHPBar = pygame.transform.scale(self.enemyHPBar, (WIN_WIDTH / 3, 50))
        self.enemyHPBarBG = pygame.image.load(self.resource_path('assets/enemy_health_bar_background.png'))
        self.enemyHPBarBG = pygame.transform.scale(self.enemyHPBarBG, (WIN_WIDTH / 3, 50))
        self.enemyHPBarFGGold = pygame.image.load(self.resource_path('assets/enemy_health_bar_foreground_gold.png'))
        self.enemyHPBarFGGold = pygame.transform.scale(self.enemyHPBarFGGold, (WIN_WIDTH / 3, 50))
        self.enemyHPBarFGSilver = pygame.image.load(self.resource_path('assets/enemy_health_bar_foreground_silver.png'))
        self.enemyHPBarFGSilver = pygame.transform.scale(self.enemyHPBarFGSilver, (WIN_WIDTH / 3, 50))

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.Group()
        self.gear_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.combat_enemy_sprites = pygame.sprite.Group()
        self.combat_background_sprites = pygame.sprite.Group()
        self.combat_attack_sprites = pygame.sprite.Group()
        self.combat_UI_Sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.UI_Sprites = pygame.sprite.Group()
        self.temp_Sprite_list = []

        self.player = Character(self, WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.font = pygame.font.Font(self.resource_path('assets/BKANT.TTF'), 9)

        self.EnemyList = ['Wolf',
                          'Goblin']

        self.milliseconds_delay = 2000  # 1 seconds
        self.CharacterAttackTimer = pygame.USEREVENT + 1
        self.EnemyAttackTimer = pygame.USEREVENT + 2
        self.previousLevel = 0

        self.current_level_no = 0
        self.level_list = []
        # self.level_list.append(AttackScreen(self, self.player))
        self.level_list.append(StartLevel(self, self.player))
        self.level_list.append(Level_02(self, self.player))
        self.level_list.append(Level_03(self, self.player))
        self.level_list.append(Level_04(self, self.player))
        self.level_list.append(Level_05(self, self.player))
        self.level_list.append(Level_06(self, self.player))
        self.level_list.append(Level_07(self, self.player))
        self.level_list.append(Level_08(self, self.player))
        self.level_list.append(Level_09(self, self.player))
        self.current_level = self.level_list[self.current_level_no]
        self.current_level.terrainGen()
        self.current_level.GenerateEnemies(None)

        # Set up logging
        log = "bot.log"
        logging.basicConfig(filename=log, level=logging.DEBUG, format='%(asctime)s %(message)s', filemode='a',
                            datefmt='%d/%m/%Y %H:%M:%S')

        self.the_font = pygame.font.Font(None, 20)

        self.message_log = []

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def AttackLevelChange(self, EnemyName):
        tempNum = len(self.level_list)
        self.previousLevel = self.current_level_no
        self.level_list.insert(tempNum, (AttackScreen(self, self.player)))
        self.current_level_no = tempNum
        self.current_level = self.level_list[tempNum]
        self.level = self.current_level
        for sprite in self.background_sprites:
            self.temp_Sprite_list.append(sprite)
            sprite.kill()
        self.current_level.terrainGen()
        self.current_level.GenerateEnemies(EnemyName)

    def RemoveAttackLevel(self):
        tempNum = len(self.level_list) - 1
        for sprite in self.combat_background_sprites:
            sprite.kill()
        for sprite in self.combat_UI_Sprites:
            sprite.kill()
        if len(self.combat_enemy_sprites) > 0:
            for sprite in self.combat_enemy_sprites:
                sprite.kill()
        for sprite in self.temp_Sprite_list:
            self.background_sprites.add(sprite)

        self.temp_Sprite_list.clear()
        self.all_sprites.update()
        self.current_level_no = self.previousLevel
        self.current_level = self.level_list[self.current_level_no]
        self.previousLevel = self.current_level_no
        self.level_list.pop(tempNum)
        self.player.collision_rect.x = self.player.rect.x + 22
        self.player.collision_rect.y = self.player.rect.bottom - 5

    def LevelChange(self, direction):
        self.leveldirection = direction

        if self.leveldirection == 'right':
            self.player.rect.x = 1
            self.player.collision_rect.x = self.player.rect.x + 22
            self.current_level_no += 3
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'left':
            self.player.rect.x = WIN_WIDTH - BORDER_TILESIZE - 10
            self.player.collision_rect.x = self.player.rect.x + 22
            self.current_level_no -= 3
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'down':
            self.player.rect.y = 5
            self.player.collision_rect.y = self.player.rect.bottom - 5
            self.current_level_no += 1
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'up':
            self.player.rect.bottom = WIN_HEIGHT - 10
            self.player.collision_rect.y = self.player.rect.bottom - 5
            self.current_level_no -= 1
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()

        self.current_level.GenerateEnemies(None)
        self.current_level.terrainGen()

        if self.current_level_no == 0:
            self.console_print('You are in town')

        # logging.info('------------------------------------')
        # logging.info(str(self.current_level))
        # for i in range(len(self.all_sprites)):
        #     logging.info(('Layer:', self.all_sprites.get_layer_of_sprite(self.all_sprites.get_sprite(i)), 'Sprite:',
        #                   self.all_sprites.get_sprite(i), self.all_sprites.get_sprite(i).collision_rect))
        # logging.info('------------------------------------')

    def goToTown(self):
        self.player.rect.x = WIN_WIDTH / 2
        self.player.rect.y = WIN_HEIGHT / 2
        self.player.collision_rect.x = self.player.rect.x + 22
        self.player.collision_rect.y = self.player.rect.bottom - 5
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.level = self.current_level

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()

        self.current_level.GenerateEnemies(None)
        self.current_level.terrainGen()

        self.console_print('You are in town')

    def DeathReset(self):
        self.player.hp = self.player.max_hp
        if self.player.exp > 0:
            self.player.exp = floor(self.player.exp * .9)

        self.player.rect.x = WIN_WIDTH / 2
        self.player.rect.y = WIN_HEIGHT / 2
        self.player.collision_rect.x = self.player.rect.x + 22
        self.player.collision_rect.y = self.player.rect.bottom - 5

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.level = self.current_level

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()

        self.current_level.GenerateEnemies(None)
        self.current_level.terrainGen()

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.player.EXPBarText = str(self.player.exp) + "/" + str(self.player.exp_to_level)
        self.player.EXPText = self.font.render(str(self.player.EXPBarText), True, BLACK, None)

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.player.HPBarText = str(round(self.player.hp)) + "/" + str(round(self.player.max_hp))
        self.player.HPText = self.font.render(str(self.player.HPBarText), True, BLACK, None)

    def UIBuild(self):
        UIPanel(self, 0, WIN_HEIGHT, self.BottomPanel_IMG)  # Background Panel
        HUDMAIN(self, 10, WIN_HEIGHT + 10)  # HP/MP/XP HUD BARS

        self.RedHPBar = HPBarInterior(self, 193, WIN_HEIGHT + 22)  # HP RED BAR
        MPBarInterior(self, 193, WIN_HEIGHT + 65)
        self.EXPYellowBar = pygame.image.load(self.resource_path('assets/XPBarInside.png'))
        # EnemyHPBarBG(self, WIN_WIDTH / 2, 10, self.enemyHPBarBG)
        # EnemyHPBar(self, WIN_WIDTH / 2, 10, self.enemyHPBar)
        # EnemyHPBarFG(self, WIN_WIDTH / 2, 10, self.enemyHPBarFGSilver)

    def console_print(self, message):
        self.message_log.append(message)

    def update_log(self):
        # create a surface for the log:
        # This one the same width as the RESOLUTION and 1/3 the height
        self.log_surf = pygame.Surface((WIN_WIDTH / 2, 160))
        self.log_surf.blit(self.textboxIMG, (0, 0, WIN_WIDTH / 2, 160))
        # Populate it with, say, the last three messages:
        # Note: You could do this in a more elegant loop if you wanted to.
        #       You would probably be served by checking to see if you have any messages at all before
        #       searching through the message log, to avoid looking for elements that aren't in the list.
        #       for this example I added 3 placeholder messages at the start of the main function
        #       to avoid that problem here.
        if len(self.message_log) > 0:
            new_log = []
            m1 = self.message_log[-1]
            m2 = self.message_log[-2]
            m3 = self.message_log[-3]
            m4 = self.message_log[-4]
            m5 = self.message_log[-5]
            m6 = self.message_log[-6]
            new_log.append(m1)
            new_log.append(m2)
            new_log.append(m3)
            new_log.append(m4)
            new_log.append(m5)
            new_log.append(m6)
            font_y = 10
            for m in new_log:
                message = self.the_font.render(m, True, BLACK)
                self.log_surf.blit(message, (15, font_y))
                font_y += 20  # gives a little padding for the next message
        # blit it to the main surface in a spot where it'll fit snugly:
        # sorry for the magic numbers, ideally you would pre-define these positions
        # as variables

        self.screen.blit(self.log_surf, (WIN_WIDTH / 2, WIN_HEIGHT))

    def new(self):

        self.playing = True
        self.UIBuild()
        self.console_print('')
        self.console_print('')
        self.console_print('')
        self.console_print('')
        self.console_print('')
        self.console_print('')

    def DebugSettings(self):
        if self.DEBUGGING:
            self.DEBUGMOD = 100
            self.player.max_hp = 100 * self.DEBUGMOD
            self.player.hp = self.player.max_hp
            self.player.CharacterStrength = self.player.playerLevel * 5 * self.DEBUGMOD
        else:
            self.DEBUGMOD = 1
            self.player.max_hp = self.player.playerLevel * 20 + 80
            self.player.hp = self.player.max_hp
            self.player.CharacterStrength = 5 * self.player.playerLevel

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.player.HPBarText = str(self.player.hp) + "/" + str(self.player.max_hp)
        self.player.HPText = self.font.render(str(self.player.HPBarText), True, BLACK, None)
        self.player.HPBarTextRect = self.player.HPText.get_rect()
        self.player.HPBarTextRect.center = (275, WIN_HEIGHT + 36)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.exp += 1
                if event.key == pygame.K_b:
                    self.player.exp -= 1
                if event.key == pygame.K_KP_PLUS:
                    self.player.changeHealth(10)
                if event.key == pygame.K_KP_MINUS:
                    self.player.changeHealth(-10)
                if event.key == pygame.K_t:
                    self.goToTown()
                if event.key == pygame.K_d:
                    self.DEBUGGING = not self.DEBUGGING
                    self.DebugSettings()

            # if event.type == self.CharacterAttackTimer:
            #     self.player.canAttack = True
            if event.type == self.EnemyAttackTimer:
                self.current_level.Monster1.AttackCharacter(self)
                pygame.time.set_timer(self.EnemyAttackTimer, 0)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if self.player.AttackChoice:
            #         self.player.Loot()

    def update(self):
        self.all_sprites.update()
        self.current_level.update()
        self.update_log()

    def draw(self):
        if not self.player.isAttackable:
            self.screen.blit(WIN_Attack_BG, (0, 0))

            # self.screen.blit(self.enemyHPBarBG, (WIN_HEIGHT/3, 10))
            # self.screen.blit(self.enemyHPBar, (WIN_HEIGHT / 3, 10))
            # self.screen.blit(self.enemyHPBarFGSilver, (WIN_HEIGHT / 3, 10))

        self.current_level.draw(self.screen)

        self.screen.blit(self.player.LevelText, self.player.LevelTextRect)
        self.screen.blit(
            pygame.transform.scale(self.EXPYellowBar, (((self.player.exp / self.player.exp_to_level) * 164), 28)),
            (193, WIN_HEIGHT + 109))
        self.screen.blit(self.player.HPText, self.player.HPBarTextRect)
        self.screen.blit(self.player.MPText, self.player.MPBarTextRect)
        self.screen.blit(self.player.EXPText, self.player.EXPBarTextRect)
        if self.DEBUGGING:
            self.screen.blit(self.DEBUGText, self.DEBUGTextRect)
        ################### Drawing Squares around objects for collisions ##################################
        #
        # for object in self.background_sprites:
        #     pygame.draw.rect(self.screen, BLACK, object.collision_rect)
        # for object in self.enemy_sprites:
        #     pygame.draw.rect(self.screen, RED, object.rect)
        # pygame.draw.rect(self.screen, WHITE, self.player.collision_rect)
        #
        # # for object in self.background_sprites:
        # #     pygame.draw.rect(self.screen, BLACK, object.rect)
        # # pygame.draw.rect(self.screen, WHITE, self.player.rect)
        #
        # for sprite in self.combat_attack_sprites:
        #     pygame.draw.rect(self.screen, BLUE, sprite.rect)

        ###################################################################################################
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):

        # Main Game Loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over_screen(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over_screen()

pygame.quit()
sys.exit()
