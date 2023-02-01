import pygame
from pygame.sprite import Sprite
import os

main_dir = os.path.dirname(os.path.abspath(__file__))

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self,ai_game):
        """initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #load the alien image and set its rect attribute.
        self.image = pygame.image.load(os.path.join(main_dir, "alienpic.png")).convert()
        #make alien smaller
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alien's alien's exact horizontal positon.
        self.x = float(self.rect.x)
    def check_edges(self):
        """return True if alien is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    def update (self):
        """move the alien to the right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
        
            