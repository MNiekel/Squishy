import pygame

from pygame.locals import *
from globals import *

class SoundController(object):
    def __init__(self):
        self.path = "Resources/"
        self.init_music("resources/Music.mp3")
        self.music = False
        self.pause = False

    def play_music(self):
        pygame.mixer.music.play(-1)
        self.music = True

    def init_music(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.4)

    def load_sound(self, filename):
        print "loading sound " + filename
        return pygame.mixer.Sound(self.path + filename + ".wav")

    def play_sound(self, snd_id):
        self.sounds[snd_id].play()

    def toggle_music(self):
        if self.music:
            if self.pause:
                pygame.mixer.music.unpause()
                self.pause = False
            else:
                pygame.mixer.music.pause()
                self.pause = True
