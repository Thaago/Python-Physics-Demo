# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:45:28 2022

@author: Thomas Goldstein

Has various physics engines - gravity for example.
"""

import numpy
from Physics import gravitationalForce as gf

DEBUG = True

class GravityEngineEulerIntegrationElementwise():
    """A physics engine that computes the force of gravity on its bodies and
    then moves them according to Euler integration (large errors).
    
    bodies -> a list of attached bodies of length n
    
    The current implementation is an elementwise calculation
    which is known to be very slow compared to vector math, but it is explicit
    and easy (later confusing methods can be checked against it).
    
    See here: https://stackoverflow.com/questions/52562117/efficiently-compute-n-body-gravitation-in-python
    for better methods
    
    All of the fast methods makes use of a unified array of all calculations.
    
    allPos -> a numpy array (n,3) or positions used in calculations
    
    And does matrix/vector/blas functions on it. However, the possibility
    of an object having multiple physics engines attached (component based model)
    and that not all bodies belong to the all engines means that having a central
    master array of positions is not trivial. Maybe make an engine manager and have
    each engine operate on a filtered copy? Then the result is assigned back to
    the master? That would be faster than regenerating the array from objects
    each timestep.
    
    """
    def __init__(self):
        self.bodies = []
        
        #is a component! So it must have an engine (itself)
        self.engine = self
    
    def register(self,body,component):
        self.bodies.append(body)
        
    def deregister(self,body,component):
        self.bodies.remove(body)
        
    def advance(self,timeStep):
        if DEBUG: print("timestep: "+str(timeStep))
        #compute force array shape (n,3)
        bodyCount = len(self.bodies)
        
        forces = numpy.zeros((bodyCount,bodyCount,3))
        for i in range(bodyCount):
            for j in range(bodyCount):
                if i<j:#by using strict, diagonals remain 0
                    forces[i,j]= gf(self.bodies[i],self.bodies[j])
                    forces[j,i] = -1*forces[i,j]
        if DEBUG: print(forces)
        #apply forces to objects with integrator
        for i in range(bodyCount):
            #could be folded into above but for clarity seperate
            totalForce = numpy.sum(forces[i,:], axis=0)
            if DEBUG: print("force on body "+str(i)+" : "+str(totalForce))
            
            #actual Euler integration here:
            self.bodies[i].mom += totalForce*timeStep
            if DEBUG: print("momengum of body "+str(i)+" : "+str(self.bodies[i].mom))
            self.bodies[i].pos += self.bodies[i].mom/self.bodies[i].mass*timeStep
            if DEBUG: print("pos of body "+str(i)+" : "+str(self.bodies[i].pos))