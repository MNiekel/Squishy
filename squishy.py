import pygame
import mysprite
import time

from pygame.locals import *
from globals import *

STARTPOS = (380, 400)
MAXLIVES = 3
STEP = 23

class Squishy(mysprite.MySprite):
    def __init__(self, image, screen):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.topleft = STARTPOS
        self.step = STEP
        self.lives = MAXLIVES
        self.direction = LEFT
        self.moving = False
        self.restimage = self.image
        self.frame = 0
        self.delay = 100
        self.current = []
        self.in_animation = False
        #self.jumping = False
        #self.falling = False
        self.animations = {}

    def set_animations(self, img_list, label):
        self.animations[label] = img_list

    def reset(self):
        self.rect.topleft = STARTPOS
        self.lives = MAXLIVES

    def move(self, key):
        #check place next to you, if empty -> move, check if jumping possible
        print "moving"
        if key == K_LEFT:
            self.direction = LEFT
            self.current = self.animations[LEFT]
            self.in_animation = True
            self.frame = 0
            right = self.rect.right
            bottom = self.rect.bottom
            self.image = self.current[self.frame]
            self.rect = self.image.get_rect()
            self.rect.right = right
            self.rect.bottom = bottom
            self.start = pygame.time.get_ticks()
        if key == K_RIGHT:
            self.direction = RIGHT

    def update(self):
        time = pygame.time.get_ticks()
        if (self.in_animation and (time - self.start > self.delay)):
            self.frame = (self.frame + 1) % len(self.current)
            self.image = self.current[self.frame]
            self.start = time
            if self.frame == 0:
                print self.frame
                self.in_animation = False
                self.image = self.restimage
                bottomleft = self.rect.bottomleft
                self.rect = self.image.get_rect()
                self.rect.bottomleft = bottomleft
