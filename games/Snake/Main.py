import pygame
import time
import random
import os
import json
from importlib.machinery import SourceFileLoader

pygame.init()

white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
red = (210, 50, 100)
blue = (50, 125, 255)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Paul\'s Snake Game')

maindirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
currentdirectory = os.path.dirname(os.path.abspath(__file__))
assetdirectory = os.path.join(currentdirectory, "assets")

# PAUL """API"""
def post_highscore(posted_score, posted_game="None", paul_endpoint="https://paulis.online/endpoint", maindir_int=maindirectory):
    # Import requests if not already imported
    try:
        requests
    except NameError:
        import requests
    # Get maindir_internal
    maindir_internal = os.path.join(maindir_int)
    # Post the score to the leaderboard using the """API"""
    # Get posted name from name.json in maindir
    with open(os.path.join(maindir_internal, "name.json"), "r") as rfile:
        posted_name = json.load(rfile)["name"]
    # If if name is blank, use "Anonymous"
    if posted_name == "":
        posted_name = "Anonymous"
    r = requests.get(paul_endpoint, params={'task':'put', 'name': posted_name, 'score': posted_score, 'game': posted_game})
    # Print the response
    print(r.text)

main_menu = SourceFileLoader('main', os.path.join(maindirectory, 'main.py')).load_module()

clock = pygame.time.Clock()

snake_block = 25
snake_speed = 15

font_style = pygame.font.SysFont("comicsansms", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

snake_song = pygame.mixer.Sound(os.path.join(assetdirectory, "Snake.wav"))
song_channel = pygame.mixer.Channel(1)

def Your_score(score):
    int_score = int(score)
    with open(os.path.join(assetdirectory, "scores.json"), "r") as f:
        data = json.load(f)
    if int_score > data["apples"]:
        data["apples"] = int_score
        with open(os.path.join(assetdirectory, "scores.json"), "w") as f:
            json.dump(data, f)

    value = score_font.render("Score: " + str(score), True, gray)
    dis.blit(value, [0, 0])
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [round(x[0] / snake_block) * snake_block, round(x[1] / snake_block) * snake_block, snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
def gameLoop(saved_score=False):
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    Left = False
    Right = False
    Up = False
    Down = False


    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Suck! Take the L, Press C-Play Again or Esc-Quit", red)
            Your_score(Length_of_snake - 1)
            if not saved_score:
                post_highscore(int(Length_of_snake - 1), posted_game="Snake")
                saved_score = True
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    song_channel.stop()
                    main_menu.main(False)
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                        song_channel.stop()
                        main_menu.main(False)
                        quit()

                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                song_channel.stop()
                main_menu.main(False)
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    song_channel.stop()
                    main_menu.main(False)
                    quit()
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    if Right:
                        x1_change = snake_block
                        y1_change = 0
                    else:
                        Left = True
                        Up = False
                        Down = False
                        Right = False
                if event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    if Left:
                        x1_change = -snake_block
                        y1_change = 0
                    else:
                        Left = False
                        Up = False
                        Down = False
                        Right = True
                    
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    if Down:
                        x1_change = 0
                        y1_change = snake_block
                    else:
                        Left = False
                        Up = True
                        Down = False
                        Right = False
                if event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    if Up:
                        x1_change = 0
                        y1_change = -snake_block
                    else:
                        Left = False
                        Up = False
                        Down = True
                        Right = False
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        pygame.display.update()
        if round(abs(x1 - foodx)) < snake_block and round(abs(y1 - foody)) < snake_block:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

            Length_of_snake += 1
        clock.tick(snake_speed)
    pygame.quit()
song_channel.play(snake_song, loops=-1)
gameLoop()
