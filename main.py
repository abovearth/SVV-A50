# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:45:13 2017

@author: Roeland
"""
import Inputs
import Math
import Slice

nSlices = 50
nBooms = Inputs.ns

###Discretization
Slices = []
for i in xrange(nSlices):
    z=i*Inputs.L/nSlices
    Slices.append(Slice(z)) # Boom Discretization happens in the constructor of the Slice class
###End of Discretization

### Geometry Processing

# Boom Area Calculation
Astringer = Inputs.tst*(Inputs.wst+Inputs.hst) #thinwalled assumption
sigmainext = 0.
sigmaithis = 0.
sigmaiprevious = 0.
for i in xrange(len(Slices)):
    for j in xrange(len(Slice[i].booms)):
        Slice[i].booms[j].calculateBoomArea(Astringer,sigmainext,sigmaithis,sigmaiprevious)
        
# Floor inertia calculations
yBarFloor = (-(Inputs.R-Inputs.hf)*2*Inputs.tsFloor*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))/(2*Math.Pi*Inputs.R*Inputs.tsSkin+2*Inputs.tsFloor*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))
IxxFloor = 1./12.*Inputs.tsFloor*(2*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))**3+Inputs.tsFloor*2*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*(Inputs.R-Inputs.hf-yBarFloor)
IyyFloor = 1./12.*(2*Math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))*Inputs.tsFloor**3

for i in xrange(len(Slices)):
    Slices[i].calculateYBar()
    Slices[i].calculateIxx(IxxFloor)
    Slices[i].calculateIyy(IyyFloor)

    
### End of Geometry Processing