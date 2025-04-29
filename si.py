import math
import random
import pygame

screen_width = 800
screen_height = 500
player_startx = 370
player_starty = 380
enemy_startymin = 50
enemy_startymax = 150
enemy_speedx = 2
enemy_speedy = 20
bullet_speedy = 2
hitbox_distance = 27

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load('background.png')

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = player_startx
playerY = player_starty
playerX_change = 0

player2Img = pygame.image.load('player2.png')
player2X = 400
player2Y = player_starty
player2X_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 7

for i in range(num_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(enemy_startymin, enemy_startymax))
    enemyX_change.append(enemy_speedx)
    enemyY_change.append(enemy_speedy)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = player_starty
bulletX_change = 0
bulletY_change = bullet_speedy
bullet_state = "ready"

bullet2Img = pygame.image.load('bullet.png')
bullet2X = 0
bullet2Y = player_starty
bullet2X_change = 0
bullet2Y_change = bullet_speedy
bullet2_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameover_text():
    over_text = over_font.render("Game Over!", True, (255, 255, 255))
    screen.blit(over_text, (200, 200))

def player(x, y):
    screen.blit(playerImg, (x, y))

def player2(x, y):
    screen.blit(player2Img, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire2(x, y):
    global bullet2_state
    bullet2_state = "fire"
    screen.blit(bullet2Img, (x + 16, y + 10))

def coll(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < hitbox_distance

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire(bulletX, bulletY)
            if event.key == pygame.K_a:
                player2X_change = -2
            if event.key == pygame.K_d:
                player2X_change = 2
            if event.key == pygame.K_LCTRL and bullet2_state == "ready":
                bullet2X = player2X
                fire2(bullet2X, bullet2Y)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_a, pygame.K_d]:
                player2X_change = 0

    playerX += playerX_change
    player2X += player2X_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 64:
        playerX = screen_width - 64

    if player2X <= 0:
        player2X = 0
    elif player2X >= screen_width - 64:
        player2X = screen_width - 64

    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = player_starty
        bullet_state = "ready"

    if bullet2_state == "fire":
        fire2(bullet2X, bullet2Y)
        bullet2Y -= bullet2Y_change
    if bullet2Y <= 0:
        bullet2Y = player_starty
        bullet2_state = "ready"

    for i in range(num_enemy):
        if enemyY[i] > player_starty - 32:
            for j in range(num_enemy):
                enemyY[j] = 2000
            gameover_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speedx
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 64:
            enemyX_change[i] = -enemy_speedx
            enemyY[i] += enemyY_change[i]

        if coll(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = player_starty
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - 64)
            enemyY[i] = random.randint(enemy_startymin, enemy_startymax)

        if coll(enemyX[i], enemyY[i], bullet2X, bullet2Y):
            bullet2Y = player_starty
            bullet2_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - 64)
            enemyY[i] = random.randint(enemy_startymin, enemy_startymax)

        enemy(enemyX[i], enemyY[i], i)
        if bulletY <= 0:
            bulletY = player_starty
            bullet_state = "ready"
        elif bullet_state == "fire":
            fire(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    player2(player2X, player2Y)
    show_score(textX, textY)
    pygame.display.update()