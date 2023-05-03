import pygame

from terrain import *
import math
import random
from character import *
from SpriteUtilities import *


class EnemyTemplate(pygame.sprite.Sprite):
    def __init__(self, game, x, y, AttackStrength, Health, EXPGain):
        self.game = game

        self.EnemyName = 'ChangeMe'

        self.x = x
        self.y = y
        self.width = 64
        self.height = 64

        self.max_hp = Health
        self.hp = self.max_hp
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.HPBarText = str(self.hp) + "/" + str(self.max_hp)
        self.HPText = self.font.render(str(self.HPBarText), True, BLACK, None)
        self.HPBarTextRect = self.HPText.get_rect()
        self.HPBarTextRect.center = (WIN_WIDTH / 2, 25)

        self.EXPGive = EXPGain

        self.attackPower = AttackStrength

        self.x_change = 0
        self.y_change = 0
        self.isFrozen = False
        self.frozenCount = 0

        self.facing = 'left'
        self.facing_list = ['down', 'up', 'right', 'left']
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 25
        self.collision_count = 0

        if self.game.player.isAttackable:
            self.inCombat = False
        else:
            self.inCombat = True

        self.AttackingMovement = False

        self.milliseconds_delay = 2000  # 1 seconds
        self.CharacterAttackTimer = pygame.USEREVENT + 1
        self.EnemyAttackTimer = pygame.USEREVENT + 2

        self.goblin_walking_spritesheet = SpriteSheet('assets/goblin.png')
        self.goblin_attack_spritesheet = SpriteSheet('assets/goblinsword.png')
        self.image = self.game.goblin_walking_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(self.rect.center)
        self.rect.x = self.x
        self.rect.y = self.y

        self.collision_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self._layer = self.rect.bottom

        if not self.inCombat:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.enemy_sprites)
        else:
            pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_enemy_sprites)

        self.down_animations = []

        self.right_animations = []
        self.up_animations = []
        self.left_animations = []
        self.left_attack_animations = []
        self.death_animations = []

        self.AttackPlayerAnim = False
        self.attack_anim_done = True
        self.DeathAnimation = False

    def update(self):
        self.movement()
        self.animate()
        # self.collide_enemy()

        self.rect.x += self.x_change
        self.collision_rect.x += self.x
        self.collide_terrain('x')
        self.rect.y += self.y_change
        self.collision_rect.y += self.y
        self.collide_terrain('y')

        self.x_change = 0
        self.y_change = 0

        if self.rect.x > WIN_WIDTH or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > WIN_HEIGHT:
            self.kill()

        # if self.inCombat and self.attack_anim_done == False:
        #     self.game.player.canAttack = True
        #     self.attack_anim_done = True

    def movement(self):
        if not self.inCombat:
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)

            if self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)

            if self.facing == 'up':
                self.y_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)

            if self.facing == 'down':
                self.y_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = random.choice(self.facing_list)
                    self.movement_loop = 0
                    self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)

        else:
            self.facing = 'left'
            if self.AttackingMovement:
                if self.rect.left - self.game.player.rect.right >= 15:
                    dx, dy = (self.game.player.rect.x - self.rect.right), (self.game.player.rect.y - self.rect.y)
                    rads = math.atan2(dy, dx)
                    self.player_direction = rads
                    if self.isFrozen:
                        self.x_change += math.cos(self.player_direction) * 2
                        self.y_change += math.sin(self.player_direction) * 2
                    else:
                        self.x_change += math.cos(self.player_direction) * 5
                        self.y_change += math.sin(self.player_direction) * 5
                    # self.x_change -= ENEMY_SPEED * 5
                    self.movement_loop -= 5
                    # print(self.movement_loop, -self.max_travel, (self.rect.left - self.game.player.rect.right))
                    if self.movement_loop <= -self.max_travel or (self.rect.left - self.game.player.rect.right <= 15):
                        self.AttackingMovement = False
                        self.movement_loop = 0
                        self.game.player.canAttack = True
                    # if self.rect.left - self.game.player.rect.right <= 15:
                else:
                    # print('True?')
                    self.AttackingMovement = False
                    self.movement_loop = 0
                    self.game.player.canAttack = True

        # self.game.all_sprites.change_layer(self, self.rect.bottom)

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.down_animations) / FPS
                if self.animation_loop >= len(self.down_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.up_animations) / FPS
                if self.animation_loop >= len(self.up_animations) - 1:
                    self.animation_loop = 0
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                if not self.inCombat:
                    self.image = self.left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += len(self.left_animations) / FPS
                    if self.animation_loop >= len(self.left_animations) - 1:
                        self.animation_loop = 0
                else:
                    self.image = self.left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += len(self.left_animations) / FPS
                    if self.animation_loop >= len(self.left_animations) - 1:
                        self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += len(self.right_animations) / FPS
                if self.animation_loop >= len(self.right_animations) - 1:
                    self.animation_loop = 0

        if self.AttackPlayerAnim:
            self.image = self.left_attack_animations[math.floor(self.animation_loop)]
            self.animation_loop += len(self.left_attack_animations) / FPS
            if self.animation_loop >= len(self.left_attack_animations) - 1:
                self.animation_loop = 0
                self.AttackPlayerAnim = False
                self.attack_anim_done = True
                self.game.player.canAttack = True

        if self.DeathAnimation:
            self.image = self.death_animations[math.floor(self.animation_loop)]
            self.animation_loop += len(self.death_animations) / FPS
            if self.animation_loop >= len(self.death_animations) - 1:
                self.animation_loop = 0
                self.DeathAnimation = False
                self.game.player.Loot(self.EXPGive, self)
                self.kill()

    def collide_terrain(self, direction):

        if direction == 'x':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.rect, object.collision_rect)
                if collide:
                    self.collision_count += 1
                    if self.x_change > 0:  # Moving Right
                        self.rect.right = object.collision_rect.x
                        # for _ in range(10):
                        #     self.rect.x -= 1
                        self.facing = 'left'
                        self.movement_loop = 0
                        self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)
                        if self.collision_count >= 3:
                            self.collision_count = 0
                            self.facing = 'up'
                            self.movement_loop = 0
                            self.max_travel = random.randint(WIN_WIDTH / 10, WIN_WIDTH / 8)

                    if self.x_change < 0:  # Moving Left
                        self.rect.x = object.collision_rect.right
                        # for _ in range(10):
                        #     self.rect.x += 1
                        self.facing = 'right'
                        self.movement_loop = 0
                        self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)
                        if self.collision_count >= 3:
                            self.collision_count = 0
                            self.facing = 'down'
                            self.movement_loop = 0
                            self.max_travel = random.randint(WIN_WIDTH / 10, WIN_WIDTH / 8)

        if direction == 'y':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.rect, object.collision_rect)
                if collide:
                    self.collision_count += 1
                    if self.y_change > 0:  # Moving Down
                        self.rect.bottom = object.collision_rect.y
                        # for _ in range(10):
                        #     self.rect.y -= 1
                        self.facing = 'up'
                        self.movement_loop = 0
                        self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)
                        if self.collision_count >= 3:
                            self.collision_count = 0
                            self.facing = 'right'
                            self.movement_loop = 0
                            self.max_travel = random.randint(WIN_WIDTH / 10, WIN_WIDTH / 8)
                    if self.y_change < 0:  # Moving Up
                        self.rect.top = object.collision_rect.bottom
                        # for _ in range(10):
                        #     self.rect.x += 1
                        self.facing = 'down'
                        self.movement_loop = 0
                        self.max_travel = random.randint(WIN_WIDTH/10, WIN_WIDTH/8)
                        if self.collision_count >= 3:
                            self.collision_count = 0
                            self.facing = 'left'
                            self.movement_loop = 0
                            self.max_travel = random.randint(WIN_WIDTH / 10, WIN_WIDTH / 8)

    def collide_enemy(self):
        pass

    def AttackCharacter(self, game):
        game = game
        MonsterAttack = random.randint(1 + int(self.attackPower), 5 + int(self.attackPower))
        MonsterAttack = MonsterAttack - self.game.player.CharacterArmor
        if MonsterAttack < 0:
            MonsterAttack = 0
        if self.rect.left - self.game.player.rect.right > 15:
            game.console_print((self.EnemyName + ' advances towards you.'))
            if self.isFrozen:
                self.max_travel = random.randint(math.floor(WIN_WIDTH / 7), math.floor(WIN_WIDTH / 6))
                self.frozenCount += 1
                if self.frozenCount == 3:
                    self.isFrozen = False
            else:
                self.max_travel = random.randint(WIN_WIDTH / 5, WIN_WIDTH / 4)
            self.movement_loop = 0
            self.AttackingMovement = True
        else:
            self.AttackPlayerAnim = True
            self.attack_anim_done = False
            game.console_print((self.EnemyName + ' attack you for ' + str(MonsterAttack) + ' damage'))
            self.game.player.changeHealth(-MonsterAttack)
            self.game.player.checkForDeath()
            self.CheckForDeath()
            # self.game.player.canAttack = True
            # pygame.time.set_timer(self.game.CharacterAttackTimer, self.game.milliseconds_delay)

    def CheckForDeath(self):
        if self.hp <= 0:
            self.hp = 0
            self.font = pygame.font.Font('assets/BKANT.TTF', 20)
            self.HPBarText = str(self.hp) + "/" + str(self.max_hp)
            self.HPText = self.font.render(str(self.HPBarText), True, BLACK, None)
            self.HPBarTextRect = self.HPText.get_rect()
            self.HPBarTextRect.center = (WIN_WIDTH / 2, 25)
            self.animation_loop = 0
            self.DeathAnimation = True
            # self.game.player.Loot(self.EXPGive, self)
            # self.kill()

    def TakeDamage(self, damage):
        if self.hp - damage > 0:
            self.hp -= damage
        else:
            self.hp = 0

