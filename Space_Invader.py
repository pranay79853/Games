import pygame
import random
import math

# ---------------- INITIALIZE ----------------

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")

clock = pygame.time.Clock()

# ---------------- LOAD IMAGES ----------------

background = pygame.image.load("Background.png")
background = pygame.transform.scale(
    background,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

icon = pygame.image.load("UFO.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("Player.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))

enemy_original = pygame.image.load("Enemy.png")
enemy_original = pygame.transform.scale(enemy_original, (64, 64))

bulletImg = pygame.image.load("Bullet.webp")
bulletImg = pygame.transform.scale(bulletImg, (32, 32))

# ---------------- PLAYER ----------------

playerX = 370
playerY = 500

playerX_change = 0
PLAYER_SPEED = 6

# ---------------- ENEMIES ----------------

num_of_enemies = 6

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):

    enemyImg.append(enemy_original)

    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))

    enemyX_change.append(3)
    enemyY_change.append(40)

# ---------------- BULLET ----------------

bulletX = 0
bulletY = playerY

bullet_state = "ready"
bullet_speed = 10

# ---------------- SCORE ----------------

score_value = 0

font = pygame.font.Font("freesansbold.ttf", 32)
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score():
    score = font.render(
        "Score : " + str(score_value),
        True,
        (255, 255, 255),
    )
    screen.blit(score, (10, 10))


def game_over_text():
    text = over_font.render(
        "GAME OVER",
        True,
        (255, 255, 255),
    )
    screen.blit(text, (180, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"

    screen.blit(bulletImg, (x + 16, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(
        (enemyX - bulletX) ** 2 +
        (enemyY - bulletY) ** 2
    )

    return distance < 30


# ---------------- GAME LOOP ----------------

running = True

while running:

    clock.tick(60)

    screen.blit(background, (0, 0))

    # -------- EVENTS --------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_SPEED

            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_SPEED

            if event.key == pygame.K_SPACE:

                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # -------- PLAYER --------

    playerX += playerX_change

    if playerX < 0:
        playerX = 0

    if playerX > 736:
        playerX = 736

    # -------- ENEMIES --------

    for i in range(num_of_enemies):

        # Game Over

        if enemyY[i] > 440:

            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            continue

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision

        collision = isCollision(
            enemyX[i],
            enemyY[i],
            bulletX,
            bulletY,
        )

        if collision:

            bullet_state = "ready"
            bulletY = playerY

            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # -------- BULLET --------

    if bullet_state == "fire":

        fire_bullet(bulletX, bulletY)

        bulletY -= bullet_speed

        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = playerY

    # -------- DRAW --------

    player(playerX, playerY)

    show_score()

    pygame.display.update()

pygame.quit()