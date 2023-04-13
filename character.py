import pygame
import math
from config import *
from SpriteUtilities import *


class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        self.x = x
        self.y = y
        self.width = CHARACTER_TILESIZE
        self.height = CHARACTER_TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.collision_rect = pygame.Rect(self.x+5, self.y, self.width - 10, self.height / 4)

        self._layer = self.collision_rect.bottom

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.player_sprite)

        self.mask = pygame.mask.from_surface(self.image)

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height)]

        # self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
        #                       self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
        #                       self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]
        #
        # self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
        #                         self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
        #                         self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]
        #
        # self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
        #                          self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
        #                          self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collision_rect.x += self.x_change
        self.collide_terrain('x')
        self.rect.y += self.y_change
        self.collision_rect.y = self.rect.bottom-10
        self.collide_terrain('y')

        self.x_change = 0
        self.y_change = 0

        current_pos_x = self.rect.x
        current_pos_y = self.rect.y
        if current_pos_x > WIN_WIDTH:
            self.rect.x = BORDER_TILESIZE + 5
            self.game.current_level_no += 1
            self.game.current_level = self.game.level_list[self.game.current_level_no]
            self.game.level = self.game.current_level
            print("Moved East\nLevel:", self.game.current_level_no)


    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if any((keys[pygame.K_UP], keys[pygame.K_DOWN])):
            self.game.all_sprites.change_layer(self, self.collision_rect.bottom)

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_terrain(self, direction):

        if direction == 'x':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.collision_rect, object.collision_rect)
                if collide:
                    if self.x_change > 0: # Moving Right
                        self.rect.right = object.collision_rect.x+5
                        #self.rect.x = object.collision_rect.x - self.collision_rect.width
                        self.collision_rect.right = object.collision_rect.x
                        #self.collision_rect.x = object.collision_rect.x - self.collision_rect.width
                    if self.x_change < 0: # Moving Left
                        self.rect.x = object.collision_rect.right-5
                        self.collision_rect.x = object.collision_rect.right

        if direction == 'y':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.collision_rect, object.collision_rect)
                if collide:
                    if self.y_change > 0: # Moving Down
                        self.rect.bottom = object.collision_rect.y
                        self.collision_rect.y = self.rect.bottom-10
                    if self.y_change < 0: # Moving Up
                        self.rect.bottom = object.collision_rect.bottom+10
                        self.collision_rect.y = object.collision_rect.bottom

    def collide_enemy(self):
        pass
