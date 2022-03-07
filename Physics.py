# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 13:48:03 2022

@author: Thomas Goldstein

Note: use scipy instead of numpy for fortran wrappers of linalg functions?
"""
import numpy

#import scipy.constants
#actual G: scipy.constants.G

#Make the numbers more human readable:
# with G=1, mass =1, radius =1, things will orbit with a radius of 1.
G = 1.0
K = 1.0 #electric constant (Coulomb's law constant)

def gravitationalForce(body1,body2):
    """
    Returns the force on body1 due to body2 gravity: -(Gm1m2)/r^2 * r^

    Parameters
    ----------
    body1 : PhysicsBody
        Object to be acted on
    body2 : PhysicsBody
        Acting object

    Returns
    -------
    numpy arracy of length 3 
        force vector on body1

    """
    
    #this is not the most efficient way to do this but good enough
    #doing radiusVector/radius**3 saves calculating the radius unit vector
    
    #probably faster: importing numpy.subtract and numpy.linalg.norm as names
    #in the module. This improves the lookup speed of the functions
    #also probably faster to use scipy versions!
    
    radiusVector = numpy.subtract(body2.pos,body1.pos)# from 1 to 2 is 2 minus 1
    radius = numpy.linalg.norm(radiusVector)
    
    #Note: some sort of error checking or cuttoff for radii being too small
    #would prevent nonphysically large forces.
    
    return (G*body1.mass*body2.mass/radius**3)*radiusVector

def electricForce(body1,body2,charge1,charge2):
    """
    Unlike gravity, the electrostatic force depends on object charge, and as
    that is included as a component rather than in the base physicsbody, this
    force requires it as an argument.
    """
    radiusVector = numpy.subtract(body2.pos,body1.pos)
    radius = numpy.lanalg.norm(radiusVector)
    
    return (K*charge1.charge*charge2.charge/radius**3)*radiusVector