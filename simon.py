import random, sys, time, pygame
from pygame.locals import *

WINDOWWIDTH = 480
WINDOWHEIGHT = 580

WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

YELLOWRECT = pygame.Rect(20, 20, 200, 200)
BLUERECT = pygame.Rect(240, 20, 200, 200)
REDRECT = pygame.Rect(20, 240, 200, 200)
GREENRECT = pygame.Rect(240, 240, 200, 200)

FPS = 40

pygame.init()

BEEP1 = pygame.mixer.Sound('beep1.ogg')
BEEP2 = pygame.mixer.Sound('beep2.ogg')
BEEP3 = pygame.mixer.Sound('beep3.ogg')
BEEP4 = pygame.mixer.Sound('beep4.ogg')

FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Simulate')

BASICFONT = pygame.font.SysFont('tahoma', 24)
infoSurf = BASICFONT.render('Match the pattern by clicking on the button.', 1,WHITE)
infoRect = infoSurf.get_rect()
infoRect.topleft = (10, WINDOWHEIGHT - 50)

def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, (20, 20, 200, 200))
    pygame.draw.rect(DISPLAYSURF, BLUE, (240, 20, 200, 200))
    pygame.draw.rect(DISPLAYSURF, RED, (20, 240, 200, 200))
    pygame.draw.rect(DISPLAYSURF, GREEN, (240, 240, 200, 200))

def drawStartButton():
        startButton = pygame.Rect(140, 190, 200, 100)
        pygame.draw.rect(DISPLAYSURF, BRIGHTGREEN, startButton)
        STARTFONT = pygame.font.SysFont('tahoma', 50)
        startSurface = STARTFONT.render('START', 1, WHITE)
        startRect = startSurface.get_rect(center=(startButton.center))
        DISPLAYSURF.blit(startSurface, startRect)
        return startRect


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW, YELLOWRECT
    elif BLUERECT.collidepoint((x, y)):
        return BLUE, BLUERECT
    elif REDRECT.collidepoint((x, y)):
        return RED, REDRECT
    elif GREENRECT.collidepoint((x, y)):
        return GREEN, GREENRECT
    return None, None

def flashButtonAnimation(color, time):
    if color == YELLOW:
        locationTuple = YELLOWRECT.topleft
        flashColor = BRIGHTYELLOW
        sound = BEEP1
    elif color == BLUE:
        locationTuple = BLUERECT.topleft
        flashColor = BRIGHTBLUE
        sound = BEEP2
    elif color == RED:
        locationTuple = REDRECT.topleft
        flashColor = BRIGHTRED
        sound = BEEP3
    elif color == GREEN:
        locationTuple = GREENRECT.topleft
        flashColor = BRIGHTGREEN
        sound = BEEP4

    sound.play()
    pygame.draw.rect(DISPLAYSURF, flashColor, (locationTuple[0], locationTuple[1], 200, 200))
    pygame.display.update()
    pygame.time.wait(time)
    drawButtons()
    pygame.display.update()

def addToSequence(score, sequence, simonsTurn):
    sequence.append(random.choice((YELLOW, BLUE, RED, GREEN)))
    simonsTurn = False
    moveNum = 0
    return score, sequence, simonsTurn, moveNum

def playSequence():
    for color in sequence:
        pygame.time.wait(250)
        drawButtons()
        pygame.display.update()
        flashButtonAnimation(color, 500)

def addToAnswerSequence(color, answerSequence):
    answerSequence.append(color)
    return answerSequence, moveNum

def gameOverMsg(clickedRect, moveNum, sequence):
    OVERFONT = pygame.font.SysFont('tahoma', 50)
    overSurface = OVERFONT.render('SORRY!', 1, WHITE)
    overRect = overSurface.get_rect(center=(clickedRect.center))
    DISPLAYSURF.blit(overSurface, overRect)
    pygame.display.update()
    pygame.time.wait(500)
    flashButtonAnimation(sequence[moveNum], 2000)
    msgSurface = BASICFONT.render('Game Over', 1, WHITE)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (180, 460)
    DISPLAYSURF.blit(msgSurface, msgRect)
    scoreMsg = f"Your score: {moveNum}"
    scoreSurface = BASICFONT.render(scoreMsg, 1, WHITE)
    scoreRect = scoreSurface.get_rect()
    scoreRect.topleft = (165, 500)
    DISPLAYSURF.blit(scoreSurface, scoreRect)
    pygame.display.update()
    pygame.time.wait(2000)

def checkAnswer(moveNum, sequence, answerSequence, simonsTurn, bestStreak, pregame):
    if sequence[moveNum] != answerSequence[moveNum]:
        gameOverMsg(clickedRect, moveNum, sequence)
        pregame = True
        simonsTurn = True
        moveNum = 0
        sequence = []
        answerSequence = []
        bestStreak = 0
    else:
        flashButtonAnimation(clickedButton, 500)
        if moveNum == len(sequence)-1:
            if moveNum > bestStreak:
                bestStreak = moveNum
            simonsTurn = True
            answerSequence = []
        else:
            moveNum = moveNum + 1
    return moveNum, simonsTurn, answerSequence, bestStreak, sequence, pregame



running = True
pregame = True
simonsTurn = True
score = 0
sequence = []
answerSequence = []
move = 0
moveNum = 0
bestStreak = 0
mouseCount = 0

while running:
    clickedButton = None
    mousex = None
    mousey = None
    DISPLAYSURF.fill(bgColor)
    drawButtons()
    if pregame == True:
        startRect = drawStartButton()
        DISPLAYSURF.blit(infoSurf, infoRect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if pregame == True:
                if startRect.collidepoint((mousex, mousey)):
                    pregame = False
                    DISPLAYSURF.fill(bgColor)
                    drawButtons()
                    pygame.display.update()
            else:
                pregame = False
                clickedButton, clickedRect = getButtonClicked(mousex, mousey)
                answerSequence, moveNum = addToAnswerSequence(clickedButton, answerSequence)
                moveNum, simonsTurn, answerSequence, bestStreak, sequence, pregame = checkAnswer(moveNum, sequence, answerSequence, simonsTurn, bestStreak, pregame)

    pygame.display.update()

    if simonsTurn:
        if pregame == False:
            score, sequence, simonsTurn, moveNum = addToSequence(score, sequence, simonsTurn)
            pygame.time.wait(750)
            playSequence()

    FPSCLOCK.tick(FPS)
