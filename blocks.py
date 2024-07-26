#Contrling the blocks movement

import pygame
from pygame.locals import *
from attribute import *

class Block(pygame.sprite.Sprite):
    def __init__(self, type, i, row=0, col=0):
        super().__init__()
        self.image = pygame.image.load('./images/{0}.png'.format(BlockList[type]))
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.i = i
        self.remove = False

    def update(self):
        self.rect.center = (self.row*Width+Width//2, self.col*Height+Height//2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Group(object):
    def __init__(self, type, shape, pos=(4,-3)):
        super().__init__()
        self.row = pos[0]
        self.col = pos[1]
        self.shape = shape
        self.type = type
        self.tick = 0
        self.rotation = 0
        self.poped = False
        self.blocks = [Block(self.type, i) for i in range(4)]

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    def update(self):
        self.tick += 1
        if self.tick >= 30:
            self.down()
            self.tick = 0
        self.key_event()
        for block in self.blocks:
            block.row = Shapes[self.shape][self.rotation][block.i][0]+self.row
            block.col = Shapes[self.shape][self.rotation][block.i][1]+self.col
            block.update()

    def key_event(self):
        from main import KeyActions
        from main import GameFrame
        PopedPoses = GameFrame.getPopedPoses()
        if KeyActions[2]:
            self.down()
            KeyActions[2] = False
        elif KeyActions[0]:
            if False not in [block.row > 0 and (block.row-1, block.col) not in PopedPoses for block in self.blocks]:
                self.row -= 1
            KeyActions[0] = False
        elif KeyActions[1]:
            if False not in [block.row < 9 and (block.row+1, block.col) not in PopedPoses for block in self.blocks]:
                self.row += 1
            KeyActions[1] = False
        elif KeyActions[3]:
            self.rotate()
            KeyActions[3] = False

    def down(self):
        from main import GameFrame
        if False not in [block.col < 12 and (block.row, block.col+1) not in GameFrame.getPopedPoses() for block in self.blocks]:
            self.col += 1
        else:
            self.poped = True

    def rotate(self):
        from main import GameFrame
        self.rotation += 1
        if self.rotation >= len(Shapes[self.shape]):
            self.rotation = 0
        for block in self.blocks:
            FuturePos = Shapes[self.shape][self.rotation][block.i]
            FuturePos = (FuturePos[0]+self.row, FuturePos[1]+self.col)
            if FuturePos[0] < 0 or FuturePos[0] > 9 or FuturePos[1] > 12 or FuturePos in GameFrame.getPopedPoses():
                self.rotation -= 1
                break
