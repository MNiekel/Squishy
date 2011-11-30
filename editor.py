import pygame
import mysprite
import imagecontroller
import time
import sys

from pygame.locals import *
from globals import *

#types of level images
_BUTTON = 'O'
_WALL = 'W'
_SQUISHY = 'S'
PATH = 'levels/'

COLS = 20
ROWS = 12

def tostring(num):
    file = open(PATH + 'level' + str(num), 'w')
    file.write('\n'.join([''.join(row) for row in matrix]))
    file.write('\n')
    file.close()

num = int(raw_input('Please enter level number (0-1000): '))
while (num < 0 or num > 1000):
    num = int(raw_input('Incorrect number, please try again: '))

pygame.init()
clock = pygame.time.Clock()

image_loader = imagecontroller.ImageController()

screen = pygame.display.set_mode((840, 480))
background = image_loader.get_bg("Background")
wall = image_loader.get_box(WALL)
button = image_loader.get_box(BUTTON)
squishy = image_loader.get("Stand")

matrix = [[' ' for i in range(COLS)] for j in range(ROWS)]
cursor = (wall, _WALL)

screen.blit(wall, [0, 0])
screen.blit(button, [0, SIZE])
screen.blit(squishy, [0, 2*SIZE])
screen.blit(background, [SIZE, 0])

pygame.display.flip()

while True:
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                tostring(num)
                sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            print event.button
            print pygame.mouse.get_pos()
            if event.button == 1:
                (x, y) = pygame.mouse.get_pos()
                x = (x / SIZE) * SIZE - SIZE
                y = (y / SIZE) * SIZE
                if x < 0:
                    if (y >= 0) and (y < SIZE):
                        cursor = (wall, _WALL)
                    elif (y >= SIZE) and (y < 2*SIZE):
                        cursor = (button, _BUTTON)
                    elif (y >= 2*SIZE) and (y < 3*SIZE):
                        cursor = (squishy, _SQUISHY)
                else:
                    grid_x = x / SIZE
                    grid_y = y / SIZE
                    print "pos = ", x, y
                    print "grid = ", grid_x, grid_y
                    matrix[grid_y][grid_x] = cursor[1]
                    background.blit(cursor[0], [x, y])
                    screen.blit(background, [SIZE, 0])
                    pygame.display.flip()

    (x, y) = pygame.mouse.get_pos()
    x = (x / SIZE) * SIZE - SIZE
    y = (y / SIZE) * SIZE
    if (x >= 0):
        screen.blit(background, [SIZE, 0])
        screen.blit(cursor[0], [x + SIZE, y])
        pygame.display.flip()
