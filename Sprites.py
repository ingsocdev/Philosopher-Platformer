#!/bin/bash

import os, sys, pygame
import Engine

import copy

from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, engine):
        pygame.sprite.Sprite.__init__(self)
        self.Engine = engine
        self.AnimationEngine = self.Engine.AnimationEngine

        # Set up player attributes
        self.state = 'STANDING'
        self.health = 5
        self.immunity_window = 0
        self.speed = 5
        self.is_dead = False
        self.sound_played = False
        self.walk_toggle = 0
        self.DIRECTION = 'RIGHT'

        # Player Images
        self.image, self.rect = self.Engine.load_image('Resources/NietzscheStandingRight.png')
        self.heart, self.heart_rect = self.Engine.load_image('Resources/Heart.png')
        self.right_walking_array = 'Resources/PlayerRightWalk1.png','Resources/PlayerRightWalk2.png'
        self.left_walking_array = 'Resources/PlayerLeftWalk1.png','Resources/PlayerLeftWalk2.png'
        self.standing_right = self.Engine.load_image('Resources/NietzscheStandingRight.png')[0]
        self.standing_left = self.Engine.load_image('Resources/NietzscheStandingLeft.png')[0]

        # Set x/y values via constructor
        self.xpos = x
        self.ypos = y
        self.rect.topleft = self.xpos, self.ypos

        # Define Physics properties
        self.gravity = 1
        self.velocity = 12

        self.Attacks = []
        self.AttackTimer = copy.copy(self.Engine.Timer)
        self.AttackTimer.set_seconds(0.5)

    def update(self):
        if self.is_dead == False:
            SECOND = self.Engine.FPS
            
            # Check for collisions, if hit by enemy player is immune for 1 second
            if self.Engine.check_collision_type(self.rect) == "ENEMY" and self.health > 0 and self.immunity_window == 0:
                self.health -= 1
                self.immunity_window += 1
            elif not self.immunity_window == 0:
                self.immunity_window += 1
            if self.immunity_window >= SECOND:
                self.immunity_window = 0

            # If player is dead play the Death.wav sound
            if self.health < 1:
                self.is_dead = True
                if self.sound_played == False:
                    self.Engine.play_sound('Resources/Sounds/Death.wav')
                    self.sound_played = True
                    
            # Draw the player's health to the display
            for i in range(self.health):
                self.heart_rect.topleft = (i * 25 + 10,10)
                self.Engine.draw(self.heart, self.heart_rect)
            
            # This is to reset the player sprite to its
            # left/right image if not moving
            if self.walk_toggle == 0:
                self.image = self.standing_right
            else:
                self.image = self.standing_left
              
            if self.is_dead == False:
                self.walk()
                
            bubble, bubblerect = self.Engine.Interface.speak(self.rect, 'victorybubble.png')
            if bubble != 0:
                self.Engine.draw(bubble, bubblerect)
        else:
            # Send sprite vertically off screen (death animation)
            # Stop moving when sprite is no longer visible
            if not self.rect.topleft[1] < -60:
                new_position = self.rect.move((0, -10))
                self.rect = new_position

    def walk(self):
        new_position = self.rect.move((self.speed, 0))
        keys = pygame.key.get_pressed()
        # Check for keyboard input to move the sprite
        if keys[K_RIGHT] or keys[K_d]:
            self.walk_toggle = 0
            self.AnimationEngine.load_images(self.right_walking_array)
            self.image = self.Engine.load_image(self.AnimationEngine.switch_sprite_image())[0]
            #self.rect = new_position
            self.DIRECTION = 'RIGHT'
            self.rect = new_position

        if keys[K_LEFT] or keys[K_a]:
            self.walk_toggle = 1
            new_position = self.rect.move((self.speed - 10, 0))
            self.AnimationEngine.load_images(self.left_walking_array)
            self.image = self.Engine.load_image(self.AnimationEngine.switch_sprite_image())[0]
            self.rect = new_position
            self.DIRECTION = 'LEFT'

        if keys[K_UP] or keys[K_w]:
            self.state = 'JUMPING'

        if keys[K_SPACE] and self.AttackTimer.STATE == 'STOP':
            print 'space pressed'
            self.Attacks.append(Attack(self))
            self.AttackTimer.start()
        elif self.AttackTimer.STATE == 'START':
            self.AttackTimer.update()
        
        for i in self.Attacks[:]:
            if i.update() == 1:
                self.Attacks.remove(i)
           
        if self.state == 'JUMPING':
            self.jump()

    def jump(self):
        if self.gravity < (self.velocity * 2):
            new_position = self.rect.move((0, self.gravity - self.velocity))
            self.gravity += 1
            self.rect = new_position
        else:
            self.velocity = 12
            self.gravity = 1
            self.state = 'STANDING'

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, engine):
        pygame.sprite.Sprite.__init__(self)
        self.Engine = engine

        # Enemy Images
        self.image, self.rect = self.Engine.load_image('Resources/Lizard.png')
        self.win_image = self.Engine.load_image('Resources/LizardWin.png')[0]

        # Enemy Attributes
        self.health = 3
        self.walk_frames = 0
        self.speed = 3
        self.direction = 'RIGHT'

        # Enemy coords
        self.xpos = x
        self.ypos = y
        self.bounds = (self.xpos - 50, self.xpos + 50)
        self.rect.topleft = self.xpos, self.ypos

    def update(self):
        self.enemy_win()
        if self.Engine.check_collision_type(self.rect) == '' or self.Engine.check_collision_type(self.rect) == 'ENEMY':
            self.move()

    def move(self):
        new_position = self.rect.move((0,0))
        if not self.rect.topleft[0] < self.bounds[0] and not self.rect.topleft[0] > self.bounds[1]:
            if self.direction == 'RIGHT':
                new_position = self.rect.move((self.speed, 0))
            elif self.direction == 'LEFT':
                new_position = self.rect.move((self.speed - (self.speed * 2), 0))
        else:
            if self.rect.topleft[0] <= self.bounds[0]:
                self.direction = 'RIGHT'
                new_position = self.rect.move((self.speed, 0))
            elif self.rect.topleft[0] >= self.bounds[1]: 
                self.direction = 'LEFT'
                new_position = self.rect.move((self.speed - (self.speed * 2), 0))
        self.rect = new_position

    def enemy_win(self):
        if self.Engine.Player.is_dead == True:
            bubble, bubblerect = self.Engine.Interface.speak(self.rect, 'victorybubble.png')
            if bubble != 0:
                self.Engine.draw(bubble, bubblerect)
            self.image = self.win_image


class Attack():
    def __init__(self, sender):
        self.x = sender.rect.topleft[0]
        self.y = sender.rect.topleft[1]
        self.DIRECTION = sender.DIRECTION
        self.Engine = sender.Engine
        self.image, self.rect = self.Engine.load_image('Resources/GlobeAttack.png')
        self.rect.topleft = self.x, self.y + (sender.rect.size[0] / 2)

    def update(self):
        if self.Engine.check_collision_type(self.rect) == 'ENEMY':
            print 'colided with enemy'
            return 1
        else:
            if self.DIRECTION == 'RIGHT':
                new_position = self.rect.move((20, 0))
            elif self.DIRECTION == 'LEFT':
                new_position = self.rect.move((-20, 0))
            self.rect = new_position

        if self.rect.topleft[0] > (self.Engine.Screen.get_rect().size[0] + self.rect.size[0]):
            return 1
        elif self.rect.topleft[0] < self.Engine.Screen.get_rect().size[0] - (self.Engine.Screen.get_rect().size[0] + self.rect.size[0]):
            return 1

        self.Engine.draw(self.image, self.rect)
        return 0
            
        
