import os
import pygame
pygame.init()

maindir = os.path.abspath(os.path.dirname(__file__))
assetdir = os.path.join(maindir, 'assets')

class Tile:
    def __init__(self, type, x_given, y_given):
        self.id_num = type
        match type:
            case 0:
                self.type = None
                self.img = pygame.image.load(os.path.join(assetdir, 'empty.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = False
                self.img_rect = pygame.Rect(40*y_given, 40*x_given, 40, 40)
            case 1:
                self.type = 'dirt'
                self.img = pygame.image.load(os.path.join(assetdir, 'dirt.png'))
                self.img.set_colorkey((255, 0, 0))
                self.collision = True
                self.img_rect = pygame.Rect(40*y_given, 40*x_given, 40, 40)
            case 2:
                self.type = 'lava'
                self.img = pygame.image.load(os.path.join(assetdir, 'lava.png'))
                self.collision = False
                self.img_rect = pygame.Rect(10+40*y_given, 10+40*x_given, 21, 21)
            case 3:
                self.type = 'goal'
                self.img = pygame.image.load(os.path.join(assetdir, 'goal.png'))
                self.collision = False
                self.img_rect = pygame.Rect(40*y_given, 40*x_given, 40, 40)
            case 4:
                self.type = 'coin'
                self.img = pygame.image.load(os.path.join(assetdir, 'coin.png'))
                self.collision = False
                self.img_rect = pygame.Rect(5+40*y_given, 5+40*x_given, 30, 30)
            case 5:
                self.type = 'sign'
                self.img = pygame.image.load(os.path.join(assetdir, 'sign.png'))
                self.collision = False
                self.text = "If you're reading this, Eli forgot this sign exists :("
                self.img_rect = pygame.Rect(40*y_given, 40*x_given, 40, 40)
        self.img.set_colorkey((255, 0, 0))
    
    def get_img(self):
        return self.img
    
    def get_img_rect(self):
        return self.img_rect