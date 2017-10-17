# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:39:59 2017

@author: ivan
"""
from lxml import etree

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
