# -*- coding: utf-8 -*-
"""
python file containing the inputs
Created on Mon Feb 20 09:24:58 2017

@author: Roeland
"""

class Inputs:
    def __init__(self):
        self.L = 34.0 #Length of the fuselage
        self.Lf1 = 5.0 #Length parameter
        self.Lf2 = 14.6 #Length parameter
        self.Lf3 = 7.6 #Length parameter
        self.R = 2.1 #Fuselage radius
        self.hf = 1.5 #Floor height
        self.tsSkin = 0.003 #Skin thickness
        self.tsFloor = 0.02 #Floor thickness
        self.tst = 0.0012 #Thickness of stiffener
        self.hst = 0.015 #height of stiffener
        self.wst = 0.02 #Width of stiffener
        self.ns = 36 #Number of stiffeners
        self.dtailz = 3.1 #z-distance of aerodynamic center of the tail to the back of the fuselage
        self.dtaily = 4.5 #y-distance of aerodynamic center of the tail to the back of the fuselage
        self.dtgy = 1.9 #y-distance between bottom of the fuselage and the landing gear
        self.Sx = 1.6*10**5 #Lateral force on the tail
        self.W = 64000 #Design landing mass