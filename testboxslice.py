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
        boomArea = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
        self.booms = []
        for i in xrange(len(self.x)): #Discretization in booms            
            self.booms.append(GP.Boom(self.x[i],self.y[i],self.z))
            self.booms[i].boomArea = boomArea[i]
        self.xBar = 0. #Symmetry thus stays zero
        self.yBar = 0.
        self.Ixx = 0.0
        self.Iyy = 0.0
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
        
    
    def calculateIxx(self):
        self.Ixx = 0.
        for i in xrange(len(self.booms)):
            self.Ixx += self.booms[i].boomArea*(self.booms[i].y-self.yBar)**2
        
    def calculateIyy(self):
        self.Iyy = 0.
        for i in xrange(len(self.booms)):
            self.Iyy += self.booms[i].boomArea*(self.booms[i].x-self.xBar)**2
            
    def calculateIxy(self):
        self.Ixy = 0.
        for i in xrange(len(self.booms)):
            self.Ixy += self.booms[i].boomArea*(self.booms[i].y-self.yBar)*(self.booms[i].x-self.xBar)

def OpenSectionShearFlow(Sx,Sy,Slice):    
    BoomAreaTimesX1 = 0.
    BoomAreaTimesY1 = 0.
    

    for j in xrange(len(Slice.booms)):#only cell
        BoomAreaTimesX1 += Slice.booms[j].boomArea*Slice.booms[j].x
        BoomAreaTimesY1 += Slice.booms[j].boomArea*(Slice.booms[j].y)
        
        Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX1) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY1)
        if j==len(Slice.booms):
            Slice.booms[j].qb = 0.#cut
        