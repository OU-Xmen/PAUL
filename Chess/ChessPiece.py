import pygame, os
pygame.init()
maindirectory = os.path.dirname(os.path.abspath(__file__))
assetdirectory = os.path.join(maindirectory, 'assets')

class Empty:
    def __init__(self, i, j):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = None
        self.color = None

class Pawn:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'P'
        self.has_moved = False
        if color == 'black':
            self.color = 'black'
            self.forward = 1
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_pawn.png'))
        else:
            self.color = 'white'
            self.forward = -1
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_pawn.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []
        scope = lambda x: board[self.i + self.forward][self.j + x]

        # find legal single move
        if not scope(0).color:
            legal_moves.append((self.i + self.forward, self.j))

            # find legal double move
            if not self.has_moved and board[self.i + 2*self.forward][self.j]:
                legal_moves.append((self.i + 2*self.forward, self.j))

        # find legal jumps
        for d in [-1, 1]:
            if (self.j+d in range(8)) and scope(0).color != scope(d).color and scope(d).color:
                legal_moves.append((self.i + self.forward, self.j + d))
        
        return legal_moves

class Knight:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'N'
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_knight.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_knight.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []
        scope = lambda zi, zj: board[self.i + zi][self.j + zj]

        # find half of legal moves
        for a in [-1, 1]:
            for b in [-2, 2]:
                in_bounds_a = (self.i+a in range(8)) and (self.j+b in range(8))
                in_bounds_b = (self.i+b in range(8)) and (self.j+a in range(8))
                if in_bounds_a and scope(a, b).color != self.color:
                        legal_moves.append((self.i + a, self.j + b))
                if in_bounds_b and scope(b, a).color != self.color:
                        legal_moves.append((self.i + b, self.j + a))
        
        return legal_moves


class Bishop:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'B'
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_bishop.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_bishop.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        # key:
        # R: white R; W: white piece, B: black piece
        # R..W
        #  __x  | can move up to, but not incuding, a white piece
        # R..B
        #  ___x | can move up to or capture a black piece
        # if blank tile: move forward
        # if opposite color: capture
        # if white piece: stop

        legal_moves = []
        scope = lambda zi, zj: board[self.i + zi][self.j + zj]

        for a, b in [(-1, 1), (-1, -1), (1, -1), (1, 1)]: # directions to look for legal moves
            za, zb = a, b
            in_bounds = lambda: (self.i+za in range(8)) and (self.j+zb in range(8))
            if in_bounds():
                while True:
                    if not in_bounds(): break

                    if scope(za, zb).color == self.color:
                        break
                    elif not scope(za, zb).color:
                        legal_moves.append((self.i + za, self.j + zb))
                        za += a
                        zb += b
                    else:
                        legal_moves.append((self.i + za, self.j + zb))
                        break
            else:
                break
        
        return legal_moves

class Rook:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'R'
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_rook.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_rook.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def get_legal_moves(self, board):
        # key:
        # R: white R; W: white piece, B: black piece
        # R..W
        #  __x  | can move up to, but not incuding, a white piece
        # R..B
        #  ___x | can move up to or capture a black piece
        # if blank tile: move forward
        # if opposite color: capture
        # if white piece: stop

        legal_moves = []
        scope = lambda zi, zj: board[self.i + zi][self.j + zj]

        for a, b in [(0, 1), (-1, 0), (0, -1), (1, 0)]: # directions to look for legal moves
            za, zb = a, b
            in_bounds = lambda: (self.i+za in range(8)) and (self.j+zb in range(8))
            if in_bounds():
                while True:
                    if not in_bounds(): break

                    if scope(za, zb).color == self.color:
                        break
                    elif not scope(za, zb).color:
                        legal_moves.append((self.i + za, self.j + zb))
                        za += a
                        zb += b
                    else:
                        legal_moves.append((self.i + za, self.j + zb))
                        break
            else:
                break
        
        return legal_moves


class Queen:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'Q'
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_queen.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_queen.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        return Rook.get_legal_moves(self, board) + Bishop.get_legal_moves(self, board)

class King:
    def __init__(self, i, j, color):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'K'
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'black_king.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(assetdirectory, 'white_king.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []
        scope = lambda zi, zj: board[self.i + zi][self.j + zj]

        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                in_bounds = (self.i+a in range(8)) and (self.j+b in range(8))
                if (a != 0 or b != 0) and in_bounds:
                    if scope(a, b).color != self.color:
                        legal_moves.append((self.i + a, self.j + b))
        
        return legal_moves