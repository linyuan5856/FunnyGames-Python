import random, sys, pygame
from pygame.locals import *
from GameColor import *

FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, '宽度和Grid宽度不能整除'
assert WINDOWHEIGHT % CELLSIZE == 0, '高度和Grid高度不能整除'

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
FONTNAME = 'freesansbold.ttf'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('贪吃蛇')
    BASICFONT = pygame.font.Font(FONTNAME, 18)
    FPSCLOCK = pygame.time.Clock()

    showStartScreen()

    while True:
        runGame()
        showGameOverScreen()


def runGame():
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    direction = RIGHT

    apple = getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif (event.key == K_w or event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_s or event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif (event.key == K_a or event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_d or event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT

        head = wormCoords[HEAD]
        if head['x'] == -1 or head['x'] == CELLWIDTH or head['y'] == -1 or head['y'] == CELLHEIGHT:
            print('越界')
            return  # DEAD 出边界

        for wormBody in wormCoords[1:]:
            if wormBody['x'] == head['x'] and wormBody['y'] == head['y']:
                print('撞车')
                return  # DEAD 头尾撞

        if head['x'] == apple['x'] and head['y'] == apple['y']:  # eat a apple
            apple = getRandomLocation()
        else:
            del wormCoords[-1]

        if direction == UP:
            newhead = {'x': head['x'], 'y': head['y'] - 1}
        elif direction == DOWN:
            newhead = {'x': head['x'], 'y': head['y'] + 1}
        elif direction == LEFT:
            newhead = {'x': head['x'] - 1, 'y': head['y']}
        elif direction == RIGHT:
            newhead = {'x': head['x'] + 1, 'y': head['y']}

        wormCoords.insert(0, newhead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawApple(apple)
        drawWorm(wormCoords)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('press a key to play', True, GRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()

    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font(FONTNAME, 100)
    titleSurf1 = titleFont.render('Worm', True, WHITE, HALFGREEN)
    titleSurf2 = titleFont.render('Worm', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf1.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        if checkForKeyPress():
            pygame.event.get()
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        degrees1 += 3
        degrees2 += 8


def terminate():
    pygame.init()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font(FONTNAME, 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score:%s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x']*CELLSIZE
        y = coord['y']*CELLSIZE
        rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, HALFGREEN, rect)
        innerRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, innerRect)


def drawApple(coord):
    x = coord['x']*CELLSIZE
    y = coord['y']*CELLSIZE
    rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, rect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
