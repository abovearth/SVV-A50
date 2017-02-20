# -*- coding: utf-8 -*-
"""
Boom class
Created on Mon Feb 20 09:51:55 2017

@author: Roeland
"""

class Boom:
    #Boom Parameters
    x = 0.
    y = 0.
    z = 0.
    boomArea = 0.

    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        
    def calculateBoomArea(self,Astringer,sigmainext,sigmaithis,sigmaiprevious):
        self.boomArea = Astringer + Inputs.tsSkin/6.*(2.+sigmainext/sigmaithis) + Inputs.tsSkin/6.*(2.+sigmaiprevious/sigmaithis)