# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 12:15:54 2017

@author: garridomarquez
"""
from __future__ import division
import numpy as np
import moduleFlog as flog
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#import os

#This function gets the conditional probablity of x|y and y|x
def pCond(interXY,x,y,n):
    pinterXY=interXY/n
    pY=y/n
    pX=x/n
    pCondXY=pinterXY/pY
    pCondYX=pinterXY/pX
    return pCondXY,pCondYX,pCondXY*pCondYX
    

#measure proposed
def measureRedundancy(px,py):
    return px*py

#create object blog Handler
curBlog=flog.Blog("coupleofpixels")
#Here I will read a List categs with each category, the number of documents labeled with it
categs=curBlog.getAllCategoriesFreq()

#Here I will read the total N of posts in the blogs
N=len(curBlog.getAllPostsFiles())


#Calculate full matrix of metrics ij between every category in the list categs
matMetric=np.matrix
x=0
y=0
for i in range(0,len(categs)):
    for j in range(i+1,len(categs)):
        #Here get the size of the intersection ietj between i and j 
        ietj=curBlog.getIntersectionSizeBetweenCatACatB(categs[i][2],categs[j][2])
        pcondVal=pCond(int(ietj),int(categs[i][1]),int(categs[j][1]),N)
        matMetric[x][y]=pcondVal[0]
        matMetric[y][x]=pcondVal[1]
        X=categs[i][2]
        Y=categs[j][2]
        Z=measureRedundancy(pcondVal[0],pcondVal[1])
        y=+1
    x+=1


fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()