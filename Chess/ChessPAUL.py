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
    pauldirectory = os.path.join(assetdirectory, 'paul_face')
    B = SourceFileLoader('ChessBoard', os.path.join(maindirectory, 'ChessBoard.py')).load_module()
    CP = SourceFileLoader('ChessPiece', os.path.join(maindirectory, 'ChessPiece.py')).load_module()
except ImportError:
    print("One or more modules failed to load")
    quit()

def main():
    # create 800x600 window
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Chess')
    icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
    background = pygame.image.load(os.path.join(assetdirectory, 'background.png'))
    pygame.display.set_icon(icon)

    game_board = B.Board()
    legal_moves_flag = False
    made_move = []
    whose_turn = 0 # start with white

    # create PAUL face dictionary
    def paul_faces(face):
        if face == 'idle': new = pygame.image.load(os.path.join(pauldirectory, 'idle.png'))
        if face == 'think': new = pygame.image.load(os.path.join(pauldirectory, 'think.png'))
        if face == 'lose': new = pygame.image.load(os.path.join(pauldirectory, 'lose.png'))
        if face == 'win': new = pygame.image.load(os.path.join(pauldirectory, 'win.png'))
        return new

    while True: # game loop
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.blit(background, (0, 0))
        game_board.draw_board(screen)

        if whose_turn == 0: # white player makes a move
            paul_face = paul_faces('idle')
            screen.blit(paul_face, (630, 90))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_board and game_board.board[mouse_ij[0]][mouse_ij[1]].id and game_board.board[mouse_ij[0]][mouse_ij[1]].color == ('white','black')[whose_turn]:
                        made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                        if made_move:
                            whose_turn = 1
        else:
            paul_face = paul_faces('think')
            screen.blit(paul_face, (630, 90))
            pygame.display.flip()
            time.sleep(random.uniform(0.5, 2))
            black_pieces = game_board.find_pieces('black')
            paul_i, paul_j = black_pieces[random.randint(0, len(black_pieces) - 1)]
            while not game_board.board[paul_i][paul_j].get_legal_moves(game_board.board):
                paul_i, paul_j = black_pieces[random.randint(0, len(black_pieces) - 1)]
            paul_moves = game_board.board[paul_i][paul_j].get_legal_moves(game_board.board)
            paul_move = paul_moves[random.randint(0, len(paul_moves) - 1)]
            game_board.make_move(paul_move, paul_i, paul_j)
            whose_turn = 0


        pygame.display.flip()

        break_flag = False
        winner = game_board.game_is_over()
        if winner == 'White':
            print("White wins!")
            paul_face = paul_faces('lose')
            break_flag = True
        elif winner == 'Black':
            print("Black wins!")
            paul_face = paul_faces('win')
            break_flag = True
        
        if break_flag:
            screen.blit(background, (0, 0))
            game_board.draw_board(screen)
            screen.blit(paul_face, (630, 90))
            pygame.display.flip()
            time.sleep(1.5)
            break

if __name__ == "__main__": main()