# -*- coding: utf-8 -*-
"""
python file containing the inputs
Created on Mon Feb 20 09:24:58 2017

@author: Roeland
"""

class Inputs:
    L = 34.0 #Length of the fuselage
    Lf1 = 5.0 #Length parameter
    Lf2 = 14.6 #Length parameter
    Lf3 = 7.6 #Length parameter
    R = 2.1 #Fuselage radius
    hf = 1.5 #Floor height
    tsSkin = 0.003 #Skin thickness
    tsFloor = 0.02 #Floor thickness
    tst = 0.0012 #Thickness of stiffener
    hst = 0.015 #height of stiffener
    wst = 0.02 #Width of stiffener
    ns = 36 #Number of siffeners
    dtailz = 3.1 #z-distance of aerodynamic center of the tail to the back of the fuselage
    dtaily = 4.5 #y-distance of aerodynamic center of the tail to the back of the fuselage
    dtgy = 1.9 #y-distance between bottom of the fuselage and the landing gear
    Sx = 1.6*10**5 #Lateral force on the tail
    W = 64000 #Design landing mass