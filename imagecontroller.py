import pygame
import os

from pygame.locals import *
from globals import *

class ImageController(object):
    def __init__(self):
        self.path = "resources/"
        self.images = {}
        self.animations = {}

    def get(self, filename):
        if self.images.has_key(filename):
            return self.images[filename]
        else:
            print "loading image " + filename
            img = pygame.image.load(self.path + filename + ".gif").convert()
            img.set_colorkey(TRANSPARENT)
            self.images[filename] = img
            return img

    def get_box(self, type):
        if type == CARD:
            return self.get("CardBox")
        if type == WOOD:
            return self.get("WoodBox")
        if type == METAL:
            return self.get("MetalBox")
        if type == STONE:
            return self.get("StoneBox")
        if type == WALL:
            return self.get("Wall")

    def get_bg(self, filename):
        return pygame.image.load(self.path + filename + ".bmp").convert()

    def get_animation(self, filename):
        img_list = []
        i = 0
        full = self.path + filename + str(i) + ".png"
        while os.path.exists(full):
            img = pygame.image.load(full).convert()
            img.set_colorkey(TRANSPARENT)
            img_list.append(img)
            i += 1
            full = self.path + filename + str(i) + ".png"
        
        return img_list
