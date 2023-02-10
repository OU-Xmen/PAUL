import pygame
from logger import *
from importlib.machinery import SourceFileLoader
from tkinter import messagebox
import os

main_dir = os.path.dirname(os.path.abspath(__file__))

print("Loading games...")
#log("Loading games...")



'''
Will be added when game run logic is set up.
try:
    import slide_puzzle.Game
    import asteroids.main
    import AlienInvasion.alien_invasion
except ImportError:
    print("One or more modules failed to load.")
    quit()
'''

# Initialize pygame and set up window
pygame.init()
log("Pygame initialized", 1)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("P.A.U.L. - Main Menu")

# Define colors
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# Load font
font = pygame.font.Font(None, 36)

# Load image
splash_image = pygame.image.load("assets/img/paul.jpg")
splash_image = pygame.transform.scale(splash_image, (800, 600))
pygame.display.set_icon(splash_image)

slide_image = pygame.image.load("assets/img/slide_puzzle.png")
log("Images loaded", 1)

# Load sounds
paul_sound = pygame.mixer.Sound("assets/sounds/paul.wav")
music = pygame.mixer.Sound("assets/sounds/fallen_down.wav")
log("Sounds loaded", 1)

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
games = [
    "Puzzle", "Asteroids", "Tetris", "Pong", "Hangman", "Mad Libs", "Scoreboard"
]

def errorHandler(error, i=4):
    log(error, i)
    messagebox.showerror("Error", f"P.A.U.L. has encountered an error:\n{error}\nProgram will now quit.")
    cleanup()
    quit()


def game_runner(i):
    game_to_run = games[i]
    
    print(f"{game_to_run} was clicked")

    if game_to_run == "Puzzle":
        print("Running Slide Puzzle") # run Slide Puzzle script
        log(f"Preparing to run {game_to_run}.")
        try:
            music.stop()
            slide_puzzle = SourceFileLoader('Slide puzzle', os.path.join(main_dir, 'Slide puzzle\SlideGame.py')).load_module()
            slide_puzzle.main()
        except Exception as e:
            errorHandler(e)

    elif game_to_run == "Asteroids":
        print("Running Asteroids") # run Asteroids
        log(f"Preparing to run {game_to_run}.")
        try:
            music.stop()
            asteroids = SourceFileLoader('asteroids', os.path.join(main_dir, 'asteroids\main.py')).load_module()
            asteroids.main()
            log("Astroids successfully loaded.")
        except Exception as e:
            errorHandler(e)
            
    elif game_to_run == "Tetris":
        print("Running Tetris") # run Space Invaders 
        log(f"Preparing to run {game_to_run}")
        try:
            music.stop()
            tetris = SourceFileLoader('tetris', os.path.join(main_dir, 'tetris\\main.py')).load_module()
            tetris.main()
        except Exception as e:
            errorHandler(e)
    elif game_to_run == "Pong":
        print("Running Pong") # run whatever game 4 is
        log(f"Preparing to run {game_to_run}")
        try:
            music.stop()
            Pong = SourceFileLoader('Pong', os.path.join(main_dir, 'Pong\\Pong.py')).load_module()
            Pong.main()
        except Exception as e:
            errorHandler(e)
    elif game_to_run == "Hangman":
        print("Hangman") # run whatever game 5 is
        log(f"Preparing to run {game_to_run}")
        try:
            music.stop()
            hangman = SourceFileLoader('Hangman Game', os.path.join(main_dir, 'Hangman Game\\HangMan.py')).load_module()
            hangman.main()
        except Exception as e:
            errorHandler(e)
    elif game_to_run == "Mad Libs":
        print("Running Mad Libs") # run whatever game 6 is
        log(f"Preparing to run {game_to_run}")
        try:
            music.stop()
            mad_libs = SourceFileLoader('mad_libs', os.path.join(main_dir, 'mad_libs\\code\\mad_libs.py')).load_module()
            mad_libs.main()
        except Exception as e:
            errorHandler(e)
    elif game_to_run == "Scoreboard":
        print("Switching to Scoreboard") # Show scoreboard
        log(f"Preparing to run {game_to_run}")
    else:
        log(f"Game selection not valid", 2)
        raise Exception("No valid game selection made.")
        

# Splash screen flag
def main(splash):

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                # Check if any button was clicked
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        game_runner(i)


        # Clear screen
        screen.fill(WHITE)

        if splash:
            # Draw splash screen
            screen.blit(splash_image, (0, 0))
            pygame.display.update()
            paul_sound.play()
            log("Running splash screen")
            pygame.time.wait(3000)  # Show splash screen for 3 seconds
            music.play(loops=-1) # loop music forever
            splash = False
            log("Running main menu")
        else:
            # Draw buttons
            music.set_volume(.5)
            for i, rect in enumerate(button_rects):
                pygame.draw.rect(screen, pygame.Color("darkred"), rect)
                button_text = font.render(f"{games[i]}", True, BLACK)
                screen.blit(button_text, (rect.x + 25, rect.y + 75))
            

        pygame.display.update()

def cleanup():
    try:
        pygame.quit()
        log("Program terminated\n\n")
    except:
        pass
    

if __name__ == '__main__':
    try: 
        main(True)
    except Exception as e:
        cleanup()