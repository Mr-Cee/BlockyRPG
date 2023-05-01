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
from Inventory import *
from Item import *


class Game:
    def __init__(self):
        pygame.init()
        self.DEBUGMOD = 1
        self.DEBUGGING = False
        self.screen = pygame.display.set_mode((WIN_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.characterList = []
        self.showInventory = False

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

        items = [pygame.Surface((50, 50), pygame.SRCALPHA) for x in range(4)]
        pygame.draw.circle(items[0], (255, 0, 0), (25, 25), 25)
        pygame.draw.circle(items[1], (0, 255, 0), (25, 25), 25)
        pygame.draw.circle(items[2], (255, 255, 0), (25, 25), 25)
        pygame.draw.circle(items[3], (0, 0, 255), (25, 25), 25)


        self.Inventory = Inventory(self)
        self.InventorySelected = None
        self.InventoryClickable = True

        # print(self.Inventory.Add(Test))

        self.EnemyList = ['Wolf',
                          'Goblin',
                          'Red Imp',
                          'Gray Spider'
                          ]

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
        # for sprite in self.temp_Sprite_list:
        #     self.background_sprites.add(sprite)

        self.temp_Sprite_list.clear()
        self.all_sprites.update()
        self.current_level_no = self.previousLevel
        self.current_level = self.level_list[self.current_level_no]
        self.previousLevel = self.current_level_no
        self.level_list.pop(tempNum)
        self.player.rect.x, self.player.rect.y = self.player.previousPOS[0], self.player.previousPOS[1]
        self.player.collision_rect.x = self.player.rect.x + 22
        self.player.collision_rect.y = self.player.rect.bottom - 5

        self.current_level.terrainGen()

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
        self.player.mp = self.player.max_mp
        if self.player.exp > 0:
            self.player.exp = floor(self.player.exp * .9)

        if not self.player.isAttackable:
            self.RemoveAttackLevel()
            self.goToTown()
        else:
            self.current_level_no = 0
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
            self.goToTown()

        self.player.isAttackable = True
        self.player.AttackChoice = False
        self.player.canAttack = True

        self.player.rect.x = WIN_WIDTH / 2
        self.player.rect.y = WIN_HEIGHT / 2
        self.player.collision_rect.x = self.player.rect.x + 22
        self.player.collision_rect.y = self.player.rect.bottom - 5

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.combat_background_sprites) > 0:
            for sprite in self.combat_background_sprites:
                sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()
        if len(self.combat_enemy_sprites) > 0:
            for sprite in self.combat_enemy_sprites:
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

        HPBarInterior(self, 193, WIN_HEIGHT + 22)  # HP RED BAR
        MPBarInterior(self, 193, WIN_HEIGHT + 65)
        EXPBarInterior(self, 193, WIN_HEIGHT + 109)

        # Creates Inventory Screen
        self.inventoryIMG = pygame.image.load('assets/TestInventory.png')
        self.inventorySurface = pygame.Surface((500, 500))
        self.inventorySurface.blit(self.inventoryIMG, (0, 0, 500, 500))


    def console_print(self, message):
        # self.message_log.append(message)

        while message:
            i = 0
            while self.the_font.size(message[:i])[0] < (WIN_WIDTH/2-15) and i < len(message):
                i += 1
            if i < len(message):
                i = message.rfind(" ", 0, i) + 1

            self.message_log.insert(0, message[:i])
            message = message[i:]

    def update_log(self):
        # create a surface for the log:
        self.log_surf = pygame.Surface((WIN_WIDTH / 2, 160))
        self.log_surf.blit(self.textboxIMG, (0, 0, WIN_WIDTH / 2, 160))

        if len(self.message_log) > 0:
            new_log = []
            m = len(self.message_log)
            n = 0
            for _ in range(m):
                new_log.insert(0, self.message_log[n])
                n += 1
                if n == 7:
                    break

            font_y = 10
            for m in new_log:
                message = self.the_font.render(m, True, BLACK)
                self.log_surf.blit(message, (15, font_y))
                font_y += 20

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
        self.InventorySelected = None

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
            if event.type == pygame.MOUSEBUTTONUP:
                self.InventoryClickable = True
            if event.type == pygame.MOUSEBUTTONDOWN and self.InventoryClickable:
                self.InventoryClickable = False
                if self.showInventory:
                # If right-clicked, get a random item
                    if event.button == 3:
                        self.Inventory.Add(Item(self, 1), self.Inventory.Get_First_Empty())
                    elif event.button == 1:
                        pos = self.Inventory.Get_pos()
                        if self.Inventory.In_grid(pos[0], pos[1]):
                            if self.InventorySelected:
                                self.InventorySelected = self.Inventory.Add(self.InventorySelected, pos)
                                print("put down")
                            elif self.Inventory.items[pos[0]][pos[1]]:
                                print('pickup')
                                self.InventorySelected = self.Inventory.items[pos[0]][pos[1]]
                                self.Inventory.items[pos[0]][pos[1]] = None
                                # print(self.InventorySelected[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.showInventory = not self.showInventory
                    self.player.canAttack = not self.player.canAttack
                if event.key == pygame.K_KP_PLUS:
                    self.player.changeHealth(10)
                    self.player.changeMana(25)
                if event.key == pygame.K_KP_MINUS:
                    self.player.changeHealth(-10)
                    self.player.changeMana(-50)
                if event.key == pygame.K_t:
                    if self.player.isAttackable:
                        if self.current_level_no == 0:
                            self.console_print('Already in Town!')
                        else:
                            self.goToTown()
                    else:
                        self.console_print('Not while in combat')
                if event.key == pygame.K_d:
                    self.DEBUGGING = not self.DEBUGGING
                    self.DebugSettings()
            if event.type == self.EnemyAttackTimer:
                self.current_level.Monster1.AttackCharacter(self)
                pygame.time.set_timer(self.EnemyAttackTimer, 0)

    def update(self):

        # if self.showInventory:
        #     print(self.Inventory.Get_pos())

        self.all_sprites.update()
        self.current_level.update()
        self.update_log()

    def draw(self):
        if not self.player.isAttackable:
            self.screen.blit(WIN_Attack_BG, (0, 0))
        self.current_level.draw(self.screen)

        self.screen.blit(self.player.LevelText, self.player.LevelTextRect)

        self.screen.blit(self.player.HPText, self.player.HPBarTextRect)
        self.screen.blit(self.player.MPText, self.player.MPBarTextRect)
        self.screen.blit(self.player.EXPText, self.player.EXPBarTextRect)

        if self.showInventory:
            mousex, mousey = pygame.mouse.get_pos()
            self.screen.blit(self.inventorySurface, (((WIN_WIDTH-500)/2), ((WIN_HEIGHT-500)/2)))
            self.Inventory.draw()
            self.gear_sprites.draw(self.inventorySurface)
            if self.InventorySelected:
                self.screen.blit(self.InventorySelected.resize(40), (mousex, mousey))
                # obj = self.font.render(str(self.InventorySelected[1]), True, (0, 0, 0))
                # self.screen.blit(obj, (mousex + 15, mousey + 15))

        if self.DEBUGGING:
            self.screen.blit(self.DEBUGText, self.DEBUGTextRect)


        ################### Drawing Squares around objects for collisions ##################################
        #
        # for object in self.background_sprites:
        #     pygame.draw.rect(self.screen, BLACK, object.collision_rect)
        # for object in self.enemy_sprites:
        #     pygame.draw.rect(self.screen, RED, object.rect)
        # for sprite in self.combat_enemy_sprites:
        #     pygame.draw.rect(self.screen, RED, sprite.rect)
        # pygame.draw.rect(self.screen, WHITE, self.player.collision_rect)

        # # for object in self.background_sprites:
        # #     pygame.draw.rect(self.screen, BLACK, object.rect)
        # pygame.draw.rect(self.screen, WHITE, self.player.rect)
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
