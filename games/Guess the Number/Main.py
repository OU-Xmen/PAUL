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

# Load assets
gameIcon = pygame.image.load(os.path.join(assets_dir, 'paulicon.png')) 
background = pygame.image.load(os.path.join(assets_dir, 'background.png'))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the window size and properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guess the Number")
pygame.display.set_icon(gameIcon)

theme = pygame.mixer.Sound(os.path.join(assets_dir, 'Guess the Number.wav'))
song_channel = pygame.mixer.Channel(1)

# Set the font and font size
font = pygame.font.SysFont(None, 48)

# Set the random number to guess
number = random.randint(1, 1000)

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

def init_words(text, size, center_x, center_y, text_color):
    font = pygame.font.SysFont('comicsansms', size)
    temp_rend = pygame.font.Font.render(font, text, True, text_color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect

# Create buttons
button_width = 100
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

quit_rend, quit_rect = init_words('QUIT', 30, 50, 50, (200, 0, 0))

song_channel.play(theme, loops = -1)

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            song_channel.stop()
            main.main(False)
            quit()

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse click was on the button
            if button_rect.collidepoint(mouse_pos):
                if input_text == '':
                    message = "Pathetic..."
                else:
                    num_guesses += 1
                    guess = int(input_text)
                    if guess == number:
                        message = "You win!"
                    elif guess < number:
                        message = "Too low..."
                    else:
                        message = "Too high..."
            if quit_rect.collidepoint(mouse_pos):
                running = False
                song_channel.stop()
                main.main(False)
                quit()

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text == '':
                    message = "Pathetic..."
                else:
                    num_guesses += 1
                    guess = int(input_text)
                    if guess == number:
                        message = "You win!"
                    elif guess < number:
                        message = "Too low..."
                    else:
                        message = "Too high..."
            if event.unicode.isdigit():
                pygame.key.set_repeat(250, 50)
                input_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                pygame.key.set_repeat(250, 50)
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False
                song_channel.stop()
                main.main(False)
                quit()

    # apply background
    screen.blit(background, (0, 0))

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

    screen.blit(quit_rend, quit_rect)

    # Draw the message
    message_surface = font.render(message, True, BLACK)
    message_x = (SCREEN_WIDTH - message_surface.get_width()) // 2
    message_y = (SCREEN_HEIGHT - message_surface.get_height()) // 2 + 100
    screen.blit(message_surface, (message_x, message_y))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
