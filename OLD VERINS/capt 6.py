#Import Libs
import pygame
from pygame import *
from random import randint

#inisalition
pygame.init()

clock= time.Clock()

#difine constints
WINDOW_HIGHT = 1100
WINDOW_WIDTH = 600
WINDOW_REZ = (WINDOW_HIGHT, WINDOW_WIDTH)

#dfine tiles
WIDTH = 100
HIGHT = 100
GRID_REZ = (WIDTH, HIGHT)

#define colors
WHITE = (255, 255, 255)

SPAWN_RATE = 150
FRAME_RATE = 60

#create window
GAME_WINDOW = display.set_mode(WINDOW_REZ)
display.set_caption('Attack of the vampire pizzas')
background_img = image.load('restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_REZ)

#set up ennamy img
pizza_img = image.load('vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, GRID_REZ)

#------------------------------------------------
#set up clases

class VampireSprite(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.lane = randint(0, 4)
        all_vampires.add(self)
        self.image = VAMPIRE_PIZZA.copy()
        y = 50 + self.lane*100
        self.rect = self.image.get_rect(center = (1100, y))
    def update(self, game_window):
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x -= self.speed
        game_window.blit(self.image, (self.rect.x, self.rect.y))

#------------------------------------------------
#set up class instanses and groups

all_vampires = sprite.Group()

#-----------------------------------------------------

#DRAW GRID
tile_color = WHITE
for row in range(6):
    for column in range(11):
        draw.rect(BACKGROUND, tile_color,(WIDTH*column, HIGHT*row, WIDTH, HIGHT), 1)

#display backgrond
GAME_WINDOW.blit(BACKGROUND, (0, 0))

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

        if randint(1, SPAWN_RATE) == 1:
            VampireSprite()
        for vampire in all_vampires:
            vampire.update(GAME_WINDOW)
            
    display.update()

clock.tick(FRAME_RATE)

#end of main game loop
#------------------------------------------------
#Clean up game
pygame.quit()
