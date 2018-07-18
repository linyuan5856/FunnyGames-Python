import pygame, random, sys
from pygame.locals import *
from GameColor import *

FPS = 30
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

BGCLOCR = BLACK
BOARDCOLOR = HALFBLUE
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = DARKGRAY
COLORS = (HALFBLUE, HALFGREEN, HALFRED, HALFYELLOW)
BRIGHTCOLORS = (BLUE, GREEN, RED, YELLOW)

FONTNAME = 'freesansbold.ttf'
BG_SOUND_NAME1 = 'tetrisb.mid'
BG_SOUND_NAME2 = 'tetrisc.mid'

# Shape
S_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '..00..',
     '.00..',
     '.....'],

    ['.....',
     '..0..',
     '..00.',
     '...0.',
     '.....']]

Z_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.00..',
     '..00.',
     '.....'],

    ['.....',
     '..0..',
     '.00..',
     '.0...',
     '.....']]

I_SHAPE_TEMPLATE = [
    ['..0..',
     '..0..',
     '..0..',
     '..0..',
     '.....'],

    ['.....',
     '.....',
     '0000.',
     '.....',
     '.....']]

O_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.00..',
     '.00..',
     '.....']]

J_SHAPE_TEMPLATE = [
    ['.....',
     '.0...',
     '.000.',
     '.....',
     '.....'],

    ['.....',
     '..00.',
     '..0..',
     '..0..',
     '.....'],

    ['.....',
     '.....',
     '.000.',
     '...0.',
     '.....'],

    ['.....',
     '..0..',
     '..0..',
     '.00..',
     '.....']]

L_SHAPE_TEMPLATE = [
    ['.....',
     '...0.',
     '.000.',
     '.....',
     '.....'],

    ['.....',
     '..0..',
     '..0..',
     '..00.',
     '.....'],

    ['.....',
     '.....',
     '.00..',
     '.0...',
     '.0...'],

    ['.....',
     '.00..',
     '.0...',
     '.0...',
     '.....']]

T_SHAPE_TEMPLATE = [
    ['.....',
     '..0..',
     '.000.',
     '.....',
     '.....'],

    ['.....',
     '..0..',
     '..00.',
     '..0..',
     '.....'],

    ['.....',
     '.....',
     '.000.',
     '..0..',
     '.....'],

    ['.....',
     '..0..',
     '.00..',
     '..0..',
     '.....']]

SHAPES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE
          }


def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, BIGFONT

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('俄罗斯方块')
    FPSCLOCK = pygame.time.Clock()

    BIGFONT = pygame.font.Font(FONTNAME, 100)
    BASICFONT = pygame.font.Font(FONTNAME, 18)

    if random.randint(0, 1) == 0:
        pygame.mixer.music.load(BG_SOUND_NAME1)
    else:
        pygame.mixer.music.load(BG_SOUND_NAME2)
    pygame.mixer.music.play(-1, 0.0)

    while True:
        runGame()
        showTextScreen('Game Over')


def runGame():
    checkForQuit()
    DISPLAYSURF.fill(BGCLOCR)
    FPSCLOCK.tick(FPS)
    pygame.display.update()


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    pass


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def calculateLevelAndFallFraq(score):
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -5,
                'color': random.randint(0, len(COLORS) - 1)
                }
    return newPiece


def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES['shape'][piece['rotation']][y][x] != BLANK:
                board[x + piece['x'], y + piece['y']] = piece['color']


def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x > 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    pass


def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False

    return True


def removeCompleteLines(board):
    pass


def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy + (boxy * BOXSIZE)))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    pass


def drawBoard(board):
    pass


def drawStatus():
    pass


def drawPiece(piece, pixelx=None, pixely=None):
    pass


def drawNextPiece(piece):
    pass


if __name__ == '__main__':
    main()
