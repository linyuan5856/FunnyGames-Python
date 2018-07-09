import pygame, random, sys
from GameColor import *
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 4
BOARDHEIGHT = 3

assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0, '边界必须是偶数'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDHEIGHT * BOARDWIDTH, "颜色总数 和 格子总数不匹配"


def main():
    global DISPLAYER_SURF, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYER_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mouseX = 0
    mouxeY = 0
    pygame.display.set_caption('Memory Puzzle')

    mainboard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxedData(False)

    firstSelection = None
    DISPLAYER_SURF.fill(BGCOLOR)
    startGameAnimation(mainboard)

    while True:
        mouseClicked = False
        DISPLAYER_SURF.fill(BGCOLOR)
        drawBoard(mainboard, revealedBoxes)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEMOTION:
                mouseX, mouxeY = e.pos
            elif e.type == MOUSEBUTTONUP:
                mouseX, mouxeY = e.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mouseX, mouxeY)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighLightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainboard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainboard,boxx, boxy)
                    icon2shape, icon2color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainboard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainboard)
                        pygame.time.wait(2000)

                        mainboard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxedData(False)
                        drawBoard(mainboard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainboard)
                        firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxedData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    numIconUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    icons = icons[:numIconUsed] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == DONUT:
        pygame.draw.circle(DISPLAYER_SURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYER_SURF, color, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYER_SURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYER_SURF, color,
                            ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1),
                             (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYER_SURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYER_SURF, color, (left + i, top + BOXSIZE - i), (left + BOXSIZE - i, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYER_SURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYER_SURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shaper, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shaper, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYER_SURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, -1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYER_SURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighLightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYER_SURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE - 10), 4)


def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxedData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxedData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYER_SURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


if __name__ == '__main__':
    main()
