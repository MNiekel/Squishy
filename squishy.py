import pygame
import mysprite
import time
import levelsurface
import sys

from pygame.locals import *
from globals import *

STARTPOS = (400, 440)
ANIMATION_DELAY = 50

class Squishy(mysprite.MySprite):
    def __init__(self, image, screen, level):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.bottomleft = STARTPOS
        self.direction = LEFT
        self.level = level
        self.default = self.image #image of Squishy when he is standing still
        self.frame = 0
        self.delay = ANIMATION_DELAY
        self.current = [] #current animation
        self.animations = {}
        self.sounds = {}
        self.moving = False
        self.falling = False
        self.dead = False
        self.in_animation = False

    def printme(self):
        print self.image
        print self.rect

    def set_animations(self, img_list, label):
        self.animations[label] = img_list

    def set_sounds(self, sound, label):
        self.sounds[label] = sound

    def reset(self):
        self.image = self.default
        self.rect = self.image.get_rect()
        self.rect.bottomleft = STARTPOS
        self.frame = 0
        self.moving = False
        self.falling = False
        self.dead = False
        self.in_animation = False

    def get_x(self):
        if self.in_animation and not self.falling:
            rect = self.image.get_bounding_rect()
            return self.rect.left + (rect.centerx / SIZE) * SIZE
        return self.rect.left

    def check_killed(self, rect):
        if self.dead:
            return True
        if self.in_animation:
            self.set_current_animation(SQUISHED)
            self.rect.left = rect.left
            self.rect.top = (rect.bottom / SIZE) * SIZE
        else:
            self.set_current_animation(SQUISHED)
        self.dead = True
        self.sounds[SQUISHED_SND].play()
        self.last_update = pygame.time.get_ticks()

        return True

    def set_current_animation(self, dir):
        self.direction = dir
        self.in_animation = True
        self.frame = 0
        self.current = self.animations[dir]
        self.image = self.current[self.frame]
        if dir == LEFT:
            bottomright = self.rect.bottomright
            self.rect = self.image.get_rect()
            self.rect.bottomright = bottomright
        elif dir == RIGHT:
            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft
        elif dir == JUMP_LEFT:
            bottomright = self.rect.bottomright
            self.rect = self.image.get_rect()
            self.rect.bottomright = bottomright
        elif dir == JUMP_RIGHT:
            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft

    def move(self, key, lvl):
        if self.in_animation or self.falling or self.dead:
            return
        x = self.rect.left / SIZE
        y = (self.level.get_height() - self.rect.bottom) / SIZE
        if key == K_LEFT:
            if (self.level.check_obstacle(x - 1, y) == 0) or \
                (self.level.check_obstacle(x - 1, y) == BUTTON):
                self.set_current_animation(LEFT)
            elif (self.level.check_obstacle(x - 1, y + 1) == 0) or \
                (self.level.check_obstacle(x - 1, y + 1) == BUTTON):
                self.set_current_animation(JUMP_LEFT)
        if key == K_RIGHT:
            if (self.level.check_obstacle(x + 1, y) == 0) or \
                (self.level.check_obstacle(x + 1, y) == BUTTON):
                self.set_current_animation(RIGHT)
            elif (self.level.check_obstacle(x + 1, y + 1) == 0) or \
                (self.level.check_obstacle(x + 1, y + 1) == BUTTON):
                self.set_current_animation(JUMP_RIGHT)

        if self.in_animation:
            self.sounds[MOVE_SND].play()
        self.last_update = pygame.time.get_ticks()

    def reset_image(self, dir):
        self.image = self.default
        self.mask = pygame.mask.from_surface(self.image)
        self.in_animation = False
        if dir == LEFT:
            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft
        elif dir == RIGHT:
            bottomright = self.rect.bottomright
            self.rect = self.image.get_rect()
            self.rect.bottomright = bottomright
        if dir == JUMP_LEFT:
            topleft = self.rect.topleft
            self.rect = self.image.get_rect()
            self.rect.topleft = topleft
        elif dir == JUMP_RIGHT:
            topright = self.rect.topright
            self.rect = self.image.get_rect()
            self.rect.topright = topright

        x = self.rect.left / SIZE
        y = (self.level.get_height() - self.rect.bottom) / SIZE
        if self.level.check_obstacle(x, y - 1) == 0:
            self.falling = True
            self.set_current_animation(FALLING)
            self.last_update = pygame.time.get_ticks()
        elif self.level.check_obstacle(x, y) == BUTTON:
            print "GEWONNEN!!!"
            self.sounds[BUTTON_SND].play()
            event = pygame.event.Event(RESTART)
            pygame.event.post(event)

    def update(self):
        time = pygame.time.get_ticks()
        if (self.dead and (time - self.last_update > self.delay)):
            self.frame = (self.frame + 1) % len(self.current)
            self.image = self.current[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update = time
            if self.frame == 0:
                self.kill()
                event = pygame.event.Event(RESTART)
                pygame.event.post(event)
        if (self.falling and (time - self.last_update > self.delay)):
            topright = self.rect.topright
            self.rect = self.image.get_rect()
            self.rect.topright = topright
            self.rect.top += SIZE / len(self.current)
            self.frame = (self.frame + 1) % len(self.current)
            self.image = self.current[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update = time
            if self.frame == 0:
                self.falling = False
                self.reset_image(self.direction)
        if (self.in_animation and (time - self.last_update > self.delay)):
            self.frame = (self.frame + 1) % len(self.current)
            self.image = self.current[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update = time
            if self.frame == 0:
                self.in_animation = False
                self.reset_image(self.direction)
