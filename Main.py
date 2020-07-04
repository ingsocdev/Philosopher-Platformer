#!/bin/bash

import pygame, sys
import Sprites
import Engine

from pygame.locals import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400,300))
#background = pygame.Surface(screen.get_size())
#background = background.convert()
#background.fill((22,22,22))
pygame.display.set_caption("Zarathustra Hears Voices");

#screen.blit(background, (0,0))

BACKGROUNDSURF = pygame.display.set_mode((400,300),0,32)
#send the surface to the engine with FPS = 30
Engine = Engine.Engine(screen, 30)
Grass = Engine.load_image('Resources/GrassTerrain.png')

fps_clock = pygame.time.Clock()

while True:
    fps_clock.tick(Engine.FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    #screen.blit(background, (0,0))
    Engine.update()
    screen.blit(Grass[0], (0, 272))
    screen.blit(Grass[0],(59,272))
    screen.blit(Grass[0],(118,272))
    screen.blit(Grass[0],(177,272))
    screen.blit(Grass[0],(236,272))
    screen.blit(Grass[0],(295,272))
    screen.blit(Grass[0],(354,272))
    

    pygame.display.flip()
    
    
