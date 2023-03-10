import pygame
import random
import os

def main():
    main_dir = os.path.dirname(os.path.abspath(__file__))

    # initialize pygame
    pygame.init()

    # set window size
    window_size = (800, 600)

    # initialize the window
    screen = pygame.display.set_mode(window_size)

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
        image = pygame.image.load(f"{main_dir}\hangman" + str(i) + ".png")
        images.append(image)

    # list of words
    words = ["python", "apple", "orange", "computer", "science"]

    # select a random word
    word = random.choice(words)

    # set initial variables
    hangman_status = 0
    guessed_letters = []
    word_to_guess = ["_"] * len(word)

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
        if "_" not in word_to_guess or hangman_status == 6:
            running = False

    # deinitialize pygame
    pygame.quit()# Write your code here :-)

if __name__ == "__main__":
    main()