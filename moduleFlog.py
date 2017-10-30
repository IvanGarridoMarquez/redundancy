# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:20:00 2017

@author: ivan
"""

import mysql.connector
from lxml import etree
import ConfigParser

def setConexion(db_user,db_password,db_host,db_database):
    cnx=mysql.connector.connect(user=db_user,password=db_password,host=db_host,database=db_database)
    return cnx
    

class Post:
    date=""
    author=""
    tags=[]
    cats=[]
    text=""
    title=""
    locfile=""
    dbID=0

    def __init__(self,myfile,dbRel=0):
        f=open(myfile)
        document = etree.fromstring(f.read())
        
        self.date=document.xpath("date/text()")
    #    print date[0]
        
        self.title=document.xpath("title/text()")
    #    print title[0]    
        
        self.author=document.xpath("author/text()")
    #   print author[0]
        
        self.tags=document.xpath("tags_set/tag/text()")
    #    for tag in tags:
    #        print tag.text
        
        self.cats=document.xpath("categories_set/category/text()")
    #    for cat in cats:
    #       print cat.text
            
        self.text=document.xpath("text/text()")[0]
    #    print text
        self.locfile=myfile
        self.dbID=dbRel
        f.close


class Blog:
    "Blog handling class"
    name=""
    idC=""
    catgs=[]
    keys=[]
    dbCon=0
    loc=""
    db_user=""
    db_password=""
    db_host=""
    db_database=""
    
    def __init__(self,nam):
        config=ConfigParser.RawConfigParser()
        config.read('flog.conf')
        self.db_user=config.get('DataBase', 'user')
        self.db_password=config.get('DataBase', 'password')
        self.db_host=config.get('DataBase', 'host')
        self.db_database=config.get('DataBase', 'database')
        corpus_loc=config.get('Corpus', 'corpus_dir')        
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        dbH=cnx.cursor()        
        
        if corpus_loc[-1:]!='/':
            corpus_loc+="/x"
        else:
            corpus_loc+="x"

        dbH.execute("SELECT idblog, blogName FROM blog where blogName='"+nam+"';")
        bx=dbH.fetchone()
        self.name=bx[1]
        self.idC=bx[0]
        self.loc=corpus_loc+nam+"/"
        dbH.execute("SELECT idcategory FROM category where blog="+str(self.idC)+";")
        for ct in dbH:
            self.catgs.append(ct[0])
        dbH.execute("SELECT idtag FROM tag where blog="+str(self.idC)+";")
        for tg in dbH:
            self.keys.append(tg[0])
        dbH.close()
            
    def getAllPostsFiles(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        postF=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        self.dbCon.execute("select post.file from post where blog="+str(self.idC))
        for pst in self.dbCon:
            postF.append(self.loc+sep+pst[0])
        self.dbCon.close()
        return postF
        
    def getAllCategoriesNames(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        cats=""
        catNam=[]
        for cat in self.catgs:
            cats+=str(cat)+","
        self.dbCon.execute("SELECT categoryName FROM category where idcategory in ("+cats[:-1]+");")
        for cN in self.dbCon:
            catNam.append(cN[0])
        self.dbCon.close()
        return catNam
        
    def getAllCategoriesFreq(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        cats=""
        catNam=[]
        for cat in self.catgs:
            cats+=str(cat)+","
        self.dbCon.execute("select category.categoryName, count(*) as freq, category.idcategory as catg from category_link inner join category on category_link.cat=category.idcategory where category.blog="+str(self.idC)+" group by category_link.cat order by freq desc;")
        for cN in self.dbCon:
            catNam.append(cN)
        self.dbCon.close()
        return catNam
        
    def setLocation(self,locdir):
        self.loc=locdir
        
    def getACategoryName(self,idcat):
        if idcat in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("SELECT categoryName FROM category where idcategory="+str(idcat)+";")
            name=self.dbCon.fetchone()[0]
            self.dbCon.close()
            return name
        else:
            return "Category not found"

    def getPostsFromACategory(self,idcat):
        catDoc=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        if idcat in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("select post.file, entry from category_link inner join post on category_link.entry=post.idblogEntry where category_link.cat="+str(idcat)+";")
            for fl in self.dbCon:
                catDoc.append([self.loc+sep+fl[0],fl[1]])
            self.dbCon.close()
            return catDoc
        else:
            return "Category not found"
            
    def getIntersectionSizeBetweenCatACatB(self,a,b):
        if a in self.catgs and b in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("select count(*) as i from category_link where cat="+str(a)+" and entry in (select entry from category_link where cat="+str(b)+");")
            interx=self.dbCon.fetchone()[0]
            self.dbCon.close()
            return int(interx)
        else:
            return "Category not found"
