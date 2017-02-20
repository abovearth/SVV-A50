# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:48:10 2017

@author: Roeland
"""
import Boom
import Math
import Inputs

class Slice:
    zDistance = 0.
    booms = []
    xBar = 0. #Symmetry thus stays zero
    yBar = 0.
    Ixx = 0.
    Iyy = 0.
    
    def __init__(self,z):
        self.zDistance = z
        for i in xrange(Inputs.ns): #Discretization in Booms
            x = Inputs.R*Math.cos(i*Inputs.ns/360)
            y = Inputs.R*Math.sin(i*Inputs.ns/360)
            self.booms.append(Boom(x,y,z))
            
    def calculateYBar(self):
        yBar = 0.
        boomAreaSum = 0.
        for i in xrange(len(self.booms)):
            yBar = yBar + self.booms[i].y*self.booms[i].boomArea
            boomAreaSum = boomAreaSum + self.booms[i].boomArea
        self.yBar = yBar/boomAreaSum
        
    def calculateIxx(self,IxxFloor):
        Ixx = IxxFloor
        for i in xrange(len(self.booms)):
            Ixx = Ixx + self.booms[i].boomArea*(self.booms[i].y-self.yBar)**2
        
    def calculateIyy(self,IyyFloor):
        Iyy = IyyFloor
        for i in xrange(len(self.booms)):
            Iyy = Iyy + self.booms[i].boomArea*(self.booms[i].x-self.xBar)**2
        