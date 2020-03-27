import pygame
import random
#pylint: disable=no-member

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("github.com/erkkke")
pygame.display.set_icon(pygame.image.load("logo.png"))

background_img = pygame.image.load("background.jpg")
life_img = pygame.image.load("life.png")
GameOver_img = pygame.image.load("GameOver.png")

# Player
player_img = pygame.image.load("player.png")
player_x, player_y = 200, 500
player_dx = 3

# Enemy
enemy_img = pygame.image.load("enemy.png")
enemy_x, enemy_y = random.randint(0, 736), random.randint(20, 50)
enemy_dx, enemy_dy = 5, 50

# Laser
laser_img = pygame.image.load("laser.png")
laser_x, laser_y = 0, 0
laser_dy = -7

# Essentials
isLaser = False
isGameOver = False
score = 0
life = 3

# Functions
def laser(x, y):
    screen.blit(laser_img, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def Score():
    font = pygame.font.SysFont('microsofttaile', 24)
    text = font.render(f'Score: {score}', 1, (255, 255, 255))
    screen.blit(text, (800 - text.get_width() - 20, 20))

def Life():
    for i in range(0, life):
        screen.blit(life_img, (20 + (26 * i), 20))

def GameOver():
    screen.blit(GameOver_img, (0,0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    pressed = pygame.key.get_pressed()

    # Laser shot
    if pressed[pygame.K_SPACE] and not isLaser:
        isLaser = True
        laser_y = player_y - 20
        laser_x = player_x + 30

    if isLaser:
        laser_y += laser_dy

    if laser_y < 0:
        isLaser = False
    
    # Ship movement
    if pressed[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_dx

    if pressed[pygame.K_RIGHT]:
        if player_x < 736:
            player_x += player_dx

    if pressed[pygame.K_UP]:
        if player_y >= 300:
            player_y -= player_dx
    
    if pressed[pygame.K_DOWN]:
        if player_y <= 530:
            player_y += player_dx
        

    # Enemy movement
    enemy_x += enemy_dx

    if enemy_x < 0 or enemy_x > 736:
        enemy_dx = -enemy_dx
        enemy_y += enemy_dy

    # Win collision
    if isLaser:
        wcol_x = enemy_x - laser_x
        wcol_y = enemy_y - laser_y
        if -64 <= wcol_x <= 5 and -64 <= wcol_y <= 25:
             score += 1
             isLaser = False
             enemy_x, enemy_y = random.randint(0, 736), random.randint(20, 50)
    
    # Loss collision
    lcol_x = enemy_x - player_x
    lcol_y = enemy_y - player_y
    if -64 <= lcol_x <= 64 and -64 <= lcol_y <= 64:
        life -= 1
        enemy_x, enemy_y = random.randint(0, 736), random.randint(20, 50)
        player_x, player_y = 200, 500

    # Game Over
    if life == 0:
        isGameOver = True
        GameOver()
        if pressed[pygame.K_TAB]:
            isGameOver = False
            enemy_x, enemy_y = random.randint(0, 736), random.randint(20, 50)
            player_x, player_y = 200, 500
            life = 3
            score = 0

    # Condition to start and restart the game
    if not isGameOver:
        screen.blit(background_img, (0, 0))
        player(player_x, player_y)
        enemy(enemy_x, enemy_y)
        Score()
        Life()
        if isLaser: laser(laser_x, laser_y)

    pygame.display.flip()