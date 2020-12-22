# Importing required modules and classes
import pygame
import random
import math
from pygame import mixer

# Color tuples
Gold = (255, 215, 0)
Darkgreen = (34, 139, 34)
Orange = (255, 140, 0)
Black = (0, 0, 0)
white = (255, 255, 255)
# Initialising pygame
pygame.init()

# the window(W,H)
screen = pygame.display.set_mode((800, 600))
# Background image
background = pygame.image.load('galaxy.png')
# Background Music(-1 is used for loop music)
mixer.music.load('vintage.wav')
mixer.music.play(-1)
# Title and icon
pygame.display.set_caption('DS Galaxy')
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)
# Player
playerimg = pygame.image.load('rocket.png')
playerx = 370
playery = 480
playerx_c = 0
# enemies
enemyimg = []
enemyx = []
enemyy = []
enemyx_c = []
enemyy_c = []
numbere = 6
for i in range(numbere):
    enemyimg.append(pygame.image.load('monster.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_c.append(0.5)
    enemyy_c.append(30)

# Bullet
# Ready: cant see bullet on screen
# Fire: Bullet is currently moving
Bulletimg = pygame.image.load('bullet.png')
Bulletx = 0
Bullety = 480
Bulletx_c = 0
Bullety_c = 0.7
Bullet_state = 'Ready'
# Score
scoreval = 0
scr = pygame.font.Font('freesansbold.ttf', 20)
# Gameover Text
govert = pygame.font.Font('freesansbold.ttf', 64)
# Victory Text
victoryt = pygame.font.Font('freesansbold.ttf', 64)
# Play Again Text
againt = pygame.font.Font('freesansbold.ttf', 20)
# Instructions on top
instruction = pygame.font.Font('freesansbold.ttf', 20)


def inst():
    instruct = instruction.render('Use left and right arrows to move, and space to shoot', True, Gold)
    screen.blit(instruct, (180, 10))


def playagain():
    pagain = againt.render('Beat your High score, play again!!!', True, Gold)
    screen.blit(pagain, (225, 320))


def scoreboard(x, y):
    score = scr.render('ScOrE: ' + str(scoreval), True, (255, 215, 0))
    screen.blit(score, (x, y))


def govertext():
    gover = govert.render('GaMe OvEr!!!', True, Darkgreen)
    screen.blit(gover, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = 'Fire'
    screen.blit(Bulletimg, (x + 16, y + 10))


def victorytext():
    victory = victoryt.render('ViCtOrY!!!', True, Orange)
    screen.blit(victory, (240, 250))


# Use of distance formula
def collision(Xe, Ye, Xb, Yb):
    distance = math.sqrt((math.pow(Xe - Xb, 2)) + (math.pow(Ye - Yb, 2)))
    if distance < 27:
        return True
    else:
        return False


# running and closing the game(Game Loop)
# while loop which works till close button isn't clicked
running = True
while running:
    # RGB: Red, Green, Blue (Background color of window)(every value go from 0 to 255)
    screen.fill(Black)
    # background image
    screen.blit(background, (0, 0))
    # Calling instructions
    inst()
    for event in pygame.event.get():
        # clicking close button
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed right or left(pressed or released)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_c = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_c = 0.3
            if event.key == pygame.K_SPACE:
                if Bullet_state is 'Ready':
                    bsound = mixer.Sound('laser.wav')
                    bsound.play()
                    # Fired from rocket so x is same
                    Bulletx = playerx
                    fire_bullet(Bulletx, Bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_c = 0
    # addition and subtraction of coordinates on pressing and releasing
    # Main while loop continued from here
    playerx += playerx_c
    # Checking for boundaries for both enemy and player
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    # Bullet Movement
    if Bullety <= 0:
        Bullety = 480
        Bullet_state = 'Ready'

    if Bullet_state is 'Fire':
        fire_bullet(Bulletx, Bullety)
        Bullety -= Bullety_c
    # Enemy
    for i in range(numbere):
        # Victory
        if scoreval > 20:
            mixer.music.stop()
            victorytext()
            playagain()
            break

        # Gameover
        if enemyy[i] > 440:
            for j in range(numbere):
                enemyy[j] = 9999
            mixer.music.stop()
            govertext()
            playagain()
            break
        enemyx[i] += enemyx_c[i]
        if enemyx[i] <= 0:
            enemyx_c[i] = 0.3
            enemyy[i] += enemyy_c[i]
        elif enemyx[i] >= 736:
            enemyx_c[i] = -0.3
            enemyy[i] += enemyy_c[i]
        # Collision
        collide = collision(enemyx[i], enemyy[i], Bulletx, Bullety)
        if collide:
            explosionSound = mixer.Sound("blast.wav")
            explosionSound.play()
            Bullety = 480
            Bullet_state = "Ready"
            scoreval += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)


    # Player Image
    player(playerx, playery)
    # Score on top left
    scoreboard(10, 10)
    # SETTINGS UPDATE
    pygame.display.update()
