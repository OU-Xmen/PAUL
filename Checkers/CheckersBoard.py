import CheckersPiece as CP

class Board:
    def __init__(self):
        # initialize board
        self.width, self.height = 8, 8
        self.board = []
        for _ in range(self.height):
            self.board.append([0]*self.width)

        # create blank pieces
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = CP.Checker(-1, 60*j+60, 60*i+60, False)

        # create 12 black pieces
        for i in [5, 6, 7]:
            for j in [0, 2, 4, 6]:
                self.board[i][j+((i+1)%2)].set_life(True)
                self.board[i][j+((i+1)%2)].set_color(0)

        #create 12 red pieces
        for i in range(0, 3):
            for j in [1, 3, 5, 7]:
                self.board[i][j-(i%2)].set_life(True)
                self.board[i][j-(i%2)].set_color(1)
    
    def draw_board(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j].draw_piece(screen)