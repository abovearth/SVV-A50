# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:45:13 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()
import math
import GeometryProcessing as GP
import ForcesProcessing as FP
import StressProcessing as SP

nSlices = 50
nBooms = Inputs.ns

###Discretization
Slices = []
for i in xrange(nSlices):
    z=i*Inputs.L/nSlices
    Slices.append(GP.Slice(z)) # Boom Discretization happens in the constructor of the Slice class
###End of Discretization



# Floor inertia calculations
yBarFloor = (-(Inputs.R-Inputs.hf)*2*Inputs.tsFloor*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))/(2*math.pi*Inputs.R*Inputs.tsSkin+2*Inputs.tsFloor*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))
IxxFloor = 1./12.*Inputs.tsFloor*(2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))**3+Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*(Inputs.R-Inputs.hf-yBarFloor)
IyyFloor = 1./12.*(2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2))*Inputs.tsFloor**3

#Start of Feedback Loop
change = 0.02
while change>0.01:
    
    # Boom Area Calculation
    Astringer = Inputs.tst*(Inputs.wst+Inputs.hst) #thinwalled assumption
    
    for i in xrange(len(Slices)):
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].calculateBoomArea(Astringer,Slices[i].booms[j-1],Slices[i].booms[(j+1)%len(Slices[i].booms)])
            if ( Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)>change:
                change =  Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea
            Slices[i].booms[j].previousBoomArea = Slices[i].booms[j].boomArea
    
    for i in xrange(len(Slices)):
        Slices[i].calculateYBar()
        Slices[i].calculateIxx(IxxFloor)
        Slices[i].calculateIyy(IyyFloor)
        
    for i in xrange(len(Slices)):
        Mx = FP.Mx(Slices[i].z)
        My = FP.My(Slices[i].z)
        Ixx = Slices[i].Ixx
        Iyy = Slices[i].Iyy
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].sigma = SP.DirectStress(Mx,My,Ixx,Iyy,Slices[i].booms[j].x,Slices[i].booms[j].y)
#End of Feedback Loop

for i in xrange(len(Slices)):
    Sx = FP.Sx(Slices[i].z)
    Sy = FP.Sy(Slices[i].z)
    qbi = SP.OpenSectionShearFlow(yBarFloor,Sx,Sy,Slices[i])
    qs0i = SP.ClosedSectionShearFlow()
    
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