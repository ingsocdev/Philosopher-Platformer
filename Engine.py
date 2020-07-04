#!/bin/bash

import os, sys, random, pygame
from pygame.locals import *

import Sprites
import Interface
import AnimationEngine
import WeatherEngine
import Timer
import Camera

class Engine():
    def __init__(self, screen = None, FPS = 30):
        print 'Engine Initialized'
        self.FPS = FPS
        if screen is not None:
            self.Screen = screen

        self.Timer = Timer.Timer(FPS)
        self.AnimationEngine = AnimationEngine.AnimationEngine()
        self.WeatherEngine = WeatherEngine.WeatherEngine(self)
        self.Interface = Interface.Interface()
        self.Player = Sprites.Player(50,220, self)
        self.Enemy = Sprites.Enemy(screen.get_rect().topright[0] - 100, 228, self)
        self.Camera = Camera.Camera(self.Screen, self.Player)
        
    def update(self):
        self.Camera.update()
        self.WeatherEngine.update()
        sprites = pygame.sprite.RenderPlain((self.Player, self.Enemy))
        sprites.draw(self.Screen)
        sprites.update()
        
    def play_sound(self, filename):
        sound = pygame.mixer.Sound(filename)
        sound.play()

    def load_image(self, name, colorkey = None):
        try:
            image = pygame.image.load(name)
        except pygame.error, message:
                print 'Cannot load image: ', name
                raise SystemExit, message
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def check_collision(self, rect1, rect2):
        if rect1.topleft[0] + rect1.size[0] >= rect2.topleft[0] and rect1.topleft[0] < rect2.topleft[0] + rect2.size[0] and rect1.topleft[1] > rect2.topleft[1] - rect2.size[0]:
            return True
        else:
            return False

    def check_collision_type(self, rect):
        collisionType = ""
        if self.check_collision(rect, self.Enemy.rect) == True:
            collisionType = "ENEMY"
            return collisionType
        return collisionType

    def draw(self, image, rect):
        self.Screen.blit(image, rect)

    def return_random(self, n1, n2):
        return random.randint(n1, n2)




    
