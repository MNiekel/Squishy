import pygame
import os
import sys

from pygame.locals import *
from globals import *

COLS = 20
ROWS = 12

class LevelSurface(pygame.Surface):
    def __init__(self, background):
        pygame.Surface.__init__(self, background.get_size())
        self.convert()
        self.set_colorkey(TRANSPARENT)
        self.fill(TRANSPARENT)

        self.background = background

        self.path = "levels/"
        self.images = {}
        self.matrix = [[' ' for i in range(COLS)] for j in range(ROWS)]
        self.oldmatrix = [[0 for i in range(COLS)] for j in range(ROWS)]

    def initialize(self, img_control, level = 0):
        self.set_images(img_control)
        return self.build_level(level)

    def set_images(self, img_control):
        self.images[BUTTON] = img_control.get_box(BUTTON)
        self.images[WALL] = img_control.get_box(WALL)
        self.images[STONE] = img_control.get_box(STONE)
        self.images[CARD] = img_control.get_box(CARD)
        self.images[WOOD] = img_control.get_box(WOOD)
        self.images[METAL] = img_control.get_box(METAL)

    def read_level(self, filename):
        full = self.path + filename
        if not os.path.isfile(full):
            print "File does not exist: ", full
            sys.exit()
        file = open(self.path + filename, 'r')
        return file.readlines()

    def draw_level(self):
        rows = len(self.oldmatrix)
        for y in range(0, rows):
            row = self.oldmatrix[y]
            for x in range(0, len(row)):
                type = row[x]
                if not type == 0:
                    self.blit(self.images[type], [SIZE*x, SIZE*y])

    def build_level(self, level = 0):
        pos = None
        matrix = self.read_level("level" + str(level))
        self.oldmatrix = [[0 for i in range(COLS)] for j in range(ROWS)]
        for y in range(0, len(matrix)):
            row = matrix[y].rstrip() #haal spaties rechts en eol weg
            for x in range(0, len(row)):
                self.matrix[y][x] = row[x]
                if row[x] == 'W':
                    self.oldmatrix[y][x] = WALL
                elif row[x] == 'O':
                    self.oldmatrix[y][x] = BUTTON
                elif row[x] == ' ':
                    self.oldmatrix[y][x] = 0
                elif row[x] == 'S':
                    self.oldmatrix[y][x] = 0
                    pos = (SIZE * x, SIZE * y)
        self.draw_level()
        return pos

    def check_obstacle(self, x, y): #x, y in screen coordinates
        return self.oldmatrix[y/SIZE][x/SIZE]

    def get_type(self, x, y): #x, y in screen coordinates
        return self.oldmatrix[y/SIZE][x/SIZE]

    def show_next_box(self, type):
        self.oldmatrix[ROWS-1][0] = type
        rect = Rect(0, self.get_height() - SIZE, SIZE, SIZE)
        self.blit(self.images[type], rect)

    def set_obstacle(self, x, y, type): #x, y in screen coordinates
        x = x / SIZE
        y = y / SIZE
        if y < 0:
            return False
        self.oldmatrix[y][x] = type
        rect = Rect(SIZE*x, SIZE*y, SIZE, SIZE)
        self.blit(self.images[type], rect)
        return True

    def remove_obstacle(self, x, y): #x, y in screen coordinates
        x = x / SIZE
        y = y / SIZE
        self.oldmatrix[y][x] = 0
        rect = Rect(SIZE*x, SIZE*y, SIZE, SIZE)
        surf = self.background.subsurface(rect)
        self.blit(surf, rect)

    def clear_all_obstacles(self):
        self.blit(self.background, [0, 0])
