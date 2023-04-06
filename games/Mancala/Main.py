try:
    import pygame
    pygame.init()
    import os
    import time
    from importlib.machinery import SourceFileLoader
    
    maindirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    currentdirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(currentdirectory, 'assets')
    main_menu = SourceFileLoader("main", os.path.join(maindirectory, 'main.py')).load_module()
except ImportError:
    print("One or more modules failed to load. Please try again.")
    quit()

# create a window with resolution 800x600
size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mancala")
icon = pygame.image.load(os.path.join(assetdirectory, 'paulicon.png'))
pygame.display.set_icon(icon)

#define font
font = pygame.font.SysFont('comicsansms', 30)

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARDCOLOR = (128, 101, 23)
HOLECOLOR = (118, 91, 13)

# game variables
binAmount = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

playerOne = True

messageCode = 0

giveawayPile = -1

lastRecipient = -1

chosenBin = -1

running = True
while running: # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # MOUSE CLICK COLLISION HANDLER
            if playerOne and a1_rect.collidepoint(mouse_pos):
                chosenBin = 5
            elif playerOne and b1_rect.collidepoint(mouse_pos):
                chosenBin = 4
            elif playerOne and c1_rect.collidepoint(mouse_pos):
                chosenBin = 3
            elif playerOne and d1_rect.collidepoint(mouse_pos):
                chosenBin = 2
            elif playerOne and e1_rect.collidepoint(mouse_pos):
                chosenBin = 1
            elif playerOne and f1_rect.collidepoint(mouse_pos):
                chosenBin = 0
            elif not(playerOne) and a2_rect.collidepoint(mouse_pos):
                chosenBin = 12
            elif not(playerOne) and b2_rect.collidepoint(mouse_pos):
                chosenBin = 11
            elif not(playerOne) and c2_rect.collidepoint(mouse_pos):
                chosenBin = 10
            elif not(playerOne) and d2_rect.collidepoint(mouse_pos):
                chosenBin = 9
            elif not(playerOne) and e2_rect.collidepoint(mouse_pos):
                chosenBin = 8
            elif not(playerOne) and f2_rect.collidepoint(mouse_pos):
                chosenBin = 7
            else:
                chosenBin = -2
                messageCode = -2 # invalid input

            if int(chosenBin) >= 0:
                giveawayPile = binAmount[chosenBin]
                binAmount[chosenBin] = 0
                if int(giveawayPile) <= 0:
                    messageCode = -1 # empty bin was chosen

            recipient = chosenBin + 1
            while int(giveawayPile) > 0:
                if playerOne and int(recipient) == 13:
                    recipient = 0
                if (not playerOne) and (int(recipient) == 6):
                    recipient = 7

                binAmount[recipient] = int(binAmount[recipient]) + 1
                giveawayPile = int(giveawayPile) - 1

                if int(giveawayPile) == 0:
                    lastRecipient = recipient
                else:
                    recipient = int(recipient) + 1
                    if int(recipient) > 13:
                        recipient = 0

            if playerOne and int(lastRecipient) == 6:
                playerOne = True
            elif playerOne and int(binAmount[lastRecipient]) == 1 and int(lastRecipient < 6):
                binAmount[6] = int(binAmount[6]) + int(binAmount[lastRecipient]) + int(binAmount[12 - int(lastRecipient)])
                binAmount[lastRecipient] = 0
                binAmount[12 - int(lastRecipient)] = 0
                playerOne = not playerOne
            elif (not playerOne) and int(lastRecipient) == 13:
                playerOne = False
            elif not playerOne and int(binAmount[lastRecipient]) == 1 and int(lastRecipient > 6):
                binAmount[13] = int(binAmount[13]) + int(binAmount[lastRecipient]) + int(binAmount[12 - int(lastRecipient)])
                binAmount[lastRecipient] = 0
                binAmount[12 - int(lastRecipient)] = 0
                playerOne = not playerOne
            elif int(messageCode) >= 0:
                playerOne = not playerOne

            # checking for the end of the game
            sideOne = 0
            sideTwo = 0
            for j in range(6):
                sideOne = int(sideOne) + int(binAmount[j])
                sideTwo = int(sideTwo) + int(binAmount[j + 7])
    
            if int(sideOne) == 0 or int(sideTwo) == 0:
                running = False
                binAmount[6] = int(binAmount[6]) + int(sideOne)
                binAmount[13] = int(binAmount[13]) + int(sideTwo)
                for k in range(6):
                    binAmount[k] = 0
                    binAmount[k + 7] = 0

        # if event.type == pygame.K_ESCAPE:
            main_menu.main(False)

    # Fill the screen with black
    screen.fill(BLACK)

    # draw the board
    board_x, board_y = 62, 150
    board_width, board_height = 675, 300
    board_rect = pygame.Rect(board_x, board_y, board_width, board_height)
    pygame.draw.rect(screen, BOARDCOLOR, board_rect, 0)

    # draw the mancalas
    mancala_w, mancala_h = 75, 250

    player_one_mancala_x, player_one_mancala_y = 637, 175
    player_one_mancala_rect = pygame.Rect(player_one_mancala_x, player_one_mancala_y, mancala_w, mancala_h)
    pygame.draw.ellipse(screen, HOLECOLOR, player_one_mancala_rect, 0)
    player_one_mancala_text = font.render(str(binAmount[6]), True, BLACK)
    screen.blit(player_one_mancala_text, player_one_mancala_rect.center)

    player_two_mancala_x, player_two_mancala_y = 87, 175
    player_two_mancala_rect = pygame.Rect(player_two_mancala_x, player_two_mancala_y, mancala_w, mancala_h)
    pygame.draw.ellipse(screen, HOLECOLOR, player_two_mancala_rect, 0)
    player_two_mancala_text = font.render(str(binAmount[13]), True, BLACK)
    screen.blit(player_two_mancala_text, player_two_mancala_rect.center)

    # draw the pits
    pit_w = 65
    pit_h = 65
    pit_radius = pit_w // 2
    
    a1_center = a1_x, a1_y = 587, 375
    a1_rect = pygame.Rect(a1_x - pit_radius, a1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, a1_center, pit_radius,  0)
    a1_text = font.render(str(binAmount[5]), True, BLACK)
    screen.blit(a1_text, a1_rect.center)

    b1_center = b1_x, b1_y = 512, 375
    b1_rect = pygame.Rect(b1_x - pit_radius, b1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, b1_center, pit_radius,  0)
    b1_text = font.render(str(binAmount[4]), True, BLACK)
    screen.blit(b1_text, b1_rect.center)

    c1_center = c1_x, c1_y = 437, 375
    c1_rect = pygame.Rect(c1_x - pit_radius, c1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, c1_center, pit_radius,  0)
    c1_text = font.render(str(binAmount[3]), True, BLACK)
    screen.blit(c1_text, c1_rect.center)

    d1_center = d1_x, d1_y = 362, 375
    d1_rect = pygame.Rect(d1_x - pit_radius, d1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, d1_center, pit_radius,  0)
    d1_text = font.render(str(binAmount[2]), True, BLACK)
    screen.blit(d1_text, d1_rect.center)

    e1_center = e1_x, e1_y = 287, 375
    e1_rect = pygame.Rect(e1_x - pit_radius, e1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, e1_center, pit_radius, 0)
    e1_text = font.render(str(binAmount[1]), True, BLACK)
    screen.blit(e1_text, e1_rect.center)

    f1_center = f1_x, f1_y = 212, 375
    f1_rect = pygame.Rect(f1_x - pit_radius, f1_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, f1_center, pit_radius, 0)
    f1_text = font.render(str(binAmount[0]), True, BLACK)
    screen.blit(f1_text, f1_rect.center)

    a2_center = a2_x, a2_y = 212, 225
    a2_rect = pygame.Rect(a2_x - pit_radius, a2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, a2_center, pit_radius,  0)
    a2_text = font.render(str(binAmount[12]), True, BLACK)
    screen.blit(a2_text, a2_rect.center)

    b2_center = b2_x, b2_y = 287, 225
    b2_rect = pygame.Rect(b2_x - pit_radius, b2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, b2_center, pit_radius,  0)
    b2_text = font.render(str(binAmount[11]), True, BLACK)
    screen.blit(b2_text, b2_rect.center)

    c2_center = c2_x, c2_y = 362, 225
    c2_rect = pygame.Rect(c2_x - pit_radius, c2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, c2_center, pit_radius,  0)
    c2_text = font.render(str(binAmount[10]), True, BLACK)
    screen.blit(c2_text, c2_rect.center)

    d2_center = d2_x, d2_y = 437, 225
    d2_rect = pygame.Rect(d2_x - pit_radius, d2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, d2_center, pit_radius,  0)
    d2_text = font.render(str(binAmount[9]), True, BLACK)
    screen.blit(d2_text, d2_rect.center)

    e2_center = e2_x, e2_y = 512, 225
    e2_rect = pygame.Rect(e2_x - pit_radius, e2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, e2_center, pit_radius, 0)
    e2_text = font.render(str(binAmount[8]), True, BLACK)
    screen.blit(e2_text, e2_rect.center)

    f2_center = f2_x, f2_y = 587, 225
    f2_rect = pygame.Rect(f2_x - pit_radius, f2_y - pit_radius, pit_w, pit_h)
    pygame.draw.circle(screen, HOLECOLOR, f2_center, pit_radius, 0)
    f2_text = font.render(str(binAmount[7]), True, BLACK)
    screen.blit(f2_text, f2_rect.center)
    
    # draw the message
    if playerOne and messageCode == 0:
        message = "Player One's Turn..."
    elif not playerOne and messageCode == 0:
        message = "Player Two's Turn..."
    elif playerOne and messageCode == -2:
        message = "Invalid input. Try again, Player One."
    elif not playerOne and messageCode == -2:
        message = "Invalid input. Try again, Player Two."    
    elif playerOne and messageCode == -1:
        message = "You must choose a non-empty bin, Player One."
    elif not playerOne and messageCode == -1:
        message = "You must choose a non-empty bin, Player Two."

    message_text = font.render(message, True, WHITE)
    screen.blit(message_text, (screen_width // 6, screen_height // 6))

    # update the display
    pygame.display.update()

# Quit pygame after 5 seconds
if not running and int(binAmount[13]) < int(binAmount[6]):
    win_message = "The game is over, Player One wins!"
elif not running and int(binAmount[13]) > int(binAmount[6]):
    win_message = "The game is over, Player Two wins!"
else:
    win_message = "The game is over and ended in a tie."

win_text = font.render(win_message, True, WHITE)
screen.blit(win_text, (screen_width // 6, screen_height * 5 // 6))

time.sleep(5)
main_menu.main(False)