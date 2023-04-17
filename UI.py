from SpriteUtilities import *
from config import *

class UIPanel(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game
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

        self._layer = GAME_HEIGHT + 100

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.UI_Sprites)

    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen

        # Draw the Background
        self.screen.fill(self.background)

        # Draw all the sprite lists we have
        self.UI_Sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)

