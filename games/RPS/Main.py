try:
    import pygame
    pygame.init()
    import random
    import os
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    currentdirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(currentdirectory, "assets")
    main_menu = SourceFileLoader('main', os.path.join(maindirectory, 'main.py')).load_module()
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
    

def init_words(text, size, center_x, center_y, text_color):
    font = pygame.font.SysFont('comicsansms', size)
    temp_rend = pygame.font.Font.render(font, text, True, text_color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect


def main():
    # create window, set size, caption, and icon
    size = WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Rock Paper Scissors")
    icon = pygame.image.load(os.path.join(assetdirectory, "paulicon.png"))
    background = pygame.image.load(os.path.join(assetdirectory, "background.png"))
    pygame.display.set_icon(icon)

    # define important variables
    player = ""
    paul = paul_choice()
    message = ""
    message_color = 'black'

    # define basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # define font
    font = pygame.font.SysFont("comicsans", 30)

    # create the buttons
    rock_button_size = rock_button_width, rock_button_height = 150, 100
    rock_button_pos = rock_button_x, rock_button_y = 75, 250
    rock_button_rect = pygame.Rect(rock_button_pos, rock_button_size)

    paper_button_size = paper_button_width, paper_button_height = 150, 100
    paper_button_pos = paper_button_x, paper_button_y = 325, 250
    paper_button_rect = pygame.Rect(paper_button_pos, paper_button_size)

    scissors_button_size = scissors_button_width, scissors_button_height = 150, 100
    scissors_button_pos = scissors_button_x, scissors_button_y = 575, 250
    scissors_button_rect = pygame.Rect(scissors_button_pos, scissors_button_size)

    quit_rend, quit_rect = init_words('QUIT', 30, 50, 50, (200, 0, 0))

    # Game loop
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


            # check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rock_button_rect.collidepoint(mouse_pos):
                    player = "rock"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                        message_color = 'green'
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                        message_color = 'red'
                    elif comparison == "tie":
                        message = "It's a tie!"
                        message_color = "orange"

                elif paper_button_rect.collidepoint(mouse_pos):
                    player = "paper"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                        message_color = 'green'
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                        message_color = 'red'
                    elif comparison == "tie":
                        message = "It's a tie!"
                        message_color = "orange"
                    
                elif scissors_button_rect.collidepoint(mouse_pos):
                    player = "scissors"
                    comparison = compare_choices(player, paul)
                    if comparison == "player":
                        message = "You Win!"
                        message_color = 'green'
                    elif comparison == "paul":
                        message ="P.A.U.L. Wins!"
                        message_color = 'red'
                    elif comparison == "tie":
                        message = "It's a tie!"
                        message_color = "orange"
                
                elif quit_rect.collidepoint(mouse_pos):
                    running = False
                    main_menu.main(False)
                    quit()
                    
                paul = paul_choice()
                    

        screen.blit(background, (0, 0))

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

        screen.blit(quit_rend, quit_rect)

        # draw message
        message_text = font.render(message, True, message_color)
        message_text_x = (WIDTH - message_text.get_width()) // 2
        message_text_y = (HEIGHT - message_text.get_height()) // 3
        screen.blit(message_text, (message_text_x, message_text_y))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

