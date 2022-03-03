# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:45:17 2022

@author: Thomas Goldstein

Manages graphics using vPython. A physics body could have multiple visuals, each
using a different engine.

The engine stores the actual visual object! This is against the usual component
based model! Resolve. 
"""

import vpython

class VPythonGraphicsEngine():
    def __init__(self):
        self.bodies = []#just a list
        self.visuals = {}#dictionary keys are physics body IDs
        
        
        #initialization of camera and axes
        #for multiple vpython systems/windows will need to manage canvases later
        #TODO: manage canvases - each engine gets its own
        self.center = vpython.sphere(pos=vpython.vector(0,0,0),
                                     radius=.1,
                                     color=vpython.color.white)
        #vpython.scene.center(vpython.vector(0,0,0))
        #axes
        self.xhat = vpython.arrow(pos=vpython.vector(0,0,0),
                                  axis=vpython.vector(1,0,0),
                                  color=vpython.color.red)
        self.yhat = vpython.arrow(pos=vpython.vector(0,0,0),
                                  axis=vpython.vector(0,1,0),
                                  color=vpython.color.blue)
        self.zhat = vpython.arrow(pos=vpython.vector(0,0,0),
                                  axis=vpython.vector(0,0,1),
                                  color=vpython.color.green)
    
    def register(self,body,component):
        self.bodies.append(body)
        self.visuals[body.ID] = component
        
    def deregister(self,body,component):
        self.bodies.remove(body)
        del self.visuals[body.ID]

    def advance(self,timeElapsed):
        for body in self.bodies:
            visual = self.visuals[body.ID]
            visual.pos.x = body.pos[0]
            visual.pos.y = body.pos[1]
            visual.pos.z = body.pos[2]
            #note: vpython vectors are not iterable and don't map to arrays/lists
            #nicely, so elementwise assignment is best. The constructor for
            #vectors even takes 3 arguments.
            
#test=VPythonGraphicsEngine()