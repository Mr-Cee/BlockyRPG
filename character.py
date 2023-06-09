import logging
import random

from Item import Item
from UI import *
#import pyautogui as pyautogui
import pygame
import math
from config import *
from SpriteUtilities import *
from Spell import *



class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        log = "bot.log"
        logging.basicConfig(filename=log, level=logging.DEBUG, format='%(asctime)s %(message)s', filemode='a',
                            datefmt='%d/%m/%Y %H:%M:%S')

        self.game = game
        self.screen = self.game.screen
        self.dt = self.game.clock.tick(FPS * 250)
        self.screen = self.game.screen

        self.baseHP = 100
        self.itemHP = 0
        self.max_hp = self.baseHP+self.itemHP
        self.hp = self.max_hp

        self.baseMP = 100
        self.itemMP = 0
        self.max_mp = self.baseMP + self.itemMP
        self.mp = self.max_mp

        self.playerLevel = 1
        self.exp = 0
        self.exp_to_level = 10

        self.CharacterStrength = 5
        self.CharacterArmor = 0
        self.CritChance = 0
        self.CritBonus = 0

        self.IceBoltDamage = 10
        self.IceBoltCost = 10
        self.FireballDamage = 30
        self.FireballCost = 25
        self.AcidDamage = 75
        self.AcidCost = 50

        self.HealAmount = 25
        self.HealCost = 25

        self.font = pygame.font.Font('assets/BKANT.TTF', 40)
        self.LevelText = self.font.render(str(self.playerLevel), True, BLACK, None)

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.HPBarText = str(self.hp) + "/" + str(self.max_hp)
        self.HPText = self.font.render(str(self.HPBarText), True, BLACK, None)
        self.HPBarTextRect = self.HPText.get_rect()
        self.HPBarTextRect.center = (275, WIN_HEIGHT + 36)

        self.MPBarText = str(self.mp) + "/" + str(self.max_mp)
        self.MPText = self.font.render(str(self.MPBarText), True, BLACK, None)
        self.MPBarTextRect = self.MPText.get_rect()
        self.MPBarTextRect.center = (275, WIN_HEIGHT + 77)

        self.EXPBarText = str(self.exp) + "/" + str(self.exp_to_level)
        self.EXPText = self.font.render(str(self.EXPBarText), True, BLACK, None)
        self.EXPBarTextRect = self.EXPText.get_rect()
        self.EXPBarTextRect.center = (275, WIN_HEIGHT + 123)

        self.isAttackable = True  # Allows the character to attack or be attacked
        self.moveTowardsEnemy = False
        self.CastSpellStart = False
        self.tempAttackPause = 0
        self.canAttack = False
        self.AttackChoice = False
        self.monsterToAttack = None

        self.x = x
        self.y = y
        self.width = CHARACTER_TILESIZE
        self.height = CHARACTER_TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.movement_loop = 0
        self.max_travel = 10

        self.facing = 'down'
        self.animation_loop = 1
        self.animation_loop_speed = 0.5

        self.image = self.game.character_spritesheet.get_sprite(0, 192, self.width, self.height)
        self.FireballImage = self.game.WeaponsAndMagicSpritesheet.get_sprite(68, 198, 24, 12)
        self.AcidImage = self.game.WeaponsAndMagicSpritesheet.get_sprite(74, 246, 18, 12)
        self.SpellCastSheet = SpriteSheet('assets/CharacterSpellSheet.png')
        self.SpellName = ''
        self.MeleeSlashSheet = SpriteSheet('assets/CharacterSlashSheet.png')
        self.SwordSlashSheet = SpriteSheet('assets/WEAPON_longsword_slash.png')
        self.MeleeAttack_Anim = False

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)

        # Character Level Text
        self.LevelTextRect = self.LevelText.get_rect()
        self.LevelTextRect.center = (78, WIN_HEIGHT + 79)

        self.collision_rect = pygame.Rect(self.x + 22, self.y - 5, 20, 10)

        self._layer = self.collision_rect.bottom

        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.player_sprite)

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(64, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(128, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(192, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(256, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(320, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(384, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(448, 128, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(512, 128, self.width, self.height)
                                ]

        self.up_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(128, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(192, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(256, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(320, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(384, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(448, 0, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(512, 0, self.width, self.height)
                              ]

        self.left_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(64, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(128, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(192, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(256, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(320, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(384, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(448, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(512, 64, self.width, self.height)
                                ]

        self.right_animations = [self.game.character_spritesheet.get_sprite(0, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(64, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(128, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(192, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(256, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(320, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(384, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(448, 192, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(512, 192, self.width, self.height)
                                 ]

        self.spellcast_animations = [self.SpellCastSheet.get_sprite(0, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(64, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(128, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(192, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(256, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(320, 200, self.width, self.height),
                                     self.SpellCastSheet.get_sprite(384, 200, self.width, self.height)
                                     ]

        self.melee_attack_animation = [self.MeleeSlashSheet.get_sprite(0, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(64, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(128, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(192, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(256, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(320, 192, self.width, self.height),
                                       self.MeleeSlashSheet.get_sprite(384, 192, self.width, self.height)]

        self.weapon_sword_animations = [self.SwordSlashSheet.get_sprite(0, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(64, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(128, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(192, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(256, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(320, 192, self.width, self.height),
                                        self.SwordSlashSheet.get_sprite(384, 192, self.width, self.height)]

        self.milliseconds_delay = 3000  # 1 seconds
        self.timer_event = pygame.USEREVENT + 1
        # pygame.time.set_timer(self.timer_event, self.milliseconds_delay)

    def update(self):
        self.checkForLevelUp()
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collision_rect.x += self.x_change
        self.pos.x = self.rect.right
        self.collide_terrain('x')

        self.rect.y += self.y_change
        self.collision_rect.y = self.rect.bottom - 5
        self.pos.y = self.rect.y + 32
        self.collide_terrain('y')

        self.game.all_sprites.change_layer(self, self.collision_rect.bottom)

        self.x_change = 0
        self.y_change = 0

        if self.collision_rect.right > WIN_WIDTH:
            self.game.LevelChange('right')
        if self.collision_rect.left < 0:
            self.game.LevelChange('left')
        if self.collision_rect.bottom > WIN_HEIGHT:
            self.game.LevelChange('down')
        if self.collision_rect.top < 0:
            self.game.LevelChange('up')

        # print('Player', self._layer)

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 128, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_loop_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_loop_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 0
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_loop_speed
                if self.animation_loop >= 8:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.CastSpellStart:
                self.image = self.spellcast_animations[math.floor(self.animation_loop)]
                self.animation_loop += 7 / FPS
                if self.animation_loop >= 6:
                    self.CastSpellStart = False
                    self.animation_loop = 0
                    self.CastSpell()
            else:
                if self.x_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(0, 192, self.width, self.height)
                    # self.image = self.SpellCastSheet.get_sprite(0, 200, self.width, self.height)
                else:
                    self.image = self.right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += len(self.right_animations) / FPS
                    if self.animation_loop >= len(self.right_animations) - 1:
                        self.animation_loop = 0
        if self.MeleeAttack_Anim:
            self.image = self.melee_attack_animation[math.floor(self.animation_loop)]
            # self.screen.blit(self.weapon_sword_animations[math.floor(self.animation_loop)], (self.rect.x, self.rect.y))
            self.animation_loop += len(self.melee_attack_animation) / FPS
            if self.animation_loop >= len(self.melee_attack_animation) - 1:
                self.MeleeAttack_Anim = False
                self.animation_loop = 0
                self.MeleeAttack()

    def movement(self):
        if self.isAttackable:
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
        elif self.moveTowardsEnemy:
            if self.monsterToAttack.rect.left - self.rect.right >= 15:
                dx, dy = (self.monsterToAttack.rect.x - self.rect.right), (self.monsterToAttack.rect.y - self.rect.y)
                rads = math.atan2(dy, dx)
                self.monster_direction = rads
                self.x_change += math.cos(self.monster_direction) * 5
                self.y_change += math.sin(self.monster_direction) * 5
                self.movement_loop += PLAYER_SPEED

                if self.movement_loop >= self.max_travel or self.monsterToAttack.rect.left - self.rect.right <= 15:
                    self.moveTowardsEnemy = False
                    self.movement_loop = 0
                    if self.game.player.hp > 0 and self.Enemy.hp > 0:
                        pygame.time.set_timer(self.game.EnemyAttackTimer, self.game.milliseconds_delay)
            else:
                self.moveTowardsEnemy = False
                self.movement_loop = 0
                if self.game.player.hp > 0 and self.Enemy.hp > 0:
                    pygame.time.set_timer(self.game.EnemyAttackTimer, self.game.milliseconds_delay)

    def collide_terrain(self, direction):

        if direction == 'x':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.collision_rect, object.collision_rect)
                if collide:
                    if self.x_change > 0:  # Moving Right
                        self.rect.right = object.collision_rect.x + 22
                        self.collision_rect.right = object.collision_rect.x
                    if self.x_change < 0:  # Moving Left
                        self.rect.x = object.collision_rect.right - 22
                        self.collision_rect.x = object.collision_rect.right

        if direction == 'y':
            for object in self.game.background_sprites:
                collide = pygame.Rect.colliderect(self.collision_rect, object.collision_rect)
                if collide:
                    if self.y_change > 0:  # Moving Down
                        self.rect.bottom = object.collision_rect.top - 5
                        self.collision_rect.bottom = object.collision_rect.top
                    if self.y_change < 0:  # Moving Up
                        self.rect.y = object.collision_rect.bottom - self.height + 5
                        self.collision_rect.top = object.collision_rect.bottom

                    # print('Object Layer:', object._layer)
                    # print('Player Layer:', self._layer)
                    # print('Player Collision', self.collision_rect.bottom)
                    # print('---------------')
                    # print(self.game.all_sprites.get_layer_of_sprite(self))

                    # logging.info('------------------------------------')
                    # logging.info(str(self.game.current_level))
                    # for i in range(len(self.game.all_sprites)):
                    #     logging.info(
                    #         ('Layer:', self.game.all_sprites.get_layer_of_sprite(self.game.all_sprites.get_sprite(i)), 'Sprite:',
                    #          self.game.all_sprites.get_sprite(i), self.game.all_sprites.get_sprite(i).collision_rect))
                    # logging.info('------------------------------------')

    def collide_enemy(self):

        if self.isAttackable:

            self.templist = []
            for object in self.game.enemy_sprites:
                collide = pygame.Rect.colliderect(self.collision_rect, object.rect)
                if collide:
                    enemyRedHPBar = EnemyHPBarInterior(self.game, object, WIN_WIDTH / 3 + 11, 16)
                    enemyHPFG = EnemyHPBarFG(self.game, object, WIN_WIDTH / 3, 10)

                    self.isAttackable = False
                    self.canAttack = True
                    object.facing = 'left'
                    # self.game.enemyHPBar = pygame.transform.scale(self.game.enemyHPBar,
                    #                                               (round(object.hp / object.max_hp * (WIN_WIDTH / 3)),
                    #                                                50))
                    self.tempAttack(object, object.EnemyName)
                    self.templist.append(object)

            # if len(templist) > 0:
            #     for item in templist:
            #         item.kill()

    def Loot(self, EXPGain, EnemyObject):
        self.changeEXP(math.ceil(EXPGain) * self.game.DEBUGMOD)
        self.isAttackable = True
        self.AttackChoice = False
        self.canAttack = True

        self.game.console_print(
            ('You killed the ' + EnemyObject.EnemyName + ' and gained ' + str(math.ceil(EXPGain)) + ' experience'))

        if self.game.Inventory.checkForAvailableSpace():
            if self.game.availableInventorySpace:
                randID = random.randint(0, 7)
                TempDMG = random.randint(self.playerLevel, self.playerLevel+10)
                TempArmor = random.randint(self.playerLevel, self.playerLevel+10)
                TempHP = random.randint(self.playerLevel, self.playerLevel+10)
                tempMP = random.randint(self.playerLevel, self.playerLevel+10)
                TempCC = random.randint(self.playerLevel, self.playerLevel+1)
                TempCB = random.randint(self.playerLevel, self.playerLevel+1)
                Loot = Item(self, randID, TempDMG, TempArmor, TempHP, tempMP, TempCC, TempCB)
                self.game.Inventory.Add(Loot, self.game.Inventory.Get_First_Empty())
                # print(Loot)
                self.game.console_print('You Looted a ' + str(Loot.Description))
            else:
                self.game.console_print('Inventory Full')
        else:
            self.game.console_print('Inventory Full')

        if len(self.templist) > 0:
            for item in self.templist:
                item.kill()

        self.game.RemoveAttackLevel()

        self.rect.x, self.rect.y = self.previousPOS
        self.collision_rect.x = self.rect.x + 22
        self.collision_rect.y = self.rect.bottom - 5

    def Flee(self):
        self.changeHealth(-20)
        if self.checkForDeath():
            return
        self.isAttackable = True
        self.AttackChoice = False
        self.canAttack = True

        self.game.console_print('You fled the battle!')

        if len(self.templist) > 0:
            for item in self.templist:
                item.kill()

        self.game.RemoveAttackLevel()

        self.rect.x, self.rect.y = self.previousPOS
        self.collision_rect.x = self.rect.x + 22
        self.collision_rect.y = self.rect.bottom - 5

    def tempAttack(self, EnemyObject, EnemyName):
        EnemyObject = EnemyObject

        self.tempAttackPause = 1 * FPS
        self.AttackChoice = True

        self.previousPOS = (self.rect.x, self.rect.y)
        self.facing = 'right'
        self.rect.x = BORDER_TILESIZE + 5
        self.rect.y = WIN_HEIGHT / 2 - self.height / 3
        # self.collision_rect = pygame.Rect(self.x + 15, self.y - 5, 35, 10)
        self.collision_rect.x = self.rect.x + 15
        self.collision_rect.y = self.y - 5

        self.game.AttackLevelChange(EnemyName)

        # self.button("Test", WIN_WIDTH/2, WIN_HEIGHT/2, 100, 200, TEMPCOLOR, WHITE, self.TempAttackButton())
        # self.AttackMenu_Rect = pygame.Rect(WIN_WIDTH / 2, WIN_HEIGHT / 2, 100, 200)

    def CastSpell(self):
        EnemyObject = self.monsterToAttack
        if self.SpellName == 'Fireball':
            if self.mp >= self.FireballCost:
                Fireball(self.game, EnemyObject, self, self.FireballDamage, self.FireballCost)
                self.changeMana(-self.FireballCost)
            else:
                self.game.console_print('Need at least ' + str(self.FireballCost) + '  mana to cast ' + self.SpellName)
                self.canAttack = True
        elif self.SpellName == 'Acid':
            if self.mp >= self.AcidCost:
                Acidball(self.game, EnemyObject, self, self.AcidDamage, self.AcidCost)
                self.changeMana(-self.AcidCost)
            else:
                self.game.console_print('Need at least ' + str(self.AcidCost) + ' mana to cast ' + self.SpellName)
                self.canAttack = True
        elif self.SpellName == 'Ice Bolt':
            if self.mp >= self.IceBoltCost:
                Icebolt(self.game, EnemyObject, self, self.IceBoltDamage, self.IceBoltCost)
                self.changeMana(-self.IceBoltCost)
            else:
                self.game.console_print('Need at least ' + str(self.IceBoltCost) + ' mana to cast ' + self.SpellName)
                self.canAttack = True
        elif self.SpellName == 'Heal':
            if self.mp >= self.HealCost:
                self.changeHealth(math.ceil(self.max_hp / 5))
                self.changeMana(-self.HealCost)
                pygame.time.set_timer(self.game.EnemyAttackTimer, self.game.milliseconds_delay)
            else:
                self.game.console_print('Need at least ' + str(self.FireballCost) + '  mana to cast ' + self.SpellName)
                self.canAttack = True
        else:
            spell_image = self.FireballImage

    def CastSpellFromBar(self):
        self.animation_loop = 0
        self.CastSpellStart = True

    def AttackMonster(self):
        self.Enemy = self.monsterToAttack
        if self.Enemy.rect.left - self.rect.right > 15:
            self.max_travel = random.randint(WIN_WIDTH / 5, WIN_WIDTH / 4)
            self.movement_loop = 0
            self.moveTowardsEnemy = True
        else:
            self.animation_loop = 0
            self.MeleeAttack_Anim = True

    def MeleeAttack(self):
        self.DidCrit=False
        self.attackDamage = random.randint(1 + self.CharacterStrength, 5 + self.CharacterStrength)
        CriticalChance = random.randint(1, 100)
        if CriticalChance <= self.CritChance:
            CB = self.CritBonus / 100 + 1
            self.attackDamage = self.attackDamage * CB
            self.DidCrit = True

        if self.attackDamage > self.Enemy.hp:
            self.attackDamage = self.Enemy.hp
        self.Enemy.hp -= self.attackDamage

        if self.DidCrit:
            self.game.console_print(
                ('You attacked the ' + self.Enemy.EnemyName + ' for ' + str(self.attackDamage) + ' CRITICAL damage'))
            self.DidCrit=False
        else:
            self.game.console_print(
            ('You attacked the ' + self.Enemy.EnemyName + ' for ' + str(self.attackDamage) + ' damage'))
        if self.Enemy.hp > 0:
            self.game.enemyHPBar = pygame.transform.scale(self.game.enemyHPBar, (
                math.floor((self.Enemy.hp / self.Enemy.max_hp) * (WIN_WIDTH / 3)), 50))

            self.font = pygame.font.Font('assets/BKANT.TTF', 20)
            self.Enemy.HPBarText = str(round(self.Enemy.hp)) + "/" + str(round(self.Enemy.max_hp))
            self.Enemy.HPText = self.font.render(str(self.Enemy.HPBarText), True, BLACK, None)

        if self.Enemy.hp <= 0:
            self.Enemy.hp = 0
            self.Enemy.CheckForDeath()

        if self.game.player.hp > 0 and self.Enemy.hp > 0:
            pygame.time.set_timer(self.game.EnemyAttackTimer, self.game.milliseconds_delay)

    def checkForLevelUp(self):
        if self.exp >= self.exp_to_level:
            tempxp = self.exp - self.exp_to_level
            self.playerLevel += 1
            self.exp = tempxp
            self.exp_to_level *= 2

            self.CharacterStrength += 5
            self.IceBoltDamage += 5
            self.FireballDamage += 10
            self.AcidDamage += 15

            self.font = pygame.font.Font('assets/BKANT.TTF', 40)
            self.LevelText = self.font.render(str(self.playerLevel), True, BLACK, None)

            self.font = pygame.font.Font('assets/BKANT.TTF', 20)
            self.EXPBarText = str(self.exp) + "/" + str(self.exp_to_level)
            self.EXPText = self.font.render(str(self.EXPBarText), True, BLACK, None)
            self.EXPBarTextRect = self.EXPText.get_rect()
            self.EXPBarTextRect.center = (290, WIN_HEIGHT + 123)

            self.baseHP += 20
            self.max_hp = self.baseHP + self.itemHP
            self.hp = self.max_hp
            self.font = pygame.font.Font('assets/BKANT.TTF', 20)
            self.HPBarText = str(self.hp) + "/" + str(self.max_hp)
            self.HPText = self.font.render(str(self.HPBarText), True, BLACK, None)

            self.baseMP += 20
            self.max_mp = self.baseMP + self.itemMP
            self.mp = self.max_mp
            self.font = pygame.font.Font('assets/BKANT.TTF', 20)
            self.MPBarText = str(self.mp) + "/" + str(self.max_mp)
            self.MPText = self.font.render(str(self.MPBarText), True, BLACK, None)

            self.game.console_print(('You have leveled up to ' + str(self.playerLevel) + '!'))

    def checkForDeath(self):
        # Check for Death
        if self.hp <= 0:
            self.game.console_print('You died! You have lost ' + str(math.ceil(self.exp / 10)) + ' exp!')
            self.game.DeathReset()
            return True
            # pass

    def changeHealth(self, hpAmount):
        if self.hp + hpAmount < self.max_hp:
            self.hp += hpAmount
        else:
            self.hp = self.max_hp
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.HPBarText = str(round(self.hp)) + "/" + str(round(self.max_hp))
        self.HPText = self.font.render(str(self.HPBarText), True, BLACK, None)
        self.checkForDeath()

    def changeMana(self, mpAmount):

        if self.mp + mpAmount < 0:
            self.mp = 0

        if self.mp + mpAmount < self.max_mp:
            self.mp += mpAmount
        else:
            self.mp = self.max_mp

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.MPBarText = str(round(self.mp)) + "/" + str(round(self.max_mp))
        self.MPText = self.font.render(str(self.MPBarText), True, BLACK, None)

    def changeEXP(self, expAmount):
        self.exp += expAmount
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.EXPBarText = str(self.exp) + "/" + str(self.exp_to_level)
        self.EXPText = self.font.render(str(self.EXPBarText), True, BLACK, None)
        self.checkForLevelUp()
