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


Astringer = Inputs.tst*(Inputs.wst+Inputs.hst) #thinwalled assumption
    
# Floor inertia calculations
Floorwidth = 2*math.sqrt(Inputs.R**2-(Inputs.R-Inputs.hf)**2)
yBar = (-(Inputs.R-Inputs.hf)*Inputs.tsFloor*Floorwidth)/(2*math.pi*Inputs.R*Inputs.tsSkin+Inputs.tsFloor*Floorwidth+36*Astringer)
IxxFloor = 1./12.*Floorwidth*Inputs.tsFloor**3+Inputs.tsFloor*Floorwidth*(Inputs.R-Inputs.hf-yBar)
IyyFloor = 1./12.*Inputs.tsFloor*Floorwidth**3
print "yBar = " + str(yBar) + " IxxFloor = " + str(IxxFloor) + " IyyFloor = " + str(IyyFloor)

#Start of Feedback Loop
change = 0.0
while change<0.0001:
    
    # Boom Area Calculation
    for i in xrange(len(Slices)):
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].calculateBoomArea(Astringer,Slices[i].booms[j-1],Slices[i].booms[(j+1)%len(Slices[i].booms)])
            #print Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea
            if ( Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)>change:
                change =  Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea
            Slices[i].booms[j].previousBoomArea = Slices[i].booms[j].boomArea
    
    for i in xrange(len(Slices)):
        Slices[i].calculateXBar()
        Slices[i].calculateYBar()
        Slices[i].calculateIxx(IxxFloor)
        Slices[i].calculateIyy(IyyFloor)
        Slices[i].calculateIxy()
        
    for i in xrange(len(Slices)):
        Mx = FP.Mx(Slices[i].z)
        My = FP.My(Slices[i].z)
        Ixx = Slices[i].Ixx
        Iyy = Slices[i].Iyy
        Ixy = Slices[i].Ixy
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].sigma = SP.DirectStress(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,Slices[i].booms[j].y)
#End of Feedback Loop

for i in xrange(len(Slices)):
    Sx = FP.Vx(Slices[i].z)
    Sy = FP.Vy(Slices[i].z)
    qbi = SP.OpenSectionShearFlow(yBar,Sx,Sy,Slices[i])
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