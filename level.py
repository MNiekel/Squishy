import pygame

from pygame.locals import *
from globals import *

class Level(pygame.Surface):
    def __init__(self, img_control, screen, background, level):
        pygame.Surface.__init__(self, screen.get_size())
        self.convert()
        self.set_colorkey(TRANSPARENT)
        self.fill(TRANSPARENT)
        self.level = level
        self.images = {}
        self.set_images(img_control)
        self.image = pygame.Surface((SIZE, SIZE)).convert()
        self.image.set_colorkey(TRANSPARENT)
        self.image.fill(TRANSPARENT)
        self.screen = screen
        self.background = background

    def set_images(self, img_control):
        self.images[BUTTON] = img_control.get_box(BUTTON)
        self.images[WALL] = img_control.get_box(WALL)
        self.images[STONE] = img_control.get_box(STONE)
        self.images[CARD] = img_control.get_box(CARD)
        self.images[WOOD] = img_control.get_box(WOOD)
        self.images[METAL] = img_control.get_box(METAL)

    def set_level(self, level):
        self.level = level

    def build_level(self):
        self.clear_all_obstacles()
        lev = self.level
        for y in range(0, len(lev)):
            for x in range(0, len(lev[y])):
                type = lev[y][x]
                if not type == 0:
                    ypos = self.get_height() - SIZE
                    self.blit(self.images[type], [SIZE*x, ypos - SIZE*y])

    def check_obstacle(self, x, y):
        return self.level[y][x]

    def get_type(self, x, y):
        return self.level[y][x]

    def show_next_box(self, type):
        self.level[0][0] = type
        rect = Rect(0, self.get_height() - SIZE, SIZE, SIZE)
        self.blit(self.images[type], rect)

    def set_obstacle(self, x, y, type):
        self.level[y][x] = type
        rect = Rect(SIZE*x, self.get_height() - SIZE*(y+1), SIZE, SIZE)
        self.blit(self.images[type], rect)

    def remove_obstacle(self, x, y):
        print "removing obstacle"
        self.level[y][x] = 0
        rect = Rect(SIZE*x, self.get_height() - SIZE*(y+1), SIZE, SIZE)
        surf = self.background.subsurface(rect)
        self.blit(surf, rect)

    def clear_all_obstacles(self):
        print "clearing level"
        self.blit(self.background, [0, 0])
