# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:30:33 2022

@author: Thomas Goldstein

Contains the logic for timing in a simulation and acts as a parent for various
physicsbodies.
"""
import time

class Simulation():
    def __init__(self):
        self.bodies = {}
        self.engines = {}
        self.time = time.time()
        self.totalTime = 0.0
        
    def timeInit(self):
        self.time = time.time()
        self.totalTime = 0.0
        
    def currentElapsedTime(self):
        return time.time()-self.time
    
    def advance(self):
        currentTime = time.time()
        elapsedTime = currentTime-self.time
        self.time = currentTime
        self.totalTime += elapsedTime
        for engine in self.engines.values():
            engine.advance(elapsedTime)