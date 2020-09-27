#Import Libs
import pygame
from pygame import *
from random import randint, choice

#inisalition
pygame.init()
pygame.mixer.init()

clock = time.Clock()

#difine constints
WINDOW_HEIGHT = 1100
WINDOW_WIDTH = 600
WINDOW_REZ = (WINDOW_HEIGHT, WINDOW_WIDTH)

#dfine tiles
WIDTH = 100
HEIGHT = 100
GRID_REZ = (WIDTH, HEIGHT)

#define colors
WHITE = (255, 255, 255)

SPAWN_RATE = 360
FRAME_RATE = 60

LV1_STARTING_BUCKS = 15
LV2_STARTING_BUCKS = 25
BUCK_RATE = 120
STARTING_BUCK_BOOSTER = 1
STARTING_HEALTH = 100

MAX_BAD_REVIEWS = 3
WIN_TIME = FRAME_RATE * 60 * 3

FAST_SPEED = 3
REG_SPEED = 2
SLOW_SPEED = 1

cannon_coordinates = []

FIRE_RATE = 60

#create window
GAME_WINDOW = display.set_mode(WINDOW_REZ)
display.set_caption('Attack of the vampire pizzas')
background_img = image.load('./Assets/restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_REZ)

#set up ennamy img
were_img = image.load('./Assets/were_pizza.png')
were_surf = Surface.convert_alpha(were_img)
WERE_PIZZA = transform.scale(were_surf, (WIDTH, HEIGHT))

zombie_img = image.load('./Assets/zombie_pizza.png')
zombie_surf = Surface.convert_alpha(zombie_img)
ZOMBIE_PIZZA = transform.scale(zombie_surf, (WIDTH, HEIGHT))

pizza_img = image.load('./Assets/vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, GRID_REZ)

med_health_img = image.load('./Assets/pizza60health.png')
med_health_surf = Surface.convert_alpha(med_health_img)
MED_HEALTH = transform.scale(med_health_surf, GRID_REZ)

low_health_img = image.load('./Assets/pizza30health.png')
low_health_surf = Surface.convert_alpha(low_health_img)
LOW_HEALTH = transform.scale(low_health_surf, GRID_REZ)
#set up trap img
garlic_img = image.load('./Assets/garlic.png')
garlic_surf = Surface.convert_alpha(garlic_img)
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT))

cutter_img = image.load('./Assets/pizzacutter.png')
cutter_surf = Surface.convert_alpha(cutter_img)
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT))

pepperoni_img = image.load('./Assets/pepperoni.png')
pepperoni_surf = Surface.convert_alpha(pepperoni_img)
PEPPERONI = transform.scale(pepperoni_surf, (WIDTH, HEIGHT))

table_img = image.load('./Assets/pizza-table.png')
table_surf = Surface.convert_alpha(table_img)
TABLE = transform.scale(table_surf, (WIDTH, HEIGHT))

table_img = image.load('./Assets/pizza-table.png')
table_surf = Surface.convert_alpha(table_img)
TABLE = transform.scale(table_surf, (WIDTH, HEIGHT))

explosion_img = image.load('./Assets/explosion.png')
explosion_surf = Surface.convert_alpha(explosion_img)
EXPLOSION = transform.scale(explosion_surf, (WIDTH, HEIGHT))


cannon_img = image.load('./Assets/anchovy-cannon.png')
cannon_surf = Surface.convert_alpha(cannon_img)
CANNON = transform.scale(cannon_surf, (WIDTH, HEIGHT))

anchovy_img = image.load('./Assets/anchovy.png')
anchovy_surf = Surface.convert_alpha(anchovy_img)
ANCHOVY = transform.scale(anchovy_surf, (WIDTH, HEIGHT))
#------------------------------------------------
#set up clases

