import pygame


class Inventory:
    def __init__(self, game):
        self.rows = 9
        self.col = 5
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 33
        self.x = 26
        self.y = 22
        self.border = 3
        self.game = game

    # draw everything
    def draw(self):
        # draw background
        pygame.draw.rect(self.game.inventorySurface, (100, 100, 100),
                         (self.x, self.y, (self.box_size + self.border) * self.col + self.border,
                          (self.box_size + self.border) * self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border) * x + self.border,
                        self.x + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                pygame.draw.rect(self.game.inventorySurface, (180, 180, 180), rect)
                if self.items[x][y]:
                    self.game.inventorySurface.blit(self.items[x][y].resize(self.box_size), rect)

    # get the square that the mouse is over
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()

        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border) - 4
        y = y // (self.box_size + self.border)
        return (x, y)

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

    # check whether the mouse in in the grid
    def In_grid(self, x, y):
        if x < 0 or x > (self.col - 1):
            return False
        if y < 0 or y > (self.rows - 1):
            return False
        return True
        # if 0 > x > self.col - 1:
        #     return False
        # if 0 > y > self.rows - 1:
        #     return False

