# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 10:52:23 2022

@author: Thomas Goldstein

The basic root of everything that interacts with the physic simulation.
Can then add components that enable gravity, collisions, etc.

Note that control of components is HERE: as an example, add and remove physics
engines to the body using this class' methods, not directly acting on the 
engine's list of bodies.

Root data is also stored here: pos/mom/mass/visuals
This is a downside for physics optimization.

To add functionality, make an engine in the main program and then add its 
associated component here, which could just be the engine itself if no further 
data is needed.
"""
import numpy
class PhysicsBody():
    """The basic root of everything that interacts with the physic simulation.
    Can then add components that enable gravity, collisions, etc.
    Each has:
        ID -> a string ID, hopefully unique
        pos -> position vector in meters: numpy array of length 3
        mom -> momentum vector in kgm/s: numpy array of length 3
        mass -> mass of the object in kg: float
        physicsEngines -> list of physics engines that can effect it
        graphicsEngines -> the graphical representation (could be multiple)
    """
    def __init__(self,ID,pos,mom,mass):
        self.ID = ID
        self.pos = numpy.array(pos)
        self.mom = numpy.array(mom)
        self.mass = mass
        # self.physicsEngines = []
        # self.graphicsEngines = []
        # self.visuals = []
        
        self.components = []
        
   
 
    
    #a more general method
    def addComponent(self,component):
        """Adds component to own list and registers with engine."""
        if component in self.components:
            print("Attempted to add duplicate component to body: "
                   + self.ID)
            return
        #add to own list
        #print("addcomponent debug component:")
        #print(component)
        self.components.append(component)
        #register with engine
        component.engine.register(self,component)
        #component.engine.bodies.append(self)
        
    def removeComponent(self,component):
        """Removes component from own list and deregisters with engine."""
        if not component in self.components:
            print("Attempted to remove absent component from body: "
                   + self.ID)
            return
        self.components.remove(component)
        component.engine.deregister(self,component)
        #component.engine.bodies.remove(self)
         
        
        # def addPhysicsEngine(self,engine):
        #     """Registers this body with the physics engine given."""
        #     if engine in self.physicsEngines:
        #         print("Attempted to add duplicate engine to body: "
        #               + self.ID)
        #         return
            
        #     self.physics.append(engine)
        #     engine.bodies.append(self)
            
        # def removePhysicsEngine(self,engine):
        #     """Removes this body from the physics engine given."""
        #     if not engine in self.physicsEngines:
        #         print("Attempted to remove not attached engine to body: " 
        #               + self.ID)
        #         return
            
        #     self.physicsEngines.remove(engine)
        #     engine.bodies.remove(self)