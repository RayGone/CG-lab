# -*- coding: utf-8 -*-
"""
cg_lab1.py
Created on Mon Nov 11 15:42:40 2019

@author: GRegAtom
"""

from primitives import * 
from graphics import *  

def getLineSegment():
    ax = input("Enter x co-ordinate for line A: ")    
    ay = input("Enter y co-ordinate for line A: ")
    
    p1 = Pointt(ax,ay)
    print(p1)
    p1.draw(win)
    
    
    ax = input("Enter x co-ordinate for line B: ")    
    ay = input("Enter y co-ordinate for line B: ")
        
    p2 = Pointt(ax,ay)
    print(p2)
    p2.draw(win)
    
    l1 = LineSegment(p1,p2)
    print(l1)
    l1.draw(win)
    return  l1


if __name__ == '__main__':
    print("********* Computational Geometry : Lab1 **************")
    print("Dimension of the canvas is 500x500")
    print()
    try:
        win = GraphWin("CG Lab1", 500, 500)
        l1 = getLineSegment()
        print('\nInsert point to compare: ')
        ax = int(input('insert x-co-ordinate: '))
        ay = int(input('insert y-co-ordinate: '))
        status = l1.where_does_this_point_lie(ax,ay)
        print('The given point lies "',status,'" the given line segment')
        p = Pointt(ax,ay)
        p.draw(win)
        input("Terminating.....")
        win.close()
    except:
        print("ERROR!!!!",sys.exc_info()[0])
        input("Terminating......")
        win.close()
