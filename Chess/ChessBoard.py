import ChessPiece as CP
import pygame
pygame.init()

class Board:
    def __init__(self):
        # initialize board
        self.board = []
        for _ in range(8):
            self.board.append([0]*8)

        # define empty squares
        for i in range(8):
            for j in range(8):
                self.board[i][j] = CP.Empty(i, j)
        
        matt = lambda i: ('black', 'white')[int(i/7)]

        # create pawns
        for i in [1, 6]:
            for j in range(8):
                color = ('black', 'white')[int((i-1)/5)]
                self.board[i][j] = CP.Pawn(i, j, color)
        
        # create knights
        for i in [0, 7]:
            for j in [1, 6]:
                self.board[i][j] = CP.Knight(i, j, matt(i))
        
        # create bishops
        for i in [0, 7]:
            for j in [2, 5]:
                self.board[i][j] = CP.Bishop(i, j, matt(i))

        # create rooks
        for i in [0, 7]:
            for j in [0, 7]:
                self.board[i][j] = CP.Rook(i, j, matt(i))

        # create queens and kings
        for i in [0, 7]:
            self.board[i][3] = CP.Queen(i, 3, matt(i))
            self.board[i][4] = CP.King(i, 4, matt(i))
    
    def draw_board(self, screen):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen,(170, 110, 20), (60*(1+j), 60*(1+i), 60, 60))
                if self.board[i][j].id:
                    self.board[i][j].draw_piece(screen)