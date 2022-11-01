# see content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
from ctypes.wintypes import RGB
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from settings import *
import os

vec = pg.math.Vector2

# setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# platforms = []

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def colorbyte():
    return randint(0, 255)

# classes
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.fill((self.r, self.g, self.b))
        # self.image = pg.image.load(os.path.join(img_folder, 'SpriteCan.webp')).convert()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        print(self.rect.center)


        # self.speed = 5
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            # self.rect.x += -1
            self.acc.x = -5
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            # self.rect.y + 1
            self.acc.x = 5
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.acc.y = 5

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False


        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

    def jump(self):
        self.rect.x +=1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -20
            print("I've been hit!!!")


    def update(self):
        # set gravity
        self.acc = vec(0,PLAYER_GRAV)
        # use controls defined above
        self.controls()
        # friction
        self.acc += self.vel * -PLAYER_FRIC
        if self.rect.bottom > HEIGHT:
            self.acc.y += -(PLAYER_GRAV)
            self.vel.y = 0
            self.pos.y = HEIGHT
            self.image.fill((colorbyte(), colorbyte(), colorbyte()))
        if self.rect.top <= 5:
            # self.vel.y = 0
            # self.pos.y = 0
            self.acc.y += 5.1
            self.image.fill(STARTING_COLOR)
        if self.rect.right > WIDTH:
            # self.rect.right = 0
            # self.vel.x = 0
            # self.pos.x = WIDTH
            self.acc.x += -5.1
        if self.rect.left < 0:
            # self.rect.left = 0
            # self.vel.x = 0
            # self.pos.x = 0
            self.acc.x += 5.1
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        #self.rect.centerx = self.pos
        self.rect.midbottom = self.pos

        self.collide_with_walls('x')
        self.collide_with_walls('y')

class Pewpew(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.owner = ""
    def update(self):
        if self.owner == "player":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if (self.rect.y < 0):
            self.kill()
            print(pewpews)

class Healthbar(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# mobs
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 5*random.choice([-1,1])
        self.speedy = 5*random.choice([-1,1])
        self.inbounds = True

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery

    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1

    def update(self):
        self.boundscheck()
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy

# init pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My game...")
clock = pg.time.Clock()

# Create a group for all sprites
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
pewpews = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(WIDTH/2, HEIGHT/2, 100, 35)
plat2 = Platform(WIDTH/3, HEIGHT/4, 80, 30)
ground = Platform(0, HEIGHT-20, WIDTH, 20)


for i in range(40):
    global mob_color
    mob_color = (colorbyte(), colorbyte(), colorbyte())
    m = Mob(randint(0, WIDTH), randint(0, HEIGHT), 25, 25, mob_color)
    all_sprites.add(m)
    mobs.add(m)
    print(m)

# add instances to groups
all_sprites.add(player, plat, plat2, ground)
all_plats.add(plat, plat2, ground)

# Game loop
running = True

while running:
    dt = clock.tick(FPS)

    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        print("I've struck a platform!!")
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        print("I've struck a mob...")
        SCORE += 1
        player.health += -1
        if player.r < 255:
            player.r += 15

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONUP:
            p = Pewpew(player.rect.midtop[0], player.rect.midtop[1], 10, 10)
            p.owner = "player"
            all_sprites.add(p)
            pewpews.add(p)
            mpos = pg.mouse.get_pos()
            print(mpos)
            # get a list of all sprites that are under the mouse cursor
            clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            for m in mobs:
                if m.rect.collidepoint(mpos):
                    print(m)
                    m.kill()
                    SCORE += 1

            # print(clicked_sprites)k 
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()

    # Update all sprites
    all_sprites.update()

    # Draw
    screen.fill(BLACK)
    # draw player color
    player.image.fill((player.r,player.g,player.b))
    # draw all sprites
    all_sprites.draw(screen)
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH/2, HEIGHT/24)
    draw_text("FPS: " + str(dt), 22, WHITE, WIDTH/2, 23*HEIGHT/24)
    draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    if mobhits:
        pg.draw.line(screen, (RED), [player.rect.centerx, player.rect.centery], [mobhits[0].rect.centerx, mobhits[0].rect.centery], 5)
    if player.colliding:
        pg.draw.line(screen, (RED), [player.rect.centerx, player.rect.centery], [player.hitx, player.hity], 5)

    pg.display.flip() # buffering system that sets up update system to be faster, flip display


pg.quit()