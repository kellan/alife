import sys, pygame
import random

class World:
    directions = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(1,-1),(-1,0)]

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.wood = [[False for i in range(width)] for j in range(height)]
        self.termites = []

    def init_wood(self, n):
        for i in range(n):
            (x,y) = self.random_point()
            self.set_wood(x,y,True)

    def init_termites(self, n):
        for i in range(n):
            (x,y) = self.random_point()

            t = Termite(x, y)
            self.termites.append(t)

    def random_point(self):
        x = random.randrange(self.width)
        y = random.randrange(self.height)

        return (x,y)

    def point_delta(self, p, direction):
        d_x,d_y = direction
        x = (p[0]+d_x) % self.width
        y = (p[1]+d_y) % self.height
        return (x, y)

    def set_wood(self,x,y,val):
        self.wood[y][x] = val

    def get_wood(self,x,y):
        return self.wood[y][x]

class Termite:
    directions = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(1,-1),(-1,0)]

    def __init__(self, x, y):
        self.facing = self.random_direction()
        self.x = x
        self.y = y
        self.carrying = False

    def random_direction(self):
        return random.choice(self.directions)

class Game:
    def __init__(self, width, height):
        self.block_size = 10
        self.width = width
        self.height = height

        self.color_bg = [0, 0, 0]
        self.color_wood = [255,0,0] # red
        self.color_termite = [200,200,0] # yellow

        self.world = World(self.height, self.width)        
        self.world.init_wood(50)
        self.world.init_termites(10)

    def paint_block(self, color, left, top):
        #Rect(left, top, width, height) -> Rect
        pygame.draw.rect(
            self.screen, 
            color, 
            (left*self.block_size, top*self.block_size, self.block_size, self.block_size))

    def termite_move(self, t):
        self.paint_block(self.color_bg, t.x, t.y) # erase

        # 10% chance, pick a new direction
        if (random.randrange(10) == 0):
            t.facing = t.random_direction()

        (x, y) = self.world.point_delta((t.x,t.y), t.facing)
        t.x = x
        t.y = y

        return t

    def paint_wood(self):
        for y in range(self.world.height):
            for x in range(self.world.width):
                if self.world.get_wood(x,y):
                    self.paint_block(self.color_wood, x, y)

    def paint_termites(self):
        for t in self.world.termites:
            self.paint_block(self.color_termite, t.x, t.y)

    def termites(self):
        return self.world.termites;

    def run(self):
        pygame.init()
        size = [self.width*self.block_size, self.height*self.block_size]
        self.screen = pygame.display.set_mode(size)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            for t in self.termites():
                self.termite_move(t)

            # paint background
            self.screen.fill(self.color_bg)

            self.paint_wood();
            self.paint_termites();

            pygame.display.flip()
            pygame.time.wait(50)


#termite = Game()
#termite.run()

if __name__ == "__main__":
    termite = Game(64,64)
    termite.run()
    
