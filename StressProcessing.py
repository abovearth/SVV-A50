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
    sigmax = ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*x
    sigmay = ((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*y
    return sigmax + sigmay

def DirectStressSeparate(Mx,My,Ixx,Iyy,Ixy,x,y):
    sigmax = ((My*Ixx-Mx*Ixy)/(Ixx*Iyy-Ixy**2))*x
    sigmay = ((Mx*Iyy-My*Ixy)/(Ixx*Iyy-Ixy**2))*y
    return sigmax, sigmay

def FloorShear(nFloor, Slice, Sx, Sy):
    floorsection =  Inputs.Floorwidth/nFloor
    Slice.qf=[]
    for i in xrange(nFloor):       
        FloorX = ((-Inputs.Floorwidth/2+floorsection*i)+floorsection/2)
        FloorY = -Inputs.R-Inputs.hf
        Slice.Qxf = Inputs.Floorwidth*Inputs.tsFloor*FloorX#symmetry
        Slice.Qyf = Inputs.Floorwidth*Inputs.tsFloor*FloorY
        Slice.qf.append(-((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Slice.Qxf)-((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Slice.Qyf))
        
def OpenSectionShearFlow(Sx,Sy,Slice, Qxf, Qyf, yBar):    
    BoomAreaTimesX1 = 0.
    BoomAreaTimesY1 = 0.
    BoomAreaTimesX2 = 0.
    BoomAreaTimesY2 = 0.

    for j in xrange(len(Slice.booms)):#upper cell
        if j<=19 or j>=35:
            BoomAreaTimesX1 += Slice.booms[j].boomArea*Slice.booms[j].x
            BoomAreaTimesY1 += Slice.booms[j].boomArea*(Slice.booms[j].y)
            if j >= 0 and j <= 18:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX1) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY1)
            elif j==19: 
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Slice.Qxf + BoomAreaTimesX1) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(Slice.Qyf + BoomAreaTimesY1)
                Slice.booms[j].qbnofloor = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX1) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY1)
            if j==35:
                Slice.booms[j].qb = 0.#cut
            #Slice.booms[19].qb
        if j <= 34 and j > 19:
            BoomAreaTimesX2 += Slice.booms[j].boomArea*Slice.booms[j].x
            BoomAreaTimesY2 += Slice.booms[j].boomArea*(Slice.booms[j].y)
            if j == 20:
                Slice.booms[j].qb = 0.#cut
            elif j>= 21 and j <= 33:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX2) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY2)
            elif j == 34:
                Slice.booms[j].qb = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Slice.Qxf + BoomAreaTimesX2) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(-Slice.Qyf + BoomAreaTimesY2)  
                Slice.booms[j].qbnofloor = -((Sx*Slice.Ixx-Sy*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesX1) -((Sy*Slice.Iyy-Sx*Slice.Ixy)/(Slice.Ixx*Slice.Iyy+Slice.Ixy**2))*(BoomAreaTimesY1)
            
           
def ClosedSectionShearFlow(nFloor, LengthBetween2Booms, Slice):
    floorsection =  Inputs.Floorwidth/nFloor
    for i in xrange(nFloor):     
            FloorX = ((-Inputs.Floorwidth/2+floorsection*i)+floorsection/2)
            FloorY = -Inputs.R-Inputs.hf
            qf = (math.sqrt(FloorX**2+FloorY**2)*Slice.qf[i]*floorsection)
    for j in xrange(len(Slice.booms)): 
        Slice.qs0I = ((Inputs.R * Slice.booms[j].qb * LengthBetween2Booms) + qf)/(-2*Inputs.AreaI) 
        Slice.qs0II = ((Inputs.R * Slice.booms[j].qb * LengthBetween2Booms) - qf)/(-2*Inputs.AreaII)

def TorqueShearFlow(Slice,LengthBetween2Booms,Mz):
    #theta = math.pi/180*146.7969
    #totalArea = math.pi*Inputs.R**2
    #AreaI  = Inputs.R**2 * (180./math.pi+2*math.asin(Inputs.hf/Inputs.R))
    #AreaI  = (Inputs.R**2)/2 *(theta - math.sin(theta))
    #AreaII = Inputs.R**2 * (180./math.pi-2*math.asin(Inputs.hf/Inputs.R))
    #AreaII = totalArea - AreaI
    #deltaFloor = FloorWidth/Inputs.tsFloor
    #deltaI  = deltaFloor + Inputs.R * (180./math.pi+2*math.asin(Inputs.hf/Inputs.R))/Inputs.tsFloor
    #deltaII = deltaFloor + Inputs.R * (180./math.pi-2*math.asin(Inputs.hf/Inputs.R))/Inputs.tsFloor
    #openSectionIntegralI = 0.
    #openSectionIntegralII = 0.
    J = LengthBetween2Booms/3 * Inputs.tsSkin**3
    Jfloor = Inputs.Floorwidth/3 * Inputs.tsFloor**3
    
    #Jfloor is take twice -> torque higher?
    JsumI  = 22*J + Jfloor
    JsumII = 14*J +Jfloor
    #print JsumI, JsumII
    T1 = Mz/(1. + JsumII/JsumI)
    T2 = Mz - T1
    Slice.qT1 = T1/(2*Inputs.AreaI)
    Slice.qT2 = T2/(2*Inputs.AreaII)

def errorSHEAR():
    #for j in xrange(len(Slice.booms)):
    #    if j<10 or j>=25:
    #        openSectionIntegralI += Slice.booms[j].qb*LengthBetween2Booms/Inputs.tsSkin
    #    elif j==10:
    #        openSectionIntegralI += Slice.booms[j].qb* (2*Inputs.R * ((math.asin(Inputs.hf/Inputs.R)) %(10./180.*math.pi)) /Inputs.tsSkin + FloorWidth/Inputs.tsFloor) #10./180.*math.pi = 10 degrees in radians
    #    elif j>=11 and j<24:
    #        openSectionIntegralII += Slice.booms[j].qb*LengthBetween2Booms/Inputs.tsSkin
    #    elif j==24:
    #        openSectionIntegralII += Slice.booms[j].qb* (2*Inputs.R * (10./180.*math.pi - (math.asin(Inputs.hf/Inputs.R)) %(10./180.*math.pi)) /Inputs.tsSkin + FloorWidth/Inputs.tsFloor)
    
    cellIopensectionmoment  = 0.
    cellIIopensectionmoment = 0.
    xBarFloor = 0.
    yBarFloor = Inputs.R-Inputs.hf
    for j in xrange(len(Slice.booms)):
        if j<10 or j>=25:
            cellIopensectionmoment += Slice.booms[j].qb * math.sqrt( ((Slice.booms[j].x + Slice.booms[(j+1)%len(Slice.booms)].x)/2-Slice.xBar)**2 + ((Slice.booms[j].y + Slice.booms[(j+1)%len(Slice.booms)].y)/2-Slice.yBar)**2 )
        elif j==10:
            cellIopensectionmoment += Slice.booms[j].qb * math.sqrt( (xBarFloor-Slice.xBar)**2 + (yBarFloor-Slice.yBar)**2 ) #assumption that the contribution of the 2* 6.6 degrees of skin to the ybar are negligible, and i'm too lazy
        elif j>=11 and j<24:
            cellIIopensectionmoment += Slice.booms[j].qb * math.sqrt( ((Slice.booms[j].x + Slice.booms[(j+1)%len(Slice.booms)].x)/2-Slice.xBar)**2 + ((Slice.booms[j].y + Slice.booms[(j+1)%len(Slice.booms)].y)/2-Slice.yBar)**2 )
        elif j==24:
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
        if j<=10 or j>=25:
            Slice.booms[j].qs = Slice.booms[j].qb + qs0I 
        elif j>=11 and j<=24:
            Slice.booms[j].qs = Slice.booms[j].qb + qs0II
        #print "Slice (z = " + str(Slice.z) + "), Boom (j = " + str (j) + ") qs = " + str(Slice.booms[j].qs)
            
    #check for the difference between integral of qs*dy and Vy
    integral = 0.
    for j in xrange(len(Slice.booms)):
        integral += Slice.booms[j].qs*(Slice.booms[j].y+math.sin(j*10/180*math.pi+5/180*math.pi))
    #print "Difference between integral of qs*dy " + str(integral) +" and Vy " + str( math.sqrt((FP.Vy(Slice.z))**2 + (FP.Vx(Slice.z))**2))+ " at Slice.z  (" + str(Slice.z) + ") = " + str(abs(integral - math.sqrt((FP.Vy(Slice.z))**2 + (FP.Vx(Slice.z))**2)))
    #print  "Difference between integral of qs*dy " + str(integral) + "V_tot" + str(math.sqrt((FP.Vy(Slice.z))**2 + (FP.Vx(Slice.z))**2) + "is" + str(math.sqrt((FP.Vy(Slice.z))**2 + (FP.Vx(Slice.z))**2) - integral)

def ShearStress(qs,t):
    return qs/t
    
def VonMises(sigmax,sigmay,shearxy):
    return math.sqrt(1/2*((sigmax-sigmay)**2)+3*shearxy**2)