""" Classes of the game Helped MacGyver to escape"""
from typing import List, Any

import pygame
from pygame.locals import *
from constantes import *
import random


class Level:
    """Class to create a level"""
    def __init__(self, file):
        self.file = file
        self.structure = 0
        self.score = 0
        self.score_text = ''

    def generate(self):
        """Method for generating the level based on the file.
        We create a general list, containing a list by line to display"""
        #Open the file
        with open(self.file, "r") as file:
            structure_lvl = []
            for line in file:
                line_lvl = []
                for sprite in line:
                    if sprite != '\n':
                         line_lvl.append(sprite)
                structure_lvl.append(line_lvl)
        self.structure = structure_lvl

    def show(self, window):
        """Method to display the level according to the structure list returned by generer()"""
        #Loading images (only arrival cell contains transparency)
        wall = pygame.image.load(image_wall).convert_alpha()
        start = pygame.image.load(image_start).convert_alpha()
        finish = pygame.image.load(image_gardien).convert_alpha()
        ether = pygame.image.load(image_ether).convert()
        syringe = pygame.image.load(image_syringe).convert()
        plastic = pygame.image.load(image_plastic_bottle).convert_alpha()

        # Score
        if (self.score <= 3):
            myfont = pygame.font.SysFont("monospace", 22)
            self.score_text = myfont.render("My score: " + str(self.score), 1, (23, 216, 216))

        #We browse the list of the level
        num_line = 0
        for line in self.structure:
            #We go through the lists of lines
            num_case = 0
            for sprite in line:
                 #The actual position in pixels is calculated
                 x = num_case * size_sprite
                 y = num_line * size_sprite
                 if sprite == 'm':       #m = Wall
                    window.blit(wall, (x,y))
                 elif sprite == 'd':     #d = Start
                    window.blit(start, (x,y))
                 elif sprite == 'a':     #a = Finish
                    window.blit(finish, (x,y))
                 elif sprite == 'e':     #d = ether
                    window.blit(ether, (x,y))
                 elif sprite == 's':     #d = seringue
                    window.blit(syringe, (x,y))
                 elif sprite == 'p':     #d = plastique
                    window.blit(plastic, (x,y))

                 num_case += 1
            num_line += 1

        window.blit(self.score_text, (93, 5))

    def place_Items(self, window):
        structure_items = ['e', 's', 'p']

        for item in structure_items:
            x = self.get_Random_Coordinates()
            y = self.get_Random_Coordinates()

            while (self.check_If_Valid(x, y) == False):
                x = self.get_Random_Coordinates()
                y = self.get_Random_Coordinates()

            self.structure[x][y] = item

    def check_If_Valid(self, x, y):
        if (self.structure[x][y]) == '0':
            return True
        else:
            return False

    def get_Random_Coordinates(self):
        return random.randint(1, number_sprite_side - 1)

    def remove_Item(self, x, y):
        self.structure[x][y] = '0'

    def to_Win(self, window):
        myfont = pygame.font.SysFont("monospace", 22)
        self.score_text = myfont.render("Victory!!", 1, (0, 0, 255))
        window.blit(self.score_text, (93, 30))

    def to_Lose(self, window):
        myfont = pygame.font.SysFont("monospace", 22)
        self.score_text = myfont.render("You are dead!", 1, (0,0, 255))
        window.blit(self.score_text, (93, 30))

class Person:
    """Class to create a character"""
    def __init__(self, lvl):
        #Sprites of the character
        self.right = pygame.image.load(image_mg).convert_alpha()
        self.left = pygame.image.load(image_mg).convert_alpha()
        self.up = pygame.image.load(image_mg).convert_alpha()
        self.down = pygame.image.load(image_mg).convert_alpha()
        #Position of the character in box and pixels
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        #Default direction
        self.direction = self.right
        #level in which the character is located
        self.lvl = lvl
        self.item_counter = 0


    def move(self, lvl, direction):
        """Method to move the character"""

        #Move to the right
        if direction == 'right':
            #Not to exceed the screen
            if self.case_x < (number_sprite_side - 1):
                #We check that the destination box is not a wall
                if self.lvl.structure[self.case_y][self.case_x+1] != 'm':
                    #Moving a box
                    self.case_x += 1
                    #Calculation of the actual pixel position
                    self.x = self.case_x * size_sprite
            #Image in the right direction
            self.direction = self.right

        #Move to the left
        if direction == 'left':
            if self.case_x > 0:
                if self.lvl.structure[self.case_y][self.case_x-1] != 'm':
                    self.case_x -= 1
                    self.x = self.case_x * size_sprite
            self.direction = self.left

        #move up
        if direction == 'up':
            if self.case_y > 0:
                if self.lvl.structure[self.case_y-1][self.case_x] != 'm':
                    self.case_y -= 1
                    self.y = self.case_y * size_sprite
            self.direction = self.up

        #move down
        if direction == 'down':
            if self.case_y < (number_sprite_side -1):
                if self.lvl.structure[self.case_y+1][self.case_x] != 'm':
                    self.case_y += 1
                    self.y = self.case_y * size_sprite
            self.direction = self.down

        current_item_in_box = self.lvl.structure[self.case_y][self.case_x]
        if (current_item_in_box == 'e' or current_item_in_box == 's' or current_item_in_box == 'p'):
            lvl.score = lvl.score + 1
            lvl.remove_Item(self.case_y, self.case_x)
