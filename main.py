import pygame

# Initialize pygame and set up window
pygame.init()
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

# Load sounds
paul_sound = pygame.mixer.Sound("assets/sounds/paul.mp3")
music = pygame.mixer.Sound("assets/sounds/fallen_down.ogg")

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
    "Puzzle", "Asteroids", "Aliens", "Game 4", "Game 5", "Game 6", "Scoreboard"
]


# Splash screen flag
splash = True

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
                    print(f"{games[i]} was clicked")

    # Clear screen
    screen.fill(WHITE)

    if splash:
        # Draw splash screen
        screen.blit(splash_image, (0, 0))
        pygame.display.update()
        paul_sound.play()
        pygame.time.wait(3000)  # Show splash screen for 3 seconds
        music.play(loops=-1) # loop music forever
        music.set_volume(.5)
        splash = False
    else:
        # Draw buttons
        for i, rect in enumerate(button_rects):
            pygame.draw.rect(screen, pygame.Color("darkred"), rect)
            button_text = font.render(f"{games[i]}", True, BLACK)
            screen.blit(button_text, (rect.x + 25, rect.y + 75))
        

    pygame.display.update()

# Quit pygame
pygame.quit()
