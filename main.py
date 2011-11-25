import pygame
import sys
import time
import imagecontroller
import squishy
import level
import box
import random

from pygame.locals import *
from globals import *

pygame.init()
#pygame.key.set_repeat()
clock = pygame.time.Clock()


images = imagecontroller.ImageController()

#init screen
screen = pygame.display.set_mode(PANDORA)
background = images.get_bg("Background")
screen.blit(background, [0, 0])

#init level
level = level.Level(images, screen, background)
level.build_level(screen)
screen.blit(level, [0, 0])

#init squishy
player = squishy.Squishy(images.get("Lazarus_stand"), screen, level)
player.set_animations(images.get_animation("Left"), LEFT)
player.set_animations(images.get_animation("Right"), RIGHT)
player.set_animations(images.get_animation("Jump_Left"), JUMP_LEFT)
player.set_animations(images.get_animation("Jump_Right"), JUMP_RIGHT)
player.set_animations(images.get_animation("Falling"), FALLING)

#init spritelist
rendering = pygame.sprite.RenderUpdates()
rendering.add(player)
rendering.add(box.Box(images.get_box(CARD), level, CARD))

pygame.display.flip()

while True:
    clock.tick(100)

    for event in pygame.event.get():
        #game.evaluate_event(event)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == NEW_BOX:
            type = random.choice([CARD, WOOD, METAL, STONE])
            xpos = player.get_x()
            rendering.add(box.Box(images.get_box(type), level, type, xpos))
            print type

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_LEFT, K_RIGHT):
                player.move(event.key, level)

    #call sprite updates
    rendering.update()
    pygame.display.update(rendering.draw(screen))
    pygame.display.update()

    screen.blit(background, [0, 0])
    screen.blit(level, [0, 0])
