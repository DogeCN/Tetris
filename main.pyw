#Main codes to start the game

from game import *
import sys

def init():
    global GameFrame, Clock, KeyActions
    pygame.init()
    pygame.display.set_caption('Tetris')
    pygame.key.set_repeat(200, 15)
    Display = pygame.display.set_mode((Width*10, Height*13))
    GameFrame = Game(Display)
    Clock = pygame.time.Clock()
    KeyActions = [False for i in range(4)]
init()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            GameFrame.scoreFlie(GameFrame.score)
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                KeyActions[0] = True
            elif event.key == K_RIGHT:
                KeyActions[1] = True
            elif event.key == K_DOWN:
                KeyActions[2] = True
            elif event.key == K_SPACE:
                KeyActions[3] = True
    GameFrame.update()
    GameFrame.draw()
    Clock.tick(60)
    pygame.display.update()
