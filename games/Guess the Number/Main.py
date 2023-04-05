import pygame
import random
from importlib.machinery import SourceFileLoader
import os

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, 'assets')
main = SourceFileLoader('main', os.path.join(main_dir, ("main.py"))).load_module()

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the window size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the font and font size
font = pygame.font.SysFont(None, 48)

# Set the random number to guess
number = random.randint(1, 100)

# Set the initial number of guesses to 0
num_guesses = 0

# Define the message variable
message = ""

# Create a text input box
input_box_width = 200
input_box_height = 50
input_box_x = (SCREEN_WIDTH - input_box_width) // 2
input_box_y = (SCREEN_HEIGHT - input_box_height) // 2 - 100
input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
input_text = ""

# Create a button
button_width = 100
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse click was on the button
            if button_rect.collidepoint(mouse_pos):
                # Increment the number of guesses
                num_guesses += 1

                # Get the user's guess
                guess = int(input_text)

                # Check if the guess is correct
                if guess == number:
                    message = "You win!"
                elif guess < number:
                    message = "Too low!"
                else:
                    message = "Too high!"

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            # Check if the key is a number
            if event.unicode.isdigit():
                # Add the digit to the input text
                input_text += event.unicode
            # Check if the key is the backspace key
            elif event.key == pygame.K_BACKSPACE:
                # Remove the last character from the input text
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False
                main.main(False)
                break

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the input box
    pygame.draw.rect(screen, BLACK, input_box, 2)
    input_text_surface = font.render(input_text, True, BLACK)
    input_text_x = input_box.x + 5
    input_text_y = input_box.y + (input_box_height - input_text_surface.get_height()) // 2
    screen.blit(input_text_surface, (input_text_x, input_text_y))

    # Draw the button
    pygame.draw.rect(screen, BLACK, button_rect)
    button_text = font.render("Guess", True, WHITE)
    button_text_x = button_rect.x + (button_width - button_text.get_width()) // 2
    button_text_y = button_rect.y + (button_height - button_text.get_height()) // 2
    screen.blit(button_text, (button_text_x, button_text_y))

    # Draw the message
    message_surface = font.render(message, True, BLACK)
    message_x = (SCREEN_WIDTH - message_surface.get_width()) // 2
    message_y = (SCREEN_HEIGHT - message_surface.get_height()) // 2 + 100
    screen.blit(message_surface, (message_x, message_y))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
