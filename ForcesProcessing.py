# -*- coding: utf-8 -*-
"""
Forces Processing
Created on Wed Feb 22 09:31:12 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()

def Sx(z):
    Sx = 0
    if z>Inputs.Lf1:
        Sx += 0
    if z>Inputs.Lf2:
        Sx += 0
    return Sx
    
def Sy(z):
    q = -Inputs.W/Inputs.L
    Sy = q*z
    if z>Inputs.Lf1:
        Sy += 0
    if z>Inputs.Lf2:
        Sy += 0
    return Sy
    
def Mx(z):
    Mx = 0
    if z>Inputs.Lf1:
        Mx += 0
    if z>Inputs.Lf2:
        Mx += 0
    return Mx
    
def My(z):
    My = 0
    if z>Inputs.Lf1:
        My += 0
    if z>Inputs.Lf2:
        My += 0
    return My
    
def Mz(z):
    Mz = 0
    if z>Inputs.Lf1:
        Mz += 0
    if z>Inputs.Lf2:
        Mz += 0
    return Mz