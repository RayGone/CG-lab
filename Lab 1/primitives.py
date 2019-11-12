# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:42:40 2019

@author: GRegAtom
"""
from graphics import *

class Pointt:
    xc = None
    yc = None

    def __init__(self,x=0, y=0):
        self.xc = int(x)
        self.yc = int(y)
        
    def __str__(self):
        return "This is a Point with co-ordinate ({},{})".format(self.xc,self.yc)
    
    def __repr__(self):
        return [self.xc,self.yc]
    
    @classmethod    
    def get_point_with(cls,x,y):
        cls.xc = int(x)
        cls.yc = int(y)
        return cls
    
    def draw(self,window,color='black'):
        c = Point(self.xc,self.yc)
        c.draw(window)
        

class LineSegment:
    Point_A = None
    Point_B = None
            
    def __init__(self,p1=None,p2=None):
        if(p1==None or p2==None):
            self.Point_A = Pointt()
            self.Point_B = Pointt()
        else:
            self.Point_A = p1
            self.Point_B = p2
        
    def __str__(self):
        return "This is an Line Segment with points A({},{}) and B({},{})".format(self.Point_A.xc,self.Point_A.yc,self.Point_B.xc,self.Point_B.yc)
           
    def __repr__(self):
        return [repr(self.Point_A),repr(self.Point_B)]
    
    @classmethod
    def get_linesegment_with(cls,p1,p2):
        cls.Point_A = p1
        cls.Point_B = p2
        return cls
    
    def draw(self,window,color='black'):
        c = Line(Point(self.Point_A.xc,self.Point_A.yc), Point(self.Point_B.xc,self.Point_B.yc))
        c.draw(window)
        
    def where_does_this_point_lie(self,x,y):
        if x==self.Point_A.xc and y==self.Point_A.yc:
            return 'start'
        elif x==self.Point_B.xc and y==self.Point_B.yc:
            return 'terminal'
        else:
            self.slope = (self.Point_B.yc-self.Point_A.yc)/(self.Point_B.xc-self.Point_A.xc)
            m = 0
            if x < self.Point_A.xc:
                m = (self.Point_A.yc-y)/(self.Point_A.xc-x)
            else :
                m = (y-self.Point_A.yc)/(x-self.Point_A.xc)
                
            if abs(self.slope-m) <= 0.01:
                if (self.Point_A.xc <= self.Point_B.xc and x>self.Point_A.xc and x<self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x<self.Point_A.xc and x>self.Point_B.xc):
                    return 'between'
                elif (self.Point_A.xc <= self.Point_B.xc and x > self.Point_A.xc and x > self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x < self.Point_A.xc and x < self.Point_B.xc):
                    return 'beyond'                
                elif (self.Point_A.xc <= self.Point_B.xc and x < self.Point_A.xc and x < self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x > self.Point_A.xc and x > self.Point_B.xc):
                    return 'behind'
                else:
                    return 'unknown A'
            else:
                return 'unknown B'
                