import pygame
import time
import random
import math
from pygame import mixer

# Initialize the game
pygame.init()

# create the display/screen
width = 800
heigh = 600
window = pygame.display.set_mode((width, heigh))

# Titlu
pygame.display.set_caption("Invadatorii Spatiului")

# Iconita
icon = pygame.image.load('poze/weapon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('poze/spaceship.png')
playerX = 0
playerY = 0

# Background
background = pygame.image.load('poze/background.jpg')

#Background sound
mixer.music.load('poze/melodiebackground.mp3')
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

# Inamici
enemyImg = []
enemyX = []
enemyY = []
mersX = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('poze/ufo.png'))
    enemyX.append(random.randint(64, 736))
    enemyY.append(random.randint(64, 100))
    mersX.append(random.randint(64, 736))

# Glont
# Ready = nu poti sa vezi glontul
# Fire = glontul se misca
bulletImg = pygame.image.load('poze/glont.png')
bulletX = 0
bulletY = 400
bullet_state = "ready"

# Cursor invizibil
cursorVizibil = False
pygame.mouse.set_visible(cursorVizibil)

#Scor
score_value=0
font= pygame.font.Font('freesansbold.ttf', 32)

textX=10
textY=10

#Game over

over_font=pygame.font.Font('freesansbold.ttf',64)


def game_over_text():
    over_text= over_font.render("GAME OVER",True,(255,255,255),)
    window.blit(over_text,(200,250))


def show_score():
    score= font.render("Score: "+str(score_value),True,(255,255,255),)
    window.blit(score,(textX,textY))


def player():
    window.blit(playerImg, (playerX, playerY))

# Functia care randeaza inamicul


def enemy():
    window.blit(enemyImg[i], (enemyX[i], enemyY[i]))

# Functia care defineste trasul glontului


def fire_bullet():
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImg, (bulletX+16, bulletY+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


pygame.display.update()
# Game loop
running = True
while running:

    # fundalul
    window.fill((0, 0, 0))
    # background
    window.blit(background, (0, 0))
    playerX = pygame.mouse.get_pos()[0]
    playerY = pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('poze/untitled.wav')
                    bullet_sound.play()
                    # Sincer nu stiu sa explic astea dar gen ia valorile astea pentru o singura data ca sa traga glontul de unde trebuie
                    bulletY = playerY
                    bulletX = playerX
                    fire_bullet()

    # Caracterul urmareste pozitia mouseului
    if(playerX > 736):
        pygame.mouse.set_pos(736, playerY)
    elif(playerX == 0):
        pygame.mouse.set_pos(1, playerY)
    elif(playerY > 536):
        pygame.mouse.set_pos(playerX, 536)


    for i in range(num_of_enemies):

        #Gameover
        if enemyY[i]>500:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        if enemyX[i] % mersX[i] > 2:
            if mersX[i] > enemyX[i]:
                enemyX[i] += 1
            else:
                enemyX[i] -= 1
        else:
            mersX[i] = random.randint(64, 736)
            enemyY[i] += 10
         # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound=mixer.Sound('poze/bum.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(64, 736)
            enemyY[i] = random.randint(64, 100)
        enemy()
    # miscarea glontului
    if bullet_state is "fire":
        fire_bullet()
        bulletY -= 5
    # Daca glontul e la coord.y = 0 sau mai mic atunci poti sa tragi din nou
    if bulletY <= 0:
        bullet_state = "ready"
    player()
    show_score()
    pygame.display.update()
