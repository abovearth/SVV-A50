# -*- coding: utf-8 -*-
"""
Stress Processing
Created on Wed Feb 22 09:54:48 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()
import math
import ForcesProcessing as FP

def DirectStress(Mx,My,Ixx,Iyy,Ixy,x,y):
    return ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*x+((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*y
    
def OpenSectionShearFlow(yBarFloor,Sx,Sy,Slice):
    Qxf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(0-Slice.xBar)#symmetry
    Qyf = Inputs.tsFloor*2*math.sqrt(Inputs.R**2+(Inputs.R-Inputs.hf)**2)*abs(yBarFloor-Slice.yBar)
    BoomAreaTimesX = 0.
    BoomAreaTimesY = 0.
    for j in xrange(len(Slice.booms)):#upper cell
        if j<=1 or j>=17:
            BoomAreaTimesX += Slice.booms[j].boomArea*abs(Slice.booms[j].x-Slice.xBar)
            BoomAreaTimesY += Slice.booms[j].boomArea*abs(Slice.booms[j].y-Slice.yBar)
            if j<1:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY)
            elif j>=17 or j==1: #add floor with a corrected orientation
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Qxf + BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Qyf + BoomAreaTimesY)
            if j==26:
                Slice.booms[j].qb = 0.#cut
    BoomAreaTimesX = 0.
    BoomAreaTimesY = 0.
    for j in xrange(len(Slice.booms)):#lower cell
        if j==2:
            Slice.booms[j].qb = 0. #cut
        if j>=2 and j<17:
            BoomAreaTimesX += Slice.booms[j].boomArea*abs(Slice.booms[j].x-Slice.xBar)
            BoomAreaTimesY += Slice.booms[j].boomArea*abs(Slice.booms[j].y-Slice.yBar)
            if j>=2:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY)
            if j==16: #add floor
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qxf + BoomAreaTimesX) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Qyf + BoomAreaTimesY)
    for j in xrange(len(Slice.booms)):
        Slice.booms[j].qb = Slice.booms[j].qb *-1. #correct the orientation from clockwise to counterclockwise

def ClosedSectionShearFlow(FloorWidth,Slice,LengthBetween2Booms):
    AreaI  = Inputs.R**2 * (180./math.pi+2*math.asin(Inputs.hf/Inputs.R))
    AreaII = Inputs.R**2 * (180./math.pi-2*math.asin(Inputs.hf/Inputs.R))
    #Gref = 1.0
    deltaFloor = FloorWidth/Inputs.tsFloor
    deltaI  = deltaFloor + Inputs.R * (180./math.pi+2*math.asin(Inputs.hf/Inputs.R))/Inputs.tsFloor
    deltaII = deltaFloor + Inputs.R * (180./math.pi-2*math.asin(Inputs.hf/Inputs.R))/Inputs.tsFloor
    openSectionIntegralI = 0.
    openSectionIntegralII = 0.
    for j in xrange(len(Slice.booms)):
        if j<1 or j>=17:
            openSectionIntegralI += Slice.booms[j].qb*LengthBetween2Booms/Inputs.tsSkin
        elif j==1:
            openSectionIntegralI += Slice.booms[j].qb* (2*Inputs.R * ((math.asin(Inputs.hf/Inputs.R)) %(10./180.*math.pi)) /Inputs.tsSkin + FloorWidth/Inputs.tsFloor) #10./180.*math.pi = 10 degrees in radians
        elif j>=2 and j<16:
            openSectionIntegralII += Slice.booms[j].qb*LengthBetween2Booms/Inputs.tsSkin
        elif j==16:
            openSectionIntegralII += Slice.booms[j].qb* (2*Inputs.R * (10./180.*math.pi - (math.asin(Inputs.hf/Inputs.R)) %(10./180.*math.pi)) /Inputs.tsSkin + FloorWidth/Inputs.tsFloor)
    
    cellIopensectionmoment  = 0.
    cellIIopensectionmoment = 0.
    xBarFloor = 0.
    yBarFloor = Inputs.R-Inputs.hf
    for j in xrange(len(Slice.booms)):
        if j<1 or j>=17:
            cellIopensectionmoment += Slice.booms[j].qb * math.sqrt( ((Slice.booms[j].x + Slice.booms[(j+1)%len(Slice.booms)].x)/2-Slice.xBar)**2 + ((Slice.booms[j].y + Slice.booms[(j+1)%len(Slice.booms)].y)/2-Slice.yBar)**2 )
        elif j==1:
            cellIopensectionmoment += Slice.booms[j].qb * math.sqrt( (xBarFloor-Slice.xBar)**2 + (yBarFloor-Slice.yBar)**2 ) #assumption that the contribution of the 2* 6.6 degrees of skin to the ybar are negligible, and i'm too lazy
        elif j>=2 and j<16:
            cellIIopensectionmoment += Slice.booms[j].qb * math.sqrt( ((Slice.booms[j].x + Slice.booms[(j+1)%len(Slice.booms)].x)/2-Slice.xBar)**2 + ((Slice.booms[j].y + Slice.booms[(j+1)%len(Slice.booms)].y)/2-Slice.yBar)**2 )
        elif j==16:
            cellIIopensectionmoment += Slice.booms[j].qb * math.sqrt( (xBarFloor-Slice.xBar)**2 + (yBarFloor-Slice.yBar)**2 ) #assumption that the contribution of the 2* 3.4 degrees of skin to the ybar are negligible, and i'm too lazy
    """
    rateOfTwistI  = 1./(2.*AreaI *Gref)*(-1.*qs0II*deltaFloor+qs0I *deltaI +openSectionIntegralI )
    rateOfTwistII = 1./(2.*AreaII*Gref)*(-1.*qs0I *deltaFloor+qs0II*deltaII+openSectionIntegralII)    
    0. = cellIopensectionmoment + cellIIopensectionmoment + 2*AreaI *qs0I + 2*AreaII*qs0II
    """
    #qs0I = (cellIopensectionmoment + cellIIopensectionmoment + 0. + 2*AreaII*qs0II)/(2*AreaI)
    #rateOfTwistII = 1./(2.*AreaII*Gref)*(-1.*(cellIopensectionmoment + cellIIopensectionmoment + 0. + 2*AreaII*qs0II)/(2*AreaI) *deltaFloor+qs0II*deltaII+openSectionIntegralII)    
    #1./(2.*AreaI *Gref)*(-1.*qs0II*deltaFloor+(cellIopensectionmoment + cellIIopensectionmoment + 0. + 2*AreaII*qs0II)/(2*AreaI) *deltaI +openSectionIntegralI ) = 1./(2.*AreaII*Gref)*(-1.*(cellIopensectionmoment + cellIIopensectionmoment + 0. + 2*AreaII*qs0II)/(2*AreaI) *deltaFloor+qs0II*deltaII+openSectionIntegralII)    
    qs0II = ((cellIopensectionmoment + cellIIopensectionmoment)*(-deltaI/(2*AreaI) - deltaFloor/(2*AreaII)) + AreaI/AreaII*openSectionIntegralI - openSectionIntegralII)/(AreaII/AreaI*deltaI - AreaI/AreaII*deltaII)
    qs0I = (cellIopensectionmoment + cellIIopensectionmoment + 0. + 2*AreaII*qs0II)/(2*AreaI)
    
    #totalShearFlow
    for j in xrange(len(Slice.booms)):
        if j<=1 or j>=17:
            Slice.booms[j].qs = Slice.booms[j].qb + qs0I 
        elif j>=2 and j<=16:
            Slice.booms[j].qs = Slice.booms[j].qb + qs0II
        #print "Slice (z = " + str(Slice.z) + "), Boom (j = " + str (j) + ") qs = " + str(Slice.booms[j].qs)
            
    #check for the difference between integral of qs*dy and Vy
    integral = 0.
    for j in xrange(len(Slice.booms)):
        integral += Slice.booms[j].qs*LengthBetween2Booms#(Slice.booms[j].y+math.sin(j*10/180*math.pi+5/180*math.pi))
    print "Difference between integral of qs*ds " + str(integral) +" and Vx " + str( FP.Vx(Slice.z)) +" and Vy " + str( FP.Vy(Slice.z)) + " at Slice.z  (" + str(Slice.z) + ") = " + str(abs(integral - FP.Vy(Slice.z)-FP.Vx(Slice.z)))
    
def ShearStress(qs,t):
    return qs/t
    
def TotalStress():
    return 0