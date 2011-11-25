import pygame
import mysprite
import level

from globals import *
from pygame.locals import *

class Box(mysprite.MySprite):
    def __init__(self, image, level, type, xpos = 400):
        mysprite.MySprite.__init__(self, image, level)

        self.type = type
        self.rect.bottomleft = (xpos, 0)

    def update(self):
        self.rect.bottom += 1
        x = self.rect.left / 40
        y = (self.screen.get_height() - self.rect.bottom) / 40
        if not (self.screen.check_obstacle(x, y) == 0):
            type = self.screen.get_type(x, y)
            if (type >= self.type or type < 0):
                self.screen.set_obstacle(x, y+1, self.type)
                self.kill()
                event = pygame.event.Event(NEW_BOX)
                pygame.event.post(event)
            else:
                self.screen.remove_obstacle(x, y)
