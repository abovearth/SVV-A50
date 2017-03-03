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
#import testboxslice as TS
from mpl_toolkits.mplot3d import Axes3D
from readfile import readfile
from writefile import writefile

nSlices = 288
nFloor = 50
nBooms = Inputs.ns
zlist = []
###Discretization
Slices = []

for i in xrange(nSlices):
    z=i*Inputs.L/nSlices
    Slices.append(GP.Slice(z))
    zlist.append(z)
    
z=Inputs.Lf1
Slices.append(GP.Slice(z))
zlist.append(z)
z=Inputs.Lf1+Inputs.Lf2
Slices.append(GP.Slice(z))
zlist.append(z)
z=34.-14.57805078
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
#print "yBar = " + str(yBar) + " IxxFloor = " + str(IxxFloor) + " IyyFloor = " + str(IyyFloor)
yBarRing = (2*math.pi*Inputs.R*Inputs.tsSkin)/(2*math.pi*Inputs.R*Inputs.tsSkin+Inputs.tsFloor*Floorwidth+36*Astringer)
IyyRing = math.pi*Inputs.R**3*Inputs.tsSkin
IxxRing = math.pi*Inputs.R**3*Inputs.tsSkin + 2*math.pi*Inputs.tsSkin*Inputs.R*(yBar)**2
#print "yBar = " + str(yBarRing) + " IxxRing = " + str(IxxRing) + " IyyRing = " + str(IyyRing)

#Normal stress
for i in xrange(len(Slices)):
    Mx = FP.Mx(Slices[i].z)
    My = FP.My(Slices[i].z)
    Iyy =	0.1535701345
    Ixx = 	0.051422806
    #Ixx = 0.144951214222284
    #Iyy = 0.262243038
    Ixy = 0.0
    #if i == 16:
        #for j in xrange(len(Slices[i].booms)):
            #print ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*Slices[i].booms[j].x, ((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*(Slices[i].booms[j].y-yBar)
    for j in xrange(len(Slices[i].booms)):
                Slices[i].booms[j].sigma = SP.DirectStress(Mx,My,Ixx,Iyy,Ixy,Slices[i].booms[j].x,Slices[i].booms[j].y)
               
    #Floor stress (floor is 'disretized' into n sections of a thick slab, each carrying individual normal stress
    flx = []
    fly = []
    Slices[i].FloorSigmaX=[]
    Slices[i].FloorSigmaY=[]         
    floorsection =  Inputs.Floorwidth/nFloor
    for k in xrange(nFloor):
        Mx = FP.Mx(Slices[i].z)
        My = FP.My(Slices[i].z)
        IxyFloor = 0.
        FloorX = ((-Inputs.Floorwidth/2+floorsection*k)+floorsection/2)
        FloorY = (-(Inputs.R-Inputs.hf+yBar))
        floorStress = SP.DirectStressSeparate(Mx,My,Ixx,Iyy,Ixy,FloorX,FloorY)
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
            if abs( Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)>change:
                change =  abs(Slices[i].booms[j].previousBoomArea - Slices[i].booms[j].boomArea)
                print change
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
    Sx = FP.Vx(Slices[i].z)
    Sy = FP.Vy(Slices[i].z)
    Mz = FP.Mz(Slices[i].z, yBar)
    SP.FloorShear(nFloor, Slices[i], 0., Sy)        
    #qbi = SP.OpenSectionShearFlow(yBar,Sx,Sy,Slices[i])
    #qs0i = SP.ClosedSectionShearFlow(Floorwidth,Slices[i],LengthBetween2Booms)

    
    #if i == 15:
        #print
        #print Slices[i].qf
    SP.OpenSectionShearFlow(0.,Sy,Slices[i], yBar, nFloor)
    #if i == 15:
        #print
        #print Slices[i].qf
    #TS.OpenSectionShearFlow(Sx,Sy,Slices[i])        
    #SP.ClosedSectionShearFlow(nFloor,LengthBetween2Booms,Slices[i])
    #SP.TorqueShearFlow(Slices[i],LengthBetween2Booms,Mz)
    SP.errorSHEAR(Slices[i],LengthBetween2Booms,Mz)


###Shear validation
qbdy = []
qbdx = []
for t in xrange(len(Slices)):
    qb =[]      
    qy = []
    qx = []
    qfloor = Slices[t].qf

    for j in xrange(len(Slices[t].booms)):
        qb.append(Slices[t].booms[j].qb)
        qy.append(Slices[t].booms[j].qb * abs((Slices[t].booms[j].y)-Slices[t].booms[j-1].y))
        qx.append(Slices[t].booms[j].qb * abs((Slices[t].booms[j].x)-Slices[t].booms[j-1].x))
    qbdy.append(sum(qy)+sum(qfloor)*Inputs.tsFloor)
    qbdx.append(sum(qx)+sum(qfloor)*Inputs.tsFloor)
    """for i in range(len(qb)):
        if i <=19:
            if qb[i] - qb[i-1] < 0:
                qb[i] = -1 * qb[i]
                
            """
    """
    qs0 =[]
    for j in xrange(len(Slices[t].booms)):
        if j<=19 or j>=35:
            qs0.append(Slices[t].booms[j].qb+Slices[t].qs0I+Slices[t].qT1)
        if j <= 34 and j > 19:
            qs0.append(Slices[t].booms[j].qb+Slices[t].qs0II+Slices[t].qT2)
    """
    
    #print Slices[t].qs0I, Slices[t].qs0II 
