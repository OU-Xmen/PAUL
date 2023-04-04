try:
    import pygame
    pygame.init()
    import os
    import sys
    import time
    import random
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, 'assets')
    B = SourceFileLoader('CheckersBoard', os.path.join(maindirectory, 'CheckersBoard.py')).load_module()
    CP = SourceFileLoader('CheckersPiece', os.path.join(maindirectory, 'CheckersPiece.py')).load_module()
    main_menu = SourceFileLoader('main', os.path.join(maindirectory, "..", "main.py")).load_module()
except ImportError as e:
    print("One or more modules failed to load")
    print(e)
    quit()

# create 800x600 window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Checkers')
icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
background = pygame.image.load(os.path.join(assetdirectory, 'background.png'))
pygame.display.set_icon(icon)

# initialize font and text objects
black = (0, 0, 0)
haha_funny = pygame.font.SysFont('comicsansms', 50)
def init_words(text, center_x, center_y, color):
    temp_rend = pygame.font.Font.render(haha_funny, text, True, color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect

red_win_rend, red_win_rect = init_words('You win!', width-140, 80, 'red')
black_win_rend, black_win_rect = init_words('You Win!', width-140, 80, black)
pause_rend, pause_rect = init_words('Pause', width-140, 440, black)
resume_rend, resume_rect = init_words('Resume', width-140, 440, black)
quit_rend, quit_rect = init_words('Quit', width-140, 520, black)
play_again_rend, play_again_rect = init_words('Play Again', width-140, 440, black)

def pause_menu(game_board):
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))
        screen.blit(resume_rend, resume_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(mouse):
                    return False
                if quit_rect.collidepoint(mouse):
                    game_board.shut_up()
                    main_menu.main(False)
                    quit()

def play_again_menu(winner):
    while True:
        mouse = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        if winner == 'Red':
            screen.blit(red_win_rend, red_win_rect)
        elif winner == 'Black':
            screen.blit(black_win_rend, black_win_rect)
        screen.blit(play_again_rend, play_again_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(mouse):
                    # restart the game
                    return True
                if quit_rect.collidepoint(mouse):
                    return False

def main():
    game_board = B.Board()
    whose_turn = 0 # start with black
    what_to_do = False

    while True: # game loop
        bruh = False
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.blit(background, (0, 0))
        game_board.draw_board(screen)
        screen.blit(pause_rend, pause_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(mouse):
                    what_to_do = pause_menu(game_board)
                elif mouse_on_board:
                    piece_clicked = game_board.board[mouse_ij[0]][mouse_ij[1]]
                    if piece_clicked.id and piece_clicked.id == ('B', 'R')[whose_turn]:
                        made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                        if made_move:
                            whose_turn = 1 - whose_turn
        
        if what_to_do: break

        screen.blit(background, (0, 0))
        game_board.draw_board(screen)
        screen.blit(pause_rend, pause_rect)
        pygame.display.flip()

        break_flag = False
        bruh = game_board.test_for_win()
        if bruh:
            if bruh == 'R': bruh = 'Red'
            if bruh == 'B': bruh = 'Black'
            print(f'{bruh} wins!')
            screen.blit(background, (0, 0))
            game_board.draw_board(screen)
            pygame.display.flip()
            time.sleep(1.5)
            break_flag = play_again_menu(bruh)
            break
    if break_flag:
        main()
    else:
        game_board.shut_up()
        main_menu.main(False)
        quit()

if __name__ == "__main__": main()