import pygame
import mysprite
import level

from globals import *
from pygame.locals import *

class Box(mysprite.MySprite):
    def __init__(self, image, screen, type):
        mysprite.MySprite.__init__(self, image, screen)

        self.type = type
        self.rect.bottomleft = (400, 0)

    def update(self):
        self.rect.bottom += 2
        if self.rect.top > self.screen.get_height():
            print "BOEM"
            self.kill()
