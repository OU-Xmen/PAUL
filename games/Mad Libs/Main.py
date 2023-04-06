try:
    import pygame   
    pygame.init()
    import os
    from importlib.machinery import SourceFileLoader
    maindirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    currentdirectory = os.path.dirname(os.path.abspath(__file__))
    assetdirectory = os.path.join(currentdirectory, 'assets')
    main_menu = SourceFileLoader('main', os.path.join(maindirectory, 'main.py')).load_module() # Updated for issue #14
except ImportError:
    print('One or more modules failed to import. Please try again.')
    quit()

# Window settings
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mad Libs')
icon = pygame.image.load(os.path.join(assetdirectory, 'paulicon.png'))
pygame.display.set_icon(icon)

# initialize font and text objects
black = (0, 0, 0)
white = (255, 255, 255)

def init_words(text, size, center_x, center_y, color):
    font = pygame.font.SysFont('comicsansms', size)
    temp_rend = pygame.font.Font.render(font, text, True, color)
    temp_rect = temp_rend.get_rect(center = (center_x, center_y))
    return temp_rend, temp_rect

title_rend, title_rect = init_words('Mad Libs', 50, width//2, height//3, black)
play_rend, play_rect = init_words('PLAY', 30, width//2, height//2, black)
quit_rend, quit_rect = init_words('QUIT', 20, 50, 50, black)
story1_rend, story1_rect = init_words('STORY 1', 30, width//4, height//2, black)
story2_rend, story2_rect = init_words('STORY 2', 30, width//2, height//2, black)
story3_rend, story3_rect = init_words('STORY 3', 30, (width*3)//4, height//2, black)

def play_screen(story):
    temp = temp

def select_screen():
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(white)
        screen.blit(story1_rend, story1_rect)
        screen.blit(story2_rend, story2_rect)
        screen.blit(story3_rend, story3_rect)
        screen.blit(quit_rend, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if story1_rect.collidepoint(mouse):
                    play_screen('story1')
                if story2_rect.collidepoint(mouse):
                    play_screen('story2')
                if story3_rect.collidepoint(mouse):
                    play_screen('story3')
                if quit_rect.collidepoint(mouse):
                    main_menu.main(False)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.main(False)
                    break
        
        pygame.display.flip()
                

def main():
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(white)
        screen.blit(title_rend, title_rect)
        screen.blit(play_rend, play_rect)
        screen.blit(quit_rend, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse):
                    select_screen()
                if quit_rect.collidepoint(mouse):
                    main_menu.main(False)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.main(False)
                    break

        pygame.display.flip()

if __name__ == "__main__": main()

