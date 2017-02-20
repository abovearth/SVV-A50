# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:45:13 2017

@author: Roeland
"""
import Inputs
import Math

nSlices = 50
nBooms = Inputs.ns

def floorInertia():
    yBar = (-(Inputs.R-Inputs.hf)*2*Inputs.tsFloor*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))/(2*Math.Pi*Inputs.R*Inputs.tsSkin+2*Inputs.tsFloor*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))
    IxxFloor = 1./12.*Inputs.tsFloor*(2*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))**3+Inputs.tsFloor*2*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*(Inputs.R-Inputs.hf-yBar)
    