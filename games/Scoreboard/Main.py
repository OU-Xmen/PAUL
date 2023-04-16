#Scoreboard 
#is going to list games and then the top 5 scores for each game in a python window, Right now with how Json works, it only stores the top score, so it will only show the top score for each game
# wowza 

#make window
import pygame
import json 
from operator import itemgetter
from importlib.machinery import SourceFileLoader
import os
import requests
import sys
pygame.init()
screen = pygame.display.set_mode((800,600))
# pygame.set_caption("Scoreboard")

pygame.display.flip()

#scoreboard header
# Display the text "Scoreboard" in the top center
font = pygame.font.SysFont('comicsansms', 30)
text = font.render("Scoreboard", True, (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (400, 50)
screen.blit(text, text_rect)
#access asteroid score json file in the asteroids asset file in the games folder
main_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.join(main_dir, 'games')
asteroid_dir = os.path.join(game_dir, "Asteroids")
asset_dir = os.path.join(asteroid_dir, "assets")
clock = pygame.time.Clock()

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 24
SPEED = 0.5

main_menu = SourceFileLoader('main', os.path.join(main_dir, "..", "..", "main.py")).load_module()

# [LOCAL SCORES - OLD]
#asteroids_score = SourceFileLoader("scores", os.path.join(asset_dir, "scores.json")).load_module()

# [Game directories] (MUST stay in order)
# game_names = ["Asteroids", "Snake", "PAULatformer", "Puzzle", "Tetris"]
# directory_asteroids_json = os.path.join(os.path.abspath(__file__), '..', '..', 'Asteroids', 'assets', 'scores.json')
# directory_snake_json = os.path.join(os.path.abspath(__file__), '..',  '..','Snake', 'assets', 'scores.json')
# directory_paulatformer_json = os.path.join(os.path.abspath(__file__), '..', '..','PAULatformer','assets', 'scores.json')
# directory_puzzle_json = os.path.join(os.path.abspath(__file__), '..', '..','Puzzle', 'assets', 'scores.json')
# directory_tetris_json = os.path.join(os.path.abspath(__file__), '..', '..','Tetris', 'assets', 'scores.json')

# [Game paths, combined into list] (MUST stay in order of game_names)
# games_path_list = [directory_asteroids_json, directory_snake_json, directory_paulatformer_json, directory_puzzle_json, directory_tetris_json]

# Custom function to return the tuple of (name, score) of a score from game based on the path
# def get_score_from_json(filepath):
#     # print(f"Attempting to get score from {filepath}")
#     if len(filepath) <= 0:
#         raise "Unable to read score"
#     with open(os.path.join(filepath), "r") as f:
#         # read from json file and store in variable "data"
#         data = json.load(f)
#         # Get value from highscore
#         try:
#             highscore_value = data["highscore"]
#         except (ValueError, KeyError):
#             highscore_value = 0
#         # [TEMP, DOES NOT EXIST YET] Get name from highscore
#         try:
#             highscore_name = data["highscore_name"]
#         except (ValueError, KeyError):
#             highscore_name = "No name yet lol"
#     # convert highscore_value to int
#     highscore_value = int(highscore_value)
#     return (highscore_name, highscore_value)

# # Get score tuples from all games and store in list
# all_scores_list = []
# for game in games_path_list:
#     temp_score_tuple = get_score_from_json(game)
#     all_scores_list.append(temp_score_tuple)

# [Debug] Print all game scores to console
# full_scoreboard_text = ""
# game_index = 0
# placement = 50
# for score in all_scores_list:
#     game_name = game_names[game_index]
#     full_scoreboard_text = f"{str(game_name).title()} highscore, achieved by {score[0]}: {score[1]}.\n\n"
#     font = pygame.font.Font(None, 20)
#     text = font.render(full_scoreboard_text, True, (0,0,0))
#     screen.blit(text, (0,placement))
#     game_index += 1
#     placement += 50

# Reach out to PAUL endpoint for highscores
def get_highscores(game_names=["Asteroids", "Snake", "PAULatformer", "Puzzle", "Tetris"], paul_endpoint="https://web.physcorp.com/paul/endpoint.php"):
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        return f"[I have died, rip me. Error code {r.status_code}] {r.text}"
    else:
        full_text = []
        full_text.append("")
        # Loop through each game
        for game_name in game_names:
            game_dict = r.json()
            game = game_dict[game_name]
            # If game is empty, no scores
            if game == "":
                full_text.append(f"No scores for {game_name} yet!")
                full_text.append("")
            else:
                # Split scores into list
                scores = game.split(",")
                # Compile scores into a string separated by newlines
                full_text.append(f"=== {game_name} Scoreboard ===")
                full_text.append("")
                for score in scores:
                    formatted_score = score.replace(":::", " - ")
                    full_text.append(f"{formatted_score}")
                full_text.append("")
        return full_text

# Get highscores from PAUL endpoint
highscores = get_highscores()

# Output to console
print("----- FULL HIGHSCORES -----")
print(highscores)
print("---------------------------")

def scroll_credits():       
    text_height = len(highscores) * (FONT_SIZE + 10)
    scroll_y = SCREEN_HEIGHT

    while scroll_y > -text_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.main(False)
                    quit()
        screen.fill(BACKGROUND_COLOR)

        for i, line in enumerate(highscores):
            rendered_text = font.render(line, True, FONT_COLOR)
            text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, scroll_y + i * (FONT_SIZE + 10)))
            screen.blit(rendered_text, text_rect)

        scroll_y -= SPEED
        pygame.display.flip()
        clock.tick(60)

    return False  # Return False when the credits are no longer visible

#display text on pygame window
# font = pygame.font.Font(None, 20)
# text = font.render(full_scoreboard_text, True, (0,0,0))
# screen.blit(text, (0,50))

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                main_menu.main(False)
                quit()
        pygame.display.update()

        if not scroll_credits():  # Break the loop and quit when the credits are done
            break

if __name__ == '__main__':
    main()