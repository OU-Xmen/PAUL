import os
import pygame
pygame.init()
maindir = os.path.abspath(os.path.dirname(__file__))
assetdir = os.path.join(maindir, 'assets')

class Player:
    def __init__(self, start_x, start_y):
        self.bruh = 'bruh'
        self.img = pygame.image.load(os.path.join(assetdir, 'player.png'))
        self.img.set_colorkey((255, 0, 0))
        self.set_img_rect(x=40*start_y, y=40*start_x)
        self.gravity = True
        self.gravity_velocity = 0
    
    def blit_player(self, screen):
        screen.blit(self.img, self.img_rect)
    
    def set_img_rect(self, x, y, w = 34, h = 38):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img_rect = pygame.Rect((x, y, w, h))
    
    def get_img_rect(self):
        return self.img_rect
    
    def move(self, direction, speed = 2):
        match direction:
            case 'right':
                self.set_img_rect(self.x+speed, self.y, self.w, self.h)
            case 'left':
                self.set_img_rect(self.x-speed, self.y, self.w, self.h)
    
    def jump(self, dist_to_ceiling):
        if self.gravity == False:
            self.gravity = True
            if dist_to_ceiling < 5.8:
                self.gravity_velocity = 0
                self.set_img_rect(self.x, self.y-dist_to_ceiling, self.w, self.h)
            else:
                self.gravity_velocity = -5.8
                self.set_img_rect(self.x, self.y+self.gravity_velocity, self.w, self.h)

    def set_gravity(self, gravity, dist_to_floor, dist_to_ceiling):
        self.gravity = gravity
        if not gravity:
            self.gravity_velocity = 0
        elif dist_to_ceiling < abs(self.gravity_velocity) and self.gravity_velocity < 0:
            self.gravity_velocity = 0
            self.set_img_rect(self.x, self.y-dist_to_ceiling, self.w, self.h)
            return
        else:
            self.gravity_velocity += .2
            self.set_img_rect(self.x, self.y+min(self.gravity_velocity, dist_to_floor), self.w, self.h)
            return
    
    def set_gravity_velocity(self, gravity_velocity):
        self.gravity_velocity = gravity_velocity