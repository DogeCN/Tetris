#A frame of the game

from blocks import *
import random as r

class Game(object):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.BlockGroup = Group(r.randint(0, 6), r.randint(0, 6))
        self.PopedBlocks = []
        self.score = 0
        self.maxScore = self.scoreFlie()
        self.faild = False

    def draw(self):
        self.surface.fill((0, 0, 0))
        for PB in self.PopedBlocks:
            PB.draw(self.surface)
        self.BlockGroup.draw(self.surface)
        font1 = pygame.font.SysFont('Microsoft YaHei UI', 20, True)
        score = font1.render('Score: ' + str(self.score), True, BlockList[self.BlockGroup.type])
        self.surface.blit(score, (10, 10))
        maxScore = font1.render('Best Score: ' + str(self.maxScore), True, BlockList[self.BlockGroup.type])
        self.surface.blit(maxScore, (370-len(str(self.maxScore))*12, 10))
        if self.faild:
            font2 = pygame.font.SysFont('Microsoft YaHei UI', 40, True)
            font3 = pygame.font.SysFont('Microsoft YaHei UI', 20)
            text = font2.render('Game Over', True, BlockList[self.BlockGroup.type])
            tip = font3.render('Press Space to Restart', True, BlockList[self.BlockGroup.type])
            self.surface.blit(text, (150, 200))
            self.surface.blit(tip, (160, 300))

    def update(self):
        if self.faild:
            from main import KeyActions
            if KeyActions[3]:
                self.scoreFlie(self.score)
                self.__init__(self.surface)
            return
        if self.BlockGroup.poped:
            self.PopedBlocks += self.BlockGroup.blocks
            self.BlockGroup = Group(r.randint(0, 6), r.randint(0, 6))
        pygame.display.set_icon(self.BlockGroup.blocks[0].image)
        self.BlockGroup.update()
        self.clearLine()
        for PB in self.PopedBlocks:
            if PB.col <= 0:
                self.faild = True
        if self.score > self.maxScore:
            self.maxScore = self.score

    def getPopedPoses(self):
        PopedPoses = []
        for PB in self.PopedBlocks:
            PopedPoses.append((PB.row, PB.col))
        return PopedPoses

    def clearLine(self):
        total = 0
        for c in range(13):
            BlocksinLine = []
            for PB in self.PopedBlocks:
                if PB.col == c:
                    BlocksinLine.append(PB)
            if len(BlocksinLine) == 10:
                for B in BlocksinLine:
                    self.PopedBlocks.remove(B)
                total += 1
                for PB in self.PopedBlocks:
                    if PB.col < c:
                        PB.col += 1
                        PB.update()
        self.score += total**2
            

    def scoreFlie(self, score=0):
        if score != 0:
            with open('score.d', 'a', encoding='ascii') as s:
                s.write(bin(self.score) + '\n')
        else:
            with open('score.d', 'r', encoding='ascii') as s:
                scores = [int(line, 2) for line in s.readlines()]
                if scores:
                    return max(scores)
                else:
                    return 0
