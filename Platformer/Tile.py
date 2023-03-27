import os
import pygame
pygame.init()
maindir = os.path.abspath(os.path.dirname(__file__))
assetdir = os.path.join(maindir, 'assets')

class Tile:
    def __init__(self, type, x_given, y_given):
        match type:
            case 0:
                self.type = None
                self.img = pygame.image.load(os.path.join(assetdir, 'empty.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = False
            case 1:
                self.type = 'dirt'
                self.img = pygame.image.load(os.path.join(assetdir, 'dirt.png'))
                self.collision = True
            case 2:
                self.type = 'lava'
                self.img = pygame.image.load(os.path.join(assetdir, 'lava.png'))
                self.collision = True
            case 3:
                self.type = 'goal'
                self.img = pygame.image.load(os.path.join(assetdir, 'goal.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = False
            case 4:
                self.type = 'coin'
                self.img = pygame.image.load(os.path.join(assetdir, 'coin.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = False
            case 5:
                self.type = 'sign'
                self.img = pygame.image.load(os.path.join(assetdir, 'sign.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = False
                self.text = "Sign text goes here"
        self.img_rect = self.img.get_rect(x = 40*y_given, y = 40*x_given)
    
    def get_img(self):
        return self.img
    
    def get_img_rect(self):
        return self.img_rect