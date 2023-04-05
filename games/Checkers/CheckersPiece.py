import pygame, os
pygame.init()
maindirectory = os.path.dirname(os.path.abspath(__file__))
assetdirectory = os.path.join(maindirectory, 'assets')

def get_legal_jumps(i, j, id, board):
    legal_jumps = []

    if id == 'B' and i in range(2, 8):
        if (j > 1) and (not board[i - 2][j - 2].id) and (board[i - 1][j - 1].id) and (board[i - 1][j - 1].id != board[i][j].id):
            legal_jumps.append((i - 2, j - 2))
        if (j < 6) and (not board[i - 2][j + 2].id) and (board[i - 1][j + 1].id) and (board[i - 1][j + 1].id != board[i][j].id):
            legal_jumps.append((i - 2, j + 2))
    
    if id == 'R' and i in range(6):
        if (j > 1) and (not board[i + 2][j - 2].id) and (board[i + 1][j - 1].id) and (board[i + 1][j - 1].id != board[i][j].id):
            legal_jumps.append((i + 2, j - 2))
        if (j < 6) and (not board[i + 2][j + 2].id) and (board[i + 1][j + 1].id) and (board[i + 1][j + 1].id != board[i][j].id):
            legal_jumps.append((i + 2, j + 2))

    return legal_jumps

class Empty:
    def __init__(self, i, j):
        self.id = None
        self.img = pygame.image.load(os.path.join(assetdirectory, 'empty_tile.png'))
        self.img.set_colorkey((255, 0, 0))
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board): return []

class Pawn:
    def __init__(self, i, j, id):
        self.id = id
        self.king = False
        self.id = id
        if id == 'R':
            self.forward = 1
            self.img = pygame.image.load(os.path.join(assetdirectory, 'red_pawn.png'))
        elif id == 'B':
            self.forward = -1
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_pawn.png'))
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []

        # find jumps
        paul = get_legal_jumps(self.i, self.j, self.id, board)
        [legal_moves.append(item) for item in paul]

        if not legal_moves:
            # find non-jumps
            if (self.i + self.forward) in range(8):
                if (self.j > 0) and not board[self.i + self.forward][self.j - 1].id:
                    legal_moves.append((self.i + self.forward, self.j - 1))
                if (self.j < 7) and not board[self.i + self.forward][self.j + 1].id:
                    legal_moves.append((self.i + self.forward, self.j + 1))

        return legal_moves

class King:
    def __init__(self, i, j, id):
        self.id = id
        self.king = True
        if id == 'R':
            self.img = pygame.image.load(os.path.join(assetdirectory, 'red_king.png'))
        elif id == 'B':
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_king.png'))
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []

        # find jumps
        dave = get_legal_jumps(self.i, self.j, 'R', board)
        [legal_moves.append(item) for item in dave]
        dave = get_legal_jumps(self.i, self.j, 'B', board)
        [legal_moves.append(item) for item in dave]

        if not legal_moves:
            # find non-jumps
            i1 = self.i > 0
            i2 = self.i < 7
            j1 = self.j > 0
            j2 = self.j < 7
            if (i1 and j1) and not board[self.i - 1][self.j - 1].id:
                legal_moves.append((self.i - 1, self.j - 1))
            if (i1 and j2) and not board[self.i - 1][self.j + 1].id:
                legal_moves.append((self.i - 1, self.j + 1))
            if (i2 and j1) and not board[self.i + 1][self.j - 1].id:
                legal_moves.append((self.i + 1, self.j - 1))
            if (i2 and j2) and not board[self.i + 1][self.j + 1].id:
                legal_moves.append((self.i + 1, self.j + 1))
        
        return legal_moves