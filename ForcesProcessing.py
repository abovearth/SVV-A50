# -*- coding: utf-8 -*-
"""
Forces Processing based a lot on static forces.py from Kuba
Created on Wed Feb 22 09:31:12 2017

@author: Roeland
"""
import inputs
Inputs = inputs.Inputs()

g = 9.81
m = 64000.0
L1 = 5.0
L2 = 14.6
L3 = 34 - 19.6
L = L1+L2+L3
dz = 3.1
dy = 6.4
dx = 7.6
Sx = 1.6*10**5
q = 3*g*m/L
#F - front, R - rear, R = R1+R2
#forces in x
Fx = Sx*(1-((L-L1+dz)/L2))
Rx = Sx*((L-L1+dz)/L2)
#forces in y
Fy = q*((L1+L2)**2/(2*L2)) - (q*L3**2)/(2*L2)
Ry = q*L - Fy

def Vx(z):
    if z <= L1:
        Vx = 0
        
    elif L1 < z <= L2+L1:
        z = z - L1        
        Vx = Fx
        
    elif L1+L2 < z <= L:
        z = z - (L2+L1)    
        Vx = Sx
        
    return Vx
    
def Vy(z):
    if z <= L1:
        Vy = -q*z
        
    elif L1 < z <= L1+L2:
        z = z - L1
        Vy = (-q*L1 + Fy) - q*z
        
    elif L1+L2 < z <= L:
        z = z - (L2+L1)
        Vy = (-q*(L1 + L2) + Fy + Ry) - q*z
        
    
    return Vy
    
def Mx(z):
    if z <= L1:
        Mx = -0.5*q*z**2
        
    elif L1 < z <= L1+L2:
        z = z - L1
        Mx = -0.5*q*L1**2 + (-q*L1 + Fy)*z - 0.5*q*z**2
        
    elif L1+L2 < z <= L:
        z = z - (L2+L1)
        Mx = (-0.5*q*L1**2 + (-q*L1 + Fy)*L2 - 0.5*q*L2**2)+(-q*(L1 + L2) + Fy + Ry)*z - 0.5*q*z**2
        
    return Mx
    
def My(z):
    if z <= L1:
        My = 0.
        
    elif L1 < z <= L2+L1:
        z = z - L1
        My = -((Sx - Fx)/L2)*z
        
    elif L1+L2 < z <= L:
        z = z - (L2+L1)
        My = -(Sx - Fx)+((Sx-Fx)/L3)*z
        
    return My
    
    #FP.Mz(Slices[i].z,Slices[i].yBar)
def Mz(z, ybar): #ybar needed for every slice?
    #ybar = 395.52*10**-3
    Mz=0.
    if z <= L1:
        Mz = 0.
    elif L1 < z <= L2+L1:
        z = z - L1
        Mz = Sx*(Inputs.dtaily-Inputs.R+ybar)-(Rx*(Inputs.dtgy+Inputs.R-ybar)) #ybar or not
    elif L1+L2 < z <= L:
        z = z - (L2+L1)
        Mz = Sx*(Inputs.dtaily-Inputs.R+ybar)
    return Mz

def ForcesAt(z):
    return Vx(z),Vy(z),Mx(z),My(z)