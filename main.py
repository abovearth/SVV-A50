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
import matplotlib.pyplot as plt
import numpy as np
import testboxslice as TS

nSlices = 416
nFloor = 12
nBooms = Inputs.ns
zlist = []
###Discretization
Slices = []
for i in xrange(nSlices):
    z=i*Inputs.L/nSlices
    Slices.append(GP.Slice(z))
    zlist.append(z)
"""
Slices.append(TS.TestSlice())
for i in xrange(len(Slices)):
    Slices[i].calculateIxx()
    Slices[i].calculateIyy()"""
    # Boom Discretization happens in the constructor of the Slice class
#for j in xrange(len(Slices[1].booms)):
#    print Slices[1].booms[j].x
###End of Discretization


Astringer = Inputs.tst*(Inputs.wst+Inputs.hst) #thinwalled assumption
LengthBetween2Booms = Inputs.R * 10./180.*math.pi
# Floor inertia calculations
Floorwidth = 2*math.sqrt(Inputs.R**2-(Inputs.R-Inputs.hf)**2)
Asection = 2*math.pi*Inputs.R*Inputs.tsSkin+(36*Astringer)+Floorwidth*Inputs.tsFloor
Afloor = Floorwidth*Inputs.tsFloor
yBar = (-(Inputs.R-Inputs.hf)*Inputs.tsFloor*Floorwidth)/(2*math.pi*Inputs.R*Inputs.tsSkin+Inputs.tsFloor*Floorwidth+36*Astringer)
IxxFloor = 1./12.*Floorwidth*Inputs.tsFloor**3+Inputs.tsFloor*Floorwidth*(Inputs.R-Inputs.hf+yBar)**2
IyyFloor = 1./12.*Inputs.tsFloor*Floorwidth**3
print "yBar = " + str(yBar) + " IxxFloor = " + str(IxxFloor) + " IyyFloor = " + str(IyyFloor)
yBarRing = (2*math.pi*Inputs.R*Inputs.tsSkin)/(2*math.pi*Inputs.R*Inputs.tsSkin+Inputs.tsFloor*Floorwidth+36*Astringer)
IyyRing = math.pi*Inputs.R**3*Inputs.tsSkin
IxxRing = math.pi*Inputs.R**3*Inputs.tsSkin + 2*math.pi*Inputs.tsSkin*Inputs.R*(yBar)**2
print "yBar = " + str(yBarRing) + " IxxRing = " + str(IxxRing) + " IyyRing = " + str(IyyRing)

#Normal stress
for i in xrange(len(Slices)):
    Mx = FP.Mx(Slices[i].z)
    My = FP.My(Slices[i].z)
    Ixx = 0.144951214222284
    Iyy = 0.262243038
    Ixy = 0.0
    #if i == 16:
        #for j in xrange(len(Slices[i].booms)):
            #print ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*Slices[i].booms[j].x, ((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*(Slices[i].booms[j].y-yBar)
    for j in xrange(len(Slices[i].booms)):
                Slices[i].booms[j].sigma = SP.DirectStress(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,Slices[i].booms[j].y)
               
    #Floor stress (floor is 'disretized' into n sections of a thick slab, each carrying individual normal stress
    flx = []
    fly = []           
    floorsection =  Inputs.Floorwidth/nFloor
    Slices[i].FloorSigmaX=[]
    Slices[i].FloorSigmaY=[]
    for k in xrange(nFloor):
        Mx = FP.Mx(Slices[i].z)
        My = FP.My(Slices[i].z)
        IxyFloor = 0.
        FloorX = ((-Inputs.Floorwidth/2+floorsection*k)+floorsection/2)
        FloorY = (-(Inputs.R-Inputs.hf+yBar))
        floorStress = SP.DirectStressSeparate(Mx,My,Ixx,IyyFloor,IxyFloor,FloorX,FloorY)
        Slices[i].FloorSigmaX.append(floorStress[0])
        Slices[i].FloorSigmaY.append(floorStress[1])
        flx.append(FloorX)
        fly.append(FloorY)
           
