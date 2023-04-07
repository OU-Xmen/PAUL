import Levels as L
import Tile as T
import Player as P
import os
import json
import pygame
pygame.init()
maindir = os.path.dirname(os.path.abspath(__file__))
bkgrddir = os.path.join(maindir, 'assets', 'backgrounds')

current_level = L.Level(15)
new_level = current_level.get_level()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Platformer - Level Editor')

level_background = pygame.image.load(os.path.join(bkgrddir, f"{current_level.get_background()}.png")).convert()

def make_new_level_array(level):
    new_level_array = []
    [new_level_array.append([0]*20) for i in range(15)]

    for i in range(15):
        for j in range(20):
            new_level_array[i][j] = level[i][j].id_num
    
    return new_level_array

while True:
    mouse = pygame.mouse.get_pos()
    mouse_ij = [mouse[1]//40, mouse[0]//40]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            new_dict = {"level": make_new_level_array(new_level)}
            json_object = json.dumps(new_dict)

            with open("newlevel.json", "w") as outfile:
                outfile.write(json_object)

            quit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_0, pygame.K_KP0]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(0, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_1, pygame.K_KP1]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(1, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_2, pygame.K_KP2]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(2, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_3, pygame.K_KP3]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(3, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_4, pygame.K_KP4]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(4, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_5, pygame.K_KP5]:
                new_level[mouse_ij[0]][mouse_ij[1]] = T.Tile(5, mouse_ij[0], mouse_ij[1])
            if event.key in [pygame.K_6, pygame.K_KP6]:
                new_level[mouse_ij[0]][mouse_ij[1]] = P.Player(mouse_ij[0], mouse_ij[1], 'enemy')
            

    screen.blit(level_background, (0, 0))
    for i in range(15):
        for j in range(20):
            screen.blit(new_level[i][j].img, new_level[i][j].img_rect)
    pygame.display.flip()