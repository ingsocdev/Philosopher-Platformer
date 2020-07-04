#!/bin/bash

import pygame
from pygame.locals import *

class Camera():
    def __init__(self, screen, player):
        self.Player = player
        self.Screen = screen
        self.image = pygame.image.load('Resources/Background.png')
        self.rect = ((-200, -150))

    def update(self):
        print str(self.rect)
        if self.Player.rect.topleft[0] > self.Screen.get_rect()[2] / 2:
            self.rect = ((-(self.Player.rect[0]), -150))
        self.Screen.blit(self.image, self.rect)
        
