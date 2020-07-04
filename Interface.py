#!/bin/bash

import pygame
from pygame.locals import *

class Interface():
    def __init__(self, timer = 100):
        self.speech_rect = ""

        self.timer = timer
        self.tick = 0

    def speak(self, rect, graphic):
        if self.tick < self.timer:
            self.tick += 1
            image = pygame.image.load('Resources/' + graphic)
            self.speech_rect = image.get_rect()
            if not self.speech_rect.topleft == (rect.topleft[0] + rect.size[0], rect.topleft[1]):
                self.speech_rect.topleft = (rect.topleft[0] + rect.size[0], rect.topleft[1])
            return image, self.speech_rect
        else:
            return 0, 0


