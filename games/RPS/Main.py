try:
    import pygame
    pygame.init()
    import random
    import os
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(maindirectory, "assets")
except ImportError:
    print("One or more required modules could not be imported. Please try again.")
    quit()

def paul_choice():
    choice = random.choice(["rock", "paper", "scissors"])
    return choice
    
    
def compare_choices(player_choice, paul_choice):
    if player_choice == "rock":
        if paul_choice == "scissors":
            return "player"
        elif paul_choice == "paper":
            return "paul"
        else:
            return "tie"  
    elif player_choice == "paper":
        if paul_choice == "rock":
            return "player"
        elif paul_choice == "scissors":
            return "paul"
        else:
            return "tie"  
    elif player_choice == "scissors":
        if paul_choice == "paper":
            return "player"
        elif paul_choice == "rock":
            return "paul"
        else:
            return "tie"        
    

def main():
    # create window, set size, caption, and icon
    size = WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Rock Paper Scissors")
    icon = pygame.image.load(os.path.join(assetdirectory, "paulicon.png"))
    pygame.display.set_icon(icon)

    # define important variables
    player = ""
    paul = paul_choice()
    message = ""

    # define basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # define font
    font = pygame.font.SysFont("comicsans", 30)

    # create the buttons
    rock_button_size = rock_button_width, rock_button_height = 200, 200
    rock_button_pos = rock_button_x, rock_button_y = 50, 200
    rock_button_rect = pygame.Rect(rock_button_pos, rock_button_size)

    paper_button_size = paper_button_width, paper_button_height = 200, 200
    paper_button_pos = paper_button_x, paper_button_y = 300, 200
    paper_button_rect = pygame.Rect(paper_button_pos, paper_button_size)

    scissors_button_size = scissors_button_width, scissors_button_height = 200, 200
    scissors_button_pos = scissors_button_x, scissors_button_y = 550, 200
    scissors_button_rect = pygame.Rect(scissors_button_pos, scissors_button_size)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse pos
                mouse_pos = pygame.mouse.get_pos()

                # check if mouse is over rock button
                if rock_button_rect.collidepoint(mouse_pos):
                    player = "rock"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                    elif comparison == "tie":
                        message = "It's a tie!"

                elif paper_button_rect.collidepoint(mouse_pos):
                    player = "paper"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                    elif comparison == "tie":
                        message = "It's a tie!"
                    
                elif scissors_button_rect.collidepoint(mouse_pos):
                    player = "scissors"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                    elif comparison == "tie":
                        message = "It's a tie!"
                        
                paul = paul_choice()
                    

        screen.fill(WHITE)

        # draw buttons
        pygame.draw.rect(screen, BLACK, rock_button_rect, 0)
        rock_button_text = font.render("Rock", True, WHITE)
        rock_button_text_x = rock_button_x + (rock_button_width - rock_button_text.get_width()) // 2 
        rock_button_text_y = rock_button_y + (rock_button_height - rock_button_text.get_height()) // 2
        screen.blit(rock_button_text, (rock_button_text_x, rock_button_text_y))

        pygame.draw.rect(screen, BLACK, paper_button_rect, 0)
        paper_button_text = font.render("Paper", True, WHITE)
        paper_button_text_x = paper_button_x + (paper_button_width - paper_button_text.get_width()) // 2 
        paper_button_text_y = paper_button_y + (paper_button_height - paper_button_text.get_height()) // 2
        screen.blit(paper_button_text, (paper_button_text_x, paper_button_text_y))

        pygame.draw.rect(screen, BLACK, scissors_button_rect, 0)
        scissors_button_text = font.render("Scissors", True, WHITE)
        scissors_button_text_x = scissors_button_x + (scissors_button_width - scissors_button_text.get_width()) // 2 
        scissors_button_text_y = scissors_button_y + (scissors_button_height - scissors_button_text.get_height()) // 2
        screen.blit(scissors_button_text, (scissors_button_text_x, scissors_button_text_y))

        # draw message
        message_text = font.render(message, True, BLACK)
        message_text_x = (WIDTH - message_text.get_width()) // 2
        message_text_y = (HEIGHT - message_text.get_height()) // 4
        screen.blit(message_text, (message_text_x, message_text_y))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

