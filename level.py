import pygame

from pygame.locals import *
from globals import *

#level width = 20

level0 = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],\
            [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

class Level(pygame.Surface):
    def __init__(self, images, screen, bg):
        pygame.Surface.__init__(self, screen.get_size())
        self.convert()
        self.set_colorkey(TRANSPARENT)
        self.fill(TRANSPARENT)
        self.level = {}
        self.level = level0
        self.images = {}
        self.images[BUTTON] = images.get_box(BUTTON)
        self.images[WALL] = images.get_box(WALL)
        self.images[STONE] = images.get_box(STONE)
        self.images[CARD] = images.get_box(CARD)
        self.images[WOOD] = images.get_box(WOOD)
        self.images[METAL] = images.get_box(METAL)
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey(TRANSPARENT)
        self.image.fill(TRANSPARENT)
        self.screen = screen
        self.bg = bg

    def get_level(self):
        return self.level[0]

    def build_level(self, screen):
        lev = self.level
        for y in range(0, len(lev)):
            for x in range(0, len(lev[y])):
                type = lev[y][x]
                if not type == 0:
                    ypos = self.get_height() - 40
                    self.blit(self.images[type], [40*x, ypos - 40*y])

    def check_obstacle(self, x, y):
        return self.level[y][x]

    def get_type(self, x, y):
        return self.level[y][x]

    def set_obstacle(self, x, y, type):
        self.level[y][x] = type
        rect = Rect(40*x, self.get_height() - 40*(y+1), 40, 40)
        self.blit(self.images[type], rect)

    def remove_obstacle(self, x, y):
        print "removing obstacle"
        self.level[y][x] = 0
        rect = Rect(40*x, self.get_height() - 40*(y+1), 40, 40)
        surf = self.bg.subsurface(rect)
        self.blit(surf, rect)
