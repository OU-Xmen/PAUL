import os
import time
import pygame
import textwrap
import sys
from importlib.machinery import SourceFileLoader
pygame.init()
maindir = os.path.abspath(os.path.dirname(__file__))
bkgrddir = os.path.join(maindir, 'assets','backgrounds')
L = SourceFileLoader('Levels', os.path.join(maindir, 'Levels.py')).load_module()
T = SourceFileLoader('Tile', os.path.join(maindir, 'Tile.py')).load_module()
P = SourceFileLoader('Player', os.path.join(maindir, 'Player.py')).load_module()
beep = pygame.mixer.Sound(os.path.join(maindir, 'assets', 'beep.wav'))
beep.set_volume(.25)

font = pygame.font.Font(None, 36)

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Platformer')
menu_color = (160, 110, 20)
background_outside = pygame.image.load(os.path.join(maindir, 'assets','background_outside.png'))
text_displayed = False

def textbox(text, x=50, y=500, delay=0.05, background_color=(0, 0, 0), text_color=(255, 255, 255), max_width=50):
    global text_displayed
    text_displayed = True
    wrapped_text = textwrap.wrap(text, max_width)
    displayed_lines = []

    for line in wrapped_text:
        displayed_lines.append("")
        for char in line:
            displayed_lines[-1] += char
            text_surface = [font.render(line, True, text_color) for line in displayed_lines]

            # Render a filled rectangle as the background for each line
            text_background = [pygame.Surface((surface.get_width(), surface.get_height())) for surface in text_surface]
            for bg in text_background:
                bg.fill(background_color)

            # Blit the background and the text surface for each line
            for i, (bg, surface) in enumerate(zip(text_background, text_surface)):
                screen.blit(bg, (x, y + i * (font.get_height() + 5)))
                screen.blit(surface, (x, y + i * (font.get_height() + 5)))

            pygame.display.update()
            beep.play()
            time.sleep(delay)

    while text_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                text_displayed = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text_displayed = False
                    break
        time.sleep(0.1)



def game_loop(level):
    current_level = L.Level(level)
    level_rects = current_level.get_rect_list()
    level_background = pygame.image.load(os.path.join(bkgrddir, f"{current_level.get_background()}.png")).convert()
    start_x, start_y = current_level.get_start_coords()
    player = P.Player(start_x, start_y)
    arr_list = [] # list of arrow keys being held
    death_counter = 0
    coin_counter = 0
    jump_flag = False

    while True:
        read_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("AHHHHH")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    arr_list.append('right')
                if event.key == pygame.K_LEFT:
                    arr_list.append('left')
                if event.key == pygame.K_c:
                    read_flag = True
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
                    jump_flag = True
                if event.key == pygame.K_RETURN and text_displayed:
                    text_displayed = False

            if event.type == pygame.KEYUP and arr_list:
                if event.key == pygame.K_RIGHT and 'right' in arr_list:
                    arr_list.remove('right')
                if event.key == pygame.K_LEFT and 'left' in arr_list:
                    arr_list.remove('left')

        screen.blit(level_background, (0,0))
        current_level.update_level(screen)
        temp = pygame.Rect(player.get_img_rect())
        # collide_list : list of rectangles that have collision with the player
        collide_list = []
        [collide_list.append(pygame.Rect(tup[0])) for tup in level_rects if tup[2]]

        is_dead = []
        is_won = []
        level_tiles = current_level.get_level()
        for i in range(15):
            for j in range(20):
                dead_collide = pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp) or pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp)
                dead_collide = dead_collide and level_tiles[i][j].type == 'lava'
                if level_tiles[i][j].type == 'sign' and pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp):
                    if read_flag:
                        textbox(level_tiles[i][j].text)
                        print(level_tiles[i][j].text)
                if level_tiles[i][j].type == 'goal':
                    is_won.append(pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp))
                if level_tiles[i][j].type == 'lava' and dead_collide:
                    is_dead.append(pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp))
                if level_tiles[i][j].type == 'coin':
                    if pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp):
                        coin_counter += 1
                        level_tiles[i][j] = T.Tile(0, i, j)
        if any(is_won):
            print("You win!")
            print(f"Coins: {coin_counter}")
            print(f"Deaths: {death_counter}")
            time.sleep(1.5)
            game_loop(current_level.get_level_num() + 1)
        if any(is_dead) or temp[1]>600:
            death_counter += 1
            zx, zy = current_level.get_start_coords()
            player = P.Player(zx, zy)

        dist_to_floor, dist_to_ceiling = 800, 800
        
        if player.gravity:
            temp[1] += player.gravity_velocity
            bruh = [pygame.Rect.collidepoint(rec, (temp[0], temp[1])) for rec in collide_list]
            hurb = [pygame.Rect.collidepoint(rec, (temp[0]+33, temp[1])) for rec in collide_list]
            if max(bruh):
                john = collide_list[bruh.index(True)]
            elif max(hurb):
                john = collide_list[hurb.index(True)]
            else:
                john = pygame.Rect(0, -120, 40, 40)
            dist_to_floor = (player.get_img_rect().top+39) - john.top
            dist_to_ceiling = player.get_img_rect().top - (john.top+39)
        
        if jump_flag:
            player.jump(dist_to_ceiling)
        
        is_on_ground = []
        is_on_ground.append(any([pygame.Rect.collidepoint(rec, (temp[0], temp[1]+39+player.gravity_velocity)) for rec in collide_list]))
        is_on_ground.append(any([pygame.Rect.collidepoint(rec, (temp[0]+33, temp[1]+39+player.gravity_velocity)) for rec in collide_list]))
        player.set_gravity(not any(is_on_ground), dist_to_floor, dist_to_ceiling)
        if any(is_on_ground): jump_flag = False

        event_a = 'right' in arr_list
        event_b = 'left' in arr_list
        if (event_a or event_b) and (not (event_a and event_b)):
            # temporarily move the player's rectangle to where the player is about to move (if allowed)
            temp[0] += {'right': 2, 'left': -2}[arr_list[0]]
            
            is_colliding = []
            for tile in level_rects:
                tile_rect = tile[0]
                if tile[2]:
                    is_colliding.append(pygame.Rect.colliderect(tile_rect, temp))

            if not any(is_colliding):
                player.move(arr_list[0])
            elif temp[0]%40 == {'right': 39, 'left': 1}[arr_list[0]]:
                player.move(arr_list[0], 1)

        player.blit_player(screen)

        pygame.display.flip()

if __name__ == '__main__':
    game_loop(0)