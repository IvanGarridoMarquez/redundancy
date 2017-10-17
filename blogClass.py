# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:49:40 2017

@author: ivan
"""

import mysql.connector
#import numpy as np

class Blog:
    "Blog handling class"
    name=""
    idC=""
    catgs=[]
    keys=[]
    dbCon=0
    loc=""
    
    def __init__(self,nam,locdir,dbH):
        dbH.execute("SELECT idblog, blogName FROM blog where blogName='"+nam+"';")
        bx=dbH.fetchone()
        self.dbCon=dbH
        self.name=bx[1]
        self.idC=bx[0]
        self.loc=locdir
        dbH.execute("SELECT idcategory FROM category where blog="+str(self.idC)+";")
        for ct in dbH:
            self.catgs.append(ct[0])
        dbH.execute("SELECT idtag FROM tag where blog="+str(self.idC)+";")
        for tg in dbH:
            self.keys.append(tg[0])
            
    def getAllPostsFiles(self):
        postF=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        self.dbCon.execute("select post.file from post where blog="+str(self.idC))
        for pst in self.dbCon:
            postF.append(self.loc+sep+pst[0])
        return postF
        
    def getAllCategoriesNames(self):
        cats=""
        catNam=[]
        for cat in self.catgs:
            cats+=str(cat)+","
        self.dbCon.execute("SELECT categoryName FROM category where idcategory in ("+cats[:-1]+");")
        for cN in self.dbCon:
            catNam.append(cN[0])
        return catNam
        
    def setLocation(self,locdir):
        self.loc=locdir
        
    def getACategoryName(self,idcat):
        if idcat in self.catgs:
            self.dbCon.execute("SELECT categoryName FROM category where idcategory="+str(idcat)+";")
            return self.dbCon.fetchone()[0]
        else:
            return "Category not found"

    def getPostsFromACategory(self,idcat):
        catDoc=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        if idcat in self.catgs:
            self.dbCon.execute("select post.file from category_link inner join post on category_link.entry=post.idblogEntry where category_link.cat="+str(idcat)+";")
            for fl in self.dbCon:
                catDoc.append(self.loc+sep+fl[0])
            return catDoc
        else:
            return "Category not found"