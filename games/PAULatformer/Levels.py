import os
import pygame
pygame.init()
from importlib.machinery import SourceFileLoader
maindir = os.path.abspath(os.path.dirname(__file__))
assetdir = os.path.join(maindir, 'assets')
T = SourceFileLoader('Tile', os.path.join(maindir, 'Tile.py')).load_module()

class Level:
    def __init__(self, level):
        match level:
            case 0:
                self.level_num = 0
                self.id = 'Level 0: The Backrooms'
                self.background = 'tictactoe'
                level_list = [
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                ]
                self.start_x, self.start_y = 13, 1
                self.sign_list = [
                    'You are not supposed to be here.',
                    'Get out of here now.'
                ]
            case 1:
                self.level_num = 1
                self.id = 'Level 1: Asteroids'
                self.background = 'asteroids'
                level_list = [
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,3,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,5,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1],
                    [1,0,1,1,1,1,0,0,0,4,0,0,0,0,1,0,0,0,0,1],
                    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                    [1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1],
                    [1,0,0,0,0,0,1,0,4,1,1,0,0,0,0,0,0,0,4,1],
                    [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1]
                ]
                self.start_x, self.start_y = 2, 2
                self.sign_list = [
                    'Hey, you\'re getting the hang of this! See you in the next level!',
                    'Hey there! I\'m a sign. I\'m here to track you through the PAUL levels.'
                ]

            case 2:
                self.level_num = 2
                self.id = 'Level 2: Checkers'
                self.background = 'checkers'
                level_list = [
                    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,4,1],
                    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,3,1],
                    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1],
                    [1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                ]
                self.start_x, self.start_y = 12, 1
                self.sign_list = []
        
        blocks_layout = []
        [blocks_layout.append([0]*20) for i in range(15)]
        for i in range(15):
            for j in range(20):
                blocks_layout[i][j] = T.Tile(level_list[i][j], i, j)
                if level_list[i][j] == 5 and self.sign_list:
                    blocks_layout[i][j].text = self.sign_list.pop(0)
        self.level = blocks_layout

    def get_level(self):
        return self.level
    
    def get_level_num(self):
        return self.level_num

    def get_background(self):
        return self.background

    def get_rect_list(self):
        rect_list = []
        for i in range(15):
            for j in range(20):
                if self.level[i][j].collision:
                    rect_list.append((self.level[i][j].get_img_rect(), self.level[i][j].type, self.level[i][j].collision))
        return rect_list

    def get_start_coords(self):
        return self.start_x, self.start_y

    def update_level(self, screen):
        for i in range(15):
            for j in range(20):
                p1,p2 = self.level[i][j].get_img(), self.level[i][j].get_img_rect()
                screen.blit(p1,p2)