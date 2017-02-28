# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:00:48 2017

@author: Kuba
"""
import math
import GeometryProcessing as GP
import inputs
Inputs = inputs.Inputs()

class TestSlice:    

    def __init__(self):
        self.z = 0.
        self.x = [2.5, 2.5, 0, -2.5, -2.5, -2.5, 0, 2.5]
        self.y = [0, 2.5, 2.5, 2.5, 0, -2.5, -2.5, -2.5]
        self.boomArea = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
        self.booms = []
        for i in xrange(self.x.length): #Discretization in booms            
            self.booms.append(GP.Boom(self.x[i],self.y[i],self.z))
        
        self.xBar = 0. #Symmetry thus stays zero
        self.yBar = 0.
        self.Ixx = 0.0
        self.Iyy = 0.0
        self.Ixy = 0.
    
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
