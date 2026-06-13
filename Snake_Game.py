import pygame
import random
import math
import os

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Snake")

clock = pygame.time.Clock()

BACKGROUND = (18, 18, 25)
GRID = (30, 30, 40)
HEAD = (80, 255, 120)
BODY = (30, 200, 80)
FOOD = (255, 80, 80)
TEXT = (240, 240, 240)
SHADOW = (0, 0, 0)

title_font = pygame.font.SysFont("Arial", 52, bold=True)
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

HIGH_SCORE_FILE = "snake_highscore.txt"

def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0
    return 0

def save_highscore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_highscore()

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)
next_direction = (1, 0)
score = 0
speed = 5
paused = False
started = False
game_over = False

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)
next_direction = (1, 0)

score = 0
speed = 8

paused = False
started = False
game_over = False


def random_food():
    while True:
        p = (
            random.randint(0, COLS - 1),
            random.randint(0, ROWS - 1),
        )
        if p not in snake:
            return p


food = random_food()


def reset():
    global snake
    global direction
    global next_direction
    global score
    global speed
    global paused
    global game_over
    global food

    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    speed = 8

    paused = False
    game_over = False

    food = random_food()


# -------------------------
# Drawing
# -------------------------
def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


def draw_snake():

    for i, part in enumerate(snake):

        x = part[0] * CELL
        y = part[1] * CELL

        color = HEAD if i == 0 else BODY

        pygame.draw.rect(
            screen,
            color,
            (x + 2, y + 2, CELL - 4, CELL - 4),
            border_radius=7,
        )

        if i == 0:
            eye1 = (x + 7, y + 7)
            eye2 = (x + CELL - 7, y + 7)

            pygame.draw.circle(screen, (0, 0, 0), eye1, 2)
            pygame.draw.circle(screen, (0, 0, 0), eye2, 2)


def draw_food():

    t = pygame.time.get_ticks() / 300

    pulse = 2 + abs(math.sin(t)) * 4

    fx = food[0] * CELL + CELL // 2
    fy = food[1] * CELL + CELL // 2

    pygame.draw.circle(
        screen,
        FOOD,
        (fx, fy),
        int(CELL // 2 - pulse / 2),
    )


def draw_text(text, fnt, color, x, y):

    shadow = fnt.render(text, True, SHADOW)
    screen.blit(shadow, (x + 2, y + 2))

    img = fnt.render(text, True, color)
    screen.blit(img, (x, y))


# -------------------------
# Main Loop
# -------------------------
running = True

while running:

    clock.tick(speed)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if not started:
                started = True

            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_r:
                reset()

            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)

            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)

            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)

            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

    if started and not paused and not game_over:

        direction = next_direction

        hx, hy = snake[0]
        dx, dy = direction

        new_head = (hx + dx, hy + dy)

        if (
            new_head[0] < 0
            or new_head[0] >= COLS
            or new_head[1] < 0
            or new_head[1] >= ROWS
            or new_head in snake
        ):

            game_over = True

            if score > high_score:
                high_score = score
                save_highscore(high_score)

        else:

            snake.insert(0, new_head)

            if new_head == food:

                score += 1

                speed = min(20, 8 + score // 3)

                food = random_food()

            else:
                snake.pop()

    # Draw

    screen.fill(BACKGROUND)

    draw_grid()

    draw_food()

    draw_snake()

    draw_text(f"Score: {score}", font, TEXT, 15, 10)
    draw_text(f"High Score: {high_score}", font, TEXT, 15, 45)

    if not started:

        draw_text(
            "SNAKE",
            title_font,
            (100, 255, 120),
            WIDTH // 2 - 90,
            180,
        )

        draw_text(
            "Press any key to start",
            font,
            TEXT,
            WIDTH // 2 - 130,
            280,
        )

        draw_text(
            "Arrow Keys = Move",
            small_font,
            TEXT,
            WIDTH // 2 - 80,
            340,
        )

        draw_text(
            "P = Pause    R = Restart",
            small_font,
            TEXT,
            WIDTH // 2 - 95,
            370,
        )

    if paused and not game_over:

        draw_text(
            "PAUSED",
            title_font,
            (255, 220, 50),
            WIDTH // 2 - 90,
            HEIGHT // 2 - 30,
        )

    if game_over:

        draw_text(
            "GAME OVER",
            title_font,
            (255, 80, 80),
            WIDTH // 2 - 150,
            HEIGHT // 2 - 50,
        )

        draw_text(
            "Press R to Restart",
            font,
            TEXT,
            WIDTH // 2 - 110,
            HEIGHT // 2 + 20,
        )

    pygame.display.flip()

pygame.quit()