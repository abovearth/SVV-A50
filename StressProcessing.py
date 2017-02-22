# -*- coding: utf-8 -*-
"""
Stress Processing
Created on Wed Feb 22 09:54:48 2017

@author: Roeland
"""

def DirectStress(Mx,My,Ixx,Iyy,x,y):
    return Mx/Ixx*y+My/Iyy*x
    
def OpenSectionShearFlow():
    return 0
    
def ClosedSectionShearFlow():
    return 0
    
def TotalShearFlow():
    return 0
    
def ShearStress():
    return 0
    
def TotalStress():
    return 0