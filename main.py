import sys
import pygame
from config import *
from character import *
from terrain import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.characterList = []

        self.character_spritesheet = SpriteSheet('assets/CharacterSpritesheet.png')

    def createTilemap(self):
        tree_image = pygame.image.load('assets/tree.png')
        self.testTree = Tree(self, 400, 300, tree_image)

    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        # self.player_sprite = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.Group()
        # self.gear_sprites = pygame.sprite.LayeredUpdates()
        # self.background_sprites = pygame.sprite.LayeredUpdates()
        self.background_sprites = pygame.sprite.Group()
        # self.enemy_sprites = pygame.sprite.LayeredUpdates()
        # self.attack_sprites = pygame.sprite.LayeredUpdates()

        self.player = Character(self, 400, 400)

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(WIN_BG)
        self.all_sprites.draw(self.screen)

        # pygame.draw.rect(self.screen, BLACK, self.testTree.collision_rect)
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
