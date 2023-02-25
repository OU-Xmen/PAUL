import CheckersPiece as CP
import pygame
pygame.init()

class Board:
    def __init__(self):
        # initialize board
        self.board = []
        for _ in range(8):
            self.board.append([0]*8)

        # create blank pieces
        for i in range(8):
            for j in range(8):
                self.board[i][j] = CP.Empty(i, j)

        # create 12 black pieces
        for j in [0, 2, 4, 6]:
            for i in [5, 6, 7]:
                self.board[i][j+((i+1)%2)] = CP.Pawn(i, j+((i+1)%2), 'B')

        #create 12 red pieces
        for j in [1, 3, 5, 7]:
            for i in [0, 1, 2]:
                self.board[i][j-(i%2)] = CP.Pawn(i, j-(i%2), 'R')
    
    def draw_board(self, screen):
        for i in range(8):
            for j in range(8):
                self.board[i][j].draw_piece(screen)
    
    def clicked_on(self, i, j, screen, jump_switch = False):
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
                        dave = self.make_move(mouse_ij, i, j)
                        if self.board[mouse_ij[0]][mouse_ij[1]].king:
                            kevin = []
                            kevins_dog_also_named_kevin = CP.get_legal_jumps(mouse_ij[0], mouse_ij[1], 'R', self.board)
                            [kevin.append(dog_food) for dog_food in kevins_dog_also_named_kevin]
                            kevins_dog_also_named_kevin = CP.get_legal_jumps(mouse_ij[0], mouse_ij[1], 'B', self.board)
                            [kevin.append(dog_food) for dog_food in kevins_dog_also_named_kevin]
                        else:
                            kevin = CP.get_legal_jumps(mouse_ij[0], mouse_ij[1], self.board[mouse_ij[0]][mouse_ij[1]].id, self.board)
                        if abs(mouse_ij[0] - i) > 1 and kevin:
                            jump_switch = True
                            self.clicked_on(mouse_ij[0], mouse_ij[1], screen, jump_switch)
                            return True
                        else: return True
                    elif not jump_switch: return False
            
            self.draw_board(screen)
            for a, b in legal_moves:
                pygame.draw.circle(screen, (0, 0, 0), [60*(1.5+b), 60*(1.5+a)], 8)
                pygame.draw.circle(screen, (255, 255, 255), [60*(1.5+b), 60*(1.5+a)], 7)
            pygame.display.flip()
    
    def make_move(self, mouse_ij, i, j):
        old_piece = self.board[i][j]
        if old_piece.king:
            self.board[mouse_ij[0]][mouse_ij[1]] = CP.King(mouse_ij[0], mouse_ij[1], old_piece.id)
        else:
            self.board[mouse_ij[0]][mouse_ij[1]] = CP.Pawn(mouse_ij[0], mouse_ij[1], old_piece.id)
        self.board[i][j] = CP.Empty(i, j)
        if abs(i - mouse_ij[0]) > 1:
            statler = int((i + mouse_ij[0])/2)
            waldorf = int((j + mouse_ij[1])/2)
            self.board[statler][waldorf] = CP.Empty(statler, waldorf)
        
        # handle promotion
        black_at_back_rank = self.board[mouse_ij[0]][mouse_ij[1]].id == 'B' and mouse_ij[0] == 0
        red_at_back_rank = self.board[mouse_ij[0]][mouse_ij[1]].id == 'R' and mouse_ij[0] == 7
        if red_at_back_rank or black_at_back_rank:
            self.board[mouse_ij[0]][mouse_ij[1]] = CP.King(mouse_ij[0], mouse_ij[1], old_piece.id)

        return True
    
    def test_for_win(self):
        logan = []
        for i in range(8):
            for j in range(8):
                logan_two = self.board[i][j].id
                if logan_two and logan_two not in logan:
                    logan.append(logan_two)
        if len(logan) == 1:
            return logan[0]
        return False
    
    def find_pieces(self, id):
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].id == id:
                    pieces.append((i, j))
        return pieces