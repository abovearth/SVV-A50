# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:45:13 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()
import math
import slice

nSlices = 50
nBooms = Inputs.ns

###Discretization
Slices = []
for i in xrange(nSlices):
    z=i*Inputs.L/nSlices
    Slices.append(slice.Slice(z)) # Boom Discretization happens in the constructor of the Slice class
###End of Discretization

### Geometry Processing

# Boom Area Calculation
Astringer = Inputs.tst*(Inputs.wst+Inputs.hst) #thinwalled assumption
sigmainext = 1.
sigmaithis = 1.
sigmaiprevious = 1.
for i in xrange(len(Slices)):
    for j in xrange(len(Slices[i].booms)):
        Slices[i].booms[j].calculateBoomArea(Astringer,sigmainext,sigmaithis,sigmaiprevious)
        
# Floor inertia calculations
yBarFloor = (-(Inputs.R-Inputs.hf)*2*Inputs.tsFloor*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))/(2*math.pi*Inputs.R*Inputs.tsSkin+2*Inputs.tsFloor*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))
IxxFloor = 1./12.*Inputs.tsFloor*(2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))**3+Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*(Inputs.R-Inputs.hf-yBarFloor)
IyyFloor = 1./12.*(2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))*Inputs.tsFloor**3

for i in xrange(len(Slices)):
    Slices[i].calculateYBar()
    Slices[i].calculateIxx(IxxFloor)
    Slices[i].calculateIyy(IyyFloor)
    
### End of Geometry Processing
    
### Forces Processing
    

    
### End of Forces Processing
    
### Stress Processing
    

    
### End of Stress Processing
    
### Collecting Results
MaxSF1 = 0.
MaxSF2 = 0.
MaxStress = 0.
MaxStressLocation = (0.,0.,0.)
print "Maximum Shear Flow in Frame 1 at 5 m: " + str(MaxSF1)
print "Maximum Shear Flow in Frame 2 at 14.6 m: " + str(MaxSF2)
print "Maximum Stress: " + str(MaxStress)
print "Maximum Stress Location: " + str(MaxStressLocation)
    
### End of Collecting Results