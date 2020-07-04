#!/bin/bash

import pygame
from pygame.locals import *

class AnimationEngine():
    def __init__(self):
        print 'Instantiated Animation Engine'
        self.selected_index = 0
        self.interval = 0

    def load_images(self, image_list):
        self.intervalmage_list = image_list

    def switch_sprite_image(self):
    
        if self.interval == 5 * (self.selected_index + 1):
            if self.selected_index < len(self.intervalmage_list):
                self.selected_index += 1   
            if self.selected_index == len(self.intervalmage_list):
                self.interval = 0
                self.selected_index = 0
            return self.intervalmage_list[self.selected_index - 1]
        else:
            self.interval += 1
            return self.intervalmage_list[self.selected_index - 1]
