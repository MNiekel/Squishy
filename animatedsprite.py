import pygame

from pygame.locals import *

class AnimatedSprite(mysprite.MySprite):
    def __init__(self, image, screen):
        mysprite.MySprite.__init__(self, image, screen)
            self.animations = {}
            self.current = []

    def init_animation(self, img_list, label):
        self.animation[label] = img_list

    def set_current(self, label):
        self.current = self.animation[label]
