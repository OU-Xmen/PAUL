import os
import time
import json
import pygame
import textwrap
import sys
from importlib.machinery import SourceFileLoader
pygame.init()
maindir = os.path.abspath(os.path.dirname(__file__))
bkgrddir = os.path.join(maindir, 'assets', 'backgrounds')
sounddir = os.path.join(maindir, 'assets', 'sounds')

# PAUL """API"""
def post_highscore(posted_score, posted_game="None", paul_endpoint="https://web.physcorp.com/paul/endpoint.php", maindir_int=maindir):
    # Import requests if not already imported
    try:
        requests
    except NameError:
        import requests
    # Get maindir_internal
    maindir_internal = os.path.join(maindir_int, "..", "..")
    # Post the score to the leaderboard using the """API"""
    # Get posted name from name.json in maindir
    with open(os.path.join(maindir_internal, "name.json"), "r") as rfile:
        posted_name = json.load(rfile)["name"]
    # If if name is blank, use "Anonymous"
    if posted_name == "":
        posted_name = "Anonymous"
    r = requests.post(paul_endpoint, data = {'name': posted_name, 'score': posted_score, 'game': posted_game})
    # Print the response
    print(r.text)

L = SourceFileLoader('Levels', os.path.join(maindir, 'Levels.py')).load_module()
T = SourceFileLoader('Tile', os.path.join(maindir, 'Tile.py')).load_module()
P = SourceFileLoader('Player', os.path.join(maindir, 'Player.py')).load_module()
main_menu = SourceFileLoader("main", os.path.join(maindir, '..', '..', 'main.py')).load_module()

beep = pygame.mixer.Sound(os.path.join(sounddir, 'beep.wav'))
beep.set_volume(.1)
coin_sound = pygame.mixer.Sound(os.path.join(sounddir, 'coin.wav'))
coin_sound.set_volume(.25)
goal_sound = pygame.mixer.Sound(os.path.join(sounddir, 'goal.wav'))
goal_sound.set_volume(.4)
death_sound = pygame.mixer.Sound(os.path.join(sounddir, 'death.wav'))
death_sound.set_volume(.3)
jump_sound = pygame.mixer.Sound(os.path.join(sounddir, 'jump.wav'))
jump_sound.set_volume(.2)
overworld_song = pygame.mixer.Sound(os.path.join(sounddir, "Overworld.wav"))
him = pygame.mixer.Sound(os.path.join(sounddir, "HIM.wav"))

song_channel = pygame.mixer.Channel(1)
song_channel.set_volume(.5)

font = pygame.font.SysFont("comicsansms", 30)

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Platformer')
menu_color = (160, 110, 20)
background_outside = pygame.image.load(os.path.join(maindir, 'assets','background_outside.png'))
text_displayed = False

def level_transition(duration=1):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000 / 51))  # 51 comes from 256/5

    for alpha in range(255, -1, -5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000 / 51))  # 51 comes from 256/5


def textbox(text, x=50, y=500, delay=0.05, background_color=(0, 0, 0), text_color=(255, 255, 255), max_width=50):
    global text_displayed
    global level_global
    global coin_counter
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
            if text in ['My real name is...',
                    'You are not supposed to be here.',
                    'Get out of here now.']:
                song_channel.stop()
                time.sleep(delay)
    if level_global == 15 and text == 'My real name is...':
        with open(os.path.join(maindir, 'assets', 'scores.json')) as f:
            coins = json.load(f)["highscore"]
        with open(os.path.join(maindir, 'currentstats.json')) as f:
            possible_coins = json.load(f)["coin_counter"]
        if possible_coins > coins:
            with open(os.path.join(maindir, 'assets', 'scores.json'), 'w') as f:
                json.dump({"highscore": possible_coins}, f)
        post_highscore(int(possible_coins), posted_game="PAULatformer")
        quit()

    while text_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                text_displayed = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    text_displayed = False
                    break
        time.sleep(0.1)



