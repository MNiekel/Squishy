import pygame
import mysprite
import levelsurface

from globals import *
from pygame.locals import *

class Box(mysprite.MySprite):
    def __init__(self, image, level, type, xpos = 400):
        mysprite.MySprite.__init__(self, image, level)

        self.type = type
        self.rect.bottomleft = (xpos, 0)

    def update(self):
        self.rect.bottom += 2
        x = self.rect.left / SIZE
        y = (self.screen.get_height() - self.rect.bottom) / SIZE
        if not (self.screen.check_obstacle(x, y) == 0):
            type = self.screen.get_type(x, y)
            if (type >= self.type or type < 0):
                self.screen.set_obstacle(x, y+1, self.type)
                self.kill()
                event = pygame.event.Event(NEW_BOX)
                pygame.event.post(event)
            else:
                self.screen.remove_obstacle(x, y)
