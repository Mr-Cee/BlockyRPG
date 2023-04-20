from character import *


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


