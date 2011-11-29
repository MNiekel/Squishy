import pygame
import mysprite
import levelsurface

from globals import *
from pygame.locals import *

class Box(mysprite.MySprite):
    def __init__(self, image, level, type, xpos = 400):
        mysprite.MySprite.__init__(self, image, level)

        self.type = type
        self.rect.bottomleft = (xpos, -1)

    def update(self):
        old_y = self.rect.centery
        self.rect.bottom += 2
        x = self.rect.left
        y = self.rect.bottom
        type = self.screen.get_type(x, y)
        if not (type <= 0):
            if (type >= self.type):
                if not self.screen.set_obstacle(x, old_y, self.type):
                    event = pygame.event.Event(BOX_OUT_OF_SCREEN)
                else:
                    self.kill()
                    event = pygame.event.Event(NEW_BOX)
                pygame.event.post(event)
            else:
                self.screen.remove_obstacle(x, y)
