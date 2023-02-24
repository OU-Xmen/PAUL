from importlib.machinery import SourceFileLoader
import os
maindirectory = os.path.dirname(os.path.abspath(__file__))

#import CheckersPiece as CP
CP = SourceFileLoader('CheckersPiece', os.path.join(maindirectory, 'CheckersPiece.py')).load_module()


class Board:
    def __init__(self):
        # initialize board
        self.board = []
        for _ in range(8):
            self.board.append([0]*8)

        # create blank pieces
        for i in range(8):
            for j in range(8):
                self.board[i][j] = CP.Checker(-1, 60*j+60, 60*i+60, False)

        # create 12 black pieces
        for j in [0, 2, 4, 6]:
            for i in [5, 6, 7]:
                self.board[i][j+((i+1)%2)].set_life(True)
                self.board[i][j+((i+1)%2)].set_color(0)

        #create 12 red pieces
        for j in [1, 3, 5, 7]:
            for i in [0, 1, 2]:
                self.board[i][j-(i%2)].set_life(True)
                self.board[i][j-(i%2)].set_color(1)
    
    def draw_board(self, screen):
        for i in range(8):
            for j in range(8):
                self.board[i][j].draw_piece(screen)
    
    def test_for_win(self):
        logan = []
        for i in range(8):
            for j in range(8):
                logan_two = self.board[i][j].get_color_num()
                if logan_two not in logan:
                    logan.append(logan_two)
        if len(logan) == 2:
            return max(logan)
        return -1