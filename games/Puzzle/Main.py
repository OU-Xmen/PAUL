try:
    import pygame
    import json
    import os
    import sys
    import time
    import random
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    T = SourceFileLoader('Tile', os.path.join(maindirectory, 'Tile.py')).load_module() # effectively imports Tile as T
    pygame.init()

    with (open(os.path.join(maindirectory, 'assets', 'leaderboard.json'), "r")) as jasonfile:
        # read from the json file into the variable called jason
        jason = json.load(jasonfile)
except ImportError:
    print("One or more modules failed to load")
    quit()

tiledirectory = os.path.join(maindirectory, 'assets')

# create 800x600 window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Slide Puzzle')
icon = pygame.image.load(os.path.join(tiledirectory, 'icon32.png'))
pygame.display.set_icon(icon)

# initialize font and text objects
pause_color = (200, 0, 0)
haha_funny = pygame.font.SysFont('comicsansms', 50)
def init_words(text, center_x, center_y, color):
    temp_rend = pygame.font.Font.render(haha_funny, text, True, color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect

win_rend, win_rect = init_words('You win!', width/2, 80, 'white')
pause_rend, pause_rect = init_words('Pause', width-140, 80, pause_color)
resume_rend, resume_rect = init_words('Resume', width-140, 180, pause_color)
goal_rend, goal_rect = init_words('Goal:', width/2, 100, pause_color)
quit_rend, quit_rect = init_words('Quit', width-140, 260, pause_color)
play_again_rend, play_again_rect = init_words('Play Again', width-140, 180, pause_color)
high_score_rend, high_score_rect = init_words('High Score!', width/2, 80, 'white')
global time_rend, time_rect

def time_convert(sec):
    return f"Time: {format(sec, '.2f')}"

def mouse_adj_to_empty(coords, empty):
    x, y = empty.get_coords()
    x = (x-280)//80
    y = (y-180)//80

    possible_moves = []
    if x > 0: possible_moves.append((x-1, y))
    if x < 2: possible_moves.append((x+1, y))
    if y > 0: possible_moves.append((x, y-1))
    if y < 2: possible_moves.append((x, y+1))

    mx = (coords[0]-280)//80
    my = (coords[1]-180)//80

    if (mx, my) in possible_moves: return True
    return False

def mouse_hovering_over(mouse, face_list):
    for item in face_list:
        tempx, tempy = item.get_coords()
        temp_rect = pygame.Rect(tempx, tempy, 80, 80)
        if temp_rect.collidepoint(mouse):
            return item
    return None

def better_swap(to_swap, empty, face_list):
    to_swap_index = -1
    empty_index = -1

    for i in range(len(face_list)):
        if face_list[i] == to_swap:
            to_swap_index = i
        if face_list[i] == empty:
            empty_index = i
    
    face_list[to_swap_index], face_list[empty_index] = face_list[empty_index], face_list[to_swap_index]

def pause_menu():
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill('black')
        screen.blit(resume_rend, resume_rect)
        screen.blit(quit_rend, quit_rect)
        screen.blit(goal_rend, goal_rect)
        screen.blit(big_face, big_face_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(mouse):
                    return False
                if quit_rect.collidepoint(mouse):
                    return True

def play_again_menu(time_score):
    matt = False
    while True:
        mouse = pygame.mouse.get_pos()

        screen.fill('black')
        screen.blit(big_face, big_face_rect)
        if time_score < jason['slide_puzzle_score']:
            matt = True
            andrew =  float(f"{format(time_score, '.2f')}")
            jason['slide_puzzle_score'] = andrew
            with (open(os.path.join(maindirectory, 'assets', 'leaderboard.json'), "w")) as jasonfile:
                json.dump(jason, jasonfile)
        if matt:
            screen.blit(high_score_rend, high_score_rect)
        else:
            screen.blit(win_rend, win_rect)
        screen.blit(time_rend, time_rect)
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

# initialize tiles
big_face = pygame.image.load(os.path.join(tiledirectory, 'icon.png'))
big_face_rect = big_face.get_rect(center = (400, 300))
face0 = T.Tile(280, 180)
face1 = T.Tile(360, 180, os.path.join(tiledirectory, 'face01.png'))
face2 = T.Tile(440, 180, os.path.join(tiledirectory, 'face02.png'))
face3 = T.Tile(280, 260, os.path.join(tiledirectory, 'face10.png'))
face4 = T.Tile(360, 260, os.path.join(tiledirectory, 'face11.png'))
face5 = T.Tile(440, 260, os.path.join(tiledirectory, 'face12.png'))
face6 = T.Tile(280, 340, os.path.join(tiledirectory, 'face20.png'))
face7 = T.Tile(360, 340, os.path.join(tiledirectory, 'face21.png'))
face8 = T.Tile(440, 340, os.path.join(tiledirectory, 'face22.png'))

def main():

    # initialize lists for win condition
    face_list = [face0, face1, face2, face3, face4, face5, face6, face7, face8]
    solved_face = [face0, face1, face2, face3, face4, face5, face6, face7, face8]
    a = None
    is_won = False
    break_flag = False
    
    pygame.display.set_caption('Slide Puzzle')
    screen.fill('black')
    #scramble each time main() is ran
    bruh = list(range(1,9))
    for i in range(4):
        temp_a = bruh.pop(random.randint(0, len(bruh)-1))
        temp_b = bruh.pop(random.randint(0, len(bruh)-1))
        face_list[temp_a], face_list[temp_b] = face_list[temp_b], face_list[temp_a]

    start_time = time.time()
    val_float = 0
    while True: # game loop
        mouse = pygame.mouse.get_pos()
        val_time = time.time() - start_time - val_float

        tile_to_swap = mouse_hovering_over(mouse, face_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_adj_to_empty(mouse, face0) and tile_to_swap != None:
                    better_swap(tile_to_swap, face0, face_list)
            if event.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(mouse):
                pause_time = time.time()
                break_flag = pause_menu()
                val_float += time.time() - pause_time
        
        if break_flag:
            break

        screen.fill('black')
        screen.blit(pause_rend, pause_rect)
        
        # blit timer to screen
        global time_rend, time_rect
        time_rend, time_rect = init_words(time_convert(val_time), width/2, 520, 'white')
        screen.blit(time_rend, time_rect) # bruh: timer continues to run during pause_menu

        face_increment = 0
        for y in [180, 260, 340]:
            for x in [280, 360, 440]:
                face_list[face_increment].set_coords(x, y)
                face_list[face_increment].draw(screen)
                face_increment += 1

        if mouse_adj_to_empty(mouse, face0):
            face0.draw_hover(screen)
        else:
            face0.draw(screen)

        pygame.display.flip()

        if face_list == solved_face:
            time_words = time_convert(val_time)
            time_rend, time_rect = init_words(time_words, 400, 520, 'white')
            screen.blit(time_rend, time_rect)

            is_won = True
            screen.blit(win_rend, win_rect)
            for i in range(128):
                time.sleep(1/200)
                big_face.set_alpha(i)
                screen.blit(big_face, big_face_rect)
                pygame.display.flip()
            time.sleep(0.5)
            break

    if is_won:
        a = play_again_menu(val_time)
    if a:
        main()

if __name__ == '__main__':
    main()