def game_loop(level, coin_counter_func = 0, death_counter = 0):
    global text_displayed
    text_displayed = False
    current_level = L.Level(level)
    global level_global
    level_global = level
    coin_counter = coin_counter_func
    death_counter = 0
    level_rects = current_level.get_rect_list()
    level_background = pygame.image.load(os.path.join(bkgrddir, f"{current_level.get_background()}.png")).convert()
    start_x, start_y = current_level.get_start_coords()
    player = P.Player(start_x, start_y)
    arr_list = [] # list of arrow keys being held
    jump_flag = False
    crouch_flag = True if level == 15 else False
    break_flag = False

    if not song_channel.get_busy() and level < 14:
        song_channel.play(overworld_song, -1)
    if level == 14:
        song_channel.stop()
    if level == 15:
        song_channel.play(him, -1)

    while True:
        read_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("AHHHHH")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    song_channel.stop()
                    main_menu.main(False)
                    quit()
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    arr_list.append('right') if 'right' not in arr_list else None
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    arr_list.append('left') if 'left' not in arr_list else None
                if event.key == pygame.K_c:
                    read_flag = True
                if event.key in [pygame.K_LSHIFT, pygame.K_s, pygame.K_DOWN] and level != 15:
                    crouch_flag = [False, True][crouch_flag == False]
                if event.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                    if not jump_flag: jump_sound.play()
                    jump_flag = True
                if event.key == pygame.K_c and text_displayed:
                    text_displayed = False
            if event.type == pygame.KEYUP and arr_list:
                if event.key in [pygame.K_RIGHT, pygame.K_d] and 'right' in arr_list:
                    arr_list.remove('right')
                if event.key in [pygame.K_LEFT, pygame.K_a] and 'left' in arr_list:
                    arr_list.remove('left')
        if break_flag: break

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
                if level_tiles[i][j].type == 'enemy':
                    # move enemy
                    temp_enemy = pygame.Rect(level_tiles[i][j].get_img_rect())
                    enemy_dir = level_tiles[i][j].direction
                    temp_enemy[0] += {'right': 1, 'left': -1}[enemy_dir]
                    enemy_is_colliding = []
                    for tile in level_rects:
                        tile_rect = tile[0]
                        if tile[2]:
                            enemy_is_colliding.append(pygame.Rect.colliderect(tile_rect, temp_enemy))
                    if not any(enemy_is_colliding):
                        level_tiles[i][j].move(enemy_dir, 0.5)
                    elif int(temp_enemy[0]%40) == {'right': 7, 'left': 39}[enemy_dir]:
                        level_tiles[i][j].direction = ['right', 'left'][enemy_dir == 'right']

                    # check if player is colliding with enemy
                    enemy_top = level_tiles[i][j].img_rect
                    enemy_top.height = 30
                    jumped_on_enemy = []
                    jumped_on_enemy.append(pygame.Rect.collidepoint(enemy_top, (temp[0], temp[1]+37)))
                    jumped_on_enemy.append(pygame.Rect.collidepoint(enemy_top, (temp[0]+33, temp[1]+37)))
                    if max(jumped_on_enemy):
                        death_sound.play()
                        level_tiles[i][j] = T.Tile(0, i, j)
                        player.set_gravity(False)
                        player.jump(800, True)
                    else:
                        is_dead.append(pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp))
                if level_tiles[i][j].type == 'coin':
                    if pygame.Rect.colliderect(level_tiles[i][j].img_rect, temp):
                        coin_sound.play()
                        coin_counter += 1
                        level_tiles[i][j] = T.Tile(0, i, j)
        if any(is_won):
            if level == 14 or not song_channel.get_busy():
                death_sound.play()
            else:
                goal_sound.play()
            time.sleep(1)
            with open(os.path.join(maindir, "currentstats.json"), "r") as rfile:
                a = json.load(rfile)
                a["level"] += 1
                level += 1
                a["coin_counter"] = coin_counter
                a["death_counter"] += death_counter
            with open(os.path.join(maindir, "currentstats.json"), "w") as wfile:
                json.dump(a, wfile)

            print("You win!")
            print(f"Coins: {coin_counter}")
            print(f"Deaths: {death_counter}")
            level_transition()
            if int(a["level"]) <= 15:
                game_loop(level, coin_counter, death_counter)
                quit()
            else:
                quit()

        if any(is_dead) or temp[1]>600:
            death_sound.play()
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
                player.move(arr_list[0], 1.7 - crouch_flag)
            elif temp[0]%40 == {'right': 39, 'left': 1}[arr_list[0]]:
                player.move(arr_list[0], 1 - 0.5*crouch_flag)

        player.blit_player(screen)

        pygame.display.flip()

if __name__ == '__main__':
    game_loop(1)