print "qb*dy:" + str(sum(qy)+sum(qfloor)*Inputs.tsFloor)
print "qb*dx:" + str(sum(qx)+sum(qfloor)*Inputs.Floorwidth)
print "____"
print "Vx(z):" + str(FP.Vx(Slices[t].z))
print "Vy(z):" + str(FP.Vy(Slices[t].z))
print "____"
print "x diff.:" + str(FP.Vx(Slices[t].z) - (sum(qx)+sum(qfloor)*Inputs.Floorwidth))
print "y diff.:" + str(FP.Vy(Slices[t].z) - (sum(qy)+sum(qfloor)*Inputs.tsFloor))

#print Slices[t].qf[-1]*Inputs.Floorwidth

#for i in xrange(len(Slices)):
#    Mz = FP.Mz(Slices[i].z, yBar) - Slices[i].qs0I/2*Inputs.AreaI - Slices[i].qs0II/2*Inputs.AreaII
#    SP.TorqueShearFlow(Slices[i],LengthBetween2Booms,Mz)
"""    
print Slices[t].qT1, Slices[t].qT2
print Slices[t].qs0I*2*Inputs.AreaI, Slices[t].qs0II*2*Inputs.AreaII
print Slices[t].qT1*2*Inputs.AreaI + Slices[t].qT2*2*Inputs.AreaII + Slices[t].qs0I*2*Inputs.AreaI + Slices[t].qs0II*2*Inputs.AreaII
print FP.Mz(Slices[t].z, 0.)
     
"""    
##ShearStress at every location  
MaxShearStress = 0.
MaxSigmaX = 0.
MaxSigmaY = 0.
for i in xrange(len(Slices)):

    for j in xrange(len(Slices[i].booms)):

        Slices[i].booms[j].ShearStress = SP.ShearStress(Slices[i].booms[j].qs,Inputs.tsSkin)
        if Slices[i].booms[j].ShearStress>MaxShearStress:
            MaxShearStress = Slices[i].booms[j].ShearStress
        if Slices[i].booms[j].sigmax>MaxSigmaX:
            MaxSigmaX = Slices[i].booms[j].sigmax
        if Slices[i].booms[j].sigmay>MaxSigmaY:
            MaxSigmaY = Slices[i].booms[j].sigmay
            print "i",i,"j",j
    Slices[i].ShearStressFloor = []

    for k in xrange(len(Slices[i].qf)):

        Slices[i].ShearStressFloor.append(SP.ShearStress(Slices[i].qf[k],Inputs.tsFloor))
        if Slices[i].FloorSigmaX[k]>MaxSigmaX:
            MaxSigmaX = Slices[i].FloorSigmaX[k]
        if Slices[i].FloorSigmaY[k]>MaxSigmaY:
            MaxSigmaY = Slices[i].FloorSigmaY[k]


##Total Stress at every location 
MinStress = 100000000000.
MaxStress  = 0.0

MaxStressLocation = (0.,0.,0.)

for i in xrange(len(Slices)):

    for j in xrange(len(Slices[i].booms)):

        Slices[i].booms[j].VonMises = SP.VonMises(Slices[i].booms[j].sigmax, Slices[i].booms[j].sigmay, Slices[i].booms[j].ShearStress)

        if Slices[i].booms[j].VonMises>MaxStress:

             MaxStress = Slices[i].booms[j].VonMises

             MaxStressLocation = (Slices[i].booms[j].x,Slices[i].booms[j].y,Slices[i].booms[j].z)

        if Slices[i].booms[j].VonMises<MinStress:

             MinStress = Slices[i].booms[j].VonMises
    

    Slices[i].VonMisesFloor = []

    for k in xrange(len(Slices[i].qf)):

        VonMisesFloor = SP.VonMises(Slices[i].FloorSigmaX[k], Slices[i].FloorSigmaY[k],Slices[i].ShearStressFloor[k])

        Slices[i].VonMisesFloor.append(VonMisesFloor)
        #print Slices[i].VonMisesFloor
        if VonMisesFloor>MaxStress:

             MaxStress = VonMisesFloor

             MaxStressLocation = (flx[k],Inputs.hf-Inputs.R,Slices[i].z)

             #print "last change in floor of maxstress at ",i,j
        if Slices[i].booms[j].VonMises<MinStress:

             MinStress = Slices[i].booms[j].VonMises   
        
