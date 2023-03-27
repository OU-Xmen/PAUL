import os
import random
import pygame
pygame.init()
from importlib.machinery import SourceFileLoader

maindir = os.path.abspath(os.path.dirname(__file__))
assetdir = os.path.join(maindir, 'assets')
game_file = SourceFileLoader('game', os.path.join(maindir, 'game.py')).load_module()

dirt = pygame.image.load(os.path.join(assetdir, 'dirt.png'))
player = pygame.image.load(os.path.join(assetdir, 'player.png'))

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('balls')
menu_color = (160, 110, 20)

def mouse_in_box(b, mouse):
    if b[0] <= mouse[0] <= (b[0]+b[2]) and b[1] <= mouse[1] <= (b[1]+b[3]):
        return True
    return False

class TextObj:
    def __init__(self, font = 'comicsansms', font_size = 12, text = 'Sample Text', color = (20, 0, 50), xpos = 0, ypos = 0):
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, self.font_size)
        self.text = text
        self.color = color
        self.rend = pygame.font.Font.render(self.font, self.text, self.color, True)
        self.rect = self.rend.get_rect(center=(xpos, ypos))  # (xpos, ypos) is the center of the text
    
    def set_font_size(self, new_size):
        self.font = pygame.font.SysFont(self.font, new_size)

    def draw(self, screen):
        screen.blit(self.rend, self.rect)

    def draw_hover(self, screen):
        pygame.draw.rect(screen, (180, 0, 0), self.rect)
        screen.blit(self.rend, self.rect)

    def get_coords(self):
        return self.rect

    def draw_button(self, mouse):
        self.draw_hover(screen) if mouse_in_box(self.rect, mouse) else self.draw(screen)

if __name__ == '__main__':
    size = screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode(size)

    random.seed()
    rando = lambda: random.randint(0, 255)
    
    text_color = (20, 0, 200)
    paul_name = TextObj('comicsansms', 60, 'P.A.U.L. Platformer', text_color, screen_width/2, screen_height/3)
    slide_text = TextObj('comicsansms', 60, 'Play Game', text_color, screen_width/2, screen_height/2)
    quit_text = TextObj('comicsansms', 60, 'Quit', text_color, screen_width/2, screen_height/2 + 80)

    box_color_list = [(200, 0, 0), (180, 0, 0)]

    while True:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()            
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_in_box(quit_text.rect, mouse):
                    quit()
                if mouse_in_box(slide_text.rect, mouse):
                    print("Game starting...")
                    game_file.game_loop(1)
        screen.fill((200, 0, 0))

        paul_name.draw(screen)
        slide_text.draw_button(mouse)
        quit_text.draw_button(mouse)

        pygame.display.flip()