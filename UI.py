from character import *
import pygame
from config import *


class UIPanel(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game
        self.player = self.game.player
        self.background = WIN_BG
        self.UI_Sprites = self.game.UI_Sprites
        self.all_sprites = self.game.all_sprites

        self.image = image
        self.image.set_colorkey(WHITE)

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # self.rect = self.image.get_rect()
        self.rect = (self.x, self.y, self.width, self.height)
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)

    def update(self):
        # self.game.hpbar_inside_img = pygame.transform.scale(self.game.hpbar_inside_img, (round((self.player.hp / self.player.max_hp) * 164, 2), 14))
        pass

    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen

        # Draw the Background
        self.screen.fill(self.background)

        # Draw all the sprite lists we have
        self.UI_Sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)


class HPBarInterior(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/HPBarInside.png')

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.HPText = str(self.player.hp)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)

    def update(self):
        self.image = pygame.transform.scale(self.image, (round((self.player.hp / self.player.max_hp) * 164, 2), 28))


class MPBarInterior(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/MPBarInside.png')

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)


        # self.MPText = str(self.player.mp)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)

    def update(self):
        self.image = pygame.transform.scale(self.image, (round((self.player.mp / self.player.max_mp) * 164, 2), 28))


class EnemyHPBarBG(pygame.sprite.Sprite):
    def __init__(self, game, Enemy, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player
        self.Enemy = Enemy

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/enemy_health_bar_background.png')

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        print('BG Width:', self.width)
        print('BG Height:', self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.HPText = str(self.player.hp)

        self._layer = GAME_HEIGHT + 99

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_UI_Sprites)


class EnemyHPBarFG(pygame.sprite.Sprite):
    def __init__(self, game, Enemy, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player
        self.Enemy = Enemy

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/enemy_health_bar_foreground_silver.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (247, 32))
        self.image.set_colorkey(BLACK)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = WIN_WIDTH / 2, 25

        self.HPText = str(self.player.hp)

        self._layer = GAME_HEIGHT

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_UI_Sprites)


class EnemyHPBarInterior(pygame.sprite.Sprite):
    def __init__(self, game, Enemy, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player
        self.Enemy = Enemy

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/enemy_health_bar.png')

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = WIN_WIDTH/2, 25
        # self.rect.x = self.x
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.HPText = str(self.player.hp)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_UI_Sprites)

    def update(self):
        try:
            if self.Enemy.hp > 0:
                ratio = (round((self.game.current_level.Monster1.hp / self.game.current_level.Monster1.max_hp) * (WIN_WIDTH / 3 - 35), 2))
                if ratio > 0:
                    self.image = pygame.transform.scale(self.image, (ratio, 19))
                else:
                    self.image = pygame.transform.scale(self.image, (0, 19))

            else:
                self.kill()
        except AttributeError:
            pass


class EXPBarInterior(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.screen = self.game.screen
        self.player = self.game.player
        self.UI_Sprites = self.game.UI_Sprites
        self.all_sprites = self.game.all_sprites

        self.image = pygame.image.load('assets/XPBarInside.png')

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.HPText = str(self.player.hp)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)

    # def update(self):
    #     self.image = pygame.transform.scale(self.image, (((self.player.exp / self.player.exp_to_level) * 164), 28))

    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen

        # Draw all the sprite lists we have
        self.UI_Sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)


class HUDMAIN(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.player = self.game.player

        self.x = x
        self.y = y
        self.width = 364
        self.height = 140

        self.image = pygame.image.load('assets/HUDMAIN.png').convert()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)
