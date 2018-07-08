import pygame, random, sys
from GameColor import *
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60

global DISPLAYER_SURF
pygame.init()
DISPLAYER_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Memory Puzzle')
FPSCLOCK = pygame.time.Clock()

while True:

    pygame.display.update()
    DISPLAYER_SURF.fill(BLUE)

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    FPSCLOCK.tick(FPS)
