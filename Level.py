import button
from Enemy import *


class Level:
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level specific info
    """

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.screen = self.game.screen

        self.enemy_sprites = self.game.enemy_sprites
        self.combat_enemy_sprites = self.game.combat_enemy_sprites
        self.background_sprites = self.game.background_sprites
        self.combat_background_sprites = self.game.combat_background_sprites
        self.all_sprites = self.game.all_sprites
        self.player_sprite = self.game.player_sprite
        self.UI_Sprites = self.game.UI_Sprites
        self.combat_UI_Sprites = self.game.combat_UI_Sprites
        self.combat_attack_sprites = self.game.combat_attack_sprites

        # Exits Booleans
        self.north_exit = False
        self.south_exit = False
        self.west_exit = False
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 0

        # Background Image
        self.background = WIN_BG
        self.attackBackground = pygame.image.load(self.game.resource_path('assets/background_attack.png'))
        self.attackBackground = pygame.transform.scale(self.attackBackground, (WIN_WIDTH, WIN_HEIGHT))
        self.AttackSelectionBG = pygame.image.load(self.game.resource_path('assets/AttackChoiceBG.png')).convert_alpha()
        self.AttackSelectionBG = pygame.transform.scale(self.AttackSelectionBG, (WIN_WIDTH / 5 * 3, 50))
        self.AttackSelectionBG_rect = self.AttackSelectionBG.get_rect()
        self.Monster1 = None

        # Other Images
        self.tree_image = pygame.image.load(self.game.resource_path('assets/tree.png'))
        self.rock_img = pygame.image.load(self.game.resource_path('assets/large_rock.png'))
        self.building1 = pygame.image.load(self.game.resource_path('assets/Building_1.png'))
        self.wolf_spritesheet = SpriteSheet_Black('assets/Wolfsheet1.png')
        self.goblin_walking_spritesheet = SpriteSheet('assets/goblin.png')
        self.character_spritesheet = SpriteSheet('assets/CharacterSpritesheet.png')

        self.Fireball_img = pygame.image.load(self.game.resource_path('assets/flame_icon.png'))
        self.Fireball_img = pygame.transform.scale(self.Fireball_img, (40, 40))
        self.Acid_img = pygame.image.load(self.game.resource_path('assets/acid-bolt.png'))
        self.Acid_img = pygame.transform.scale(self.Acid_img, (40, 40))
        self.Icebolt_img = pygame.image.load(self.game.resource_path('assets/ice-bolt.png'))
        self.Icebolt_img = pygame.transform.scale(self.Icebolt_img, (40, 40))
        self.Heal_img = pygame.image.load(self.game.resource_path('assets/health-increase.png'))
        self.Heal_img = pygame.transform.scale(self.Heal_img, (40, 40))

        self.milliseconds_delay = 2000  # 1 seconds
        self.CharacterAttackTimer = pygame.USEREVENT + 1
        self.EnemyAttackTimer = pygame.USEREVENT + 2

        self.DEBUGMODIFIERHP = 0.5
        self.DEBUGMODIFIERSTR = 0.5
        self.DEBUGMODIFIEREXP = 100

    def terrainGen(self):
        # Horizontal Rock Walls
        # Creates Terrain when not in combat
        if self.player.isAttackable:
            tempwidthcount = 0
            tempheightcount = 0
            xpos = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1
            # Gap in the Middle
            xpos_exit = xpos
            xpos = xpos + BORDER_TILESIZE * 2
            tempwidthcount = 0
            while tempwidthcount < (WIN_WIDTH / BORDER_TILESIZE) / 2 - 1:
                Rock(self, xpos, 0, self.rock_img)
                Rock(self, xpos, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                xpos += BORDER_TILESIZE
                tempwidthcount += 1

            # Vertical Rock Wall
            ypos = 0
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1
            tempheightcount = 0
            ypos_exit = ypos
            # Gap in the Middle
            ypos = ypos + BORDER_TILESIZE * 2
            while tempheightcount < (WIN_HEIGHT / BORDER_TILESIZE) / 2 - 1:
                Rock(self, 0, ypos, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos, self.rock_img)
                ypos += BORDER_TILESIZE
                tempheightcount += 1

            if not self.east_exit:  # Adds Rocks if East Exit is False
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit, self.rock_img)
                Rock(self, WIN_WIDTH - BORDER_TILESIZE, ypos_exit + BORDER_TILESIZE, self.rock_img)
            if not self.west_exit:  # Adds Rocks if West Exit is False
                Rock(self, 0, ypos_exit, self.rock_img)
                Rock(self, 0, ypos_exit + BORDER_TILESIZE, self.rock_img)
            if not self.north_exit:  # Adds Rocks if North Exit is False
                Rock(self, xpos_exit, 0, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, 0, self.rock_img)
            if not self.south_exit:  # Adds Rocks if South Exit is False
                Rock(self, xpos_exit, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)
                Rock(self, xpos_exit + BORDER_TILESIZE, WIN_HEIGHT - BORDER_TILESIZE, self.rock_img)

            if self.in_town:
                Building(self, 25, 25, self.building1)
                Tree(self, WIN_WIDTH / 2, WIN_HEIGHT / 2 + 50, self.tree_image)
                Tree(self, WIN_WIDTH / 2, WIN_HEIGHT / 2 - 150, self.tree_image)
            else:
                for _ in range(random.randint(10, 20)):
                    Tree(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                         random.randint(BORDER_TILESIZE * 2,
                                        WIN_HEIGHT - (BORDER_TILESIZE * 2) - self.tree_image.get_height() / 2),
                         self.tree_image)
                    Rock(self, random.randint(BORDER_TILESIZE * 3, WIN_WIDTH - BORDER_TILESIZE * 3),
                         random.randint(BORDER_TILESIZE * 3, WIN_HEIGHT - BORDER_TILESIZE * 3), self.rock_img)
        # Creates Terrain while IN Combat
        else:
            for _ in range(5):
                randomYTop = random.randint(BORDER_TILESIZE, WIN_HEIGHT / 2 - self.tree_image.get_height())
                randomYBottom = random.randint(WIN_HEIGHT / 2 + self.tree_image.get_height(),
                                               WIN_HEIGHT - BORDER_TILESIZE - self.tree_image.get_height())
                randomY = random.choice((randomYTop, randomYBottom))
                randomX = random.randint(BORDER_TILESIZE, WIN_WIDTH - BORDER_TILESIZE * 3)
                Tree(self, randomX, randomY, self.tree_image)

                randomYTop = random.randint(BORDER_TILESIZE, WIN_HEIGHT / 2 - self.rock_img.get_height())
                randomYBottom = random.randint(WIN_HEIGHT / 2 + self.rock_img.get_height(),
                                               WIN_HEIGHT - BORDER_TILESIZE - self.rock_img.get_height())
                randomY = random.choice((randomYTop, randomYBottom))
                randomX = random.randint(BORDER_TILESIZE, WIN_WIDTH - BORDER_TILESIZE * 3)
                Rock(self, randomX, randomY, self.rock_img)

    def GenerateEnemies(self, Enemy):
        if self.game.DEBUGGING:
            self.DEBUGMODHP = self.DEBUGMODIFIERHP
            self.DEBUGMODSTR = self.DEBUGMODIFIERSTR
            self.DEBUGMODEXP = self.DEBUGMODIFIEREXP
        else:
            self.DEBUGMODHP = 1
            self.DEBUGMODSTR = 1
            self.DEBUGMODEXP = 1

        if Enemy is None:
            EnemyName = random.choice(self.game.EnemyList)
        else:
            EnemyName = Enemy
        EnemyList = self.game.EnemyList
        EnemyStrength = int(self.game.previousLevel) * 2 + 1
        EnemyHealth = int(self.game.previousLevel) * 10 + 5
        EnemyEXPGain = int(self.game.previousLevel) * 3 + 3
        if self.player.isAttackable:
            for _ in range(self.enemy_count):
                RandChoice = random.choice(EnemyList)
                if RandChoice == 'Wolf':
                    Wolf(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                         random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2)),
                         EnemyStrength * self.DEBUGMODSTR,
                         EnemyHealth * self.DEBUGMODHP, EnemyEXPGain * self.DEBUGMODEXP)
                if RandChoice == 'Goblin':
                    Goblin(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                           random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2)),
                           EnemyStrength * 2 * self.DEBUGMODSTR,
                           EnemyHealth * 2 * self.DEBUGMODHP, EnemyEXPGain * 2 * self.DEBUGMODEXP)
                if RandChoice == 'Red Imp':
                    Red_Imp(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                            random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2)),
                            EnemyStrength * 3 * self.DEBUGMODSTR,
                            EnemyHealth * 3 * self.DEBUGMODHP, EnemyEXPGain * 3 * self.DEBUGMODEXP)
                if RandChoice == 'Gray Spider':
                    Gray_Spider(self, random.randint(BORDER_TILESIZE * 2, WIN_WIDTH - BORDER_TILESIZE * 2),
                                random.randint(BORDER_TILESIZE * 2, WIN_HEIGHT - (BORDER_TILESIZE * 2)),
                                EnemyStrength * self.DEBUGMODSTR,
                                EnemyHealth * self.DEBUGMODHP, EnemyEXPGain * self.DEBUGMODEXP)

        else:
            if EnemyName == 'Wolf':
                self.Monster1 = Wolf(self, WIN_WIDTH - BORDER_TILESIZE * 4, WIN_HEIGHT / 2,
                                     EnemyStrength * self.DEBUGMODSTR,
                                     EnemyHealth * self.DEBUGMODHP, EnemyEXPGain * self.DEBUGMODEXP)
            if EnemyName == 'Goblin':
                self.Monster1 = Goblin(self, WIN_WIDTH - BORDER_TILESIZE * 4, WIN_HEIGHT / 2,
                                       EnemyStrength * 2 * self.DEBUGMODSTR,
                                       EnemyHealth * 2 * self.DEBUGMODHP, EnemyEXPGain * 2 * self.DEBUGMODEXP)
            if EnemyName == 'Red Imp':
                self.Monster1 = Red_Imp(self, WIN_WIDTH - BORDER_TILESIZE * 4, WIN_HEIGHT / 2,
                                        EnemyStrength * 3 * self.DEBUGMODSTR,
                                        EnemyHealth * 3 * self.DEBUGMODHP, EnemyEXPGain * 3 * self.DEBUGMODEXP)
            if EnemyName == 'Gray Spider':
                self.Monster1 = Gray_Spider(self, WIN_WIDTH - BORDER_TILESIZE * 4, WIN_HEIGHT / 2,
                                            EnemyStrength * self.DEBUGMODSTR,
                                            EnemyHealth * self.DEBUGMODHP, EnemyEXPGain * self.DEBUGMODEXP)

    # Update everything on this level
    def update(self):
        self.enemy_sprites.update()
        self.background_sprites.update()
        self.UI_Sprites.update()
        self.combat_UI_Sprites.update()
        self.combat_attack_sprites.update()

        # Heal while in Town
        if self.in_town:
            if self.player.hp < self.player.max_hp:
                self.player.changeHealth(.1)
            if self.player.mp < self.player.max_mp:
                self.player.changeMana(.1)
        else:
            if self.player.mp < self.player.max_mp:
                self.player.changeMana(.03)

    def draw(self, screen):
        # Draw everyone on this level
        self.screen = screen
        self.player = self.game.player

        if not self.player.isAttackable:
            self.screen.blit(self.attackBackground, (0, 0))

            self.combat_enemy_sprites.draw(self.screen)
            self.combat_background_sprites.draw(self.screen)
            self.combat_UI_Sprites.draw(self.screen)
            self.combat_attack_sprites.draw(self.screen)
            self.player_sprite.draw(screen)
            self.screen.blit(self.Monster1.HPText, self.Monster1.HPBarTextRect)

            if self.player.canAttack:
                self.screen.blit(self.AttackSelectionBG, (WIN_WIDTH / 5, WIN_HEIGHT - 50))

                # Attack Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 35, WIN_HEIGHT - 125,
                                 pygame.image.load(self.game.resource_path('assets/button_attack.png')), 195,
                                 50,
                                 ' Melee Attack ',
                                 ' Punches Target ',
                                 ' Deals ' + (str(self.player.CharacterStrength) + "-" + str(
                                     self.player.CharacterStrength + 10) + " damage. "),
                                 ' Cost: 0 mp ').draw() and self.player.canAttack:
                    self.player.canAttack = False
                    # pygame.time.set_timer(self.CharacterAttackTimer, self.milliseconds_delay)
                    # self.player.Loot()
                    self.player.monsterToAttack = self.game.current_level.Monster1
                    self.player.canAttack = False
                    self.player.AttackMonster()

                #  Flee Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 240, WIN_HEIGHT - 125,
                                 pygame.image.load(self.game.resource_path('assets/button_flee.png')), 195, 50,
                                 ' Flee ',
                                 ' Runs away from Battle ',
                                 ' Lose 20 hp ',
                                 ' Cost: 0 mp ').draw():
                    self.player.Flee()

                # Ice Bolt Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 35, WIN_HEIGHT - 48, self.Icebolt_img, 40, 40,
                                 ' Ice Bolt ',
                                 ' Casts an Ice Bolt at the target ',
                                 ' Deals ' + (str(self.player.IceBoltDamage) + "-" + str(
                                     self.player.IceBoltDamage + 10) + " damage. "),
                                 " Cost: " + str(
                                     self.game.player.IceBoltCost) + " mp. ").draw() and self.player.canAttack:
                    self.player.SpellName = 'Ice Bolt'
                    if self.player.mp >= self.player.IceBoltCost:
                        self.player.canAttack = False
                        self.player.monsterToAttack = self.game.current_level.Monster1
                        self.player.CastSpellFromBar()
                    else:
                        self.game.console_print(
                            'Need at least ' + str(self.player.IceBoltCost) + ' mana to cast ' + self.player.SpellName)

                # Fireball Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 110, WIN_HEIGHT - 48, self.Fireball_img,
                                 40, 40,
                                 " Fireball ",
                                 ' Launches a fireball at the target. ',
                                 ' Deals ' + (str(self.player.FireballDamage) + "-" + str(
                                     self.player.FireballDamage + 10) + " damage. "),
                                 ' Cost: ' + str(
                                     self.game.player.FireballCost) + " mp. ").draw() and self.player.canAttack:
                    self.game.player.SpellName = 'Fireball'
                    if self.player.mp >= self.player.FireballCost:
                        self.player.canAttack = False
                        self.player.monsterToAttack = self.game.current_level.Monster1
                        self.player.CastSpellFromBar()
                    else:
                        self.game.console_print(
                            'Need at least ' + str(
                                self.player.FireballCost) + ' mana to cast ' + self.player.SpellName)

                # Acid Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 185, WIN_HEIGHT - 48, self.Acid_img,
                                 40, 40,
                                 ' Acid ',
                                 ' Casts an Acid Ball at the target ',
                                 ' Deals ' + (str(self.player.AcidDamage) + "-" + str(
                                     self.player.AcidDamage + 10) + " damage. "),
                                 " Cost: " + str(
                                     self.game.player.AcidCost) + " mp. ").draw() and self.player.canAttack:
                    self.player.SpellName = 'Acid'
                    if self.player.mp >= self.player.AcidCost:
                        self.player.canAttack = False
                        self.player.monsterToAttack = self.game.current_level.Monster1
                        self.player.CastSpellFromBar()
                    else:
                        self.game.console_print(
                            'Need at least ' + str(
                                self.player.AcidCost) + ' mana to cast ' + self.player.SpellName)

                # Heal Button
                if button.Button(self.game, self.screen, WIN_WIDTH / 5 + 410, WIN_HEIGHT - 48, self.Heal_img,
                                 40, 40,
                                 " Heal ",
                                 ' Heals the player for 20% hp. ',
                                 ' Heals ' + (str(math.ceil(self.player.max_hp/5)) + " hp. "),
                                 ' Cost: ' + str(
                                     self.game.player.HealCost) + " mp. ").draw() and self.player.canAttack:
                    self.game.player.SpellName = 'Heal'
                    if self.player.mp >= self.player.HealCost:
                        self.player.canAttack = False
                        self.player.monsterToAttack = self.game.current_level.Monster1
                        self.player.CastSpellFromBar()
                    else:
                        self.game.console_print(
                            'Need at least ' + str(
                                self.player.HealCost) + ' mana to cast ' + self.player.SpellName)

        else:
            # Draw the Background
            self.screen.blit(self.background, (0, 0))

            self.all_sprites.draw(screen)
        self.UI_Sprites.draw(self.screen)
        if self.game.showInventory:
            self.screen.blit(self.game.inventorySurface, (((WIN_WIDTH-500)/2), ((WIN_HEIGHT-500)/2)))
        self.screen.blit(self.game.log_surf, (WIN_WIDTH / 2, WIN_HEIGHT))



## LEVEL MAP ##
#
# [Town LEVEL]      [LEVEL 4]       [LEVEL 7]
#  [LEVEL 2]        [LEVEL 5]       [LEVEL 8]
#  [LEVEL 3]        [LEVEL 6]       [LEVEL 9]
#
#

class StartLevel(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = False
        self.east_exit = True
        self.in_town = True

        self.enemy_count = 1


class AttackScreen(Level):

    def __init__(self, game, player, ):
        Level.__init__(self, game, player)
        self.game = game


class Level_02(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = False
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 2


class Level_03(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = False
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 3


class Level_04(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 2


class Level_05(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 4


class Level_06(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = True
        self.east_exit = True
        self.in_town = False

        self.enemy_count = 5


class Level_07(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = False
        self.south_exit = True
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 5


class Level_08(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = True
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 6


class Level_09(Level):

    def __init__(self, game, player):
        Level.__init__(self, game, player)

        self.north_exit = True
        self.south_exit = False
        self.west_exit = True
        self.east_exit = False
        self.in_town = False

        self.enemy_count = 7
