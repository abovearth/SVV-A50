# -*- coding: utf-8 -*-
"""
Forces Processing
Created on Wed Feb 22 09:31:12 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()

def Sx(z):
    Sx = 0.
    if z>Inputs.Lf1:
        Sx += 1.
    if z>Inputs.Lf2:
        Sx += 1.
    return Sx
    
def Sy(z):
    q = 3*-9.81*Inputs.W/Inputs.L
    Sy = q*z
    if z>Inputs.Lf1:
        Sy += 0
    if z>Inputs.Lf2:
        Sy += 0
    return Sy
    
def Mx(z):
    Mx = 1.
    if z>Inputs.Lf1:
        Mx += 1.
    if z>Inputs.Lf2:
        Mx += 1.
    return Mx
    
def My(z):
    My = 1.
    if z>Inputs.Lf1:
        My += 1.
    if z>Inputs.Lf2:
        My += 1.
    return My
    
def Mz(z):
    Mz = 1.
    if z>Inputs.Lf1:
        Mz += 1.
    if z>Inputs.Lf2:
        Mz += 1.
    return Mz