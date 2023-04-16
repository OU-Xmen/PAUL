import pygame
from importlib.machinery import SourceFileLoader
from tkinter import messagebox
import os
import sys


#testing now please?

main_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.join(main_dir, 'games')

print("Loading games...")

t = SourceFileLoader("themes", os.path.join(main_dir, "themes.py")).load_module()
logger = SourceFileLoader("logger", os.path.join(main_dir,"logger.py")).load_module()

page = 1

# Initialize pygame and set up window
pygame.init()
logger.log("Pygame initialized", 1)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("P.A.U.L. - Main Menu")

# Load font
font = pygame.font.SysFont('comicsansms', 26)

# Load image
# TODO change to comply with #13
splash_image = pygame.image.load("assets/img/paul.jpg")
splash_image = pygame.transform.scale(splash_image, (800, 600))
pygame.display.set_icon(splash_image)

slide_image = pygame.image.load("assets/img/slide_puzzle.png")
logger.log("Images loaded", 1)

# Load sounds
paul_sound = pygame.mixer.Sound("assets/sounds/paul.wav")
music = pygame.mixer.Sound("assets/sounds/Menu_Music.wav")
logger.log("Sounds loaded", 1)


BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

HORIZONTAL_SPACING = (WINDOW_WIDTH - (5 * BUTTON_WIDTH)) / 6
VERTICAL_SPACING = (WINDOW_HEIGHT - (3 * BUTTON_HEIGHT)) / 4

# Define where the buttons will go
button_rects = [
    pygame.Rect(150, 150, 150, 75),
    pygame.Rect(325, 150, 150, 75),
    pygame.Rect(500, 150, 150, 75),
    pygame.Rect(150, 250, 150, 75),
    pygame.Rect(325, 250, 150, 75),
    pygame.Rect(500, 250, 150, 75),
    pygame.Rect(150, 350, 500, 75)
]


# Button Labels
d_games = {
    1: ["Puzzle", "Asteroids", "Tetris", "Pong", "Hangman", "Mad Libs", "Scoreboard"],
    2: ["Checkers", "Chess", "Guess the Number", "Snake", "Tic Tac Toe", "Connect 4", "Scoreboard"],
    3: ["Mancala", "RPS", "PAULatformer", None, None, None, "Scoreboard"]
}



def errorHandler(error, i=4):
    logger.log(error, i)
    messagebox.showerror("Error", f"P.A.U.L. has encountered an error:\n{error}\nProgram will now quit.")
    cleanup()
    quit()
    
def current_page(pagenum):
    try:
        pagenum += 0
    except TypeError as e:
        errorHandler(e)
    current_games = d_games.get(pagenum)
    return current_games

def change_page(pagenum, change):
    try:
        pagenum += change
    except TypeError as e:
        errorHandler(e)
    return pagenum

def set_page_return_current_page(pagenum):
    # current_games = current_page(pagenum)
    return pagenum

def game_runner(i, games, game_dir):
    game_to_run = games[i]
    print(game_to_run)
    music.stop()
    print(f"{games[i]} was clicked")

    logger.log(f"Preparing to run {games[i]}.")
    try:
        game = SourceFileLoader('game', os.path.join(game_dir, f'{games[i]}', 'main.py')).load_module()
        game.main()
    except Exception as e:
        errorHandler(e)



# Splash screen flag
def main(splash):

    pygame.display.set_caption("P.A.U.L. - Main Menu")

    # Main game loop
    running = True
    tunes = True
    page = 1
    next_page_rect = pygame.Rect(500, 500, 150, 75)
    previous_page_rect = pygame.Rect(150, 500, 150, 75)
    settings_rect = pygame.Rect(500, 25, 150, 75)
    credits_rect = pygame.Rect(150, 25, 150, 75)



    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button was clicked
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        game_runner(i, games, game_dir)

                if next_page_rect.collidepoint(event.pos):
                    if show_next is True:
                        page = change_page(page, 1)
                if previous_page_rect.collidepoint(event.pos):
                    if show_previous is True:
                        page = change_page(page, -1)

                if settings_rect.collidepoint(event.pos):
                    music.stop()
                    settings = SourceFileLoader('settings', 'settings.py').load_module()
                
                if credits_rect.collidepoint(event.pos):
                    music.stop()
                    creditss = SourceFileLoader('credits', 'credits.py').load_module()
                    creditss.main()

        show_next = False
        show_previous = False

        # Clear screen
        try:
            screen.fill(t.BACKGROUND)
        except Exception as e:
            print(e)
            logger.log(e, 3)

        if splash:
            # Draw splash screen
            screen.blit(splash_image, (0, 0))
            pygame.display.update()
            paul_sound.play()
            logger.log("Running splash screen")
            pygame.time.wait(3000)  # Show splash screen for 3 seconds
            splash = False
            pygame.event.clear()
            logger.log("Running main menu")
        elif tunes: 
            music.play(loops=-1) # loop music forever
            tunes = False
        else:
            music.set_volume(.5)
            games = current_page(page)
            #print(games)
            for i, rect in enumerate(button_rects):
                if games[i] is not None:
                    pygame.draw.rect(screen, t.GAME_BUTTONS, rect)
                    button_text = font.render(games[i], True, t.TEXT)
                    screen.blit(button_text, (rect.x + 10, rect.y + 65))

            if page < 3:
                show_next = True
                pygame.draw.rect(screen, t.PAGE_BUTTONS, next_page_rect)
                button_text = font.render("Next Page", True, t.TEXT)
                screen.blit(button_text, (next_page_rect.x + 20, next_page_rect.y + 65))
            if page > 1:
                show_previous = True
                pygame.draw.rect(screen, t.PAGE_BUTTONS, previous_page_rect)
                button_text = font.render("Previous Page", True, t.TEXT)
                screen.blit(button_text, (previous_page_rect.x-10, previous_page_rect.y + 65))

            pygame.draw.rect(screen, t.PAGE_BUTTONS, settings_rect)
            pygame.draw.rect(screen, t.PAGE_BUTTONS, credits_rect)
            setting_button_text = font.render("Settings", True, t.TEXT)
            screen.blit(setting_button_text, (settings_rect.x, settings_rect.y + 75))
            credits_button_text = font.render("Credits", True, t.TEXT)
            screen.blit(credits_button_text, (credits_rect.x, credits_rect.y + 75))

            
            
            
        pygame.display.update()

def cleanup():
    pygame.quit()
    logger.log("Program terminated\n\n")



if __name__ == '__main__':
    try: 
        main(True)
    except Exception as e:
        cleanup()
