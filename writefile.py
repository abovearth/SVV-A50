# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 15:17:46 2017

@author: Roeland
"""

def writefile(filename,x,y,z,vm):
    sorted_lists = sorted(zip(x,y,z,vm), reverse=True, key=lambda a: a[2])
    x,y,z,vm = [[a[i] for a in sorted_lists] for i in range(4)]
    fileobject = open(filename,"w") 
    for i in xrange(len(z)):
        fileobject.write(str(x[i])+ " " + str(y[i])+ " " + str(z[i])+ " " + str(vm[i]) + '\n')  
    fileobject.close() 