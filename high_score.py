import json
from operator import itemgetter

import pygame as pg
from pygame import freetype


pg.init()
BG_COLOR = pg.Color('gray12')
BLUE = pg.Color('dodgerblue')
FONT = freetype.Font(None, 24)


def save(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)  # Write the list to the json file.


def load():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        highscores = []  # Define an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    score = 200  # Current score of the player.
    name = ''  # The name that is added to the highscores list.
    highscores = load()  # Load the json file.

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # Append the name and score and save the sorted the list
                    # when enter is pressed.
                    highscores.append([name, score])
                    save(sorted(highscores, key=itemgetter(1), reverse=True))
                    name = ''
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]  # Remove the last character.
                else:
                    name += event.unicode  # Add a character to the name.

        screen.fill((30, 30, 50))
        # Display the highscores.
        for y, (hi_name, hi_score) in enumerate(highscores):
            FONT.render_to(screen, (100, y*30+40), f'{hi_name} {hi_score}', BLUE)

        FONT.render_to(screen, (100, 360), f'Your score is: {score}', BLUE)
        FONT.render_to(screen, (100, 390), f'Enter your name: {name}', BLUE)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()