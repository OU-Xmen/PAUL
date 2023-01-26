# --------- 
# ASTEROIDS
# --------------------
# Intended for P.A.U.L
# --------------------------
# Coded by Matthew Robertson
# -----------------------------------------------------------------
# Credit to "EZ Coding" on YouTube for majority of the game's logic
# -----------------------------------------------------------------
#          CONTROLS:          |
#         UP: FORWARD         |
#       LEFT: TURN LEFT       |
#      RIGHT: TURN RIGHT      |  
# SPACE: SHOOT/START NEW GAME |
# ----------------------------|

import pygame
import math
import random

# Initializing PyGame
pygame.init()

# Setting Resolution
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Loading Assets
alienImage = pygame.image.load('asteroids/assets/alienImage.png')
background = pygame.image.load('asteroids/assets/background.png')
gameIcon = pygame.image.load('asteroids/assets/paulicon.png')
largeAsteroid = pygame.image.load('asteroids/assets/largeAsteroid.png')
mediumAsteroid = pygame.image.load('asteroids/assets/mediumAsteroid.png')
playerImage = pygame.image.load('asteroids/assets/playerImage.png')
powerupImage = pygame.image.load('asteroids/assets/powerupImage.png')
smallAsteroid = pygame.image.load('asteroids/assets/smallAsteroid.png')

# Modifying the window and initializing the clock
pygame.display.set_caption('Asteroids')
pygame.display.set_icon(gameIcon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initializing game values
game_over = False
lives = 3
score = 0
rapidFire  = False
rapid_start = -1
asteroid_count = 0


class Player(object): # Controls attributes of the player's spacecraft
    def __init__(self):
        # Player's attributes: most are used for the calculations behind turning and shooting
        self.img = playerImage
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2
        self.angle = 0
        self.rotatedSurface = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, screen): # Puts the shipn on the screen
        screen.blit(self.rotatedSurface, self.rotatedRect)

    def turnLeft(self): # Controls the math behing turning the ship to the left
        self.angle += 5
        self.rotatedSurface = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self): # turnLeft(), but right
        self.angle -= 5
        self.rotatedSurface = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self): # Moves the ship forward. Notice the distinct lack of other directions.
        self.x += self.cosine * 6
        self.y -= self.sine * 6    
        self.rotatedSurface = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def teleporting_check(self): #This one makes the screen wrap around like it does in games like Pac-Man
        if self.x > SCREEN_WIDTH +50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = SCREEN_WIDTH
        elif self.y < - 50:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT + 50:
            self.y = 0

