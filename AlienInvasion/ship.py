import pygame
from settings import Settings
from pygame.sprite import Sprite
import os

main_dir = os.path.dirname(os.path.abspath(__file__))

class Ship(Sprite):
    """A class to manage the game"""

    def __init__(self, ai_game):
        """initialize the ship and set its starting postion."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load(os.path.join(main_dir,'ship.png')).convert()
        #make ship smaller
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()

        #Start each new ship at the bottomcenter of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        #update the ship's X value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """"Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)