# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 12:15:54 2017

@author: garridomarquez
"""
from __future__ import division
import numpy as np
import moduleFlog as flog
import argparse
import math
import plotly.plotly as py
import plotly.graph_objs as go
#import os

#This function gets the conditional probablity of x|y and y|x
def pCond(interXY,x,y,n):
    pinterXY=interXY/n
    pY=y/n
    pX=x/n
    pCondXY=pinterXY/pY
    pCondYX=pinterXY/pX
    return [pCondXY,pCondYX,pCondXY*pCondYX]

#This function gets the double intersection rate
def inters2(interXY,x,y,n):
    return (interXY*interXY)/(x*y)


#mutual information    
def mutualInformation(interXY,x,y,n):
    pinterXY=interXY/n
    pY=y/n
    pX=x/n
    if pinterXY==0:
        return 0
    else:
        mi=math.log(pinterXY/(pY*pX))
        #mi=pinterXY*math.log(pinterXY/(pY*pX))
    print str(mi)+","+str(interXY)+","+str(pinterXY)+","+str(y)+","+str(pY)+","+str(x)+","+str(pX)+","+str(n)
    return mi

#measure proposed
def measureRedundancy(px,py):
    return px*py

#ploty heatmap creqtion
def createHeatmap(xx,yy,zz,plotname):
    trace = go.Heatmap(z=zz,x=xx,y=yy)
    data=go.Data([trace])
    py.iplot(data, filename=plotname)

parser = argparse.ArgumentParser(description='heatmaps')
parser.add_argument('blog', metavar='blog', type=str, help='name of the blog')
args=parser.parse_args()

#blog
blog=args.blog

#create object blog Handler
curBlog=flog.Blog(blog)
#Here I will read a List categs with each category, the number of documents labeled with it
categs=curBlog.getAllCategoriesFreq()

#Here I will read the total N of posts in the blogs
N=len(curBlog.getAllPostsFiles())


#Calculate full matrix of metrics ij between every category in the list categs
matMetric=np.zeros((len(categs),len(categs)), dtype=np.float)
x=0
y=0
X=[]
Y=[]
Z=[]
Zcond=[]
Zmi=[]
#print N
#print matMetric.shape
for i in range(0,len(categs)):
    X.append(categs[i][0])
    z=[]
    zconds=[]
    zmi=[]
    for j in range(0,len(categs)):
        #Here get the size of the intersection ietj between i and j 
        ietj=curBlog.getIntersectionSizeBetweenCatACatB(categs[i][2],categs[j][2])
        pcondVal=pCond(int(ietj),int(categs[i][1]),int(categs[j][1]),N)
        #print pcondVal
        matMetric[x][y]=pcondVal[0]
        #matMetric[y][x]=pcondVal[1]
        #X.append(categs[i][0])
        #Y.append(categs[j][0])
        z.append(measureRedundancy(pcondVal[0],pcondVal[1]))
        #z.append(inters2(int(ietj),int(categs[i][1]),int(categs[j][1]),N))
        mip=mutualInformation(int(ietj),int(categs[i][1]),int(categs[j][1]),N)
        zmi.append(mip)
        zconds.append(pcondVal[1])
        #z.append(pcondVal[0])
        #print categs[i][0].encode("utf-8")+","+categs[j][0].encode("utf-8")+","+str(pcondVal[0])+","+str(pcondVal[1])+","+str(pcondVal[2])+","+str(mip)
        y=+1
    x+=1
    Z.append(z)
    Zcond.append(zconds)
    Zmi.append(zmi)

Y=X
#createHeatmap(X,Y,Zcond,blog+'-conditional')
#createHeatmap(X,Y,Z,blog+'-redundancy')
#createHeatmap(X,Y,Zmi,blog+'-mutual_info_noLog')