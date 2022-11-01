# Sources:
# Control pygame time: https://www.geeksforgeeks.org/pygame-time/
# Find the number of sprites in a pygame group: https://www.w3schools.com/python/python_datatypes.asp

# import libraries
import pygame as pg
from pygame.sprite import Sprite
from random import randint
from settings import *
import os

# See lines 255-269 for Goals, Rules, Feedback, Freedom

# Innovations:
# Mobs are now coins
# Enemies can kill the player, also move randomly
# Enemies move faster as your score increases

# setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Images')

# create use of vector from pygame
vec = pg.math.Vector2

# define draw text feature
def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# function that adds sprites to group (used for mobs/coins & enemies)
def add_sprite_to_group(num, Class, group):
    for i in range(num):
        # Ensure that sprites don't spawn on the player
        # Set random width position to be (20, WIDTH/2 - 25) U (WIDTH/2 + 25, WIDTH)
        width_pos_1 = randint(20, WIDTH/2 - 25)
        width_pos_2 = randint(WIDTH/2 + 25, WIDTH - 20)
        width_pos_0 = randint(0, 1)
        if width_pos_0 == 0:
            width_pos = width_pos_1
        if width_pos_0 == 1:
            width_pos = width_pos_2
        # Set random height position to be (20, HEIGHT/2 - 25) U (HEIGHT/2 + 25, HEIGHT)
        height_pos_1 = randint(20, HEIGHT/2 - 25)
        height_pos_2 = randint(HEIGHT/2 + 25, HEIGHT - 20)
        height_pos_0 = randint(0, 1)
        if height_pos_0 == 0:
            height_pos = height_pos_1
        if height_pos_0 == 1:
            height_pos = height_pos_2
        # create sprites
        l = Class(width_pos, height_pos)
        all_sprites.add(l)
        group.add(l)

# create player
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # use pygame to create square of height and width 20
        self.image = pg.Surface((20, 20))
        # color of player
        self.image.fill(STARTING_COLOR)
        # self.image = pg.image.load(os.path.join(img_folder, "SpriteCan.webp")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False

    # create controls to move player around screen with both WASD and arrow keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.acc.x = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.acc.x = 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.acc.y = 1    

    # create updating method for player
    def update(self):
        # define initial acceleration
        self.acc = vec(0, 0)
        # call the controls method
        self.controls()
        # ensure the player doesn't move too far off screen
        if self.rect.bottom > HEIGHT + 50:
            self.acc.y += -3
            print("I've gone below")
        if self.rect.top <= -50:
            self.acc.y += 3
            print("I've gone above")
        if self.rect.right > WIDTH + 30:
            self.acc.x += -3
            print("I've gone right")
        if self.rect.left < -30:
            self.acc.x += 3
            print("I've gone left")
        # friction
        self.acc += self.vel * -PLAYER_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        # setting location of player's position
        self.rect.midbottom = self.pos


# create mobs (sub)class
class Mob(Sprite):
    def __init__(self, x, y):
        # call Pygame superclass
        Sprite.__init__(self)
        # self.image = pg.Surface((w, h))
        # self.image.fill(color)

        # Uses Mr. Cozort's technique to make the mobs have a coin image
        self.image = pg.image.load(os.path.join(img_folder, "GoldCoinResized.png")).convert()
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    # create moving method of the mobs
    def moving(self):
        # create random movement of mobs
        rand_int_x = randint(-1, 1)
        rand_int_y = randint(-1, 1)
        self.acc.x += rand_int_x
        self.acc.y += rand_int_y

    # create update method
    def update(self):
        # define initial acceleration
        self.acc = vec(0, 0)
        # call the moving method
        self.moving()
        # accounts for the mobs moving off screen and redirects
        if self.rect.bottom > HEIGHT + 30:
            self.acc.y += -3
            print("Coin below")
        if self.rect.top <= -30:
            self.acc.y += 3
            print("Coin above")
        if self.rect.right > WIDTH + 10:
            self.acc.x += -3
            print("Coin right")
        if self.rect.left < -10:
            self.acc.x += 3
            print("Coin left")
        # friction
        self.acc += self.vel * -MOB_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos

# Create enemies subclass
class Enemies(Sprite):
    def __init__(self, x, y):
        # calls superclass
        Sprite.__init__(self)
        self.image = pg.Surface((35, 35))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    # create moving method so that enemies randomly move around screen
    def moving(self):
        rand_int_x = randint(-2, 2)
        rand_int_y = randint(-2, 2)
        self.acc.x += rand_int_x
        self.acc.y += rand_int_y
    
    # create update method
    def update(self):
        # create acceleration
        self.acc = vec(0, 0)
        # call the moving method
        self.moving()
        # accounts for the enemies moving off screen
        if self.rect.bottom > HEIGHT - 10:
            self.acc.y += -3
            print("Enemy below")
        if self.rect.top <= 10:
            self.acc.y += 3
            print("Enemy above")
        if self.rect.right > WIDTH - 10:
            self.acc.x += -3
            print("Enemy right")
        if self.rect.left < 10:
            self.acc.x += 3
            print("Enemy left")
        # friction
        self.acc += self.vel * -ENEMY_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos


