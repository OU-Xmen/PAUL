try:
    import pygame
    pygame.init()
    import os
    import sys
    import time
    import random
    import ChessBoard as B
    import ChessPiece as CP
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, 'assets')
except ImportError:
    print("One or more modules failed to load")
    quit()

def main():
    # create 800x600 window
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Chess')
    icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
    pygame.display.set_icon(icon)

    game_board = B.Board()
    whose_turn = 0 # start with white

    while True: # game loop
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.fill("black")
        game_board.draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_board:
                    print(game_board.board[mouse_ij[0]][mouse_ij[1]].get_legal_moves(game_board.board))
                    print(f"{game_board.board[mouse_ij[0]][mouse_ij[1]].color} {game_board.board[mouse_ij[0]][mouse_ij[1]].id}")
                else:
                    print("No")

        pygame.display.flip()

if __name__ == "__main__": main()