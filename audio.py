# import pyaudio
import numpy as np
import time
import pygame
import os

class audio:

    def __init__(self, song=None):
        pygame.init()
        pygame.mixer.init()
        if song is not None:
            folder = os.getcwd() + "\music\\"
            # sound = pygame.mixer.Sound(folder + song + '.mp3')
            # sound.set_volume(.3)
            pygame.mixer.music.load(folder + song + '.mp3')
            pygame.mixer.music.set_volume(.4)
            pygame.mixer.music.play()

