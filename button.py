import pygame
from character import *

# button class
class Button():
    def __init__(self, game, surface, x, y, image, size_x, size_y, text, text2, text3):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.game = game
        self.text = text
        self.text2 = text2
        self.text3 = text3


        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.Text = self.text
        self.TextTip = self.font.render(str(self.Text), True, BLACK, None)
        self.TextRect = self.TextTip.get_rect()

        self.font = pygame.font.Font('assets/BKANT.TTF', 15)
        self.Text2 = self.text2
        self.TextTip2 = self.font.render(str(self.Text2), True, BLACK, None)
        self.TextRect2 = self.TextTip2.get_rect()

        self.Text3 = self.text3
        self.TextTip3 = self.font.render(str(self.Text3), True, BLACK, None)
        self.TextRect3 = self.TextTip3.get_rect()





    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        # print(pos)



        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.TextRect.centerx = pos[0]
            self.TextRect.bottom = pos[1]-50
            self.TextRect2.centerx = pos[0]
            self.TextRect2.bottom = pos[1] - 35
            self.TextRect3.centerx = pos[0]
            self.TextRect3.bottom = pos[1] - 16
            pygame.draw.rect(self.surface, SOFTBROWN, self.TextRect, border_radius=3)
            pygame.draw.rect(self.surface, SOFTBROWN, self.TextRect2, border_radius=3)
            pygame.draw.rect(self.surface, SOFTBROWN, self.TextRect3, border_radius=3)

            self.surface.blit(self.TextTip, self.TextRect)
            self.surface.blit(self.TextTip2, self.TextRect2)
            self.surface.blit(self.TextTip3, self.TextRect3)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        return action