class Bullet(object): # Controls the ship's bullets. NOT THE ENEMY SHIP'S BULLETS
    def __init__(self): 
        # Attributes for each bullet. Top few control the bullet's positon and size.
        # The bottom half control the math/physics behind it all
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self): # Adds the velocity to the current position to make bullets move seamlessly
        self.x += self.xv
        self.y -= self.yv
        
    def draw(self, screen): # Puts the bullets on the screen
        pygame.draw.rect(screen, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def remove_offscreen_bullets(self): # This is done to save memory. 
                                        # Imagine how awful it would be to have 
                                        # one million bullets rendered on your computer.
        if self.x < -50 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT or self.y < -50:
            return True


class Asteroid(object): # Pertains to all the asteroids on the screen.
    def __init__(self, size):
        self.size = size # Pertains to setting the size of the asteroids
        if self.size == 1:
            self.image = smallAsteroid
        elif self.size == 2:
            self.image = mediumAsteroid
        else:
            self.image = largeAsteroid
        self.w = 50 * size
        self.h = 50 * size
        self.random_location = random.choice([(random.randrange(0, SCREEN_WIDTH - self.w), random.choice([-1 * self.h - 5, SCREEN_HEIGHT + 5])), (random.choice([-1 * self.w - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.h))])
        self.x, self.y = self.random_location # This isn how the computer chooses which asteroid to display at a given time ^^^
        if self.x < SCREEN_WIDTH//2: # Gives the asteroids a certain direction of travel based on spawn location
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < SCREEN_HEIGHT//2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.xv = self.x_direction * random.randrange(1, 3)
        self.yv = self.y_direction * random.randrange(1, 3)

    def draw(self, screen): # Puts the asteroids on the screen
        screen.blit(self.image, (self.x, self.y))


class PowerUp(object): # This class pertains to the power-up that shows up every so often. 
    def __init__(self): # It allows the player to shoot at a faster rate for a limited time.
        self.img = powerupImage #Attributes
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.random_location = random.choice([(random.randrange(0, SCREEN_WIDTH - self.w), random.choice([-1 * self.h - 5, SCREEN_HEIGHT + 5])), (random.choice([-1 * self.w - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.h))])
        self.x, self.y = self.random_location

        if self.x < SCREEN_WIDTH//2: # Like the asteroids, this if-else gives the power-up it's direction of travel 
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < SCREEN_HEIGHT//2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.xv = self.x_direction * 2 # Velocity handlers
        self.yv = self.y_direction * 2

    def draw(self, screen): # Puts the power-up on the screen
        screen.blit(self.img, (self.x, self.y))

class Alien(object): # This sets the UFO that attacks the player
    def __init__(self): # Attributes
        self.img = alienImage 
        self.w = self.img.get_width()
        self.h = self.img.get_height() # The UFO gets assigned a random position
        self.random_location = random.choice([(random.randrange(0, SCREEN_WIDTH - self.w), random.choice([-1 * self.h - 5, SCREEN_HEIGHT + 5])), (random.choice([-1 * self.w - 5, SCREEN_WIDTH + 5]), random.randrange(0, SCREEN_HEIGHT - self.h))])
        self.x, self.y = self.random_location
        if self.x < SCREEN_WIDTH//2: # Direction handler
            self.x_direction = 1
        else:
            self.x_direction = -1
        if self.y < SCREEN_HEIGHT//2:
            self.y_direction = 1
        else:
            self.y_direction = -1
        self.xv = self.x_direction * 2
        self.yv = self.y_direction * 2
    
    def draw(self, screen): # Puts the UFO on the screen
        screen.blit(self.img, (self.x, self.y))


class AlienBullet(object): # Pertains to the UFO's bullets, most of this is identical to the player's bullet class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10 # These bullets are bigger and a different color
        self.h = 10
        self.dx, self.dy = player.x -self.x, player.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist # Key difference is that the UFO has AimBot
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self, screen): # Puts the bullets on the screen
        pygame.draw.rect(screen, (255, 0, 0), [self.x, self.y, self.w, self.h])

def redraw_game_window(): # Updates the game window after every action
    screen.blit(background, (0,0))
    font = pygame.font.SysFont('comicsans', 30)
    life_counter_text = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    play_again_text = font.render('Press SPACE to Play Again', 1, (255, 255, 255))
    score_text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    
    player.draw(screen) # Draws everything each time the screen updates
    for asteroid in asteroids:
        asteroid.draw(screen)
    for bullets in player_bullets:
        bullets.draw(screen)
    screen.blit(life_counter_text, (25, 25))
    for powerup in power_up:
        powerup.draw(screen)
    for alien in aliens:
        alien.draw(screen)
    for bullets in alien_bullets:
        bullets.draw(screen)

    if rapidFire: # This if statement adds a timer bar at the top of the screen while the power-up is active
        pygame.draw.rect(screen, (0, 0, 0), [SCREEN_WIDTH//2 - 51, 19, 102, 22])
        pygame.draw.rect(screen, (255, 255, 255), [SCREEN_WIDTH//2 - 50, 20, 100 - 100 * (asteroid_count - rapid_start) / 500, 20])
    if game_over: # Displays the game-over screen
        screen.blit(play_again_text, (SCREEN_WIDTH//2 - play_again_text.get_width()//2, SCREEN_HEIGHT//2 - play_again_text.get_height()//2))
    screen.blit(score_text, (25, 65))
    pygame.display.update()
    

player = Player() # Initializes the arrays of the objects
player_bullets = []
asteroids = []
power_up = []
aliens = []
alien_bullets = []

running = True # Main game loop
while running:

    clock.tick(60) # Sets the FPS
    asteroid_count += 1 # Internal timer

    if not game_over: 
        if asteroid_count % 50 == 0: # One asteroid every 50 ticks
            rand = random.choice([1, 1, 1, 2, 2, 3]) # Tells the game which asteroid to choose
            asteroids.append(Asteroid(rand)) # 50% chance for a small one, 1/3 chance for medium, 1/6 chance for large
        if asteroid_count % 5000 == 0: # One power-up every 5000 ticks
            power_up.append(PowerUp())
        if asteroid_count % 3750 == 0: # One UFO every 3750 ticks
            aliens.append(Alien())

        for i, alien in enumerate(aliens): # Handles the collision in regard to the UFO
            alien.x += alien.xv
            alien.y += alien.yv
            if alien.x > SCREEN_WIDTH + 150 or alien.x + alien.w < -100 or alien.y > SCREEN_HEIGHT + 1550 or alien.y + alien.h < -100:
                aliens.pop(i) # Screen collision, gets rid of the UFO if it goes off-screen
            if asteroid_count % 60 == 0:
                alien_bullets.append(AlienBullet(alien.x + alien.w//2, alien.y + alien.h//2))
            for bullets in player_bullets: # Deletes the UFO and awards points when you hit it with a bullet
                if (bullets.x >= alien.x and bullets.x <= alien.x + alien.w) or bullets.x + bullets.w >= alien.x and bullets.x + bullets.w <= alien.x + alien.w:
                    if (bullets.y >= alien.y and bullets.y <= alien.y + alien.h) or bullets.y + bullets.h >= alien.y and bullets.y + bullets.h <= alien.y + alien.h:
                        aliens.pop(i)
                        score += 1000

        for i, bullets in enumerate(alien_bullets):
            bullets.x += bullets.xv # Handles player collision with a UFO bullet
            bullets.y += bullets.yv
            if (bullets.x >= player.x - player.w//2 and bullets.x <= player.x + player.w//2) or bullets.x + bullets.w >= player.x - player.w//2 and bullets.x + bullets.w <= player.x + player.w//2:
                if (bullets.y >= player.y - player.h//2 and bullets.y <= player.y + player.h//2) or bullets.y + bullets.h >= player.y - player.h//2 and bullets.y + bullets.h <= player.y + player.h//2:
                    lives -= 1
                    alien_bullets.pop(i)
                    break

        player.teleporting_check() # This is how the game wraps the screen around
        for bullets in player_bullets:
            bullets.move()
            if bullets.remove_offscreen_bullets():
                player_bullets.pop(player_bullets.index(bullets))

        for asteroid in asteroids: # Gives the asteroids the abilty to move indefinitely
            asteroid.x += asteroid.xv
            asteroid.y += asteroid.yv
            
           # Checks for collision for players running into asteroids
            if (asteroid.x >= player.x - player.w // 2 and asteroid.x <= player.x + player.w // 2) or (asteroid.x + asteroid.w <= player.x + player.w // 2 and asteroid.x + asteroid.w >= player.x - player.w // 2):
                if(asteroid.y >= player.y - player.h // 2 and asteroid.y <= player.y + player.h // 2) or (asteroid.y + asteroid.h >= player.y - player.h // 2 and asteroid.y + asteroid.h <= player.y + player.h // 2):
                    lives -=1
                    asteroids.pop(asteroids.index(asteroid))
                    break

            # Checks bullet collision for asteroids
            for bullets in player_bullets:
                if (bullets.x >= asteroid.x and bullets.x <= asteroid.x + asteroid.w) or bullets.x + bullets.w >= asteroid.x and bullets.x + bullets.w <= asteroid.x + asteroid.w:
                    if (bullets.y >= asteroid.y and bullets.y <= asteroid.y + asteroid.h) or bullets.y + bullets.h >= asteroid.y and bullets.y + bullets.h <= asteroid.y + asteroid.h:
                        if asteroid.size == 3: # Each asteroid is given a different score.
                            score += 20 
                            new_asteroid_1 = Asteroid(2)
                            new_asteroid_2 = Asteroid(2) # These if statements allow the game to spawn two smaller asteroids
                            new_asteroid_1.x = asteroid.x # When a bigger one is destroyed
                            new_asteroid_2.x = asteroid.x
                            new_asteroid_1.y = asteroid.y
                            new_asteroid_2.y = asteroid.y
                            asteroids.append(new_asteroid_1)
                            asteroids.append(new_asteroid_2)
                        elif asteroid.size == 2:
                            score += 50
                            new_asteroid_1 = Asteroid(1)
                            new_asteroid_2 = Asteroid(1)
                            new_asteroid_1.x = asteroid.x
                            new_asteroid_2.x = asteroid.x
                            new_asteroid_1.y = asteroid.y
                            new_asteroid_2.y = asteroid.y
                            asteroids.append(new_asteroid_1)
                            asteroids.append(new_asteroid_2)
                        else:
                            score += 100
                        asteroids.pop(asteroids.index(asteroid))
                        player_bullets.pop(player_bullets.index(bullets))
                        break

        for powerup in power_up: # Gives the power-up collision with bullets so the game knows when to activate it
            powerup.x += powerup.xv
            powerup.y += powerup.yv
            if powerup.x < -100 or  powerup.x > SCREEN_WIDTH + 100 or powerup.y > SCREEN_HEIGHT + 100 or powerup.y < -100 - SCREEN_HEIGHT:
                power_up.pop(power_up.index(powerup))
                break
            for bullets in player_bullets:
                if (bullets.x >= powerup.x and bullets.x <= powerup.x + powerup.w) or bullets.x + bullets.w >= powerup.x and bullets.x + bullets.w <= powerup.x + powerup.w:
                    if (bullets.y >= powerup.y and bullets.y <= powerup.y + powerup.h) or bullets.y + bullets.h >= powerup.y and bullets.y + bullets.h <= powerup.y + powerup.h: 
                        rapidFire = True
                        rapid_start = asteroid_count
                        power_up.pop(power_up.index(powerup))
                        player_bullets.pop(player_bullets.index(bullets))
                        break

        if lives <= 0: # Starts the game over sequence
            game_over = True

        if rapid_start != -1: # Handles the timer of the power-up
            if asteroid_count - rapid_start > 500:
                rapidFire = False
                rapid_start = -1
 
        keys = pygame.key.get_pressed() # These are the controls
        if keys[pygame.K_LEFT]: 
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                player_bullets.append(Bullet())

    for event in pygame.event.get(): # Ends the game if the window is closed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: # This stops the game from shooting indefinitely without 
            if event.key == pygame.K_SPACE: # the power-up active if the spacebar is held down
                if not game_over:
                    if not rapidFire:
                        player_bullets.append(Bullet())
                else: # Resets the game values
                    game_over = False
                    lives = 3
                    score = 0
                    asteroids.clear()
                    aliens.clear()
                    alien_bullets.clear()
                    asteroid_count = 0
                    power_up.clear()
                    rapidFire = False

    redraw_game_window() # Updates the screen at the end of every iteration
pygame.quit() # Closes the game
