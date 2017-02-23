# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 10:40:29 2017

@author: Kuba
"""
import math
import matplotlib.pyplot as plt
import numpy as np

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
"""
print "Fy" , Fy, "Ry", Ry
print Fy + Ry, q*L
print Fx, Rx
print Fx + Rx, Sx
"""
#static diagrams
nres = 1000 #set resolution
zrange = np.linspace(0.,L,nres)
Vy = []
Mx = []
Vx = []
My = []
Mz = []
Vz = 0.
for z in zrange:
    if z <= L1:
        Vy1 = -q*z
        Mx1 = -0.5*q*z**2
        Vy.append(Vy1)
        Mx.append(Mx1)
    elif L1 < z <= L1+L2:
        z = z - L1
        Vy2 = (-q*L1 + Fy) - q*z
        Mx2 = -0.5*q*L1**2 + (-q*L1 + Fy)*z - 0.5*q*z**2
        Vy.append(Vy2)
        Mx.append(Mx2)
    elif L1+L2 < z <= L:
        z = z - (L2+L1)
        Vy3 = (-q*(L1 + L2) + Fy + Ry) - q*z
        Mx3 = (-0.5*q*L1**2 + (-q*L1 + Fy)*L2 - 0.5*q*L2**2)+(-q*(L1 + L2) + Fy + Ry)*z - 0.5*q*z**2
        Vy.append(Vy3)
        Mx.append(Mx3)
        
for z in zrange:
    if z <= L1:
        Vx1 = 0
        My1 = 0
        Vx.append(Vx1)
        My.append(My1)
    elif L1 < z <= L2+L1:
        z = z - L1        
        Vx2 = Fx
        My2 = -((Sx - Fx)/L2)*z
        Vx.append(Vx2)
        My.append(My2)
    elif L1+L2 < z <= L:
        z = z - (L2+L1)    
        Vx3 = Sx
        My3 = -(Sx - Fx)+((Sx-Fx)/L3)*z
        Vx.append(Vx3)
        My.append(My3)
#T = Sx * dy_from the centroid
#dy_centroid needed to finish this!        
#for z in zrange:
#    if z <= L1:
#        Mz1 = 0.
#        Mz.append(Mz1)
#    elif L1 < z <= L2+L1:
#        z = z - L1
#        Mz2 = 
#    elif L1+L2 < z <= L:
#        z = z - (L2+L1) 
        
        
""""""
#plot section
plt.subplot(221)
plt.title("Vy")
plt.plot(zrange, Vy)

plt.subplot(222)
plt.title("Mx")
plt.plot(zrange, Mx)

plt.subplot(223)
plt.title("Vx")
plt.plot(zrange, Vx)

plt.subplot(224)
plt.title("My")
plt.plot(zrange, My)

plt.show()
""""""