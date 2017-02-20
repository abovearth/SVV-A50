# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:48:10 2017

@author: Roeland
"""
import Boom
import Math

class Slice:
    zDistance = 0.
    booms = []
    yBar = 0.
    Ixx = 0.
    Iyy = 0.
    
    def __init__(self,nBooms,z,R):
        self.zDistance = z
        for i in xrange(nBooms):
            x = R*Math.cos(i*nBooms/360)
            y = R*Math.sin(i*nBooms/360)
            self.booms.append(Boom(x,y,z))
            
    def calculateYBar(self):
        yBar = 0.
        boomAreaSum = 0.
        for i in xrange(len(self.booms)):
            yBar = yBar + self.booms[i].y*self.booms[i].boomArea
            boomAreaSum = boomAreaSum + self.booms[i].boomArea
        self.yBar = yBar/boomAreaSum
        
    def calculateIxx():
        
    def calculateIyy():
        