import pygame

from pygame.locals import *
from globals import *

COLS = 20
ROWS = 12

class LevelSurface(pygame.Surface):
    def __init__(self, img_control, screen, background, level):
        pygame.Surface.__init__(self, screen.get_size())
        self.convert()
        self.set_colorkey(TRANSPARENT)
        self.fill(TRANSPARENT)

        self.path = "levels/"
        self.images = {}
        self.set_images(img_control)
        self.image = pygame.Surface((SIZE, SIZE)).convert()
        self.image.set_colorkey(TRANSPARENT)
        self.image.fill(TRANSPARENT)
        self.screen = screen
        self.background = background
        self.matrix = [[' ' for i in range(COLS)] for j in range(ROWS)]
        self.oldmatrix = [[0 for i in range(COLS)] for j in range(ROWS)]

    def set_images(self, img_control):
        self.images[BUTTON] = img_control.get_box(BUTTON)
        self.images[WALL] = img_control.get_box(WALL)
        self.images[STONE] = img_control.get_box(STONE)
        self.images[CARD] = img_control.get_box(CARD)
        self.images[WOOD] = img_control.get_box(WOOD)
        self.images[METAL] = img_control.get_box(METAL)

    def set_level(self, matrix):
        self.matrix = matrix

    def read_level(self, filename):
        file = open(self.path + filename, 'r')
        rows = []
        for line in file:
            rows.append(line)
        file.close()
        return rows

    def draw_level(self):
        rows = len(self.oldmatrix)
        for y in range(0, rows):
            row = self.oldmatrix[y]
            for x in range(0, len(row)):
                type = row[x]
                if not type == 0:
                    self.blit(self.images[type], [SIZE*x, SIZE*y])

    def build_level(self, filename):
        lvl = self.read_level(filename)
        for y in range(0, len(lvl)):
            row = lvl[y]
            for x in range(0, len(row)-1): #skip EOL
                self.matrix[y][x] = row[x]
                if row[x] == 'W':
                    self.oldmatrix[y][x] = WALL
                elif row[x] == 'O':
                    self.oldmatrix[y][x] = BUTTON
        self.draw_level()
        return
        if not type == 0:
            ypos = self.get_height() - SIZE
            self.blit(self.images[type], [SIZE*x, ypos - SIZE*y])

    def check_obstacle(self, x, y):
        return self.oldmatrix[y][x]

    def get_type(self, x, y):
        return self.oldmatrix[y][x]

    def show_next_box(self, type):
        self.oldmatrix[0][0] = type
        rect = Rect(0, self.get_height() - SIZE, SIZE, SIZE)
        self.blit(self.images[type], rect)

    def set_obstacle(self, x, y, type):
        self.oldmatrix[y][x] = type
        rect = Rect(SIZE*x, self.get_height() - SIZE*(y+1), SIZE, SIZE)
        self.blit(self.images[type], rect)

    def remove_obstacle(self, x, y):
        print "removing obstacle"
        self.oldmatrix[y][x] = 0
        rect = Rect(SIZE*x, self.get_height() - SIZE*(y+1), SIZE, SIZE)
        surf = self.background.subsurface(rect)
        self.blit(surf, rect)

    def clear_all_obstacles(self):
        print "clearing level"
        self.blit(self.background, [0, 0])