class Goblin(EnemyTemplate):
    def __init__(self, game, x, y, AttackStrength, Health, EXPGain):
        EnemyTemplate.__init__(self, game, x, y, AttackStrength, Health, EXPGain)
        self.EnemyName = 'Goblin'

        self.width = 64
        self.height = 64

        self.goblin_walking_spritesheet = SpriteSheet('assets/goblin.png')
        self.goblin_attack_spritesheet = SpriteSheet('assets/goblinsword.png')

        self.image = self.game.goblin_walking_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.down_animations = [self.goblin_walking_spritesheet.get_sprite(0, 0, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(64, 0, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(128, 0, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(192, 0, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(256, 0, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(320, 0, self.width, self.height)
                                ]
        self.right_animations = [self.goblin_walking_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(128, 64, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(192, 64, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(256, 64, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(320, 64, self.width, self.height)
                                 ]

        self.up_animations = [self.goblin_walking_spritesheet.get_sprite(0, 128, self.width, self.height),
                              self.goblin_walking_spritesheet.get_sprite(64, 128, self.width, self.height),
                              self.goblin_walking_spritesheet.get_sprite(128, 128, self.width, self.height),
                              self.goblin_walking_spritesheet.get_sprite(192, 128, self.width, self.height),
                              self.goblin_walking_spritesheet.get_sprite(256, 128, self.width, self.height),
                              self.goblin_walking_spritesheet.get_sprite(320, 128, self.width, self.height)
                              ]

        self.left_animations = [self.goblin_walking_spritesheet.get_sprite(0, 192, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(64, 192, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(128, 192, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(192, 192, self.width, self.height),
                                self.goblin_walking_spritesheet.get_sprite(256, 192, self.width, self.height),
                                self.game.goblin_walking_spritesheet.get_sprite(320, 192, self.width, self.height)
                                ]
        self.left_attack_animations = [self.goblin_attack_spritesheet.get_sprite(384, 192, self.width, self.height),
                                       self.goblin_attack_spritesheet.get_sprite(448, 192, self.width, self.height),
                                       self.goblin_attack_spritesheet.get_sprite(512, 192, self.width, self.height),
                                       self.goblin_attack_spritesheet.get_sprite(576, 192, self.width, self.height),
                                       self.goblin_attack_spritesheet.get_sprite(640, 192, self.width, self.height)
                                       ]

        self.death_animations = [self.goblin_walking_spritesheet.get_sprite(0, 256, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(64, 256, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(128, 256, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(192, 256, self.width, self.height),
                                 self.goblin_walking_spritesheet.get_sprite(256, 256, self.width, self.height)
                                 ]


class Red_Imp(EnemyTemplate):
    def __init__(self, game, x, y, AttackStrength, Health, EXPGain):
        EnemyTemplate.__init__(self, game, x, y, AttackStrength, Health, EXPGain)
        self.EnemyName = 'Red Imp'

        self.width = 64
        self.height = 64

        self.red_imp_walking_spritesheet = SpriteSheet('assets/Enemy_Red_Imp_Sword_Walk.png')
        self.red_imp_attack_spritesheet = SpriteSheet('assets/Enemy_Red_Imp_Sword_Attack.png')
        self.red_imp_death_spritesheet = SpriteSheet('assets/Enemy_Red_Imp_Death.png')

        self.image = self.game.goblin_walking_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.up_animations = [self.red_imp_walking_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.red_imp_walking_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.red_imp_walking_spritesheet.get_sprite(128, 0, self.width, self.height),
                              self.red_imp_walking_spritesheet.get_sprite(192, 0, self.width, self.height)
                              ]
        self.left_animations = [self.red_imp_walking_spritesheet.get_sprite(0, 64, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(64, 64, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(128, 64, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(192, 64, self.width, self.height)
                                ]

        self.down_animations = [self.red_imp_walking_spritesheet.get_sprite(0, 128, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(64, 128, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(128, 128, self.width, self.height),
                                self.red_imp_walking_spritesheet.get_sprite(192, 128, self.width, self.height)
                                ]

        self.right_animations = [self.red_imp_walking_spritesheet.get_sprite(0, 192, self.width, self.height),
                                 self.red_imp_walking_spritesheet.get_sprite(64, 192, self.width, self.height),
                                 self.red_imp_walking_spritesheet.get_sprite(128, 192, self.width, self.height),
                                 self.red_imp_walking_spritesheet.get_sprite(192, 192, self.width, self.height)
                                 ]

        self.left_attack_animations = [self.red_imp_attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                       self.red_imp_attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                       self.red_imp_attack_spritesheet.get_sprite(128, 64, self.width, self.height),
                                       self.red_imp_attack_spritesheet.get_sprite(192, 64, self.width, self.height)
                                       ]

        self.death_animations = [self.red_imp_death_spritesheet.get_sprite(0, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(64, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(128, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(192, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(256, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(256, 0, self.width, self.height),
                                 self.red_imp_death_spritesheet.get_sprite(256, 0, self.width, self.height)
                                 ]


class Gray_Spider(EnemyTemplate):
    def __init__(self, game, x, y, AttackStrength, Health, EXPGain):
        EnemyTemplate.__init__(self, game, x, y, AttackStrength, Health, EXPGain)
        self.EnemyName = 'Gray Spider'

        self.width = 64
        self.height = 64

        self.Gray_Spider_spritesheet = SpriteSheet('assets/Enemy_Gray_Spider.png')

        self.image = self.Gray_Spider_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.up_animations = [self.Gray_Spider_spritesheet.get_sprite(320, 0, self.width, self.height),
                              self.Gray_Spider_spritesheet.get_sprite(384, 0, self.width, self.height),
                              self.Gray_Spider_spritesheet.get_sprite(448, 0, self.width, self.height),
                              self.Gray_Spider_spritesheet.get_sprite(512, 0, self.width, self.height),
                              self.Gray_Spider_spritesheet.get_sprite(576, 0, self.width, self.height)
                              ]
        self.left_animations = [self.Gray_Spider_spritesheet.get_sprite(320, 64, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(384, 64, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(448, 64, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(512, 64, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(576, 64, self.width, self.height)
                                ]

        self.down_animations = [self.Gray_Spider_spritesheet.get_sprite(320, 128, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(384, 128, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(448, 128, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(512, 128, self.width, self.height),
                                self.Gray_Spider_spritesheet.get_sprite(576, 128, self.width, self.height)
                                ]

        self.right_animations = [self.Gray_Spider_spritesheet.get_sprite(320, 192, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(384, 192, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(448, 192, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(512, 192, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(576, 192, self.width, self.height)
                                 ]

        self.left_attack_animations = [self.Gray_Spider_spritesheet.get_sprite(0, 64, self.width, self.height),
                                       self.Gray_Spider_spritesheet.get_sprite(64, 64, self.width, self.height),
                                       self.Gray_Spider_spritesheet.get_sprite(128, 64, self.width, self.height),
                                       self.Gray_Spider_spritesheet.get_sprite(192, 64, self.width, self.height)
                                       ]

        self.death_animations = [self.Gray_Spider_spritesheet.get_sprite(0, 256, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(64, 256, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(128, 256, self.width, self.height),
                                 self.Gray_Spider_spritesheet.get_sprite(192, 256, self.width, self.height)
                                 ]


class Wolf(EnemyTemplate):
    def __init__(self, game, x, y, AttackStrength, Health, EXPGain):
        EnemyTemplate.__init__(self, game, x, y, AttackStrength, Health, EXPGain)

        self.EnemyName = 'Wolf'

        self.width = 32
        self.height = 64

        self.image = self.game.wolf_spritesheet.get_sprite(0, 0, self.width, self.height)

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
                                self.game.wolf_spritesheet.get_sprite(512, 288, 64, 32),
                                self.game.wolf_spritesheet.get_sprite(576, 288, 64, 32)]

        self.right_animations = [self.game.wolf_spritesheet.get_sprite(320, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(384, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(448, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(512, 96, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(576, 96, 64, 32)]

        self.left_attack_animations = [self.game.wolf_spritesheet.get_sprite(320, 352, 64, 32),
                                       self.game.wolf_spritesheet.get_sprite(384, 352, 64, 32),
                                       self.game.wolf_spritesheet.get_sprite(448, 352, 64, 32),
                                       self.game.wolf_spritesheet.get_sprite(512, 352, 64, 32),
                                       self.game.wolf_spritesheet.get_sprite(576, 352, 64, 32)]

        self.death_animations = [self.game.wolf_spritesheet.get_sprite(320, 192, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(384, 192, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(448, 192, 64, 32),
                                 self.game.wolf_spritesheet.get_sprite(512, 192, 64, 32)
                                 ]