#DISCRETIZATION
#Start of Feedback Loop
change = 0.0
iterationnumber = 0
while change<0.0001:
    print "iteration" + str(iterationnumber)
    iterationnumber+=1
    # Boom Area Calculation
    for i in xrange(len(Slices)):
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].calculateBoomArea(Astringer,Slices[i].booms[j-1],Slices[i].booms[(j+1)%len(Slices[i].booms)],LengthBetween2Booms)
            #print Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea
            if ( Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)>change:
                change =  abs(Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)
            Slices[i].booms[j].previousBoomArea = Slices[i].booms[j].boomArea
    for i in xrange(len(Slices)):
        Slices[i].calculateXBar()
        Slices[i].calculateYBar()
        Slices[i].calculateIxx(IxxFloor)
        Slices[i].calculateIyy(IyyFloor)
        Slices[i].calculateIxy()
        #print Slices[i].Ixy
        
    for i in xrange(len(Slices)):
        Mx = FP.Mx(Slices[i].z)
        My = FP.My(Slices[i].z)
        Ixx = Slices[i].Ixx
        Iyy = Slices[i].Iyy
        Ixy = Slices[i].Ixy
        for j in xrange(len(Slices[i].booms)):
            Slices[i].booms[j].sigma = SP.DirectStress(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,(Slices[i].booms[j].y-Slices[i].yBar))
            Slices[i].booms[j].sigmax = SP.DirectStressSeparate(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,(Slices[i].booms[j].y-Slices[i].yBar))[0]
            Slices[i].booms[j].sigmay = SP.DirectStressSeparate(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,(Slices[i].booms[j].y-Slices[i].yBar))[1]
        
        #End of Feedback Loop

#Shear Flow 
for i in xrange(len(Slices)):
    for j in xrange(len(Slices[i].booms)):
        Sx = FP.Vx(Slices[i].z)
        Sy = FP.Vy(Slices[i].z)
        Mz = FP.Mz(Slices[i].z, yBar)
        #qbi = SP.OpenSectionShearFlow(yBar,Sx,Sy,Slices[i])
        #qs0i = SP.ClosedSectionShearFlow(Floorwidth,Slices[i],LengthBetween2Booms)
    
        SP.FloorShear(nFloor, Slices[i], Sx, Sy)
        SP.OpenSectionShearFlow(Sx,Sy,Slices[i], Slices[i].Qxf, Slices[i].Qyf, yBar)  
        #TS.OpenSectionShearFlow(Sx,Sy,Slices[i])        
        SP.ClosedSectionShearFlow(nFloor,LengthBetween2Booms,Slices[i])
        
        if j<=19 or j>=35:
            Slices[i].booms[j].qs = Slices[i].booms[j].qb+Slices[i].qs0I
        if j <= 34 and j > 19:
            Slices[i].booms[j].qs = Slices[i].booms[j].qb+Slices[i].qs0II

t = 10       
qy =[]
for j in xrange(len(Slices[t].booms)):
        qy.append(Slices[t].booms[j].qb * abs((Slices[t].booms[j].y)-Slices[t].booms[j-1].y))
qs0 =[]
for j in xrange(len(Slices[t].booms)):
        qs0.append(Slices[t].booms[j].qs)
    
qb =[]
for j in xrange(len(Slices[t].booms)):
        qb.append(Slices[t].booms[j].qb)
    

print sum(qy)
print Slices[t].qs0I, Slices[t].qs0II 
print "____"
print FP.Vx(Slices[t].z)
print FP.Vx(Slices[t].z) - sum(qy)
print "____"
print Slices[t].qf[-1]*Inputs.Floorwidth

for i in xrange(len(Slices)):
    Mz = FP.Mz(Slices[i].z, yBar) - Slices[i].qs0I/2*Inputs.AreaI - Slices[i].qs0II/2*Inputs.AreaII
    SP.TorqueShearFlow(Slices[i],LengthBetween2Booms,Mz)
