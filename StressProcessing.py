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
    for j in xrange(len(Slice.booms)):#upper cell
        if j<10 or j>25:
            BoomAreaTimesX += Slice.booms[j].boomArea*abs(Slice.booms[j].x-Slice.xBar)
            BoomAreaTimesY += Slice.booms[j].boomArea*abs(Slice.booms[j].y-Slice.yBar)
            if j<10:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY)
            elif j>25: #add floor with a corrected orientation
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Qxf + BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Qyf + BoomAreaTimesY)
            if j==35:
                Slice.booms[j].qb = 0.#cut
    BoomAreaTimesX = 0.
    BoomAreaTimesY = 0.
    for j in xrange(len(Slice.booms)):#lower cell
        if j==11:
            Slice.booms[j].qb = 0. #cut
        if j>11 and j<25:
            BoomAreaTimesX += Slice.booms[j].boomArea*abs(Slice.booms[j].x-Slice.xBar)
            BoomAreaTimesY += Slice.booms[j].boomArea*abs(Slice.booms[j].y-Slice.yBar)
            if j>11:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY)
            if j==24: #add floor
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qxf + BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qyf + BoomAreaTimesY)
    for j in xrange(len(Slice.booms)):
        Slice.booms[j].qb = Slice.booms[j].qb *-1. #correct the orientation from clockwise to counterclockwise

def ClosedSectionShearFlow():
    
    return 0
    
def TotalShearFlow(qb,qs):
    return qb + qs
    
def ShearStress(qs,t):
    return qs/t
    
def TotalStress():
    return 0