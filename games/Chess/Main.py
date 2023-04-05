try:
    import pygame
    pygame.init()
    import os
    import time
    import random
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, 'assets')
    pauldirectory = os.path.join(assetdirectory, 'paul_face')
    B = SourceFileLoader('ChessBoard', os.path.join(maindirectory, 'ChessBoard.py')).load_module()
    CP = SourceFileLoader('ChessPiece', os.path.join(maindirectory, 'ChessPiece.py')).load_module()
    main_menu = SourceFileLoader('main', os.path.join(maindirectory, "..", "main.py")).load_module()
except ImportError:
    print("One or more modules failed to load")
    quit()

# PAUL phrases
paul_plays_a_move = [
    'You\'re really bad at this game.',
    'Is this your first time?',
    'The probability of you winning this game is approaching zero.',
    'Take THAT! Oh, wait a second...',
    'That\'s not fair, my hand slipped!',
    'You ever heard of \'opening theory\'?',
    'I definitely just blundered my queen... ;)',
    'Trigger happy or true genius?',
    'I\'ve already seen that move, it doesn\'t work.',
    'IndexError: list index out of range (just kidding)',
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
    shrek = list[random.randint(0, len(list)-1)]
    fiona = f"PAUL: {shrek}"
    return fiona

# create 800x600 window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
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

def pause_menu(game_board):
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
                    game_board.shut_up()
                    main_menu.main(False)
                    quit()

def play_again_menu(paul_face, winner):
    while True:
        mouse = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(paul_face, (630, 90))
        if winner == 'White':
            screen.blit(win_rend, win_rect)
        elif winner == 'Black':
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
    made_move = []
    whose_turn = 0 # start with white
    what_to_do = False

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
        screen.blit(pause_rend, pause_rect)

        if whose_turn == 0: # white player makes a move
            paul_face = paul_faces('idle')
            screen.blit(paul_face, (630, 90))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(mouse):
                    what_to_do = pause_menu(game_board)
                elif event.type == pygame.MOUSEBUTTONDOWN:
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

            screen.blit(background, (0, 0))
            game_board.draw_board(screen)
            screen.blit(pause_rend, pause_rect)
            paul_face = paul_faces('idle')
            screen.blit(paul_face, (630, 90))
            pygame.display.flip()
            print(talking_donkey(paul_plays_a_move))
            
            whose_turn = 0

        if what_to_do: break

        pygame.display.flip()

        break_flag = False
        winner = game_board.game_is_over()
        if winner:
            if winner == 'White':
                paul_face = paul_faces('lose')
                fiona = paul_loses
            elif winner == 'Black':
                paul_face = paul_faces('win')
                fiona = paul_wins
            print(talking_donkey(fiona))
            break_flag = play_again_menu(paul_face, winner)
            break
    if break_flag:
        main()
    else:
        game_board.shut_up()
        main_menu.main(False)
        quit()

if __name__ == "__main__": main()