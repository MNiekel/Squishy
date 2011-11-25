import pygame

from pygame.locals import *
from globals import *

#level width = 20

level0 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],\
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],\
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],\
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],\
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

class Level(pygame.Surface):
    def __init__(self, image, size):
        pygame.Surface.__init__(self, size)
        self.convert()
        self.set_colorkey(TRANSPARENT)
        self.fill(TRANSPARENT)
        self.level = {}
        self.level[0] = level0
        self.image = image

    def get_level(self):
        return self.level[0]

    def build_level(self, screen):
        lev = self.level[0]
        for y in range(0, len(lev)):
            for x in range(0, len(lev[y])):
                if lev[y][x] == 1:
                    ypos = self.get_height() - 40
                    self.blit(self.image, [40*x, ypos - 40*y])
                    print "blitting"

    def check_obstacle(self, x, y):
        return self.level[0][y][x]
