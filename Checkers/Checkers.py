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
    main_menu = SourceFileLoader('main', os.path.join(os.path.dirname(maindirectory), 'main.py')).load_module()

except ImportError as e:
    print(f"One or more modules failed to load: {e}")
    quit()

def main():
    # create 800x600 window
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Checkers')
    icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
    pygame.display.set_icon(icon)

    game_board = B.Board()
    whose_turn = 0 # start with black

    while True: # game loop
        bruh = False
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.fill("black")
        game_board.draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                piece_clicked = game_board.board[mouse_ij[0]][mouse_ij[1]]
                if mouse_on_board and piece_clicked.id and piece_clicked.id == ('B', 'R')[whose_turn]:
                    made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                    if made_move:
                        bruh = game_board.test_for_win()
                        whose_turn = 1 - whose_turn
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.main(False)
                    break
        
        pygame.display.flip()

        break_flag = False
        if bruh:
            break_flag = True
            if bruh == 'R': bruh = 'Red'
            if bruh == 'B': bruh = 'Black'
            print(f'{bruh} wins!')
        if break_flag: break

if __name__ == "__main__": main()