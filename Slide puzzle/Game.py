try:
    import pygame
    import os
    import time
    import random
    import Tile as T
    pygame.init()
except ImportError:
    print("One or more modules failed to load")
    input()
    quit()

# set directory to wherever Game.py is located
global maindirectory
maindirectory = os.path.dirname(os.path.abspath(__file__))

# create 800x600 window
size = width, height = 800, 600
game_window = pygame.display.set_mode(size)
pygame.display.set_caption('Slide Puzzle')
icon = pygame.image.load(os.path.join(maindirectory, 'tiles\\icon32.png'))
pygame.display.set_icon(icon)

# initialize font and text objects
pause_color = (255, 127, 0)
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

# initialize tiles
big_face = pygame.image.load(os.path.join(maindirectory, 'tiles\\icon.png'))
big_face_rect = big_face.get_rect(center = (400, 300))
face0 = T.Tile(280, 180)
face1 = T.Tile(360, 180, os.path.join(maindirectory, 'tiles\\face01.png'))
face2 = T.Tile(440, 180, os.path.join(maindirectory, 'tiles\\face02.png'))
face3 = T.Tile(280, 260, os.path.join(maindirectory, 'tiles\\face10.png'))
face4 = T.Tile(360, 260, os.path.join(maindirectory, 'tiles\\face11.png'))
face5 = T.Tile(440, 260, os.path.join(maindirectory, 'tiles\\face12.png'))
face6 = T.Tile(280, 340, os.path.join(maindirectory, 'tiles\\face20.png'))
face7 = T.Tile(360, 340, os.path.join(maindirectory, 'tiles\\face21.png'))
face8 = T.Tile(440, 340, os.path.join(maindirectory, 'tiles\\face22.png'))

# initialize lists for win condition
face_list = [face0, face1, face2, face3, face4, face5, face6, face7, face8]
solved_face = [face0, face1, face2, face3, face4, face5, face6, face7, face8]

def scramble(to_scramble, empty):
    empty_x, empty_y = empty.get_coords()
    swaps = []
    if empty_x > 280:
        swaps.append([empty_x-80, empty_y])
    if empty_x < 440:
        swaps.append([empty_x+80, empty_y])
    if empty_y > 180:
        swaps.append([empty_x, empty_y-80])
    if empty_y < 340:
        swaps.append([empty_x, empty_y+80])

    zx, zy = swaps[random.randint(0, len(swaps)-1)]
    
    mx = (empty_x-280)//80
    my = (empty_y-180)//80
    empty_location = 3*mx + my
    to_scramble[empty_location].set_coords(zx, zy)

    mx = (zx-280)//80
    my = (zy-180)//80
    new_location = 3*mx + my
    to_scramble[new_location].set_coords(empty_x, empty_y)

    to_scramble[empty_location], to_scramble[new_location] = to_scramble[new_location], to_scramble[empty_location]

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

def mouse_hovering_over(mouse):
    for item in face_list:
        tempx, tempy = item.get_coords()
        temp_rect = pygame.Rect(tempx, tempy, 80, 80)
        if temp_rect.collidepoint(mouse):
            return item
    return None

def better_swap(to_swap, empty):
    to_swap_index = -1
    empty_index = -1

    global face_list
    for i in range(len(face_list)):
        if face_list[i] == to_swap:
            to_swap_index = i
        if face_list[i] == empty:
            empty_index = i
    
    face_list[to_swap_index], face_list[empty_index] = face_list[empty_index], face_list[to_swap_index]

def pause_menu():
    while True:
        mouse = pygame.mouse.get_pos()
        game_window.fill('black')
        game_window.blit(resume_rend, resume_rect)
        game_window.blit(quit_rend, quit_rect)
        game_window.blit(goal_rend, goal_rect)
        game_window.blit(big_face, big_face_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(mouse):
                    return
                if quit_rect.collidepoint(mouse):
                    quit() # TODO: go back to main menu

def play_again_menu():
    while True:
        mouse = pygame.mouse.get_pos()

        game_window.fill('black')
        game_window.blit(big_face, big_face_rect)
        game_window.blit(win_rend, win_rect)
        game_window.blit(play_again_rend, play_again_rect)
        game_window.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(mouse):
                    # restart the game
                    main()
                if quit_rect.collidepoint(mouse):
                    # TODO: go back to main menu
                    quit()

def main():
    game_window.fill('black')
    for i in range(301): #scramble each time main() is ran
        scramble(face_list, face0)
        face_increment = 0
        for y in [180, 260, 340]:
            for x in [280, 360, 440]:
                face_list[face_increment].draw(game_window)
                face_increment += 1
        pygame.display.flip()
    
    while True: # game loop
        mouse = pygame.mouse.get_pos()

        tile_to_swap = mouse_hovering_over(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_adj_to_empty(mouse, face0) and tile_to_swap != None:
                    better_swap(tile_to_swap, face0)
                if pause_rect.collidepoint(mouse):
                    pause_menu()

        game_window.fill('black')
        game_window.blit(pause_rend, pause_rect)

        face_increment = 0
        for y in [180, 260, 340]:
            for x in [280, 360, 440]:
                face_list[face_increment].set_coords(x, y)
                face_list[face_increment].draw(game_window)
                face_increment += 1

        if mouse_adj_to_empty(mouse, face0):
            face0.draw_hover(game_window)
        else:
            face0.draw(game_window)

        pygame.display.flip()

        if face_list == solved_face:
            game_window.blit(win_rend, win_rect)
            for i in range(128):
                time.sleep(1/200)
                big_face.set_alpha(i)
                game_window.blit(big_face, big_face_rect)
                pygame.display.flip()
            time.sleep(0.5)
            play_again_menu()

if __name__ == '__main__':
    main()