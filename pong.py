import pygame 
import math
import numpy
import random
pygame.init()

SCREENHEIGHT = 500
SCREENWIDTH = 500

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 50)
blue = (50, 50, 255)
green = (50, 255, 50)

window = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
pygame.display.set_caption('PONG PROJECT')

font = pygame.font.Font(pygame.font.get_default_font(), 50)

pauseicon = pygame.image.load('pong\pause-xxl.png')

def pause():
    
    loop = 1
    window.blit(pauseicon, (250, 250))
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_SPACE:
                    window.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        clockobject.tick(60)

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

class Paddles(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()

    def User1_key_movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= 10
        elif key[pygame.K_s] and self.rect.y < 425:
            self.rect.y += 10

    def User2_key_movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= 10
        elif key[pygame.K_DOWN] and self.rect.y < 425:
            self.rect.y += 10

class PingPong(pygame.sprite.Sprite):        

    def __init__(self, color, width, height, posx):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(posx)
        self.vel = pygame.math.Vector2(random.choice((-3,3)), 0).rotate(random.randrange(60))
       

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()    

    def physics(self, sprite):
        self.pos += self.vel
        self.rect.center = self.pos
        if self.rect.top < 0 or self.rect.bottom > 500:
            self.vel.y *= -1
        if self.rect.colliderect(sprite):
            self.vel.x *= -1
        
    def reset(self):
        self.rect.x = random.randint(240, 250)
        self.rect.y = 250
        self.pos = (self.rect.x, self.rect.y)
        self.pos+= pygame.math.Vector2(random.choice((-3,3)), 0).rotate(random.randrange(60))
        self.rect.center = self.pos

all_sprites_list = pygame.sprite.Group()

player1block = Paddles(red, 10, 75)
player1block.rect.x = 10
player1block.rect.y = 200
player2block = Paddles(blue, 10, 75)
player2block.rect.x = 480
player2block.rect.y = 200

pongblock = PingPong(green, 10, 10, random.randint(240, 250))

all_sprites_list.add(player1block, player2block, pongblock)

paused = False
running = True

clockobject = pygame.time.Clock()

p1points = 0
p2points = 0

while running:
    clockobject.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.key == pygame.K_SPACE:
            pause()


    window.fill(black)

    if pongblock.rect.left < 0:
        p2points += 1
        pongblock.reset()
    elif pongblock.rect.right > 500:
        p1points += 1
        pongblock.reset()

    player1points = font.render(f'{p1points}', False, white)
    player2points = font.render(f'{p2points}', False, white)
    window.blit(player1points, (115, 10))
    window.blit(player2points, (365, 10))

    all_sprites_list.draw(window)
    draw_dashed_line(window, white, (250, 0), (250, 500))

    player1block.User1_key_movement()
    player2block.User2_key_movement()

    pongblock.physics(player1block)
    pongblock.physics(player2block)

    pygame.display.update()

    
pygame.quit()

