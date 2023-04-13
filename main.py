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

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.Group()
        self.gear_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.player = Character(self, WIN_WIDTH / 2, WIN_HEIGHT / 2)

        self.level_list = []
        self.level_list.append(Level_01(self, self.player))
        self.level_list.append(Level_02(self, self.player))

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.level = self.current_level




    def createTilemap(self):
        tree_image = pygame.image.load('assets/tree.png')
        rock_img = pygame.image.load('assets/large_rock.png')
        for _ in range(int(WIN_WIDTH / BORDER_TILESIZE)):
            Tree(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                 random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2) - tree_image.get_height() / 2),
                 tree_image)
            Rock(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                 random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - BORDER_TILESIZE * 2), rock_img)

        # Horizontal Rock Walls
        tempwidthcount = 0
        tempheightcount = 0
        xpos = 0
        while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
            Rock(self, xpos, 0, rock_img)
            Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, rock_img)
            xpos += BORDER_TILESIZE
            tempwidthcount += 1
        # Gap in the Middle
        xpos_exit = xpos
        xpos = xpos + BORDER_TILESIZE * 2
        tempwidthcount = 0
        while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
            Rock(self, xpos, 0, rock_img)
            Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, rock_img)
            xpos += BORDER_TILESIZE
            tempwidthcount += 1

        # Vertical Rock Wall
        ypos = 0
        while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
            Rock(self, 0, ypos, rock_img)
            Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, rock_img)
            ypos += BORDER_TILESIZE
            tempheightcount += 1
        tempheightcount = 0
        ypos_exit = ypos
        # Gap in the Middle
        ypos = ypos + BORDER_TILESIZE * 2
        while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
            Rock(self, 0, ypos, rock_img)
            Rock(self, WIN_HEIGHT - BORDER_TILESIZE, ypos, rock_img)
            ypos += BORDER_TILESIZE
            tempheightcount += 1

        if True:  # Adds Rocks if East Exit is False
            Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit, rock_img)
            Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit + BORDER_TILESIZE, rock_img)
        if True:  # Adds Rocks if West Exit is False
            Rock(self, 0, ypos_exit, rock_img)
            Rock(self, 0, ypos_exit + BORDER_TILESIZE, rock_img)
        if True:  # Adds Rocks if North Exit is False
            Rock(self, xpos_exit, 0, rock_img)
            Rock(self, xpos_exit + BORDER_TILESIZE, 0, rock_img)
        if True:  # Adds Rocks if South Exit is False
            Rock(self, xpos_exit, WIN_HEIGHT - BORDER_TILESIZE, rock_img)
            Rock(self, xpos_exit + BORDER_TILESIZE, WIN_HEIGHT - BORDER_TILESIZE, rock_img)

    def new(self):

        self.playing = True
        #self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.current_level.update()

    def draw(self):
        # self.screen.fill(WIN_BG)
        # self.all_sprites.draw(self.screen)
        self.current_level.draw(self.screen)

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
