# -*- coding: utf-8 -*-
"""
Geometry Processing
Created on Mon Feb 20 09:48:10 2017

@author: Roeland
"""

import math
import inputs
Inputs = inputs.Inputs()

class Boom:    

    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.boomArea = 0.
        self.previousBoomArea = 0.
        self.sigma = 0.
        
    def calculateBoomArea(self,Astringer,BoomPrevious,BoomNext,LengthBetween2Booms):
        #print BoomPrevious, BoomNext
        if self.sigma == 0.:
            self.boomArea = Astringer + Inputs.tsSkin*LengthBetween2Booms/6.*(2.+1.) + Inputs.tsSkin*LengthBetween2Booms/6.*(2.+1.)
        else:
            self.boomArea = Astringer + Inputs.tsSkin*LengthBetween2Booms/6.*(2.+BoomNext.sigma/self.sigma) + Inputs.tsSkin*LengthBetween2Booms/6.*(2.+BoomPrevious.sigma/self.sigma)
        
    def __repr__(self):
        return "Boom: " + "x = " + str(self.x) + ",y = " + str(self.y) + ",z = " + str(self.z) + ",boomArea = " + str(self.boomArea) + ",sigma = " + str(self.sigma)
        
class Slice:
    
    def __init__(self,z):
        self.z = z
        self.booms = []
        for i in xrange(Inputs.ns): #Discretization in booms
            x = Inputs.R*math.cos(i*360./Inputs.ns/180.*math.pi)
            y = Inputs.R*math.sin(i*360./Inputs.ns/180.*math.pi)
            self.booms.append(Boom(x,y,z))
        self.xBar = 0. #Symmetry thus stays zero
        self.yBar = 0.
        self.Ixx = 0.
        self.Iyy = 0.
        self.Ixy = 0.
    
    def calculateXBar(self):
        xBartemp = 0.
        boomAreaSum = 0.
        for i in xrange(len(self.booms)):
            xBartemp += self.booms[i].x*self.booms[i].boomArea
            boomAreaSum = boomAreaSum + self.booms[i].boomArea
        self.xBar = xBartemp/boomAreaSum
        
    def calculateYBar(self):
        yBartemp = 0.
        boomAreaSum = 0.
        for i in xrange(len(self.booms)):
            yBartemp += self.booms[i].y*self.booms[i].boomArea
            boomAreaSum = boomAreaSum + self.booms[i].boomArea
        self.yBar = yBartemp/boomAreaSum
        
    def calculateIxx(self,IxxFloor):
        self.Ixx = IxxFloor
        for i in xrange(len(self.booms)):
            self.Ixx += self.booms[i].boomArea*(self.booms[i].y-self.yBar)**2
        
    def calculateIyy(self,IyyFloor):
        self.Iyy = IyyFloor
        for i in xrange(len(self.booms)):
            self.Iyy += self.booms[i].boomArea*(self.booms[i].x-self.xBar)**2
            
    def calculateIxy(self):
        self.Ixy = 0.
        for i in xrange(len(self.booms)):
            self.Ixy += self.booms[i].boomArea*(self.booms[i].y-self.yBar)*(self.booms[i].x-self.xBar)
        
    def __repr__(self):
        return "Slice: " + "z = " + str(self.z) + ",xBar = " + str(self.xBar) + ",yBar = " + str(self.yBar) + ",Ixx = " + str(self.Ixx) + ",Iyy = " + str(self.Iyy) + ",Booms = " + str(self.booms)