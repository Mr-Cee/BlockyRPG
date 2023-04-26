import pygame
from character import *

# button class
class Button():
    def __init__(self, game, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.game = game
        self.Combat_UI_Sprites = self.game.combat_UI_Sprites

        self._layer = WIN_HEIGHT + 100



    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))



        return action
