import pygame, sys, random, GameColor
from pygame.locals import *

BOARDWIDTH = 3
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
FPS = 30
BLANK = None

BGCOLOR = GameColor.DARKTURQUOISE
TILECOLOR = GameColor.GREEN
TEXTCOLOR = GameColor.WHITE
BORDERCOLOR = GameColor.WHITE
BASICFONTSIZE = 20

BUTTONCOLOR = GameColor.WHITE
BUTTONTEXTCOLOR = GameColor.BRIGHTBLUE
MESSAGECOLOR = GameColor.WHITE

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slider Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText('newGame', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()
    allMoves = []

    while True:
        slideTo = None
        msg = ""

        if mainBoard == SOLVEDBOARD:
            msg = "Passed"
        drawBoard(mainBoard, msg)
        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spotY = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spotY) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                else:
                    blankX, blankY = getBlankPosition(mainBoard)
                    if spotx == blankX + 1 and spotY == blankY:
                        slideTo = LEFT
                    elif spotx == blankX - 1 and spotY == blankY:
                        slideTo = RIGHT
                    elif spotx == blankX and spotY == blankY + 1:
                        slideTo = UP
                    elif spotx == blankX and spotY == blankY - 1:
                        slideTo = DOWN
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            sliderAnimation(mainBoard, slideTo, 'click tile or press arrow keys to slider', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_SPACE:
            terminate()
        pygame.event.post(event)


def getStartingBoard():
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = None
    return board


def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] is None:
                return x, y


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx +-1][blanky], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blacky = getBlankPosition(board)
    return (move == UP and blacky != len(board[0]) - 1) or \
           (move == DOWN and blacky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMove = [RIGHT, LEFT, UP, DOWN]
    if not isValidMove(board, RIGHT) or lastMove is LEFT:
        validMove.remove(RIGHT)
    if not isValidMove(board, LEFT) or lastMove is RIGHT:
        validMove.remove(LEFT)
    if not isValidMove(board, UP) or lastMove is DOWN:
        validMove.remove(UP)
    if not isValidMove(board, DOWN) or lastMove is UP:
        validMove.remove(DOWN)
    return random.choice(validMove)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + tileX - 1
    top = YMARGIN + (tileY * TILESIZE) + tileY - 1
    return left, top


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return tileX, tileY
    return None, None


def drawTile(tileX, tileY, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tileX, tileY)
    pygame.draw.rect(DISPLAYSURF, TILESIZE, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    texSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    texRect = texSurf.get_rect()
    texRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(texSurf, texRect)


def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, bgcolor)
    texRect = textSurf.get_rect()
    texRect.topleft = top, left
    return textSurf, texRect


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            number = board[tileX][tileY]
            if number is not None:
                drawTile(tileX, tileY, str(number))

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def sliderAnimation(board, direction, message, animationSpeed):
    blackX, blackY = getBlankPosition(board)

    if direction == UP:
        movex = blackX
        movey = blackY + 1
    elif direction == DOWN:
        movex = blackX
        movey = blackY - 1
    elif direction == RIGHT:
        movex = blackX - 1
        movey = blackY
    elif direction == LEFT:
        movex = blackX + 1
        movey = blackY

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (movex, moveTop, TILESIZE, TILESIZE))

    number = board[movex][movey]
    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, number, 0, -i)
        elif direction == DOWN:
            drawTile(movex, movey, number, 0, i)
        elif direction == RIGHT:
            drawTile(movex, movey, number, i, 0)
        elif direction == LEFT:
            drawTile(movex, movey, number, -i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numsliders):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numsliders):
        move = getRandomMove(board, lastMove)
        sliderAnimation(board, move, 'generate new puzzle..', int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for direction in revAllMoves:
        if direction == UP:
            oppositeDir = DOWN
        elif direction == DOWN:
            oppositeDir = UP
        elif direction == RIGHT:
            oppositeDir = LEFT
        elif direction == LEFT:
            oppositeDir = RIGHT
        sliderAnimation(board, oppositeDir, '', int(TILESIZE / 2))
        makeMove(board, oppositeDir)


if __name__ == '__main__':
    main()
