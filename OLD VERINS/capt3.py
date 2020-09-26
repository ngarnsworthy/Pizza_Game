#Import Libs
import pygame
from pygame import *
#inisalition
pygame.init()

#difine constints
WINDOW_HIGHT = 1100
WINDOW_WIDTH = 600
WINDOW_REZ = (WINDOW_HIGHT, WINDOW_WIDTH)

#create window
GAME_WINDOW = display.set_mode(WINDOW_REZ)
display.set_caption('Attack of the vampire pizzas')

#set up ennamy img
pizza_img = image.load('vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100))

#dispay ennamy picture
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400))

#add peperoni
draw.circle(GAME_WINDOW, (255, 0, 0), (925, 425), 25, 0)

#ADD RECTNGLE
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 395, 110, 110), 5)

#MAKE LID

draw.rect(GAME_WINDOW, (160, 82, 45), (895, 295, 110, 110), 0)
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
