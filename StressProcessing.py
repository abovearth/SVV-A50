# -*- coding: utf-8 -*-
"""
Stress Processing
Created on Wed Feb 22 09:54:48 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()
import math

def DirectStress(Mx,My,Ixx,Iyy,x,y):
    return -Mx/Ixx*y-My/Iyy*x
    
def OpenSectionShearFlow(yBarFloor,Sx,Sy,Slice):
    Qxf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(0-Slice.xBar)#symmetry
    Qyf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(yBarFloor-Slice.yBar)
    BoomAreaTimesX = 0.
    BoomAreaTimesY = 0.
    for j in xrange(len(Slice.booms)):
        BoomAreaTimesX += Slice.boom[j].boomArea*abs(Slice.boom[j].x-Slice.xBar)
        BoomAreaTimesY += Slice.boom[j].boomArea*abs(Slice.boom[j].y-Slice.yBar)
    return -Sx/Slice.Iyy*(Qxf + BoomAreaTimesX) -Sy/Slice.Ixx*(Qyf + BoomAreaTimesY)
    
def ClosedSectionShearFlow():
    return 0
    
def TotalShearFlow():
    return 0
    
def ShearStress():
    return 0
    
def TotalStress():
    return 0