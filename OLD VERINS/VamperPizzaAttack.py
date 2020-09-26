#Import Libs
import pygame
from pygame import *
#inisalition
pygame.init()

#difine constints
WINDOW_HIGHT = 1100
WINDOW_WIDTH = 600
WINDOW_REZ = (WINDOW_HIGHT, WINDOW_WIDTH)

#dfine tiles
WIDTH = 100
HIGHT = 100
GRID_REZ = (WIDTH, HIGHT)

#define collors
WHITE = (255, 255, 255)

#create window
GAME_WINDOW = display.set_mode(WINDOW_REZ)
display.set_caption('Attack of the vampire pizzas')

#set up ennamy img
pizza_img = image.load('vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, GRID_REZ)

background_img = image.load('restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_REZ)

#-----------------------------------------------------

#DRAW GRID
tile_color = WHITE
for row in range(6):
    for column in range(11):
        draw.rect(BACKGROUND, tile_color,(WIDTH*column, HIGHT*row, WIDTH, HIGHT), 1)

#display backgrond
GAME_WINDOW.blit(BACKGROUND, (0, 0))
#dsplay eennamy
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400))
#------------------------------------------------
#start Main Game Loop
game_running = True
#Game Loop
while game_running:

#check for events
    for event in pygame.event.get():

#Exit loop on quit
        if event.type == QUIT:
            game_running = False
    display.update()

#end of main game loop
#------------------------------------------------
#Clean up game
pygame.quit()
