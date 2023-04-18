from terrain import *
import math
import random
from character import *


class Wolf(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        self.EnemyName = 'Wolf'

        self.x = x
        self.y = y
        self.width = 32
        self.height = 64

        self.x_change = 0
        self.y_change = 0

        self.facing = 'left'
        self.facing_list = ['down', 'up', 'right', 'left']
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10, 30)

        if self.game.player.isAttackable:
            self.inCombat = False
        else:
            self.inCombat = True

        self.image = self.game.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self._layer = self.rect.bottom

        if not self.inCombat:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.enemy_sprites)
        else:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_enemy_sprites)

        self.down_animations = [self.game.wolf_spritesheet.get_sprite(0, 128, self.width, self.height),
                                self.game.wolf_spritesheet.get_sprite(32, 128, self.width, self.height),
                                self.game.wolf_spritesheet.get_sprite(64, 128, self.width, self.height),
                                self.game.wolf_spritesheet.get_sprite(96, 128, self.width, self.height)]

        self.up_animations = [self.game.wolf_spritesheet.get_sprite(160, 132, self.width, self.height),
                              self.game.wolf_spritesheet.get_sprite(192, 132, self.width, self.height),
                              self.game.wolf_spritesheet.get_sprite(224, 132, self.width, self.height),
                              self.game.wolf_spritesheet.get_sprite(256, 132, self.width, self.height)]

        self.left_animations = [self.game.wolf_spritesheet.get_sprite(320, 288, 64, 32),
                                self.game.wolf_spritesheet.get_sprite(384, 288, 64, 32),
                                self.game.wolf_spritesheet.get_sprite(448, 288, 64, 32),
                                self.game.wolf_spritesheet.get_sprite(512, 288, 64, 32)]

        self.right_animations = [self.game.wolf_spritesheet.get_sprite(320, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(384, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(448, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(512, 96, 64, 32), ]

    def update(self):
        self.movement()
        self.animate()
        # self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_terrain('x')
        self.rect.y += self.y_change
        self.collide_terrain('y')

        self.x_change = 0
        self.y_change = 0

        if self.rect.x > WIN_WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > WIN_HEIGHT:
            self.kill()

    def movement(self):
        if not self.inCombat:
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(10, 30)
            if self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(10, 30)
            if self.facing == 'up':
                self.y_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(10, 30)
            if self.facing == 'down':
                self.y_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(10, 30)

        # self.game.all_sprites.change_layer(self, self.rect.bottom)

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.wolf_spritesheet.get_sprite(320, 288, 64, 32)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 0

    def collide_terrain(self, direction):

        if direction == 'x':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.rect, object.collision_rect)
                if collide:
                    if self.x_change > 0:  # Moving Right
                        self.rect.right = object.collision_rect.x
                        for _ in range(10):
                            self.rect.x -= 1
                        self.facing = 'left'
                        self.movement_loop = 0
                        self.max_travel = random.randint(10, 30)

                    if self.x_change < 0:  # Moving Left
                        self.rect.x = object.collision_rect.right
                        for _ in range(10):
                            self.rect.x += 1
                        self.facing = 'right'
                        self.movement_loop = 0
                        self.max_travel = random.randint(10, 30)

        if direction == 'y':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.rect, object.collision_rect)
                if collide:
                    if self.y_change > 0:  # Moving Down
                        self.rect.bottom = object.collision_rect.y
                        for _ in range(10):
                            self.rect.y -= 1
                        self.facing = 'up'
                        self.movement_loop = 0
                        self.max_travel = random.randint(10, 30)
                    if self.y_change < 0:  # Moving Up
                        self.rect.top = object.collision_rect.bottom
                        for _ in range(10):
                            self.rect.x += 1
                        self.facing = 'down'
                        self.movement_loop = 0
                        self.max_travel = random.randint(10, 30)
                    print('New Direction:', self.facing)

    def collide_enemy(self):
        pass
