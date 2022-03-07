# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 10:51:43 2022

@author: Thomas Goldstein

A demo physics system showing gravitational orbits.

This demo program uses the component based programming model, as used by
many game engines such as Unity. Each root object can have various 'components'
attached to it; each component is then acted on by an external engine to modify
the base object. In this way adding functionality ot the base object is as simple
as adding components.

In that system the graphical representation is
the root object to which all things are attached; however this does not allow for
the easy replacement of the graphics system (which makes sense for Unity).

In this case the root object will be PhysicsBody, to which is attached as
components various functionality:
    physics engines that effect it
    the graphical representation
    and others if wanted.
    
Each interval when appropriate, the manager for each component runs its 
functions and then updates the physicsBody. For physics engines, they compute
the forces acting on all included bodies and adjust positions. For graphics,
they take the position of the bodies and applies those to the graphical objects.

Every component must have an engine associated with it as an attribute.
A component can be an engine, in which case its engine attribute is itself.

Every engine must have an advance method which takes an elapsed time as an argument.
Every engine must have a register and deregister method which takes the body
and they component.

"""

import PhysicsBody
from Engines import PhysicsEngines
from Engines import VPythonGraphicsEngine
from Components import Component
import Simulation

#import numpy
import vpython
import time



######## Make an example multibody system
system = Simulation.Simulation()
#set engines
system.engines['Graphics'] = VPythonGraphicsEngine.VPythonGraphicsEngine()
system.engines['Gravity'] = PhysicsEngines.GravityEngineEulerIntegrationElementwise()
#add electrostatic repulsion!
#add collission!

#make some bodies - inital momentum sums to 0 to make it easier to watch
system.bodies['apple'] = PhysicsBody.PhysicsBody("apple", (1.0,0.0,0.0),
                                             (-.25,1.0,0.0), 1.0)
system.bodies['orange'] = PhysicsBody.PhysicsBody("orange", (-1.0,0.0,0.0),
                                             (-.25,-1.0,0.0), 1.0)
system.bodies['blue'] = PhysicsBody.PhysicsBody("blue", (0.0,0.0,0.5),
                                             (0.5,0.0,0.0), 1.0)
#add components to those bodies
#physics
system.bodies['apple'].addComponent(system.engines['Gravity'])
system.bodies['orange'].addComponent(system.engines['Gravity'])
system.bodies['blue'].addComponent(system.engines['Gravity'])

#visuals - positions will be set with graphics advance
system.bodies['apple'].addComponent(Component.makeComponent(
    vpython.sphere(color=vpython.color.red, radius = .1), 
    system.engines['Graphics']))
system.bodies['orange'].addComponent(Component.makeComponent(
    vpython.sphere(color=vpython.color.orange, radius = .1), 
    system.engines['Graphics']))
system.bodies['blue'].addComponent(Component.makeComponent(
    vpython.sphere(color=vpython.color.blue, radius = .1), 
    system.engines['Graphics']))

#and a convenience function that takes the above and condenses creation to 1 line
def vpythonGravityConvenience(system,name,pos,mom,mass,color):
    system.bodies[name] = PhysicsBody.PhysicsBody(name,pos,mom,mass)
    system.bodies[name].addComponent(system.engines['Gravity'])
    system.bodies[name].addComponent(Component.makeComponent(
        vpython.sphere(color=color, radius = .1), 
        system.engines['Graphics']))

#bodies get rapidly ejected with these on which is less interesting to watch imo
#vpythonGravityConvenience(system, 'green', (0.0,1.0,-1.0), (-1.0,0.0,0.0), 1.0, vpython.color.green)
#vpythonGravityConvenience(system, 'yelllow', (0.0,-1.0,1.0), (1.0,0.0,0.0), 1.0, vpython.color.yellow)

#initializes the graphics
system.engines['Graphics'].advance(0.0)

# this makes sure the initial timestep is not huge
system.timeInit()

#and a minute long simulation loop with a framerate limiter
while system.totalTime<60.0:
    #print(system.currentElapsedTime())
    if system.currentElapsedTime()<.02:
        time.sleep(.02-system.currentElapsedTime())
    system.advance()

#cleanup:
vpython.scene.delete()
