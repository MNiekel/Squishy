import pygame
import sys
import time
import imagecontroller
import squishy

from pygame.locals import *
from globals import *

pygame.init()
pygame.key.set_repeat(1)
clock = pygame.time.Clock()

screen = pygame.display.set_mode(PANDORA)

images = imagecontroller.ImageController()

background = images.get_bg("Background")
screen.blit(background, [0, 0])
rendering = pygame.sprite.RenderUpdates()
player = squishy.Squishy(images.get("Lazarus_stand"), screen)
player.set_animations(images.get_animation("Left"), LEFT)
rendering.add(player)
pygame.display.flip()
#sys.exit()

while True:
    clock.tick(80)

    for event in pygame.event.get():
        #game.evaluate_event(event)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_LEFT, K_RIGHT):
                player.move(event.key)

    #call sprite updates
    rendering.update()
    pygame.display.update(rendering.draw(screen))
    pygame.display.update()

    screen.blit(background, [0, 0])
