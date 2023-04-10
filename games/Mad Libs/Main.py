try:
    import pygame   
    pygame.init()
    import os
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    currentdirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(currentdirectory, 'assets')
    main_menu = SourceFileLoader('main', os.path.join(os.path.dirname(maindirectory), 'main.py')).load_module()
    story1 = os.path.join(assetdirectory, 'madlibs_story1.txt')
    story2 = os.path.join(assetdirectory, 'madlibs_story2.txt')
    story3 = os.path.join(assetdirectory, 'madlibs_story3.txt')
except ImportError:
    print('One or more modules failed to import. Please try again.')
    quit()

# Window settings
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mad Libs')
icon = pygame.image.load(os.path.join(assetdirectory, 'paulicon.png'))
pygame.display.set_icon(icon)

# initialize text and colors
font = pygame.font.SysFont('comicsansms', 20)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (151, 151, 151)
red = (200, 0, 0)
green = (0, 220, 0)
blue = (102, 153, 204)

# make the text box
input_box_width = 200
input_box_height = 50
input_box_x = (width - input_box_width) //2
input_box_y = (height - input_box_height) // 2 - (height //6)
input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)


def button(text, size, center_x, center_y, text_color):
    font = pygame.font.SysFont('comicsansms', size)
    temp_rend = pygame.font.Font.render(font, text, True, text_color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    temp_width, temp_height = temp_rend.get_width(), temp_rend.get_height()
    temp_box = pygame.Rect(center_x - (temp_width//2) - size//2, center_y - temp_height//2 - size//4, temp_width + size, temp_height + size//2)
    return temp_rend, temp_rect, temp_box


def init_words(text, size, center_x, center_y, text_color):
    font = pygame.font.SysFont('comicsansms', size)
    temp_rend = pygame.font.Font.render(font, text, True, text_color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        if y + fontHeight > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        text = text[i:]
    return text


title_rend, title_rect = init_words('Mad Libs', 50, width//2, height//3, black)
play_rend, play_rect, play_box = button('PLAY', 30, width//2, height//2, black)
quit_rend, quit_rect, quit_box = button('QUIT', 20, 50, 50, black)
story1_rend, story1_rect, story1_box = button('What is PAUL?', 20, width//4, height//2, black)
story2_rend, story2_rect, story2_box = button('Holiday Party', 20, width//2, height//2, black)
story3_rend, story3_rect, story3_box = button('First Performance', 20, (width*3)//4, height//2, black)
button_rend, button_rect, button_box = button('ENTER', 30, width//2, height//2, white)


def results_screen(text):
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(gray)
        pygame.draw.rect(screen, red, quit_box)
        screen.blit(quit_rend, quit_rect)
        drawText(screen, text, black, (100, 50, 600, 400), font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main(False)
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(mouse):
                    running = False
                    main_menu.main(False)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu.main(False)
                    break
        
        pygame.display.flip()
    pygame.quit()



def play_screen(story):
    story1_search = ['noun1', 'noun2', 'noun3', 'noun4', 'verb1', 'verb2', 'adjective1', 'adjective2', 'adjective3', 
                     'interrogative', 'language', 'class_level', 'family_member', 'crime', 'month', 'year', 'body part', 'your_name']
    story2_search = ['adjective1', 'holiday', 'adjective2', 'verb', 'beverage', 'bodypart1', 'derogatory_saying', 
                     'adjective3', 'bodypart2', 'food', 'place', 'adjective4', 'number']
    story3_search = ['adjective1', 'action', 'verb1', 'noun1', 'number', 'noun2', 'adjective2', 'verb2', 'noun3']
    story1_message = ['Enter a plural noun', 'Enter a single noun', 'Enter a plural noun', 'Enter a single noun', 
                      'Enter a past-tense verb', 'Enter another verb', 'Enter an adjective', 'Enter another adjective', 
                      'Enter a third adjective', 'Enter an interrogative', 'Enter a language', 'Enter your class rank', 
                      'Enter a family member', 'Enter a crime or felony', 'Enter a month', 'Enter a year', 'Enter a body part', 'Enter your name']
    story2_message = ['Enter an adjective', 'Enter a holiday', 'Enter another adjective', 'Enter a verb', 'Enter a type of drink', 'Enter a body part', 
                      'Enter a derogatory saying', 'Enter another adjective', 'Enter another body part', 'Enter a type of food',
                      'Enter a place', 'Enter another adjective', 'Enter a number rank (with suffix)']
    story3_message = ['Enter an adjective', 'Enter an action', 'Enter a verb (-ing)', 'Enter a noun', 'Enter a number between 1 and 12', 
                      'Enter a plural noun', 'Enter another adjective', 'Enter another verb',  'Enter another noun']

    i = 0

    f = open(story)
    text = f.read()

    input_text = ''
    message_rend, message_rect = init_words('', 25, width//2, height//4, black)
    running = True
    while running:

        mouse = pygame.mouse.get_pos()

        if story == os.path.join(assetdirectory, 'madlibs_story1.txt') and i >= 18:
            f.close()
            results_screen(text)
        elif story == os.path.join(assetdirectory, 'madlibs_story2.txt') and i >= 13:
            f.close()
            results_screen(text)
        elif story == os.path.join(assetdirectory, 'madlibs_story3.txt') and i >= 9:
            f.close()
            results_screen(text)    

        if story == os.path.join(assetdirectory, 'madlibs_story1.txt'):
            message_rend, message_rect = init_words(story1_message[i], 25, width//2, height//4, black)
        elif story == os.path.join(assetdirectory, 'madlibs_story2.txt'):
            message_rend, message_rect = init_words(story2_message[i], 25, width//2, height//4, black)
        elif story == os.path.join(assetdirectory, 'madlibs_story3.txt'):
            message_rend, message_rect = init_words(story3_message[i], 25, width//2, height//4, black)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main(False)
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(mouse):
                    running = False
                    main_menu.main(False)
                    break
                if button_rect.collidepoint(mouse):
                    if not input_text == '':
                        if story == os.path.join(assetdirectory, 'madlibs_story1.txt'):
                            if i < 18:
                                text = text.replace(story1_search[i], input_text)
                                input_text = ''
                                i = i + 1
                        elif story == os.path.join(assetdirectory, 'madlibs_story2.txt'):
                            if i < 13:
                                text = text.replace(story2_search[i], input_text)
                                input_text = ''
                                i = i + 1
                        elif story == os.path.join(assetdirectory, 'madlibs_story3.txt'):
                            if i < 9:
                                text = text.replace(story3_search[i], input_text)
                                input_text = ''
                                i = i + 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu.main(False)
                    break
                elif event.key == pygame.K_BACKSPACE:
                    pygame.key.set_repeat(250, 50)
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN: 
                    if not input_text == '':
                        if story == os.path.join(assetdirectory, 'madlibs_story1.txt'):
                            if i < 18:
                                text = text.replace(story1_search[i], input_text)
                                input_text = ''
                                i = i + 1
                        elif story == os.path.join(assetdirectory, 'madlibs_story2.txt'):
                            if i < 13:
                                text = text.replace(story2_search[i], input_text)
                                input_text = ''
                                i = i + 1
                        elif story == os.path.join(assetdirectory, 'madlibs_story3.txt'):
                            if i < 9:
                                text = text.replace(story3_search[i], input_text)
                                input_text = ''
                                i = i + 1
                else:
                    pygame.key.set_repeat(250, 50)
                    input_text += event.unicode
                
        screen.fill(gray)

        pygame.draw.rect(screen, black, input_box, 2)
        pygame.draw.rect(screen, red, quit_box)
        pygame.draw.rect(screen, black, button_box)
        input_text_rend = font.render(input_text, True, black)
        input_text_x = input_box.x + 5
        input_text_y = input_box.y + (input_box.height - input_text_rend.get_height()) //2
        screen.blit(input_text_rend, (input_text_x, input_text_y))
        screen.blit(quit_rend, quit_rect)
        screen.blit(button_rend, button_rect)
        screen.blit(message_rend, message_rect)
        pygame.display.flip()
    pygame.quit()

def select_screen():
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(gray)
        pygame.draw.rect(screen, blue, story1_box)
        pygame.draw.rect(screen, blue, story2_box)
        pygame.draw.rect(screen, blue, story3_box)
        pygame.draw.rect(screen, red, quit_box)
        screen.blit(story1_rend, story1_rect)
        screen.blit(story2_rend, story2_rect)
        screen.blit(story3_rend, story3_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main(False)
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if story1_rect.collidepoint(mouse):
                    play_screen(story1)
                if story2_rect.collidepoint(mouse):
                    play_screen(story2)
                if story3_rect.collidepoint(mouse):
                    play_screen(story3)
                if quit_rect.collidepoint(mouse):
                    running = False
                    main_menu.main(False)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu.main(False)
                    break
        
        pygame.display.flip()
    pygame.quit()

def main():
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(gray)
        pygame.draw.rect(screen, red, quit_box)
        pygame.draw.rect(screen, green, play_box)
        screen.blit(title_rend, title_rect)
        screen.blit(play_rend, play_rect)
        screen.blit(quit_rend, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main(False)
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse):
                    select_screen()
                if quit_rect.collidepoint(mouse):
                    running = False
                    main_menu.main(False)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu.main(False)
                    

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__": main()