### Collecting Results
MaxSF1 = 0.
MaxSF2 = 0.
print "Minimum Stress: ",MinStress
for i in range(len(Slices)):
    if Slices[i].z == Inputs.Lf1:
        for j in range(len (Slices[i].booms)):
            if abs(Slices[i].booms[j].qs)> abs(MaxSF1):
                MaxSF1 = Slices[i].booms[j].qs
    if Slices[i].z == Inputs.Lf1+Inputs.Lf2:
        for j in range(len (Slices[i].booms)):
            if abs(Slices[i].booms[j].qs)> abs(MaxSF2):
                MaxSF2 = Slices[i].booms[j].qs
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
z = 0
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
#for i,j,k in zip(xdot,ydot,qs0):
   # ax.annotate(str(k),xy=(i+0.5,j+0.1), color='g', size = '10')
for i,j,k in zip(xdot,ydot,index):
    ax.annotate(str(k),xy=(i+0.03,j-0.075), color='b', size = '7')
for i,j,k in zip(flx, fly, qfloor):
    ax.annotate(str(k),xy=(i,j+0.1), color='red', size = '10')
plt.scatter(xdot, ydot,s = B)
plt.scatter(flx, fly)
plt.show()

fig = plt.figure()
zrange = range(len(Slices))

ax = fig.add_subplot(211)
plt.plot(zrange,qbdx)
Vxplot = []
for z in zrange:
    Vxplot.append(FP.Vx(Slices[z].z))
plt.plot(zrange,Vxplot)
plt.title = "Vx vs qbdx"

ax = fig.add_subplot(212)
plt.plot(zrange,qbdy)
Vyplot = []
for z in zrange:
    Vyplot.append(FP.Vy(Slices[z].z))
plt.plot(zrange,Vyplot)
plt.title = "Vy vs qbdy"
plt.show()

fig = plt.figure()
qs0Iplot=[]
qs0IIplot=[]
qbsumplot=[]
Mzplot = []

for z in zrange:
    qs0Iplot.append(Slices[z].qs0I)
    qs0IIplot.append(Slices[z].qs0II)
    Mz=FP.Mz(z*Inputs.L/len(zrange),yBar)
    Mzplot.append(Mz)
    qbsum = 0.
    for j in xrange(len(Slices[z].booms)):
        qbsum +=Slices[z].booms[j].qb
    qbsumplot.append(qbsum)
plt.plot(zrange,qbsumplot)
plt.plot(zrange,qs0Iplot)
plt.plot(zrange,qs0IIplot)
plt.plot(zrange,Mzplot)
plt.show()

xs = []

ys = []

zs = []

c = []
cShear = []
cSigmax = []
cSigmay = []

for i in xrange (len(Slices)):

    for j in xrange (len(Slices[i].booms)):
        if j==340:
            a=1
        else:
            xs.append(Slices[i].booms[j].x)

            ys.append(Slices[i].booms[j].y)

            zs.append(Slices[i].booms[j].z)

            c.append(Slices[i].booms[j].VonMises/MaxStress)
        
            cShear.append(abs(Slices[i].booms[j].ShearStress)/MaxShearStress)
            cSigmax.append(Slices[i].booms[j].sigmax/MaxSigmaX)
            cSigmay.append(Slices[i].booms[j].sigmay/MaxSigmaY)

    for k in xrange(len(Slices[i].qf)):   

        xs.append(flx[k]+5)

        ys.append(Inputs.hf-Inputs.R)

        zs.append(Slices[i].z)

        c.append(Slices[i].VonMisesFloor[k]/MaxStress)
        
        cShear.append(abs(Slices[i].ShearStressFloor[k])/MaxShearStress)
        cSigmax.append(Slices[i].FloorSigmaX[k]/MaxSigmaX)
        cSigmay.append(Slices[i].FloorSigmaY[k]/MaxSigmaY)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs,zs,ys,c=c,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')

plt.show()

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs,zs,ys,c=cShear,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')

plt.show()

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs,zs,ys,c=cSigmax,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')

plt.show()

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs,zs,ys,c=cSigmay,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')

plt.show()

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

xsfile,ysfile,zsfile,cfile = readfile("A320_I.txt")
#writefile("A320_I_sorted.txt",xsfile,ysfile,zsfile,cfile)
for vm in cfile:
    vm=vm/max(cfile)



ax.scatter(xsfile,zsfile,ysfile,c=cfile,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')



plt.show()

ax.scatter(xs,zs,ys,c=c,cmap = plt.cm.get_cmap('jet'),marker = "d",edgecolors = 'face')

ax.set_xlabel('x Label')

ax.set_ylabel('z Label')

ax.set_zlabel('y Label')



plt.show()