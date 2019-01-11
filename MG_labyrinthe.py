"""
Helped MacGyver to escape
Game in which MacGyver must be moved to the exit through a labyrinth.

Script Python
Files : MG_labyrinthe.py, classes.py, constantes.py, n1 + images
"""

import  pygame
from pygame.locals import *

from classes import *
from constantes import *

pygame.init()
window_resolution = (450, 450)
window_resolution1 = (450, 450)
blank_color = (255, 255, 255)
green_color =  (66, 244, 89)

#Open the windows Pygame (square: width = height)
window = pygame.display.set_mode((window_side, window_side))
# Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)

#Title
pygame.display.set_caption(window_title)
window_surface = pygame.display.set_mode(window_resolution)
windows_game_info = pygame.display.set_mode(window_resolution1)

arial_font = pygame.font.SysFont("arial", 30)
Jeu_MC_Gyver_intro = arial_font.render("Jeu - Aidez MacGyver à s'échapper", False, blank_color)

arial_font = pygame.font.SysFont("arial", 28)
Jeu_MC_Gyver_info = arial_font.render("For start press K_F1 for leave press ESC", False, green_color)

window_surface.blit(Jeu_MC_Gyver_intro, [10, 10])
windows_game_info.blit(Jeu_MC_Gyver_info, [10, 50])
pygame.display.flip()

#Main Loop
continuer = 1
while continuer:
    #Loading and viewing the home screen
    home = pygame.image.load(image_start).convert()


    #Refreshments
    pygame.display.flip()

    #These variables are reset to 1 at each loop turn
    continuer_game = 1
    continuer_home = 1

    #HOST LOOP
    while continuer_home:
        #Speed limitation of the loop
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            #If the user leaves, we put the variables
            #loop to 0 to browse none and close
            if event.type == QUIT or event.type == K_ESCAPE:
                continuer_home = 0
                continuer_game = 0
                continuer = 0
                #Variable of choice of the level
                choice = 0

            elif event.type == KEYDOWN:
                #Start level 1
                if event.key == K_F1:
                    continuer_home = 0  # We leave home
                    continuer_game = 1
                    choice = 'n1'  # We define the level to load


    #we check that the player has made a choice of level
    #to not load if it leaves
    if choice != 0:
        #Loading the bottom
        fond = pygame.image.load(image_fond).convert()

        #Generating a level from a file
        lvl = Level("ressource/labyrinthe.txt")
        window.blit(fond, (0, 0))
        window.blit(home, (0, 0))
        lvl.generate()
        lvl.place_Items(window)
        lvl.show(window)

        #Creating MacGyver
        MG = Person(lvl)

    #Game Loop
    while continuer_game:
        #Speed limitation of the loop
        pygame.time.Clock().tick(30)

        x_MG = 0    # start position MG x
        y_MG = 0    # start position MG y

        for event in pygame.event.get():

            #  If the user leaves, we put the variable that continues the game
            #  AND the general variable to 0 to close the window
            if event.type == QUIT:
                continuer_game = 0
                continuer = 0

            if event.type == KEYDOWN:
                # If the user press Esc here, we just go back to the menu
                if event.key == K_ESCAPE:
                    continuer_game = 0

                # #MacGyver Move Keys
                if event.key == pygame.K_RIGHT:
                    MG.move(lvl, 'right')

                elif event.key == pygame.K_LEFT:
                    MG.move(lvl, 'left')

                elif event.key == pygame.K_UP:
                    MG.move(lvl, 'up')

                elif event.key == pygame.K_DOWN:
                    MG.move(lvl, 'down')

                window.blit(fond, (0, 0))


            # #Displays at new positions
            lvl.show(window)
            window.blit(MG.direction, (MG.x, MG.y))  # MG.direction = the image in the right direction
            pygame.display.flip()

            # #Victory -> Back to home-menu
            if lvl.structure[MG.case_y][MG.case_x] == 'a' and lvl.score == 3:
                continuer_game = 0
                lvl.to_Win(window)
            elif lvl.structure[MG.case_y][MG.case_x] == 'a' and lvl.score < 3:
                continuer_game = 0
                lvl.to_Lose(window)