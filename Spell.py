import math
import random

from character import *
from SpriteUtilities import *


class SpellTemplate(pygame.sprite.Sprite):
    def __init__(self, game, Enemy, Player, Damage, Cost):
        #  Initial Setup of Spell - Generic Attributes
        self.game = game
        self.Enemy = Enemy
        self.player = Player
        self.screen = self.game.screen
        pygame.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.combat_attack_sprites)

        self.direction = math.atan2((self.Enemy.y - self.Enemy.height / 3 - self.player.rect.y),
                                    (self.Enemy.x - self.player.rect.right))
        self.dt = self.game.clock.tick(FPS * 5)

        #  Spell Specific Attributes
        self.AttackDamage = self.CalculateDamage(Damage)
        self.ManaCost = Cost
        self.SpellName = 'Change Me'
        self.image = pygame.image.load('assets/flame_icon.png')

        #  Adjusting sprite location
        self.rect = self.image.get_rect()

        self.rect.x = self.player.rect.left
        self.rect.y = self.player.rect.y + self.player.height / 2

        self._layer = self.rect.bottom

    def update(self):
        # dx, dy = (self.Enemy.rect.x - self.rect.right), (self.Enemy.rect.y - self.rect.y)
        # rads = math.atan2(dy, dx)
        # self.rect.x += self.dt * math.cos(rads)
        # self.rect.y += self.dt * math.sin(rads)

        self.direction = math.atan2((self.Enemy.rect.y + self.Enemy.height / 3 - self.rect.y),
                                    (self.Enemy.rect.right - self.rect.right))
        self.rect.x += self.dt * math.cos(self.direction)
        self.rect.y += self.dt * math.sin(self.direction)

        self.collide_with_enemy()
        if not self.screen.get_rect().contains(self.rect):
            self.kill()

    def collide_with_enemy(self):
        collide = pygame.Rect.colliderect(self.rect, self.Enemy.rect)

        if collide:
            self.kill()
            self.Enemy.TakeDamage(self.AttackDamage)
            self.game.console_print(
                ('You cast ' + self.SpellName + ' and hit the ' + self.Enemy.EnemyName + ' for ' + str(
                    self.AttackDamage) + ' damage'))
            if self.Enemy.hp > 0:
                self.game.enemyHPBar = pygame.transform.scale(self.game.enemyHPBar, (
                    math.floor((self.Enemy.hp / self.Enemy.max_hp) * (WIN_WIDTH / 3)), 50))

                self.font = pygame.font.Font('assets/BKANT.TTF', 20)
                self.Enemy.HPBarText = str(round(self.Enemy.hp)) + "/" + str(round(self.Enemy.max_hp))
                self.Enemy.HPText = self.font.render(str(self.Enemy.HPBarText), True, BLACK, None)

            if self.Enemy.hp <= 0:
                self.Enemy.CheckForDeath()

            if self.game.player.hp > 0 and self.Enemy.hp > 0:
                pygame.time.set_timer(self.game.EnemyAttackTimer, self.game.milliseconds_delay)

    def CalculateDamage(self, damage):
        Attack = random.randint(damage, damage+10)
        if Attack > self.Enemy.hp:
            Attack = self.Enemy.hp
        return Attack


class Fireball(SpellTemplate):
    def __init__(self, game, Enemy, Player, Damage, Cost):
        SpellTemplate.__init__(self, game, Enemy, Player, Damage, Cost)

        self.AttackDamage = self.CalculateDamage(Damage)
        self.ManaCost = Cost
        self.SpellName = 'Fireball'
        self.image = self.game.WeaponsAndMagicSpritesheet.get_sprite(68, 198, 24, 12)
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.left
        self.rect.y = self.player.rect.y + self.player.rect.height/2


class Acidball(SpellTemplate):
    def __init__(self, game, Enemy, Player, Damage, Cost):
        SpellTemplate.__init__(self, game, Enemy, Player, Damage, Cost)

        self.AttackDamage = self.CalculateDamage(Damage)
        self.ManaCost = Cost
        self.SpellName = 'Acid'
        self.image = self.game.WeaponsAndMagicSpritesheet.get_sprite(74, 246, 18, 12)
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.left
        self.rect.y = self.player.rect.y + self.player.rect.height/2
