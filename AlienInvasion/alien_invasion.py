import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """overall class to manage game assets and behavior"""

    def __init__(self):
        """initialize the game, create game resources"""
        pygame.init()
        self.settings = Settings()
        #these make it fullscreen, I do not like that
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistcs 
        self.stats = GameStats(self)

        #Draw the score information
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "Play")

        #set the background color
        self.bg_color = (230,230,230)

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen() 

    def _create_fleet(self):
        """create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        #make the alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliesn that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height)- ship_height)
        number_rows = available_space_y // (2* alien_height)

        #Create full fleet of aliens
        for row_number in range(number_rows):
        #create first row of the aliens
            for alien_number in range(number_aliens_x):
                #create an alien and place it in the row
                #self._create_alien(alien_number)
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien_width = alien.rect.width
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond approprately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet an dchange the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """Respond to the shp being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decremet ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_aliens(self):
        """update the fleet of aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisons
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _update_bullets(self):
        """update postionn of bullets and get rid of old bullets"""
        #update bullet postion
        self.bullets.update()
        #ger rid of bullets that have disapperard
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
               self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

            #print(len(self.bullets)) 
    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisons"""
        #remove any bullets that have collied
            ##check for any bullet that have hit aliens
            # if so get rid of the bullet and teh alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score() 
            self.sb.check_high_score()

        if not self.aliens:
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        """respond to keypresses and mouse events"""
        #watch for keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)   
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            #Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Get rid of any remaing aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Creat new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

               
    def _check_keydown_events(self,event):
        """respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            #move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """respond to key relases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """update images on the screen and flip to new screen"""    
        #Make the most recently drawn screen visible
        #redraw the screen during each pass through the loop
        self.screen.blit(self.settings.bg_color, (0,0))
        self.ship.blitme() 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score info
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
       

if __name__ == '__main__':
    #Make a game instance, run the game
    ai = AlienInvasion()
    ai.run_game()

