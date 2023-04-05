import sys
import pygame
from pygame.locals import *
import os
from importlib.machinery import SourceFileLoader

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets") 

main_menu = SourceFileLoader('main', os.path.join(main_dir, 'main.py')).load_module()
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
board = [[None, None, None], [None, None, None], [None, None, None]]

pygame.font.init()
FONT = pygame.font.Font(None, 40)

x_sound = pygame.mixer.Sound(os.path.join(assets_dir, "x.wav"))
o_sound = pygame.mixer.Sound(os.path.join(assets_dir, "o.wav"))
music = pygame.mixer.Sound(os.path.join(assets_dir, "3am.wav"))

def display_text(text, x, y, color=BLACK, bg_color=WHITE):
    rendered_text = FONT.render(text, True, color)
    text_rect = rendered_text.get_rect()
    text_rect.center = (x, y)
    
    # Draw a white rectangle behind the text
    bg_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(DISPLAY, bg_color, bg_rect)
    
    DISPLAY.blit(rendered_text, text_rect)



def check_win(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def check_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                return False
    return True

def draw_board():
    for i in range(1, 3):
        pygame.draw.line(DISPLAY, LINE_COLOR, (WIDTH // 3 * i, 0), (WIDTH // 3 * i, HEIGHT), 5)
        pygame.draw.line(DISPLAY, LINE_COLOR, (0, HEIGHT // 3 * i), (WIDTH, HEIGHT // 3 * i), 5)

def draw_xo(row, col, player):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6
    if player == "X":
        x_sound.play()
        pygame.draw.line(DISPLAY, BLACK, (x - 50, y - 50), (x + 50, y + 50), 10)
        pygame.draw.line(DISPLAY, BLACK, (x + 50, y - 50), (x - 50, y + 50), 10)
    elif player == "O":
        o_sound.play()
        pygame.draw.circle(DISPLAY, BLACK, (x, y), 60, 10)

def main():
    pygame.init()
    game_over = False
    player_turn = "X"
    winner = None
    DISPLAY.fill(WHITE)


    while not game_over:
        draw_board()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row, col = y // (HEIGHT // 3), x // (WIDTH // 3)

                if board[row][col] is None:
                    draw_xo(row, col, player_turn)
                    board[row][col] = player_turn

                    winner = check_win(board)
                    if winner:
                        game_over = True
                    elif check_draw(board):
                        winner = "DRAW"
                        game_over = True
                    else:
                        player_turn = "O" if player_turn == "X" else "X"

        if game_over:
            if winner == "DRAW":
                display_text("It's a draw!", WIDTH // 2, HEIGHT // 2)
            else:
                display_text(f"{winner} wins!", WIDTH // 2, HEIGHT // 2)
            pygame.display.update()
            pygame.time.delay(5000)  # Delay for 5000 milliseconds (5 seconds)

        pygame.display.update()
        fpsClock.tick(FPS)
    main_menu.main(False)


if __name__ == "__main__":
    music.play(loops=-1)
    main()