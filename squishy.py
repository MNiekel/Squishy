import pygame
import mysprite
import time
import level

from pygame.locals import *
from globals import *

STARTPOS = (720, 320)
MAXLIVES = 3
STEP = 23

class Squishy(mysprite.MySprite):
    def __init__(self, image, screen, level):
        mysprite.MySprite.__init__(self, image, screen)

        self.rect.bottomleft = STARTPOS
        self.step = STEP
        self.lives = MAXLIVES
        self.direction = LEFT
        self.level = level
        self.moving = False
        self.default_img = self.image
        self.frame = 0
        self.delay = 40
        self.current = []
        self.in_animation = False
        self.animations = {}
        self.falling = False
        self.dead = False

    def set_animations(self, img_list, label):
        self.animations[label] = img_list

    def reset(self):
        self.rect.bottomleft = STARTPOS
        self.lives = MAXLIVES

    def get_x(self):
        if self.in_animation and not self.falling:
            rect = self.image.get_bounding_rect()
            return self.rect.left + (rect.centerx / 40) * 40
        return self.rect.left

    def check_killed(self):
        if self.in_animation:
            return
            rect = self.image.get_bounding_rect()
            x = self.rect.left + (rect.centerx / 40) * 40
            y = self.rect.bottom + (rect.centery / 40) * 40
        self.dead = True
        self.set_current_animation(SQUISHED)
        self.last_update = pygame.time.get_ticks()

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
            print bottomright
            self.rect = self.image.get_rect()
            self.rect.bottomright = bottomright
        elif dir == JUMP_RIGHT:
            bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = bottomleft

    def move(self, key, level):
        if self.in_animation or self.falling or self.dead:
            return
        x = self.rect.left / 40
        y = (level.get_height() - self.rect.bottom) / 40
        if key == K_LEFT:
            if level.check_obstacle(x - 1, y) == 0:
                self.set_current_animation(LEFT)
            elif level.check_obstacle(x - 1, y + 1) == 0:
                self.set_current_animation(JUMP_LEFT)
        if key == K_RIGHT:
            if level.check_obstacle(x + 1, y) == 0:
                self.set_current_animation(RIGHT)
            elif level.check_obstacle(x + 1, y + 1) == 0:
                self.set_current_animation(JUMP_RIGHT)

        self.last_update = pygame.time.get_ticks()

    def reset_image(self, dir):
        self.image = self.default_img
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

        x = self.rect.left / 40
        y = (self.level.get_height() - self.rect.bottom) / 40
        if self.level.check_obstacle(x, y - 1) == 0:
            self.falling = True
            self.set_current_animation(FALLING)
            self.last_update = pygame.time.get_ticks()

    def update(self):
        time = pygame.time.get_ticks()
        if (self.dead and (time - self.last_update > self.delay)):
            self.frame = (self.frame + 1) % len(self.current)
            self.image = self.current[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            print self.frame
            self.last_update = time
            if self.frame == 0:
                self.kill()
                event = pygame.event.Event(RESTART)
                pygame.event.post(event)
        if (self.falling and (time - self.last_update > self.delay)):
            topright = self.rect.topright
            self.rect = self.image.get_rect()
            self.rect.topright = topright
            self.rect.top += 40 / len(self.current)
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
