# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 10:46:45 2017

@author: Kuba
"""
import numpy as np
#filename = "A320_I.txt"
#filename = "A320_II.txt"
def readfile(filename):
    data=open(filename,'r')
    lines= data.readlines()
    data.close()
    lines = lines[10:]
    print lines[0]
    print lines[-1]
    x=[]
    y=[]
    z=[]
    vm=[]
    ldata = []
    for line in lines:
        l = line.split()
        ldata.append(l)
    for l in ldata:       
        x.append(l[2])
        y.append(l[2])
        z.append(l[3])
        vm.append(l[4])
        return x, y, z, vm
