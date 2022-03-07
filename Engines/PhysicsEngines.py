# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:45:28 2022

@author: Thomas Goldstein

Has various physics engines - gravity for example.
"""

import numpy
#import scypy
from Physics import gravitationalForce as gf
import Physics

DEBUG = False

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
    and that not all bodies must belong to all engines means that having a central
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
                    forces[j,i] = -1*forces[i,j] # could do this all at once after loops by subtracting a numpy transpose
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
            
class CoulombEngineEulerVectorized():
    """A physics engine that computes the Coulomb force between charges particles.
    Uses Euler integration (bad) for simplicity.
    
    For computing the forces this version uses a vectorized format of the positions,
    masses, charges, etc in order to do the computation with numpy broadcast 
    operations. This moves the calculations from a python loop to C and is much
    faster despite the fact that its >double doing all the calculations: the matrices
    are all anti-symmetric so something really optimized would only do the calculations
    on the upper diagonal.
    """
    def __init__(self):
        self.bodies = []
        self.components = {}
        
    def register(self,body,component):
        self.bodies.append(body)
        self.components[body.ID] = component
        
    def deregister(self,body,component):
        del self.components[body.ID]
        self.bodies.remove(body)
        
    def advance (self,timeStep):
        #build various arrays - in an optimized setup they would be stored like this
        #needing to call zip is annoying compared to just doing a loop but I'm
        #pretty certain the speed increase from list comprehensions makes up for it
        bodyCount = len(self.bodies)
        (posArray,massArray,chargeArray) = zip([(numpy.array(body.pos),body.mass,self.components[body.ID].charge)
                                               for body in self.bodies])
        
        posArray = numpy.array(posArray) #shape n,3
        massArray=numpy.array(massArray) #shape n
        chargeArray=numpy.array(chargeArray) #shape n

        posDiffArray = posArray.reshape((-1,1,3)) - posArray.reshape((1,-1,3)) #shape n,n,3
        distanceArray = numpy.linalg.norm(posDiffArray,axis=2) #shape n,n
        numpy.expand_dims(distanceArray, axis=2)# shape n,n,1 for proper operations later
        # note diagonals are 0, need to address those in the bulk calculation
        distanceArray[distanceArray==0] = 1.0
        
        #note: shape set for proper multiplication with posDiffArray
        qqArray = chargeArray.reshape(-1,1,1)*chargeArray.reshape(1,-1,1) #shape n,n,1
        
        #F = (kqq/r**2)*r^
        forceArray = Physics.K*qqArray/(distanceArray**3)*posDiffArray #shape n,n,3
        forces = numpy.sum(forceArray,axis=1) #shape n,3
        #note: to bulk calculate accelerations, divide by a reshaped mass array,
        #but I'm storing momentum rather than velocity in physics bodies
        
        #do integration
        for i in range(bodyCount):
            self.bodies[i].mom += forces[i]*timeStep
            self.bodies[i].pos += self.bodies[i].mom/self.bodies[i].mass*timeStep