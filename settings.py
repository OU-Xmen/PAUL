import pygame
import themes as t
from importlib.machinery import SourceFileLoader

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a font object
font = pygame.font.Font(None, 36)

# Define the dropdown options
themes = ["Dark", "Light", "Midnight"]

# Define the dropdown button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 100

# Define the dropdown menu dimensions
MENU_WIDTH = BUTTON_WIDTH
MENU_HEIGHT = len(themes) * BUTTON_HEIGHT

# Define the dropdown menu coordinates
menu_x = 500
menu_y = 200

# Define the dropdown button coordinates
button_x = menu_x
button_y = 100

f = open("current.theme", "r")
current_theme = f.readline()
f.close()
selected_option = themes.index(current_theme.capitalize())

# Set the initial dropdown menu state
menu_open = False

# Define the function to draw the dropdown menu
def draw_menu():
    menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    menu_surface.fill(WHITE)
    for i, option in enumerate(themes):
        text_surface = font.render(option, True, BLACK)
        text_rect = text_surface.get_rect(center=(MENU_WIDTH // 2, (i + 0.5) * BUTTON_HEIGHT))
        menu_surface.blit(text_surface, text_rect)
    screen.blit(menu_surface, (menu_x, menu_y))

# Define the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = SourceFileLoader("main", "main.py").load_module()
            main.main(False)
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_rect.collidepoint(event.pos):
                main = SourceFileLoader("main", "main.py").load_module()
                main.main(False)
                quit()

                

            if event.button == 1:
                if menu_open:
                    # If the menu is open, check if the user clicked an option
                    if menu_rect.collidepoint(event.pos):
                        selected_option = (event.pos[1] - menu_y) // BUTTON_HEIGHT
                        print("Selected option:", themes[selected_option])
                        menu_open = False
                        fw = open("current.theme", "w")
                        fw.write(themes[selected_option].lower())
                        fw.close()
                
                else:
                    # If the menu is closed, check if the user clicked the button
                    if button_rect.collidepoint(event.pos):
                        menu_open = True
            elif event.button == 4:
                # Scroll up to select the previous option
                selected_option = (selected_option - 1) % len(themes)
                print("Selected option:", themes[selected_option])
                fw = open("current.theme", "w")
                fw.write(themes[selected_option].lower())
            elif event.button == 5:
                # Scroll down to select the next option
                selected_option = (selected_option + 1) % len(themes)
                print("Selected option:", themes[selected_option])
                fw = open("current.theme", "w")
                fw.write(themes[selected_option].lower())
    # Draw the button
    button_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    if menu_open:
        button_surface.fill(GRAY)
    else:
        screen.fill(BLACK)
        button_surface.fill(WHITE)
    button_text = font.render(themes[selected_option], True, BLACK)
    button_rect = button_surface.get_rect(topleft=(button_x, button_y))
    button_surface.blit(button_text, button_text.get_rect(center=(BUTTON_WIDTH // 2, BUTTON_HEIGHT // 2)))
    screen.blit(button_surface, button_rect)
    
    # Draw the menu if it's open
    if menu_open:
        draw_menu()
        menu_rect = pygame.Rect(menu_x, menu_y, MENU_WIDTH, MENU_HEIGHT)

    back_rect = pygame.Rect(500, 500, 150, 75)
    
    pygame.draw.rect(screen, t.PAGE_BUTTONS, back_rect)
    button_text = font.render("Back", True, t.TEXT)
    screen.blit(button_text, (back_rect.x+45, back_rect.y + 75))
    # Update the display
    pygame.display.update()

