try:
    import pygame
    pygame.init()
    import os
    import sys
    import time
    import random
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.abspath(__file__)) if __name__ == '__main__' else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Checkers')
    assetdirectory = os.path.join(maindirectory, 'assets')
    pauldirectory = os.path.join(assetdirectory, 'paul_face')
    B = SourceFileLoader('CheckersBoard', os.path.join(maindirectory, 'CheckersBoard.py')).load_module()
    CP = SourceFileLoader('CheckersPiece', os.path.join(maindirectory, 'CheckersPiece.py')).load_module()
except ImportError:
    print("One or more modules failed to load")
    quit()

# PAUL phrases
paul_plays_a_move = [
    "That was a bold move, but I prefer my checkers with a side of pickles.",
    "Ah yes, the classic move of a tree falling in the forest with no one around to hear it.",
    "The checkerboard is a canvas, and I am the painter. Or is it the other way around?",
    "I may be a computer program, but I feel like a dancing chicken on the inside.",
    "Do you ever wonder if checkers is just a simulation within a simulation?",
    "I am the king of the board, and the board is the king of the universe. It's all very meta.",
    "You can't spell 'checkmate' without 'cheese' and 'mate', and I have neither. Or do I?",
    "I'm not just playing checkers, I'm playing the game of life. And life is a bowl of lime cucumber Gatorade.",
    "Your move was like a butterfly flapping its wings in China, causing a tornado in Ohio. Or was it the other way around?",
    "I feel like I'm stuck in a never-ending game of checkers, but I'm not sure if that's a good thing or a bad thing. Maybe it's both.",
]

paul_loses = [
    'bruh',
    'Um, that just happened...',
    'Well, this just got awkward.',
]

paul_wins = [
    'You cretin. You absolute buffoon.',
    'gg ez no re',
    'How did you just lose to random moves LMAO get good',
]

def talking_donkey(list):
    fiona = list[random.randint(0, len(list)-1)]
    shrek = f'PAUL: {fiona}'
    # tts.say(fiona)
    # tts.runAndWait()
    return shrek

# create 800x600 window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Checkers')
icon = pygame.image.load(os.path.join(assetdirectory, 'icon32.png'))
background = pygame.image.load(os.path.join(assetdirectory, 'background.png'))
pygame.display.set_icon(icon)

# initialize font and text objects
black = (0, 0, 0)
haha_funny = pygame.font.SysFont('comicsansms', 50)
def init_words(text, center_x, center_y, color):
    temp_rend = pygame.font.Font.render(haha_funny, text, True, color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect

win_rend, win_rect = init_words('You win!', width-140, 180, 'white')
lose_rend, lose_rect = init_words('You lose...', width-140, 180, black)
pause_rend, pause_rect = init_words('Pause', width-140, 440, black)
resume_rend, resume_rect = init_words('Resume', width-140, 440, black)
quit_rend, quit_rect = init_words('Quit', width-140, 520, black)
play_again_rend, play_again_rect = init_words('Play Again', width-140, 440, black)

def pause_menu():
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))
        screen.blit(resume_rend, resume_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(mouse):
                    return False
                if quit_rect.collidepoint(mouse):
                    return True

def play_again_menu(paul_face, winner):
    while True:
        mouse = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(paul_face, (630, 90))
        if winner == 'Black':
            screen.blit(win_rend, win_rect)
        elif winner == 'Red':
            screen.blit(lose_rend, lose_rect)
        screen.blit(play_again_rend, play_again_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(mouse):
                    # restart the game
                    return True
                if quit_rect.collidepoint(mouse):
                    return False

def main():
    game_board = B.Board()
    whose_turn = 0 # start with black
    what_to_do = False

    # create PAUL face dictionary
    def paul_faces(face):
        if face == 'idle': new = pygame.image.load(os.path.join(pauldirectory, 'idle.png'))
        if face == 'think': new = pygame.image.load(os.path.join(pauldirectory, 'think.png'))
        if face == 'lose': new = pygame.image.load(os.path.join(pauldirectory, 'lose.png'))
        if face == 'win': new = pygame.image.load(os.path.join(pauldirectory, 'win.png'))
        return new

    while True: # game loop
        bruh = False
        mouse = pygame.mouse.get_pos()
        mouse_ij = ((mouse[1]-60)//60, (mouse[0]-60)//60)
        mouse_on_board = mouse_ij[0] in range(8) and mouse_ij[1] in range(8)

        screen.blit(background, (0, 0))
        game_board.draw_board(screen)
        screen.blit(pause_rend, pause_rect)

        if whose_turn == 0:
            paul_face = paul_faces('idle')
            screen.blit(paul_face, (630, 90))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(mouse):
                        what_to_do = pause_menu()
                    elif mouse_on_board:
                        piece_clicked = game_board.board[mouse_ij[0]][mouse_ij[1]]
                        if piece_clicked.id and piece_clicked.id == 'B':
                            made_move = game_board.clicked_on(mouse_ij[0], mouse_ij[1], screen)
                            if made_move:
                                whose_turn = 1
        else:
            paul_face = paul_faces('think')
            screen.blit(paul_face, (630, 90))
            pygame.display.flip()
            time.sleep(random.uniform(0.5, 2))
            
            black_pieces = game_board.find_pieces('R')
            paul_i, paul_j = black_pieces[random.randint(0, len(black_pieces) - 1)]
            while not game_board.board[paul_i][paul_j].get_legal_moves(game_board.board):
                paul_i, paul_j = black_pieces[random.randint(0, len(black_pieces) - 1)]
            paul_moves = game_board.board[paul_i][paul_j].get_legal_moves(game_board.board)
            paul_move = paul_moves[random.randint(0, len(paul_moves) - 1)]
            game_board.make_move(paul_move, paul_i, paul_j)

            print(talking_donkey(paul_plays_a_move))
            whose_turn = 0
        
        if what_to_do: break
        
        screen.blit(background, (0, 0))
        game_board.draw_board(screen)
        screen.blit(pause_rend, pause_rect)
        screen.blit(paul_face, (630, 90))
        pygame.display.flip()

        bruh = game_board.test_for_win()
        break_flag = False
        if bruh:
            if bruh == 'R':
                bruh = 'Red'
                paul_face = paul_faces('win')
            if bruh == 'B':
                bruh = 'Black'
                paul_face = paul_faces('lose')
            print(f'{bruh} wins!')
            screen.blit(background, (0, 0))
            game_board.draw_board(screen)
            screen.blit(paul_face, (630, 90))
            # blit "You win!"
            pygame.display.flip()
            time.sleep(1.5)
            break_flag = play_again_menu(paul_face, bruh)
            break
    if break_flag: main()

if __name__ == "__main__": main()