# init pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My game...")
clock = pg.time.Clock()

# Create a group for all sprites
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
enemies = pg.sprite.Group()

# instantiate classes
player = Player()

# Create mobs/coins
add_sprite_to_group(COINS, Mob, mobs)

# Create 5 Enemies
add_sprite_to_group(5, Enemies, enemies)

# add instances to groups
all_sprites.add(player)

# Game loop
running = True

while running:

    # Pre-game/Instructional Screens using for loop
    for i in range(6):
        running_i = True

        # Each screen will have own while loop
        while running_i:

            # Draw
            screen.fill(BLACK)

            # Display how to go to next screen
            if i >= 0 and i < 5:
                draw_text("(Press space to continue)", 22, WHITE, WIDTH/2, 5*HEIGHT/8)
            elif i == 5:
                draw_text("(Press space to begin)", 22, WHITE, WIDTH/2, 5*HEIGHT/8)


            # draw info on screen - different for each screen
            if i == 0:
                draw_text("Welcome to... MY GAME!!!", 22, WHITE, WIDTH/2, 8*HEIGHT/16)
            elif i == 1 :
                draw_text("GOAL:", 26, WHITE, WIDTH/2, 7*HEIGHT/16)
                draw_text("Get as many coins as you can", 22, WHITE, WIDTH/2, 8*HEIGHT/16)
            elif i == 2:
                draw_text("RULES:", 26, WHITE, WIDTH/2, 7*HEIGHT/16)
                draw_text("Watch out for the red enemies trying to devour you", 18, WHITE, WIDTH/2, 8*HEIGHT/16)
            elif i == 3:
                draw_text("FEEDBACK:", 26, WHITE, WIDTH/2, 7*HEIGHT/16)
                draw_text("Keep an eye on your points at the top of the screen", 18, WHITE, WIDTH/2, 8*HEIGHT/16)
            elif i == 4:
                draw_text("FREEDOM!!!!", 26, WHITE, WIDTH/2, 7*HEIGHT/16)
                draw_text("Use either WASD or the arrows keys to move", 18, WHITE, WIDTH/2, 8*HEIGHT/16)
            elif i == 5:
                draw_text("Good Luck!!!", 26, WHITE, WIDTH/2, 8*HEIGHT/16)
            

            # when hit space bar, moves to game
            keys = pg.key.get_pressed()
            # wait time ensures all the preview screens don't run on one space bar press
            pg.time.wait(80)
            # while loop breaks if space bar is pressed
            if keys[pg.K_SPACE]:
                running_i = False

            # check for closed window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    running_i = False

            # buffering system that sets up update system to be faster, flip display
            pg.display.flip()


    # Game Loop Part 2 (Actual Game)
    running_2 = True

    while running_2:
        dt = clock.tick(FPS)

        # if hit mob, then increase score by 1 and kill mob
        mobhits = pg.sprite.spritecollide(player, mobs, True)
        if mobhits:
            print("I've struck gold!")
            SCORE +=1
            # make enemies move faster as score increases
            ENEMY_FRIC += -ENEMY_SPEED_INC

        # if hit enemy, end game
        enemyhits = pg.sprite.spritecollide(player, enemies, False)
        if enemyhits:
            print("You've died")
            # wait after death for 400ms
            pg.time.wait(400)
            # WIN is for use on final screen
            WIN = 0
            running = False
            running_2 = False

        # if catch all the mobs, player wins and game ends
        # this returns a list of all sprites in the group 'mobs'
        if pg.sprite.Group.sprites(mobs) == []:
            print("You win!!!!!!!!!!")
            pg.time.wait(1500)
            # WIN is for use on final screen
            WIN = 1
            running = False
            running_2 = False

        # check for closed window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                running_2 = False
            

        # Update all sprites
        all_sprites.update()

        #################### Draw #######################
        # draw black screen in back
        screen.fill(BLACK)
        # draw all sprites
        all_sprites.draw(screen)

        # draw the points on screen
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH/2, HEIGHT/24)

        # buffering system that sets up update system to be faster, flip display
        pg.display.flip()

    # Game Loop Part 3 (End)
    running_3 = True

    while running_3:

        ######## Draw ############
        # Draw black screen
        screen.fill(BLACK)
        
        # If player wins/loses, draw appropriate text
        if WIN == 0:
            draw_text("You've Died", 26, WHITE, WIDTH/2, 8*HEIGHT/16)
            draw_text("(Press space to quit)", 22, WHITE, WIDTH/2, 5*HEIGHT/8)
        elif WIN == 1:
            draw_text("Congratulations on Your Victory!!", 26, WHITE, WIDTH/2, 8*HEIGHT/16)
            draw_text("(Press space to quit)", 22, WHITE, WIDTH/2, 5*HEIGHT/8)
        # Attempt to account for bugs
        else:
            running = False
            running_3 = False

        # If space bar is pressed, quit game
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            running = False
            running_3 = False

        # check for closed window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                running_3 = False

        # buffering system that sets up update system to be faster, flip display
        pg.display.flip()

# once while loop is false, quit the game
pg.quit()