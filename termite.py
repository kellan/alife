import sys, pygame
import random

pygame.init()

block_size = 10
width, height = 64, 64
size = [width*block_size, height*block_size]

color_bg = [0, 0, 0]
color_wood = [255,0,0] # red
color_termite = [200,200,0] # yellow

directions = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(1,-1),(-1,0)]

wood = []
termites = []

screen = pygame.display.set_mode(size)

def add_wood():
    # left, top
    point = [random.randrange(width), random.randrange(height)]
    wood.append(point)

def add_termite():
    # left, top, facing
    t = [random.randint(0, width), random.randrange(height), random.randrange(len(directions)), False]
    termites.append(t)

def termite_tick(t):
    paint_block(color_bg, block_size, t[0], t[1]) # erase
    t = termite_move(t)


    return t

def termite_move(t):
    if (random.randrange(10) == 0):
        t[2] = random.randrange(len(directions))

    (x, y) = point_delta(t, t[2])
    t[0] = x
    t[1] = y

    return t

def point_delta(p, facing):
    d_x,d_y = directions[facing]
    x = (p[0]+d_x) % width
    y = (p[1]+d_y) % height
    return (x, y)

def paint_wood():
    for w in wood:
        paint_block(color_wood, block_size, w[0], w[1])

def paint_termites():
    for t in termites:
        paint_block(color_termite, block_size, t[0], t[1])

def paint_block(color, block_size, left, top):
    #Rect(left, top, width, height) -> Rect
    pygame.draw.rect(screen, color, (left*block_size, top*block_size, block_size, block_size))

for i in range(50):
    add_wood()

for i in range(10):
    add_termite();

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for i,t in enumerate(termites):
        termite_tick(t)
        termites[i] = t

    # paint background
    screen.fill(color_bg)
    paint_wood()
    paint_termites()

    pygame.display.flip()
    pygame.time.wait(50)


