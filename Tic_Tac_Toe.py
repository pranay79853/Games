import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 600
ROWS, COLS = 3, 3
CELL_SIZE = GRID_SIZE // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
BLUE = (50, 100, 255)
RED = (220, 50, 50)
GREEN = (50, 180, 50)
GRAY = (240, 240, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - 2 Players")

font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 80)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner = None
win_line = None
end_time = None


def draw_grid():
    screen.fill(WHITE)

    for i in range(1, 3):
        pygame.draw.line(
            screen, BLACK,
            (0, i * CELL_SIZE),
            (GRID_SIZE, i * CELL_SIZE),
            5
        )
        pygame.draw.line(
            screen, BLACK,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, GRID_SIZE),
            5
        )


def draw_marks():
    padding = 40

    for row in range(3):
        for col in range(3):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if board[row][col] == "X":
                pygame.draw.line(
                    screen,
                    RED,
                    (x + padding, y + padding),
                    (x + CELL_SIZE - padding, y + CELL_SIZE - padding),
                    8,
                )
                pygame.draw.line(
                    screen,
                    RED,
                    (x + CELL_SIZE - padding, y + padding),
                    (x + padding, y + CELL_SIZE - padding),
                    8,
                )

            elif board[row][col] == "O":
                pygame.draw.circle(
                    screen,
                    BLUE,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    CELL_SIZE // 2 - padding,
                    8,
                )


def check_winner():
    global winner, game_over, win_line

    # Rows
    for r in range(3):
        if (
            board[r][0]
            and board[r][0] == board[r][1] == board[r][2]
        ):
            winner = board[r][0]
            game_over = True
            y = r * CELL_SIZE + CELL_SIZE // 2
            win_line = ((30, y), (GRID_SIZE - 30, y))
            return

    # Columns
    for c in range(3):
        if (
            board[0][c]
            and board[0][c] == board[1][c] == board[2][c]
        ):
            winner = board[0][c]
            game_over = True
            x = c * CELL_SIZE + CELL_SIZE // 2
            win_line = ((x, 30), (x, GRID_SIZE - 30))
            return

    # Main diagonal
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
        game_over = True
        win_line = ((30, 30), (GRID_SIZE - 30, GRID_SIZE - 30))
        return

    # Other diagonal
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        game_over = True
        win_line = ((GRID_SIZE - 30, 30), (30, GRID_SIZE - 30))
        return

    # Draw
    full = True
    for row in board:
        for cell in row:
            if cell == "":
                full = False

    if full:
        winner = "Draw"
        game_over = True


def draw_status():
    pygame.draw.rect(screen, GRAY, (0, 600, WIDTH, 100))

    if winner == "Draw":
        text = font.render("Draw!", True, BLACK)
    elif winner:
        text = font.render(f"{winner} Wins!", True, GREEN)
    else:
        text = font.render(f"Turn: {current_player}", True, BLACK)

    rect = text.get_rect(center=(WIDTH // 2, 650))
    screen.blit(text, rect)


def draw_win_line():
    if win_line:
        pygame.draw.line(screen, GREEN, win_line[0], win_line[1], 10)


def reset_game():
    global board, current_player, game_over, winner, win_line, end_time

    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None
    win_line = None
    end_time = None


clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not game_over
        ):
            mx, my = pygame.mouse.get_pos()

            if my < GRID_SIZE:
                row = my // CELL_SIZE
                col = mx // CELL_SIZE

                if board[row][col] == "":
                    board[row][col] = current_player

                    check_winner()

                    if game_over:
                        end_time = pygame.time.get_ticks()
                    else:
                        current_player = (
                            "O" if current_player == "X" else "X"
                        )

    if game_over and end_time:
        if pygame.time.get_ticks() - end_time > 3000:
            reset_game()

    draw_grid()
    draw_marks()

    if game_over and winner != "Draw":
        draw_win_line()

    draw_status()

    pygame.display.flip()