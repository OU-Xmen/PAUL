#Scoreboard 
#is going to list games and then the top 5 scores for each game in a python window, Right now with how Json works, it only stores the top score, so it will only show the top score for each game
# wowza 

#make window
import pygame
import json 
from operator import itemgetter
from importlib.machinery import SourceFileLoader
import os
pygame.init()
background_color = (234, 212, 252)
screen = pygame.display.set_mode((800,600))
screen.fill(background_color)
# pygame.set_caption("Scoreboard")

pygame.display.flip()

#scoreboard header
font = pygame.font.Font(None, 75)
text = font.render("Scoreboard", True, (0,0,0))
screen.blit(text, (250,0))
#access asteroid score json file in the asteroids asset file in the games folder
main_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.join(main_dir, 'games')
asteroid_dir = os.path.join(game_dir, "Asteroids")
asset_dir = os.path.join(asteroid_dir, "assets")
#asteroids_score = SourceFileLoader("scores", os.path.join(asset_dir, "scores.json")).load_module()

# [Game directories] (MUST stay in order)
game_names = ["Asteroids", "Snake", "PAULatformer", "Puzzle", "Tetris"]
directory_asteroids_json = os.path.join(os.path.abspath(__file__), '..', 'games', 'Asteroids', 'assets', 'scores.json')
directory_snake_json = os.path.join(os.path.abspath(__file__), '..',  'games','Snake', 'assets', 'scores.json')
directory_paulatformer_json = os.path.join(os.path.abspath(__file__), '..', 'games','PAULatformer','assets', 'scores.json')
directory_puzzle_json = os.path.join(os.path.abspath(__file__), '..', 'games','Puzzle', 'assets', 'scores.json')
directory_tetris_json = os.path.join(os.path.abspath(__file__), '..', 'games','Tetris', 'assets', 'scores.json')

# [Game paths, combined into list] (MUST stay in order of game_names)
games_path_list = [directory_asteroids_json, directory_snake_json, directory_paulatformer_json, directory_puzzle_json, directory_tetris_json]

# Custom function to return the tuple of (name, score) of a score from game based on the path
def get_score_from_json(filepath):
    # print(f"Attempting to get score from {filepath}")
    if len(filepath) <= 0:
        raise "Unable to read score"
    with open(os.path.join(filepath), "r") as f:
        # read from json file and store in variable "data"
        data = json.load(f)
        # Get value from highscore
        try:
            highscore_value = data["highscore"]
        except (ValueError, KeyError):
            highscore_value = 0
        # [TEMP, DOES NOT EXIST YET] Get name from highscore
        try:
            highscore_name = data["highscore_name"]
        except (ValueError, KeyError):
            highscore_name = "No name yet lol"
    # convert highscore_value to int
    highscore_value = int(highscore_value)
    return (highscore_name, highscore_value)

# Get score tuples from all games and store in list
all_scores_list = []
for game in games_path_list:
    temp_score_tuple = get_score_from_json(game)
    all_scores_list.append(temp_score_tuple)

# [Debug] Print all game scores to console
full_scoreboard_test = ""
game_index = 0
placement = 50
for score in all_scores_list:
    game_name = game_names[game_index]
    full_scoreboard_test = f"{str(game_name).title()} highscore, achieved by {score[0]}: {score[1]}.\n\n"
    font = pygame.font.Font(None, 20)
    text = font.render(full_scoreboard_test, True, (0,0,0))
    screen.blit(text, (0,placement))
    game_index += 1
    placement += 50

# Output to console
print("----- FULL HIGHSCORES -----")
print(full_scoreboard_test)
print("---------------------------")

#display text on pygame window
# font = pygame.font.Font(None, 20)
# text = font.render(full_scoreboard_test, True, (0,0,0))
# screen.blit(text, (0,50))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()




