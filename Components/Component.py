# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 13:54:03 2022

@author: Thomas Goldstein

Utility methods for components.

Components must have an engine attribute. This file gives a method to add that
attribute to existing classes. This could also be done with decorators, but
this is simpler, more explicit, and has less code.

It could also be done via inheritance and subclassing all needed objects but
again, in python why bother.
"""

def makeComponent(instance,engine):
    """Makes any object a component by adding an engine."""
    if hasattr(instance,'engine'):
        print("Warning! makeComponent run on instance with an engine present")
        return
    instance.engine = engine
    return instance
    
class Component():
    def __init__(self,engine):
        self.engine = engine