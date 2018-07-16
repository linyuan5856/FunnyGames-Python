import pygame, sys, random, time
from pygame.locals import *
import GameColor

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 500
BUTTONGAPSIZE = 20
TIMEOUT = 4

bgColor = GameColor.BLACK

XMARGIN = int((WINDOWWIDTH - (BUTTONSIZE * 2) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (BUTTONSIZE * 2) - BUTTONGAPSIZE) / 2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONGAPSIZE + BUTTONSIZE, BUTTONSIZE,
                        BUTTONSIZE)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q,W,A,S keys.', 1,
                                GameColor.DARKGRAY)

    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    pattern = []
    currentStep = 0
    lastClickTIme = 0
    score = 0
    waitingForInput = False
    while True:
        clickedButton = None
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score:' + str(score), 1, GameColor.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = GameColor.HALFYELLOW
                elif event.key == K_w:
                    clickedButton = GameColor.HALFBLUE
                elif event.key == K_a:
                    clickedButton = GameColor.HALFGREEN
                elif event.key == K_s:
                    clickedButton = GameColor.HALFRED

        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(
                random.choice((GameColor.HALFYELLOW, GameColor.HALFGREEN, GameColor.HALFRED, GameColor.HALFBLUE)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTIme = time.time()

                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0

            elif (clickedButton and clickedButton != pattern[currentStep]) or (
                    currentStep != 0 and time.time() - TIMEOUT > lastClickTIme):
                gameOverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flashButtonAnimation(color, animationSpeed=50):
    if color == GameColor.HALFYELLOW:
        sound = BEEP1
        flashColor = GameColor.YELLOW
        rectangle = YELLOWRECT
    elif color == GameColor.HALFBLUE:
        sound = BEEP2
        flashColor = GameColor.BLUE
        rectangle = BLUERECT
    elif color == GameColor.HALFRED:
        sound = BEEP3
        flashColor = GameColor.RED
        rectangle = REDRECT
    elif color == GameColor.HALFGREEN:
        sound = BEEP4
        flashColor = GameColor.GREEN
        rectangle = GREENRECT

    orignSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()

    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(orignSurf, (0, 0))
            flashSurf.fill((r, g, b,alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(orignSurf, (0, 0))


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, GameColor.HALFYELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, GameColor.HALFBLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, GameColor.HALFGREEN, GREENRECT)
    pygame.draw.rect(DISPLAYSURF, GameColor.HALFRED, REDRECT)


def changeBackgroundAnimation(animationSPeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor

    for alpha in range(0, 255, animationSPeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(Color=GameColor.WHITE, animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = Color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return GameColor.HALFYELLOW
    elif REDRECT.collidepoint(((x, y))):
        return GameColor.HALFRED
    elif BLUERECT.collidepoint(((x, y))):
        return GameColor.HALFBLUE
    elif GREENRECT.collidepoint(((x, y))):
        return GameColor.HALFGREEN


if __name__ == '__main__':
    main()
