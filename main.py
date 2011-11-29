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

def wait_for_space():
    press_space = False

    while not press_space:
        event = pygame.event.poll()
        if (event.type == KEYUP and event.key == K_SPACE):
            press_space = True
            pygame.event.clear()
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        if (event.type == pygame.QUIT):
            sys.exit()

images = imagecontroller.ImageController()
sounds = soundcontroller.SoundController()

#init screen
screen = pygame.display.set_mode(PANDORA)
background = images.get_bg("Background")
title = images.get_title("Title")
title_won = images.get_title("Won")
title_lost = images.get_title("Lost")
title = images.get_title("Title")
screen.blit(background, [0, 0])

#init level
level = levelsurface.LevelSurface(background)
level_num = 0
pos = level.initialize(images, level_num)
screen.blit(level, [0, 0])

#init squishy
if pos:
    player = squishy.Squishy(images.get("Stand"), screen, level, pos)
else:
    player = squishy.Squishy(images.get("Stand"), screen, level)
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
rendering.add(player)
falling_box = pygame.sprite.RenderUpdates()
box_hit_bottom_snd = sounds.load_sound("Wall")
next = random.choice([CARD, WOOD, METAL, STONE])
falling_box.add(box.Box(images.get_box(next), level, next, player.get_x()))
next = random.choice([CARD, WOOD, METAL, STONE])
level.show_next_box(next)

screen.blit(title, [0, 0])
pygame.display.flip()
sounds.play_music()

wait_for_space()

dead = False

while True:
    clock.tick(100)

    for event in pygame.event.get():
        #game.evaluate_event(event)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == BOX_OUT_OF_SCREEN:
            dead = True
            event = pygame.event.Event(RESTART)
            pygame.event.post(event)

        elif event.type == NEW_BOX:
            box_hit_bottom_snd.play()
            xpos = player.get_x()
            falling_box.add(box.Box(images.get_box(next), level, next, xpos))
            next = random.choice([CARD, WOOD, METAL, STONE])
            level.show_next_box(next)

        elif event.type == RESTART:
            if not dead:
                level_num += 1
                screen.blit(title_won, [0, 0])
            else:
                screen.blit(title_lost, [0, 0])
            pygame.display.flip()
            wait_for_space()
            dead = False
            rendering.add(player)
            falling_box.empty()
            level.clear_all_obstacles()
            pos = level.build_level(level_num)
            if pos:
                player.reset(pos)
            else:
                player.reset()
            next = random.choice([CARD, WOOD, METAL, STONE])
            xpos = player.get_x()
            falling_box.add(box.Box(images.get_box(next), level, next, xpos))
            next = random.choice([CARD, WOOD, METAL, STONE])
            level.show_next_box(next)

        elif event.type == KEYDOWN:
            if event.key == K_n:
                event = pygame.event.Event(RESTART)
                pygame.event.post(event)
            elif event.key == K_ESCAPE:
                sys.exit()
            elif event.key in (K_LEFT, K_RIGHT):
                player.move(event.key)

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
