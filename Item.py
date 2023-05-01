import pygame


class Item:
    def __init__(self, game, id):
        self.game = game
        self.id = id

        self.surface = pygame.image.load('assets/ice-bolt.png')
        # if self.id == 1:
        self.image = pygame.image.load('assets/ice-bolt.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()


    def resize(self, size):
        return pygame.transform.scale(self.surface, (size, size))
