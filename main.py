import random
import sys
import pygame
from config import *
from character import *
from terrain import *
from Level import *


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
        rock_img = pygame.image.load('assets/large_rock.png')
        for _ in range(10):
            Tree(self, random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), tree_image)
        Rock(self, 400, 400, rock_img)

    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.Group()
        self.gear_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.player = Character(self, WIN_WIDTH / 2, WIN_HEIGHT / 2)

        self.createTilemap()

        self.level_list = []
        # self.level_list.append()

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

        # # Drawing Squares around objects for collisions
        # for object in self.background_sprites:
        #     pygame.draw.rect(self.screen, BLACK, object.collision_rect)
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
