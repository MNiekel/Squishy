import pygame
from pygame.locals import *

NEW_BOX = USEREVENT + 1
RESTART = USEREVENT + 2

PANDORA = 800, 480

BLACK = 0, 0, 0
TRANSPARENT = 0, 255, 0

LEFT = 0
RIGHT = 1
JUMP_LEFT = 2
JUMP_RIGHT = 3
FALLING = 4
SQUISHED = 5

#types of blocks
WALL = -1
CARD = 1
WOOD = 2
METAL = 3
STONE = 4
