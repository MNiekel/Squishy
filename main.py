import pygame
import sys
import time
import imagecontroller
import soundcontroller
import squishy
import levelsurface
import box
import random

from pygame.locals import *
from globals import *
from levels import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

images = imagecontroller.ImageController()
sounds = soundcontroller.SoundController()
box_hit_bottom_snd = sounds.load_sound("Wall")

#init screen
screen = pygame.display.set_mode(PANDORA)
background = images.get_bg("Background")
title = images.get_title("Title")
screen.blit(background, [0, 0])

#init level
level_num = 0
old_level = lvls[level_num]
level = levelsurface.LevelSurface(images, screen, background, lvls[level_num])
level.build_level("level00")
screen.blit(level, [0, 0])

#init squishy
player = squishy.Squishy(images.get("Lazarus_stand"), screen, level)
player.set_animations(images.get_animation("Left"), LEFT)
player.set_animations(images.get_animation("Right"), RIGHT)
player.set_animations(images.get_animation("Jump_Left"), JUMP_LEFT)
player.set_animations(images.get_animation("Jump_Right"), JUMP_RIGHT)
player.set_animations(images.get_animation("Falling"), FALLING)
player.set_animations(images.get_animation("Squished"), SQUISHED)

player.set_sounds(sounds.load_sound("Button"), BUTTON_SND)
player.set_sounds(sounds.load_sound("Crush"), CRUSH_SND)
player.set_sounds(sounds.load_sound("Move"), MOVE_SND)
player.set_sounds(sounds.load_sound("Squished"), SQUISHED_SND)

#init spritelist
rendering = pygame.sprite.RenderUpdates()
falling_box = pygame.sprite.RenderUpdates()
rendering.add(player)
next = random.choice([CARD, WOOD, METAL, STONE])
falling_box.add(box.Box(images.get_box(next), level, next, player.get_x()))
next = random.choice([CARD, WOOD, METAL, STONE])
level.show_next_box(next)

screen.blit(title, [0, 0])
pygame.display.flip()
sounds.play_music()

dead = False
press_space = False

player.printme()
print player

while not press_space:
    event = pygame.event.poll()
    if (event.type == KEYUP and event.key == K_SPACE):
        press_space = True
        pygame.event.clear()
    if (event.type == KEYDOWN and event.key == K_ESCAPE):
        sys.exit()
    if (event.type == pygame.QUIT):
        sys.exit()

while True:
    clock.tick(100)

    for event in pygame.event.get():
        #game.evaluate_event(event)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == NEW_BOX:
            box_hit_bottom_snd.play()
            xpos = player.get_x()
            falling_box.add(box.Box(images.get_box(next), level, next, xpos))
            next = random.choice([CARD, WOOD, METAL, STONE])
            level.show_next_box(next)

        elif event.type == RESTART:
            player.reset()
            rendering.add(player)
            falling_box.empty()
            level_num += 1
            level.set_level(lvls[level_num])
            level.clear_all_obstacles()
            level.build_level()
            player.printme()
            print player
            next = random.choice([CARD, WOOD, METAL, STONE])
            xpos = player.get_x()
            falling_box.add(box.Box(images.get_box(next), level, next, xpos))
            next = random.choice([CARD, WOOD, METAL, STONE])
            level.show_next_box(next)
            pygame.time.wait(2000)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key in (K_LEFT, K_RIGHT):
                player.move(event.key, level)

    #call sprite updates
    rendering.update()
    falling_box.update()
    pygame.display.update(rendering.draw(screen))
    pygame.display.update(falling_box.draw(screen))
    pygame.display.update()

    screen.blit(background, [0, 0])
    screen.blit(level, [0, 0])

    #check collision
    check = pygame.sprite.spritecollide(player, falling_box, False, pygame.sprite.collide_mask)
    if check:
        dead = player.check_killed(check[0].rect)
