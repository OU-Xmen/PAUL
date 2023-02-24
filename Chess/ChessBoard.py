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
        
        # initialize last move
        self.last_move = [0, 0]
    
    def draw_board(self, screen):
        for i in range(8):
            for j in range(8):
                self.board[i][j].draw_piece(screen)

    def clicked_on(self, i, j, screen):
        if self.board[i][j].id == "P":
            legal_moves = self.board[i][j].get_legal_moves(self.board, self.last_move)
        else:
            legal_moves = self.board[i][j].get_legal_moves(self.board)
        if not legal_moves: return
        while True:
            mouse = pygame.mouse.get_pos()
            mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_ij in legal_moves:
                        self.board[mouse_ij[0]][mouse_ij[1]] = CP.dupe(mouse_ij[0], mouse_ij[1], self.board[i][j].id, self.board[i][j].color)
                        self.board[i][j] = CP.Empty(i, j)
                        
                        # account for en passant
                        both_pawns = self.board[mouse_ij[0]][mouse_ij[1]].id == "P" and self.board[self.last_move[0]][self.last_move[1]].id == "P"
                        pawns_in_line = mouse_ij[1] == self.last_move[1]
                        different_colors = self.board[mouse_ij[0]][mouse_ij[1]].color != self.board[self.last_move[0]][self.last_move[1]].color
                        if both_pawns and pawns_in_line and different_colors:
                            pawn_passed = self.board[mouse_ij[0] - self.board[mouse_ij[0]][mouse_ij[1]].forward][mouse_ij[1]] is self.board[self.last_move[0]][self.last_move[1]]
                            if pawn_passed:
                                self.board[self.last_move[0]][self.last_move[1]] = CP.Empty(self.last_move[0], self.last_move[1])
                        
                        # account for castling
                        if self.board[mouse_ij[0]][mouse_ij[1]].id == 'K' and (abs(j - mouse_ij[1]) > 1):
                            self.board[i][int((j + mouse_ij[1])/2)] = CP.Rook(i, int((j + mouse_ij[1])/2), self.board[mouse_ij[0]][mouse_ij[1]].color)
                            if mouse_ij[1] == 6:
                                self.board[i][7] = CP.Empty(i, 7)
                            elif mouse_ij[1] == 2:
                                self.board[i][0] = CP.Empty(i, 0)
                        self.last_move = mouse_ij
                        return True
                    else:
                        print("No")
                        return False
            
            for a, b in legal_moves:
                pygame.draw.circle(screen, (0, 0, 0), [60*(1.5+b), 60*(1.5+a)], 10)
                pygame.draw.circle(screen, (255, 255, 255), [60*(1.5+b), 60*(1.5+a)], 8)
            pygame.display.flip()
    
    def game_is_over(self):
        white_king = black_king = False

        for i in range(8):
            for j in range(8):
                if self.board[i][j].id == 'K':
                    if self.board[i][j].color == 'white': white_king = True
                    if self.board[i][j].color == 'black': black_king = True
        
        xor = lambda a, b: (a or b) and (not (a and b))
        if xor(white_king, black_king):
            return "White" if white_king else "Black"
        return None