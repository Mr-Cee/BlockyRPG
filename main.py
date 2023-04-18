import random
import sys
import pygame
from config import *
from character import *
from terrain import *
from Level import *
from UI import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.characterList = []

        self.font = pygame.font.Font('assets/BKANT.TTF', 10)

        self.character_spritesheet = SpriteSheet('assets/CharacterSpritesheet.png')
        self.BottomPanel_IMG = pygame.image.load('assets/BottomUI.png')
        self.hpbar_empty_img = pygame.image.load('assets/EmptyHPBar.png')
        self.hpbar_inside_img = pygame.image.load('assets/HPBarInside.png')

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.Group()
        self.gear_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.UI_Sprites = pygame.sprite.Group()

        self.player = Character(self, WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.font = pygame.font.Font('assets/BKANT.TTF', 9)

        self.current_level_no = 0
        self.level_list = []
        # self.level_list.append()
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
        self.current_level.GenerateEnemies()

        self.level = self.current_level



    def LevelChange(self, direction):
        self.leveldirection = direction

        if self.leveldirection == 'right':
            self.player.rect.x = BORDER_TILESIZE + 5
            self.player.collision_rect.x = self.player.rect.x + 5
            self.current_level_no += 3
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'left':
            self.player.rect.x = WIN_WIDTH - BORDER_TILESIZE - 5
            self.player.collision_rect.x = self.player.rect.x + 5
            self.current_level_no -= 3
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'down':
            self.player.rect.y = 0 + BORDER_TILESIZE + 5
            self.player.collision_rect.y = self.player.rect.bottom - 10
            self.current_level_no += 1
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level
        if self.leveldirection == 'up':
            self.player.rect.y = WIN_HEIGHT - BORDER_TILESIZE - 5
            self.player.collision_rect.y = self.player.rect.bottom - 10
            self.current_level_no -= 1
            self.current_level = self.level_list[self.current_level_no]
            self.level = self.current_level

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()

        self.current_level.GenerateEnemies()
        self.current_level.terrainGen()

    def DeathReset(self):
        self.player.hp = self.player.max_hp
        self.player.rect.x = WIN_WIDTH / 2
        self.player.rect.y = WIN_HEIGHT / 2
        self.player.collision_rect.x = self.player.rect.x + 5
        self.player.collision_rect.y = self.player.rect.bottom - 10
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.level = self.current_level

        for sprite in self.background_sprites:
            sprite.kill()
        if len(self.enemy_sprites) > 0:
            for sprite in self.enemy_sprites:
                sprite.kill()

        self.current_level.GenerateEnemies()
        self.current_level.terrainGen()

    def UIBuild(self):
        UIPanel(self, 0, WIN_HEIGHT, self.BottomPanel_IMG)  # Background Panel
        HUDMAIN(self, 10, WIN_HEIGHT + 10)  # HP/MP/XP HUD BARS
        self.RedHPBar = HPBarInterior(self, 193, WIN_HEIGHT + 22)  # HP RED BAR
        self.EXPYellowBar = pygame.image.load('assets/XPBarInside.png')

    # def scale_bar(self, pic, width):  ## Not Used Anymore
    #     size = pic.get_size()
    #     print(width)
    #     margin = 4
    #     middel_parat = pic.subsurface(pygame.Rect(margin, 0, size[0] - margin * 2, size[1]))
    #     scaled_image = pygame.Surface((width, size[1]))
    #     scaled_image.blit(pic, (0, 0), (0, 0, margin, size[1]))
    #     scaled_image.blit(pygame.transform.smoothscale(middel_parat, (width - margin * 2, size[1])), (margin, 0))
    #     scaled_image.blit(pic, (width - margin, 0), (size[0] - margin, 0, margin, size[1]))
    #
    #     return scaled_image

    def new(self):

        self.playing = True
        self.UIBuild()

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

    def update(self):
        self.all_sprites.update()
        self.current_level.update()

    def draw(self):
        self.current_level.draw(self.screen)
        self.screen.blit(self.player.LevelText, self.player.LevelTextRect)
        self.screen.blit(pygame.transform.scale(self.EXPYellowBar, (((self.player.exp / self.player.exp_to_level) * 164), 28)), (193, WIN_HEIGHT+109))
        self.screen.blit(self.player.HPText, self.player.HPBarTextRect)
        self.screen.blit(self.player.EXPText, self.player.EXPBarTextRect)

        # # Drawing Squares around objects for collisions
        # for object in self.background_sprites:
        #     pygame.draw.rect(self.screen, BLACK, object.collision_rect)
        # for object in self.enemy_sprites:
        #     pygame.draw.rect(self.screen, RED, object.rect)
        # pygame.draw.rect(self.screen, WHITE, self.player.collision_rect)

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
