import pygame
from pygame.locals import *

NEW_BOX = USEREVENT + 1
RESTART = USEREVENT + 2

PANDORA = 800, 480
SIZE = 40 #width and height of level raster and boxes

BLACK = 0, 0, 0
TRANSPARENT = 0, 255, 0

#animation IDs
LEFT = 0
RIGHT = 1
JUMP_LEFT = 2
JUMP_RIGHT = 3
FALLING = 4
SQUISHED = 5

#types of blocks\level images
BUTTON = -2
WALL = -1
CARD = 1
WOOD = 2
METAL = 3
STONE = 4

#sound IDs
BUTTON_SND = 0
CRUSH_SND = 1
MOVE_SND = 2
SQUISHED_SND = 3
WALL_SND = 4