"""    
print Slices[t].qT1, Slices[t].qT2
print Slices[t].qs0I*2*Inputs.AreaI, Slices[t].qs0II*2*Inputs.AreaII
print Slices[t].qT1*2*Inputs.AreaI + Slices[t].qT2*2*Inputs.AreaII + Slices[t].qs0I*2*Inputs.AreaI + Slices[t].qs0II*2*Inputs.AreaII
print FP.Mz(Slices[t].z, 0.)
     
"""  
##ShearStress at every location  
for i in xrange(len(Slices)):
    for j in xrange(len(Slices[i].booms)):
        if j==19:
            Slices[i].booms[j].ShearStress = SP.ShearStress(Slices[i].booms[j].qbnofloor + Slices[i].qs0I,Inputs.tsSkin)
        if j==34:
            Slices[i].booms[j].ShearStress = SP.ShearStress(Slices[i].booms[j].qbnofloor + Slices[i].qs0II,Inputs.tsSkin)        
        else:
            Slices[i].booms[j].ShearStress = SP.ShearStress(Slices[i].booms[j].qs,Inputs.tsSkin)
    Slices[i].ShearStressFloor = []
    for k in xrange(len(Slices[i].qf)):
        Slices[i].ShearStressFloor.append(SP.ShearStress(Slices[i].qf[k],Inputs.tsFloor))

##Total Stress at every location 
MaxStress  = 0.0
MaxStressLocation = (0.,0.,0.)
for i in xrange(len(Slices)):
    for j in xrange(len(Slices[i].booms)):
        Slices[i].booms[j].VonMises = SP.VonMises(Slices[i].booms[j].sigmax, Slices[i].booms[j].sigmay, Slices[i].booms[j].ShearStress)
        if Slices[i].booms[j].VonMises>MaxStress:
             MaxStress = Slices[i].booms[j].VonMises
             MaxStressLocation = (Slices[i].booms[j].x,Slices[i].booms[j].y,Slices[i].booms[j].z)
             print "last change in boom of maxstress at ",i,j,MaxStress,Slices[i].booms[j].sigmax, Slices[i].booms[j].sigmay, Slices[i].booms[j].ShearStress
    
    Slices[i].VonMisesFloor = []
    for k in xrange(len(Slices[i].qf)):
        VonMisesFloor = SP.VonMises(Slices[i].FloorSigmaX[k], Slices[i].FloorSigmaY[k],Slices[i].ShearStressFloor[k])
        Slices[i].VonMisesFloor.append(VonMisesFloor)
        if VonMisesFloor>MaxStress:
             MaxStress = VonMisesFloor
             MaxStressLocation = (flx[k],Inputs.hf-Inputs.R,Slices[i].z)
             print "last change in floor of maxstress at ",i,j
    
### Collecting Results
MaxSF1 = 0.
MaxSF2 = 0.
#MaxStress = 0.
#MaxStressLocation = (0.,0.,0.)
print "Maximum Shear Flow in Frame 1 at 5 m: " + str(MaxSF1)
print "Maximum Shear Flow in Frame 2 at 14.6 m: " + str(MaxSF2)
print "Maximum Stress: " + str(MaxStress)
print "Maximum Stress Location: " + str(MaxStressLocation)
    
### End of Collecting Results
    
#VALIDATION VERIFICATION DATA#
   
xdot=[]
ydot = []
B = []
z = 16
sigmatest =[]
#for z in range(nSlices):
for j in range(36):
    sigmatest.append(Slices[z].booms[j].sigma)
    B.append(abs((Slices[z].booms[j].boomArea))*10**5)
    xdot.append(Slices[z].booms[j].x)
    ydot.append(Slices[z].booms[j].y-yBar)
"""
Bsum = []
AreaDiff = []
for n in xrange(nSlices):
    Bsum.append(sum(B[n:n+36])+Afloor)
    n = n + 35
for m in xrange(len(Bsum)):
    AreaDiff.append(Bsum[m]-Asection)
"""

#plot section
index = np.arange(0.,36.,1.)

fig = plt.figure()
ax = fig.add_subplot(111)
for i,j,k in zip(xdot,ydot,qb):
    ax.annotate(str(k),xy=(i,j+0.1), color='red', size = '10')
for i,j,k in zip(xdot,ydot,qs0):
    ax.annotate(str(k),xy=(i+0.5,j+0.1), color='g', size = '10')
for i,j,k in zip(xdot,ydot,index):
    ax.annotate(str(k),xy=(i+0.03,j-0.075), color='b', size = '7')
plt.scatter(xdot, ydot,s = B)
plt.scatter(flx, fly)
plt.show()
