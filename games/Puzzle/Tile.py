import pygame
pygame.init()

class Tile:
    def __init__(self, current_x = 0, current_y = 0, img = False):
        self.current_x = current_x
        self.current_y = current_y
        
        if img:
            self.img = pygame.image.load(img)
        else:
            self.img = False
    
    def set_coords(self, new_x, new_y):
        self.current_x = new_x
        self.current_y = new_y

    def get_coords(self):
        temp = (self.current_x, self.current_y)
        return temp

    def draw(self, window):
        if self.img:
            window.blit(self.img, (self.current_x, self.current_y))
        else:
            pygame.draw.rect(window,(100, 100, 100), (self.current_x, self.current_y, 80, 80))

    def draw_hover(self, window):
        if self.img:
            window.blit(self.img, (self.current_x, self.current_y))
        else:
            pygame.draw.rect(window,(150, 150, 150), (self.current_x, self.current_y, 80, 80))