import pygame
import random
import os
import requests
response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
from importlib.machinery import SourceFileLoader

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets')


logger = SourceFileLoader('logger', os.path.join(main_dir, "logger.py")).load_module()
main_menu = SourceFileLoader('main', os.path.join(main_dir, "main.py")).load_module()


def main():
    # initialize pygame
    pygame.init()

    # set window size
    window_size = width, height = 800, 600

    # initialize the window
    screen = pygame.display.set_mode((window_size))

    # set title
    pygame.display.set_caption("Hangman Game")

    # define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # load font
    font = pygame.font.Font(None, 30)

    # load the hangman images
    images = []
    for i in range(7):
        image = pygame.image.load(os.path.join(current_dir, "hangman" + str(i) + ".png"))  # Changing to comply with issue #14
        images.append(image)

    # list of words
    words = response.text.splitlines()

    # select a random word
    word = random.choice(words)

    # set initial variables
    hangman_status = 0
    guessed_letters = []
    word_to_guess = ["_"] * len(word)

    def results(status):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_menu.main(False)
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        main_menu.main(False)
                        quit()
            
            screen.fill(white)
            word_text = font.render(word, True, black)
            screen.blit(word_text, (width // 2, height // 2))
            pygame.display.update()

            
    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main(False)
                quit()

            if event.type == pygame.KEYDOWN:
                # check if the key pressed is a letter
                if event.unicode.isalpha():
                    letter = event.unicode.lower()
                    if letter in word and letter not in guessed_letters:
                        # replace underscores with the correctly guessed letter
                        for i in range(len(word)):
                            if word[i] == letter:
                                word_to_guess[i] = letter

                    elif letter not in guessed_letters:
                        # increment hangman status
                        hangman_status += 1
                        guessed_letters.append(letter)
                        
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu.main(False)
                    quit()

        screen.fill(white)

        # draw hangman
        screen.blit(images[hangman_status], (100, 100))

        # draw word
        word_text = font.render(" ".join(word_to_guess), True, black)
        screen.blit(word_text, (250, 350))

        # draw wrong letters
        wrong_text = font.render("Wrong letters: " + " ".join(guessed_letters), True, red)
        screen.blit(wrong_text, (250, 400))

        pygame.display.update()

        # check if the game is over
        if "_" not in word_to_guess:
            status = True
            running = False
        elif hangman_status == 6:
            status = False
            running = False

    # deinitialize pygame
    results(status)

if __name__ == "__main__":
    main()
