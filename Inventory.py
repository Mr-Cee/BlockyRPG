import pygame
from config import *
from UI import *


class Inventory:
    def __init__(self, game):
        self.rows = 9
        self.col = 5
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]

        #####                Weapon  Shield  Helmet  Chest   Gloves   Legs  Boots Necklace
        #####                0         1       2       3       4       5      6      7
        self.EquipedItems = [None,    None,   None,   None,   None,   None,  None,  None]

        self.box_size = 33
        self.x = 25
        self.y = 23

        self.border = 3
        self.game = game

        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.statsTextHP = self.font.render("HP: " + str(self.game.player.hp) + "/" + (str(self.game.player.max_hp)),
                                            True, BLACK)

        self.WeaponRect = pygame.Rect(299, 214, self.box_size, self.box_size)
        self.WeaponSurface = pygame.Surface((self.box_size, self.box_size), pygame.SRCALPHA)

        self.font = pygame.font.Font('assets/BKANT.TTF', 15)

        self.TrashIMG = pygame.image.load('assets/trash-can.png')
        self.TrashIMG = pygame.transform.scale(self.TrashIMG, (40, 40))
        self.TrashIMG.set_colorkey(WHITE)

    # draw everything
    def draw(self):
        # print(pygame.mouse.get_pos(), self.Equipped_pos())

        # draw background
        self.game.screen.blit(
            self.font.render("HP: " + str(round(self.game.player.hp)) + "/" + str(round(self.game.player.max_hp)), True,
                             BLACK), ((WIN_WIDTH / 2 + 25), 300))
        self.game.screen.blit(
            self.font.render("MP: " + str(round(self.game.player.mp)) + "/" + str(round(self.game.player.max_mp)), True,
                             BLACK), ((WIN_WIDTH / 2 + 25), 325))
        self.game.screen.blit(
            self.font.render("Attack Damage: " + str(round(self.game.player.CharacterStrength)), True, BLACK),
            ((WIN_WIDTH / 2 + 25), 350))
        self.game.screen.blit(self.font.render("Armor: " + str(round(self.game.player.CharacterArmor)), True, BLACK),
                              ((WIN_WIDTH / 2 + 25), 375))
        self.game.screen.blit(
            self.font.render("Critical Chance: " + str(round(self.game.player.CritChance)) + "%", True, BLACK),
            ((WIN_WIDTH / 2 + 25), 400))
        self.game.screen.blit(
            self.font.render("Critical Bonus: " + str(round(self.game.player.CritBonus)) + "%", True,
                             BLACK), ((WIN_WIDTH / 2 + 25), 425))

        self.game.screen.blit(self.TrashIMG, (595,455))

        # print(self.Get_pos())

        # print(self.EquipedItems[0])

        for i in range(len(self.EquipedItems)):
            if self.EquipedItems[i]:
                pos = pygame.mouse.get_pos()
                pygame.draw.rect(self.game.screen, (180, 180, 180), INVENTORY_EQUIPED_REC_DICT[i])
                self.game.screen.blit(self.EquipedItems[i].resize(self.box_size), INVENTORY_EQUIPED_REC_DICT[i])
                EquippedToolTip = InventoryToolTip(self.game, ((WIN_WIDTH - 500) / 2 + 25), 350, 150, 150,
                                                   self.game.screen, self.EquipedItems[i], INVENTORY_EQUIPED_REC_DICT[i])
                EquippedToolTip.focusCheck(pos)
                EquippedToolTip.showTip()


        #
        # if self.EquipedItems[0] is not None:
        #     # pygame.draw.rect(self.game.screen, (180, 180, 180), INVENTORY_EQUIPED_REC_DICT[0])
        #     pos = pygame.mouse.get_pos()
        #     self.game.screen.blit(self.EquipedItems[0].resize(self.box_size), INVENTORY_EQUIPED_REC_DICT[0])
        #     EquippedToolTip = InventoryToolTip(self.game, ((WIN_WIDTH - 500) / 2 + 25), 350, 150, 150,
        #                                self.game.screen, self.EquipedItems[0], INVENTORY_EQUIPED_REC_DICT[0])
        #     EquippedToolTip.focusCheck(pos)
        #     EquippedToolTip.showTip()
        # if self.EquipedItems[1] is not None:
        #     # pygame.draw.rect(self.game.screen, (180, 180, 180), INVENTORY_EQUIPED_REC_DICT[1])
        #     pos = pygame.mouse.get_pos()
        #     self.game.screen.blit(self.EquipedItems[1].resize(self.box_size), INVENTORY_EQUIPED_REC_DICT[1])
        #     EquippedToolTip = InventoryToolTip(self.game, ((WIN_WIDTH - 500) / 2 + 25), 350, 150, 150,
        #                                self.game.screen, self.EquipedItems[1], INVENTORY_EQUIPED_REC_DICT[1])
        #     EquippedToolTip.focusCheck(pos)
        #     EquippedToolTip.showTip()


        for x in range(self.col):
            for y in range(self.rows):
                # rect = (self.x + (self.box_size + self.border) * x + self.border,
                #         self.y + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                rect = (((WIN_WIDTH-500)/2+25) + (self.box_size + self.border) * x + self.border,
                        self.y + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                rect2 = pygame.Rect(rect)
                # s = pygame.Surface((rect[2], rect2[3]), pygame.SRCALPHA)
                # s.fill((255, 255, 255, 5))
                # self.game.inventorySurface.blit(s, rect)
                # pygame.draw.rect(self.game.inventorySurface, (180, 180, 180), rect)

                if self.items[x][y]:
                    # print(self.items[x][y])
                    self.game.screen.blit(self.items[x][y].resize(self.box_size), rect)
                    pos = pygame.mouse.get_pos()
                    mouserectX = pos[0]#- ((WIN_WIDTH - 500) / 2)
                    mouserectY = pos[1]
                    MousePOS = mouserectX, mouserectY
                    ToolTip = InventoryToolTip(self.game, ((WIN_WIDTH - 500) / 2 + 25), 350, 150, 150,
                                                    self.game.screen, self.items[x][y], rect2)
                    ToolTip.focusCheck(MousePOS)
                    ToolTip.showTip()

    # get the square that the mouse is overi
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()

        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border) - 4
        y = y // (self.box_size + self.border)
        return (x, y)

    def Equipped_pos(self):
        mouse = pygame.mouse.get_pos()

        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border) - 4
        y = y // (self.box_size + self.border)
        return (x, y)
    def checkForAvailableSpace(self):
        for x in range(self.col):
            for y in range(self.rows):
                if not self.items[x][y]:
                    return True


    def Get_First_Empty(self):
        for y in range(self.rows):
            for x in range(self.col):
                if not self.items[x][y]:
                    self.game.availableInventorySpace = True
                    return (x, y)

                else:
                    self.game.availableInventorySpace = False

    # add an item/s
    def Add(self, Item, xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == Item[0].id:
                self.items[x][y][1] += Item[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = Item
                return temp
        else:
            self.items[x][y] = Item

    def Equip(self, Item, xy):
        x, y = xy
        if self.EquipedItems[EquipedPOS_Dict[x, y]]:
            temp = self.EquipedItems[EquipedPOS_Dict[x, y]]
            self.EquipedItems[EquipedPOS_Dict[x, y]] = Item
            return temp
        else:
            self.EquipedItems[EquipedPOS_Dict[x, y]] = Item


    def EquipItem(self, Item):

        self.game.player.itemHP += Item.HP
        self.game.player.max_hp = self.game.player.baseHP + self.game.player.itemHP
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.game.player.HPBarText = str(round(self.game.player.hp)) + "/" + str(round(self.game.player.max_hp))
        self.game.player.HPText = self.font.render(str(self.game.player.HPBarText), True, BLACK, None)


        self.game.player.itemMP += Item.MP
        self.game.player.max_mp = self.game.player.baseMP + self.game.player.itemMP
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.game.player.MPBarText = str(round(self.game.player.mp)) + "/" + str(round(self.game.player.max_mp))
        self.game.player.MPText = self.font.render(str(self.game.player.MPBarText), True, BLACK, None)

        self.game.player.CharacterStrength += Item.AttackDamage
        self.game.player.CharacterArmor += Item.Armor
        self.game.player.CritChance += Item.CritChance
        self.game.player.CritBonus += Item.CritBonus
        self.font = pygame.font.Font('assets/BKANT.TTF', 15)



    def UnequipItem(self, Item):
        self.game.player.itemHP -= Item.HP
        self.game.player.max_hp = self.game.player.baseHP + self.game.player.itemHP
        if self.game.player.hp > self.game.player.max_hp:
            self.game.player.hp = self.game.player.max_hp
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.game.player.HPBarText = str(round(self.game.player.hp)) + "/" + str(round(self.game.player.max_hp))
        self.game.player.HPText = self.font.render(str(self.game.player.HPBarText), True, BLACK, None)

        self.game.player.itemMP -= Item.MP
        self.game.player.max_mp = self.game.player.baseMP + self.game.player.itemMP
        if self.game.player.mp > self.game.player.max_mp:
            self.game.player.mp = self.game.player.max_mp
        self.font = pygame.font.Font('assets/BKANT.TTF', 20)
        self.game.player.MPBarText = str(round(self.game.player.mp)) + "/" + str(round(self.game.player.max_mp))
        self.game.player.MPText = self.font.render(str(self.game.player.MPBarText), True, BLACK, None)

        self.game.player.CharacterStrength -= Item.AttackDamage
        self.game.player.CharacterArmor -= Item.Armor
        self.game.player.CritChance -= Item.CritChance
        self.game.player.CritBonus -= Item.CritBonus
        self.font = pygame.font.Font('assets/BKANT.TTF', 15)


    def CanItemEquipSlot(self, Item, Slot):
        if Item.id == Slot:
            return True
        else:
            return False

    # check whether the mouse in in the grid
    def In_grid(self, x, y):
        if x < 0 or x > (self.col - 1):
            return False
        if y < 0 or y > (self.rows - 1):
            return False
        return True

    def In_Equip_Selection(self, x, y):
        if EquipedPOS_Dict.get((x, y)) is not None:
            return True
        else:
            return False

    def In_Trash_Grid(self, x, y):
        if x == 11 and y == 12:
            return True
        elif x == 12 and y == 12:
            return True
        else:
            return False
