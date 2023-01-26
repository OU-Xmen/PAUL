import pygame
class Settings:
    """A class to store all settings for ALien Invasion."""

    def __init__(self):
        """Initialize the games static settings."""
        #Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = pygame.image.load("space.png")

        #ship settings
        #self.ship_speed = 2.5
        self.ship_limit = 3

        #bullet settings
        #self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (50,205,50)
        self.bullets_allowed = 150

        #alien settings
        #self.alien_speed = 1.5
        self.fleet_drop_speed = 10

        #how quickly teh game speeds up
        self.speedup_scale = 1.5

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settins that change throughout the game"""
        self.ship_speed = 2.0
        self.bullet_speed = 5.0
        self.alien_speed = 2.0

        #scoring
        self.alien_points = 50

        #fleet_direction of 1 repersens right; -1 repersens left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)