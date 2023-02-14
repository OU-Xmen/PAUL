try:
    import pygame
    pygame.init()
    import os
    import sys
    import time
    import random
    import CheckersBoard as B
    import CheckersPiece as CP
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, 'assets')
except ImportError:
    print("One or more modules failed to load")
    quit()

# create 800x600 window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Checkers')
icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
pygame.display.set_icon(icon)

dark_squares_color = (170, 110, 20)
light_squares_color = (220, 170, 60)
black_piece = pygame.image.load(os.path.join(assetdirectory, 'black_piece.png'))
red_piece = pygame.image.load(os.path.join(assetdirectory, 'red_piece.png'))

game_board = B.Board()
whose_turn = 0 # start with black

while True: # game loop
    mouse = pygame.mouse.get_pos()
    mouse_tile = ((mouse[0]-60)//60, (mouse[1]-60)//60)
    mouse_on_board = mouse_tile[0] in range(8) and mouse_tile[1] in range(8)
    if mouse_on_board:
        mouse_tile_is_alive = game_board.board[mouse_tile[1]][mouse_tile[0]].get_life()
        mouse_tile_num = game_board.board[mouse_tile[1]][mouse_tile[0]].get_color_num()

    else:
        mouse_tile_is_alive = False
        mouse_tile_num = -1
    # print(mouse_tile_num)

    screen.fill("black")
    game_board.draw_board(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_tile_is_alive and whose_turn == mouse_tile_num:
            move_was_made = game_board.board[mouse_tile[0]][mouse_tile[1]].clicked_on(screen, game_board.board, whose_turn)
            if move_was_made:
                whose_turn = 1 - whose_turn

    pygame.display.flip()