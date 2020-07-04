#!/bin/bash

class Timer():
    def __init__(self, FPS):
        self.FPS = FPS
        self.STATE = 'STOP'
        self.interval = 0
        self.SECONDS = 0
        
    def set_seconds(self, seconds):
        self.SECONDS = self.FPS * seconds

    def start(self):
        self.STATE = 'START'
        self.update()

    def stop(self):
        self.STATE = 'STOP'
        self.interval = 0

    def update(self):
        if self.STATE == 'START':
            if self.interval < self.SECONDS:
                self.interval += 1
            else:
                self.STATE = 'STOP'
                self.interval = 0
