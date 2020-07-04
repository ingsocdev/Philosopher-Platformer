#!/bin/bash

import os, sys, pygame
from pygame.locals import *

import copy

class WeatherEngine():
    def __init__(self, engine, weather_type =  None):
        print 'Instantiaged Weather Engine'
        self.Engine = engine

        self.weather_type = weather_type
        self.interval = 20

        self.WeatherTimer = copy.copy(self.Engine.Timer)

        if self.weather_type == None:
            self.weather_type = self.randomize_weather()
            self.WeatherTimer.start()
        
        self.rain_color =  (3, 174, 237)
        self.Rain_Drops = []
        self.Clouds = []

        self.draw_amount_x = 0

        if self.weather_type == 'RAIN':
            self.draw_amount_x = self.Engine.Screen.get_rect()[2]/30
        elif self.weather_type == 'CLOUDY':
            self.draw_amount_x = self.Engine.Screen.get_rect()[2]/100

    def randomize_weather(self):
        SECONDS = 60
        weather_type = ''
        rand = self.Engine.return_random(1,2)
        if rand == 1:
            weather_type = 'RAIN'
            self.draw_amount_x = self.Engine.Screen.get_rect()[2]/30
        elif rand == 2:
            weather_type = 'CLOUDY'
            self.draw_amount_x = self.Engine.Screen.get_rect()[2]/100
            
        self.WeatherTimer.set_seconds(SECONDS * self.Engine.return_random(1,1))
        print str((self.WeatherTimer.SECONDS / self.Engine.FPS) / 60) + ' minutes of ' + weather_type

        return weather_type

    def update(self):
        if self.WeatherTimer.STATE == 'STOP':
            self.weather_type = self.randomize_weather()
            self.WeatherTimer.start()
        else:
            self.WeatherTimer.update()
            if self.weather_type == 'RAIN':
                self.rain()
            elif self.weather_type == 'CLOUDY':
                self.cloudy()

    def rain(self):
        for i in self.Rain_Drops[:]:
            if i.x >= 273:
                self.Rain_Drops.remove(i)
            else:
                pygame.draw.rect(self.Engine.Screen, self.rain_color, [i.y, i.x, 2, 5], 0)

        if self.interval < 30:
            self.interval += 1
            for item in list(self.Rain_Drops):
                item.update()
        else:
            self.interval = 0
            for i in range(self.draw_amount_x):
                x = RainDrop(-30, i*30, self.Engine)
                self.Rain_Drops.append(x)

    def cloudy(self):
        for i in self.Clouds[:]:
            if i.x >= self.Engine.Screen.get_rect()[2]:
                x = i
                x.x = 0
                self.Clouds.insert(0, x)
                self.Clouds.remove(i)
                
            else:
                self.Engine.draw(i.image, [i.x, i.y])
                i.update()
        if len(self.Clouds) == 0:
            for i in range(self.draw_amount_x):
                x = Cloud(i*self.Engine.Screen.get_rect()[2]/self.draw_amount_x, 20, self.Engine)
                self.Clouds.append(x)
                x = Cloud(i*self.Engine.Screen.get_rect()[2]/self.draw_amount_x, 60, self.Engine)
                self.Clouds.append(x)        
        
                
class RainDrop():
    def __init__(self, x, y, engine):
        self.Engine = engine
        self.x = x
        self.y = y
        self.x_variation = self.Engine.return_random(0,2)
    def update(self):
        self.x += 1 + self.x_variation


class Cloud():
    def __init__(self, x, y, engine):
        self.Engine = engine
        self.image = self.Engine.load_image('Resources/cloud.png')[0]
        self.x = x
        self.y_variation = self.Engine.return_random(-2,2)
        self.y = y + self.y_variation
        self.x_variation = self.Engine.return_random(0, 10) * 0.1
    def update(self):
        self.x += 0.3 + self.x_variation
        
        
