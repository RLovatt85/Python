# pyright: reportMissingImports=false
import pygame
import random
import math
import time

from pygame import mixer

# intialize the pygame
pygame.init()

# creating the screen
# pygame.display.set_mode((width,height or x and y)) in px
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space.jpg')

# background music
mixer.music.load('backgroundwar.wav')
mixer.music.play(-1)

# Title and Icon
# icon must be 32 x 32 px and loaded into game file location!!!
pygame.display.set_caption("UFO Skeet Shoot")
icon = pygame.image.load('ufoicon.png')
pygame.display.set_icon(icon)

# player
# 64 x 64 px and loaded into game file location
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 500))
    enemyY.append(random.randint(0, 90))
    enemyX_change.append(5)
    enemyY_change.append(12.5)

    # laser
    # ready-state - you can't see the bullet on the screen
    # fire - the laser is currently moving
    laserImg = pygame.image.load('laserblast.png')
    laserX = 0
    laserY = 480
    laserX_change = 0
    laserY_change = 10
    laser_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('8bitfont.ttf', 20)

textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('8bitfont.ttf', 72)


def game_over_text():
    print("calling game over text")

    over_text = over_font.render("GAME OVER", True, (175, 0, 0))
    # over_text2 = over_font.render("WE LOST", True, (255, 255, 255))
    screen.blit(over_text, (50, 200))
    # screen.blit(over_text2, (135, 440))
    mixer.music.stop()
    # mixer.Sound('explosion.wav').play()
    # time.sleep(10)


def show_score(x, y):
    score = font.render("SCORE:  " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt(math.pow(enemyX - laserX, 2) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    # controls movement of Y automatically - no control >>>playerY -= .2
    # controls movement of X automatically - no control >>>playerX += .2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it is right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            # if event.key == pygame.K_UP:
            # playerY_change = -3
            # if event.key == pygame.K_DOWN:
            # playerY_change = 3
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    # get the current x coordinate of the spaceship
                    laserX = playerX
                    laserY = playerY
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # if event.type == pygame.KEYUP:
        # if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
        # playerY_change = 0

    # 5 = 5 + -0.3(steps or speed of moving) -> 5 = 5 - 0.3
    # 5 = 5 + 0.3

    # checking for boundaries of space so it doens't go out of bounds
    playerX += playerX_change
    playerY += playerY_change

    # 800 - 64 px for the image size
    # if playerX = 0 comes from other side of screen

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        print("first for loop")
        # GAME OVER

        if enemyY[i] > playerX:

            for j in range(num_of_enemies):
                enemyY[j] = 2000
                # playerY = 100
                # playerX = 350
                pygame.K_SPACE = False
                # playerImg = pygame.image.load('explode.png')

            game_over_text()
            # time.sleep(6)
            # exit(0)

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

            # collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explode_sound = mixer.Sound('explosion.wav')
            explode_sound.play()
            laserY = 480
            laser_state = "ready"
            # enemy(enemyX[i], enemyY[i], i) = pygame.image.load('explode.png')

            score_value += 1
            # print(score_value)
            enemyX[i] = random.randint(0, 500)
            enemyY[i] = random.randint(0, 90)

        enemy(enemyX[i], enemyY[i], i)

    # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # needs to be constantly updating
    pygame.display.update()