class VampireSprite(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = REG_SPEED
        self.lane = randint(0, 4)
        all_vampires.add(self)
        self.image = VAMPIRE_PIZZA.copy()
        y = 50 + self.lane*100
        self.rect = self.image.get_rect(center = (1100, y))
        self.health = STARTING_HEALTH
        self.despawn_wait = 1000
    def update(self, game_window, counters):
        collided = sprite.spritecollide(self, all_anchovies, True)
        if collided is not None:
            for anchovy in collided:
                self.health -= 10
        if self.rect.x <= 100:
            counters.bad_reviews += 1
            self.despawn_wait = 0
        if self.despawn_wait is None:
            if self.health <= 0:
                self.image = EXPLOSION.copy()
                self.speed = 0
                self.despawn_wait = 20
                explosion_sound = pygame.mixer.Sound('./Assets/leisure_video_game_retro_8bit_explosion_003.wav')
            game_window.blit(self.image, (self.rect.x, self.rect.y))
        elif self.despawn_wait <= 0:
            self.kill()
        self.despawn_wait -= 1
        if 30 < self.health * 100 // STARTING_HEALTH < 60:
            self.image = MED_HEALTH.copy()
        elif self.health * 100 // STARTING_HEALTH <= 30:
            self.image = LOW_HEALTH
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x -= self.speed
        game_window.blit(self.image, (self.rect.x, self.rect.y))    
    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = SLOW_SPEED
        if tile.trap == DAMAGE:
            self.health -= 1
        if tile.trap == MINE:
            self.health = 0
class WerePizza(VampireSprite):
    def __init__(self):
        super(WerePizza, self).__init__()
        self.speed = FAST_SPEED
        self.image = WERE_PIZZA.copy()
    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = REG_SPEED
        if tile.trap == DAMAGE:
            self.health -= 1
        if tile.trap == MINE:
            self.health = 0

class ZombiePizza(VampireSprite):
    def __init__(self):
        super(ZombiePizza, self).__init__()
        self.health = STARTING_HEALTH * 2
        self.speed = SLOW_SPEED
        self.image = ZOMBIE_PIZZA.copy()
    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = REG_SPEED
        if tile.trap == DAMAGE:
            self.health -= 1
        if tile.trap == MINE:
            self.health = 0
    def update(self, game_window, counters):
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x -= self.speed
        if self.health <= 0 or self.rect.x <= 100:
            if self.rect.x <= 100:
                counters.bad_reviews += 1
            self.kill()
        else:
            precent_health = self.health*100//STARTING_HEALTH*2
            if precent_health > 80:
                self.image = ZOMBIE_PIZZA.copy()
            elif precent_health > 65:
                self.image = MED_HEALTH.copy() 
            elif precent_health > 50:
                self.image = LOW_HEALTH.copy()
            elif precent_health > 35:
                self.image = ZOMBIE_PIZZA.copy()
            elif precent_health > 20:
                self.image = MED_HEALTH.copy()
            else:
                self.image = LOW_HEALTH.copy()
            game_window.blit(self.image, (self.rect.x, self.rect.y))            
class BackgroundTile(sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.trap = None
        self.rect = rect
class Counters(object):
    def __init__(self, pizza_bucks, buck_rate, buck_booster, timer, fire_rate):
        self.fire_rate = fire_rate
        self.loop_count = 0
        self.display_font=font.Font('./Assets/pizza_font.ttf', 25)
        self.pizza_bucks = pizza_bucks
        self.buck_rate = buck_rate
        self.buck_booster = buck_booster
        self.bucks_rect = None
        self.timer = timer
        self.timer_rect = None
        self.bad_reviews = 0
        self.bad_rev_rect = None
    def increment_bucks(self):
        if self.loop_count % self.buck_rate == 0:
            self.pizza_bucks += self.buck_booster
    def update_cannon(self):
        for location in cannon_coordinates:
            if self.loop_count % self.fire_rate == 0:
                Anchovy(location)
                Anchovy_Sound = pygame.mixer.Sound('./Assets/zapsplat_multimedia_game_sound_digital_fast_collect_item_002_55830.wav')
                Anchovy_Sound.play()
    def draw_bucks(self, game_window):
        if bool(self.bucks_rect):
            game_window.blit(BACKGROUND, (self.bucks_rect.x, self.bucks_rect.y), self.bucks_rect)
        bucks_surf = self.display_font.render(str(self.pizza_bucks), True, WHITE)
        self.bucks_rect = bucks_surf.get_rect()
        self.bucks_rect.x = WINDOW_HEIGHT - 50
        self.bucks_rect.y = WINDOW_WIDTH - 50 
        game_window.blit(bucks_surf, self.bucks_rect)
    def draw_bad_reviews(self, game_window):
        if bool(self.bad_rev_rect):
            game_window.blit(BACKGROUND, (self.bad_rev_rect.x, self.bad_rev_rect.y), self.bad_rev_rect)
        bad_rev_surf = self.display_font.render(str(self.bad_reviews), True, WHITE)
        self.bad_rev_rect = bad_rev_surf.get_rect()
        self.bad_rev_rect.x = WINDOW_HEIGHT - 150
        self.bad_rev_rect.y = WINDOW_WIDTH - 50
        game_window.blit(bad_rev_surf, self.bad_rev_rect)
    def draw_timer(self, game_window):
        if bool(self.timer_rect):
            game_window.blit(BACKGROUND, (self.timer_rect.x, self.timer_rect.y), self.timer_rect)
        timer_surf = self.display_font.render(str((WIN_TIME - self.loop_count) // FRAME_RATE), True, WHITE)
        self.timer_rect = timer_surf.get_rect()
        self.timer_rect.x = WINDOW_HEIGHT - 250
        self.timer_rect.y = WINDOW_WIDTH - 50
        game_window.blit(timer_surf, self.timer_rect)
    def update(self, game_window):
        self.loop_count += 1
        self.increment_bucks()
        self.draw_bucks(game_window)
        self.draw_bad_reviews(game_window)
        self.draw_timer(game_window)
        self.update_cannon()   
class Trap(object):
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind = trap_kind
        self.cost = cost
        self.trap_img = trap_img
class TrapApplicator(object):
    def __init__(self):
        self.selected = None
    def select_trap(self, trap):
        if(trap.cost <= counters.pizza_bucks):
            self.selected = trap
    def select_tile(self, tile, counters):
        self.selected = tile.set_trap(self.selected, counters)     
class PlayTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if bool(trap) and not bool(self.trap):
            counters.pizza_bucks -= trap.cost
            self.trap = trap
            if trap == EARN:
                counters.buck_booster += 1
            if trap == PROJECTILE:
                cannon_coordinates.append((self.rect.x, self.rect.y))
            Place_Sound = pygame.mixer.Sound('./Assets/leisure_video_game_retro_8bit_coin_pickup_collect_003.wav')
            Place_Sound.play()
        return None

    def draw_trap(self, game_window, trap_applicator):
        if  bool(self.trap):
            game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y))
class ButtonTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if counters.pizza_bucks >= self.trap.cost:
            return self.trap
        else :
            return None
    def draw_trap(self, game_window, trap_applicator):
        if bool(trap_applicator.selected):
            if (trap_applicator.selected == self.trap):
                draw.rect(game_window, (238, 190, 47), (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5)
class InactiveTile(BackgroundTile):
    def set_trap(self, trap, counters):
        return None
    def draw_trap(self, game_window, trap_applicator):
        pass        
class Anchovy(sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__()
        self.image = ANCHOVY.copy()
        self.speed = REG_SPEED
        all_anchovies.add(self)
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0] + 40
        self.rect.y = coordinates[1] + 0
    def update(self, game_window):
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        self.rect.x += self.speed
        if self.rect.x > 1200:
            self.kill
        else:
            game_window.blit(self.image, (self.rect.x, self.rect.y))
        

#------------------------------------------------
#set up class instanses and groups

all_vampires = sprite.Group()
all_anchovies = sprite.Group()
lvl1_enemy_types = []
lvl1_enemy_types.append(VampireSprite)
lvl2_enemy_types = []
lvl2_enemy_types.append(VampireSprite)
lvl2_enemy_types.append(WerePizza)
lvl2_enemy_types.append(ZombiePizza)
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 5, CUTTER)
EARN = Trap('EARN', 5, PEPPERONI)
MINE = Trap('MINE', 10, TABLE)
PROJECTILE = Trap('PROJECTILE', 8, CANNON)
trap_applicator = TrapApplicator()

#-----------------------------------------------------

#DRAW GRID
tile_grid = []
tile_color = WHITE
for row in range(6):
    row_of_tiles = []
    tile_grid.append(row_of_tiles)
    for column in range(11):
        tile_rect = Rect(WIDTH*column, HEIGHT*row, WIDTH, HEIGHT)
        if column <= 1:
            new_tile = InactiveTile(tile_rect)
        else:
            if row == 5:
                if 2<= column <= 6:
                    new_tile = ButtonTile(tile_rect)
                    new_tile.trap = [SLOW, DAMAGE, EARN, MINE, PROJECTILE][column - 2]
                else:
                    new_tile = InactiveTile(tile_rect)
            else:
                new_tile = PlayTile(tile_rect)
        row_of_tiles.append(new_tile)
        if row == 5 and 2 <= column <= 6:
            BACKGROUND.blit(new_tile.trap.trap_img, (new_tile.rect.x, new_tile.rect.y))
        if column != 0 and row != 5:
            if column != 1:
                draw.rect(BACKGROUND, tile_color,(WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1)

#display backgrond
GAME_WINDOW.blit(BACKGROUND, (0, 0))

#------------------------------------------------
#start Main Game Loop


def run_level(enemy_list, start_bucks, clear_tiles):
#Game Loop
    GAME_WINDOW.blit(BACKGROUND, (0, 0))
    counters = Counters(start_bucks, BUCK_RATE, STARTING_BUCK_BOOSTER, WIN_TIME, FIRE_RATE)
    for vampire in all_vampires:
        vampire.kill()
    if clear_tiles:
        for row in tile_grid:
            for column_index in range(len(row)):
                if isinstance(row[column_index], PlayTile):
                    row[column_index].trap = None
    game_running = True
    program_running = True
    while game_running:
    #check for events
        for event in pygame.event.get():
    #Exit loop on quit
            if event.type == QUIT:
                game_running = False
                program_running = False
            elif event.type == MOUSEBUTTONDOWN:
                coordinates = mouse.get_pos()
                x = coordinates[0]
                y = coordinates[1]
                tile_y = y//100
                tile_x = x//100
                trap_applicator.select_tile(tile_grid[tile_y][tile_x], counters)
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    trap_applicator.select_tile(tile_grid[5][2], counters)
                if event.key == K_2:
                    trap_applicator.select_tile(tile_grid[5][3], counters)
                if event.key == K_3:
                    trap_applicator.select_tile(tile_grid[5][4], counters)
                if event.key == K_4:
                    trap_applicator.select_tile(tile_grid[5][5], counters)
                if event.key == K_5:
                    trap_applicator.select_tile(tile_grid[5][6], counters)


        if randint(1, SPAWN_RATE) == 1:
                choice(enemy_list)()

        for tile_row in tile_grid:
            for tile in tile_row:
                if bool(tile.trap):
                    GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, tile.rect.y), tile.rect)
        for vampire in all_vampires:
            tile_row = tile_grid[vampire.rect.y // 100]
            vamp_left_side = vampire.rect.x // 100 
            vamp_right_side = (vampire.rect.x + vampire.rect.width) // 100 
            if 0 <= vamp_left_side <= 10:
                left_tile  = tile_row[vamp_left_side]
            else:
                left_tile = None
            if 0 <= vamp_right_side <= 10:
                right_tile  = tile_row[vamp_left_side]
            else:
                right_tile = None
            if bool(left_tile):
                vampire.attack(left_tile)

            if bool(right_tile):
                if right_tile != left_tile:
                    vampire.attack(right_tile)
        if counters.bad_reviews >= MAX_BAD_REVIEWS:
            game_running = False
        if counters.loop_count > WIN_TIME:
            game_running = False
        for vampire in all_vampires:
            vampire.update(GAME_WINDOW, counters)
        for tile_row in tile_grid:
            for tile in tile_row:
                tile.draw_trap(GAME_WINDOW, trap_applicator)
        for anchovy in all_anchovies:
            anchovy.update(GAME_WINDOW)
        counters.update(GAME_WINDOW)        
        display.update()

        clock.tick(FRAME_RATE)
    return game_running, program_running, counters

Level_setup = [
    [lvl1_enemy_types, LV1_STARTING_BUCKS],
    [lvl2_enemy_types, LV2_STARTING_BUCKS]
]
current_level = 0
end_font = font.Font('./Assets/pizza_font.ttf', 50)
program_running = True
while program_running and current_level < len(Level_setup):
    if current_level > 0:
        clear_tiles = True
    else:
        clear_tiles = False
    game_running, program_running, counters = run_level(
        Level_setup[current_level][0],
        Level_setup[current_level][1],
        clear_tiles)
    if program_running:
        if counters.bad_reviews >= MAX_BAD_REVIEWS:
            end_surf = end_font.render('Game Over',True, WHITE)
            GAME_WINDOW.blit(end_surf, (350, 200))
            display.update()
            Game_Over_sound = pygame.mixer.Sound('./Assets/little_robot_sound_factory_Hero_Death_00.wav')
            Game_Over_sound.play() 
        elif current_level < len(level_setup):
            cont_surf = end_font.render('Press Enter for Level ' + str(current_level + 1), True, WHITE)
            GAME_WINDOW.blit(cont_surf, (150, 400))
            display.update()
            waiting_at_prompt = True
            while waiting_at_prompt:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        waiting_at_prompt = False
                        program_running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            waiting_at_prompt = False
        else:
            End_Sound = pygame.mixer.Sound('./Assets/zapsplat_multimedia_game_sound_digital_high_pitched_positive_success_complete_tone_55832')
            End_Sound.play()
            end_surf = end_font.render('You Won!!!', True, WHITE)
            GAME_WINDOW.blit(end_surf, (350, 200))
            display.update()
        current_level += 1


while program_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            program_running = False
    clock.tick(FRAME_RATE)    

#end of main game loop
#------------------------------------------------
#Clean up game
pygame.quit()
