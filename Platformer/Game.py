import os
import time
import pygame
from importlib.machinery import SourceFileLoader
pygame.init()
maindir = os.path.abspath(os.path.dirname(__file__))
L = SourceFileLoader('Levels', os.path.join(maindir, 'Levels.py')).load_module()
T = SourceFileLoader('Tile', os.path.join(maindir, 'Tile.py')).load_module()
P = SourceFileLoader('Player', os.path.join(maindir, 'Player.py')).load_module()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Platformer')
menu_color = (160, 110, 20)
background_outside = pygame.image.load(os.path.join(maindir, 'assets/background_outside.png'))

def game_loop(level):
    current_level = L.Level(level)
    level_rects = current_level.get_rect_list()
    start_x, start_y = current_level.get_start_coords()
    player = P.Player(start_x, start_y)
    arr_list = [] # list of arrow keys being held

    death_counter = 0
    coin_counter = 0

    while True:
        jump_flag = False
        mouse = pygame.mouse.get_pos()
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
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
                    jump_flag = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    arr_list.remove('right')
                if event.key == pygame.K_LEFT:
                    arr_list.remove('left')

        screen.blit(background_outside, (0, 0))
        current_level.update_level(screen)
        temp = pygame.Rect(player.get_img_rect())
        # collide_list : list of rectangles that have collision with the player
        collide_list = []
        [collide_list.append(pygame.Rect(tup[0])) for tup in level_rects]

        is_dead = []
        is_won = []
        level_tiles = current_level.get_level()
        for i in range(15):
            for j in range(20):
                if level_tiles[i][j].type == 'goal':
                    is_won.append(pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp))
                if level_tiles[i][j].type == 'lava':
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
            quit()
        if any(is_dead):
            death_counter += 1
            zx, zy = current_level.get_start_coords()
            player = P.Player(zx, zy)

        if jump_flag:
            bruh = [pygame.Rect.collidepoint(rec, (temp[0], temp[1]-13)) for rec in collide_list]
            john = collide_list[bruh.index(True)] if max(bruh) else collide_list[0]
            dist_to_ceiling = player.get_img_rect().top - (john.top+39)
            player.jump(dist_to_ceiling)

        dist_to_floor, dist_to_ceiling = 800, 800
        if player.gravity:
            temp[1] += player.gravity_velocity
            bruh = [pygame.Rect.collidepoint(rec, (temp[0], temp[1])) for rec in collide_list]
            john = collide_list[bruh.index(True)] if max(bruh) else collide_list[0]
            dist_to_floor = (player.get_img_rect().top+39) - john.top
            dist_to_ceiling = player.get_img_rect().top - (john.top+39)

        is_on_ground = []
        is_on_ground.append(any([pygame.Rect.collidepoint(rec, (temp[0], temp[1]+39)) for rec in collide_list]))
        is_on_ground.append(any([pygame.Rect.collidepoint(rec, (temp[0]+39, temp[1]+39)) for rec in collide_list]))
        player.set_gravity(not any(is_on_ground), dist_to_floor, dist_to_ceiling)

        for dir in arr_list:
            # temporarily move the player's rectangle to where the player is about to move (if allowed)
            temp[0] += {'right': 5, 'left': -5}[dir]
            
            is_colliding = []
            for tile in level_rects:
                tile_rect = tile[0]
                if tile[2]:
                    is_colliding.append(pygame.Rect.collidepoint(tile_rect, (temp[0], temp[1])))
                    is_colliding.append(pygame.Rect.collidepoint(tile_rect, (temp[0]+38, temp[1])))
                    is_colliding.append(pygame.Rect.collidepoint(tile_rect, (temp[0], temp[1]+38)))
                    is_colliding.append(pygame.Rect.collidepoint(tile_rect, (temp[0]+38, temp[1]+38)))
            
            if not any(is_colliding):
                player.move(dir)

        player.blit_player(screen)

        pygame.display.flip()

if __name__ == '__main__':
    game_loop(1)