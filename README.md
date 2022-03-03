# Python Physics Demo
Dependencies: numpy, vpython

A demo physics system.

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
Every engine must have a register and deregister method which takes as arguments the body
and the component.

The simulation can be run by running Main.py. It however requires vpython, which may be unusual for you!