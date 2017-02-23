# -*- coding: utf-8 -*-
"""
Stress Processing
Created on Wed Feb 22 09:54:48 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()
import math

def DirectStress(Mx,My,Ixx,Iyy,Ixy,x,y):
    return ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*x+((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*y
    
def OpenSectionShearFlow(yBarFloor,Sx,Sy,Slice):
    Qxf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(0-Slice.xBar)#symmetry
    Qyf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(yBarFloor-Slice.yBar)
    BoomAreaTimesX = 0.
    BoomAreaTimesY = 0.
    for j in xrange(len(Slice.booms)):
        BoomAreaTimesX += Slice.booms[j].boomArea*abs(Slice.booms[j].x-Slice.xBar)
        BoomAreaTimesY += Slice.booms[j].boomArea*abs(Slice.booms[j].y-Slice.yBar)
    return -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qxf + BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qyf + BoomAreaTimesY)
    
def ClosedSectionShearFlow():
    #Find the shear centre
    
    #
    return 0
    
def TotalShearFlow(qb,qs):
    return qb + qs
    
def ShearStress(qs,t):
    return qs/t
    
def TotalStress():
    return 0