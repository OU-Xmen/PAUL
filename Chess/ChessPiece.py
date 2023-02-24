import pygame, os
pygame.init()
maindirectory = os.path.dirname(os.path.abspath(__file__))
assetdirectory = os.path.join(maindirectory, 'assets')
# piece sets: 'letters', 'myset'
piecedirectory = os.path.join(assetdirectory, 'myset')

def dupe(i, j, id, color):
    if id == 'P':
        return Pawn(i, j, color, True)
    elif id == 'N':
        return Knight(i, j, color)
    elif id == 'B':
        return Bishop(i, j, color)
    elif id == 'R':
        return Rook(i, j, color, True)
    elif id == 'Q':
        return Queen(i, j, color)
    elif id == 'K':
        return King(i, j, color, True)
    return

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
        self.img = pygame.image.load(os.path.join(piecedirectory, 'empty_tile.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board): return []

class Pawn:
    def __init__(self, i, j, color, has_moved = False):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'P'
        self.has_moved = has_moved
        if color == 'black':
            self.color = 'black'
            self.forward = 1
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_pawn.png'))
        else:
            self.color = 'white'
            self.forward = -1
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_pawn.png'))

        '''
        x | y
        -1| 6
        1 | 1
        y = (-5/2)x + 3.5
        '''

    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board, last_move = [0, 0]):
        legal_moves = []
        scope = lambda x: board[self.i + self.forward][self.j + x]

        # find legal single move
        if not scope(0).color:
            legal_moves.append((self.i + self.forward, self.j))

            # find legal double move
            if (not self.has_moved) and board[self.i + 2*self.forward][self.j]:
                legal_moves.append((self.i + 2*self.forward, self.j))

        # find legal jumps
        for d in [-1, 1]:
            if (self.j+d in range(8)) and (self.color != scope(d).color) and scope(d).color:
                legal_moves.append((self.i + self.forward, self.j + d))
        
        # find en passant
        last_piece = board[last_move[0]][last_move[1]]
        next_to_last = last_move[0] == self.i and last_move[1] in [self.j-1, self.j+1]
        last_was_pawn = last_piece.id == "P" and last_piece.color != self.color
        white_flag = last_piece.color == 'white' and last_move[0] == 4
        black_flag = last_piece.color == 'black' and last_move[0] == 3
        if next_to_last and last_was_pawn and (white_flag or black_flag):
            legal_moves.append((self.i + self.forward, last_move[1]))

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
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_knight.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_knight.png'))
    
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
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_bishop.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_bishop.png'))
    
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
        
        return legal_moves

class Rook:
    def __init__(self, i, j, color, has_moved = False):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'R'
        self.has_moved = has_moved
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_rook.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_rook.png'))
    
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
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_queen.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_queen.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        return Rook.get_legal_moves(self, board) + Bishop.get_legal_moves(self, board)

class King:
    def __init__(self, i, j, color, has_moved = False):
        # [i][j] denote place in actual board
        self.i = i
        self.j = j
        # (x, y) denote coordinates on screen
        self.x = 60*(1+j)
        self.y = 60*(1+i)
        self.id = 'K'
        self.has_moved = has_moved
        if color == 'black':
            self.color = 'black'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'black_king.png'))
        else:
            self.color = 'white'
            self.img = pygame.image.load(os.path.join(piecedirectory, 'white_king.png'))
    
    def draw_piece(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def get_legal_moves(self, board):
        legal_moves = []
        scope = lambda zi, zj: board[self.i + zi][self.j + zj]

        # find normal moves
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                in_bounds = (self.i+a in range(8)) and (self.j+b in range(8))
                if (a != 0 or b != 0) and in_bounds:
                    if scope(a, b).color != self.color:
                        legal_moves.append((self.i + a, self.j + b))
        
        # find castles
        if not self.has_moved:
            long_empty = not (board[self.i][1].id or board[self.i][2].id or board[self.i][3].id)
            short_empty = not (board[self.i][5].id or board[self.i][6].id)
            if board[self.i][0].id == 'R' and (not board[self.i][0].has_moved) and long_empty:
                legal_moves.append((self.i, 2))
            if board[self.i][7].id == 'R' and (not board[self.i][7].has_moved) and short_empty:
                legal_moves.append((self.i, 6))
        
        return legal_moves