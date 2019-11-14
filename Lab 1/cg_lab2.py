# -*- coding: utf-8 -*-
"""
cg_lab2.py
Created on Thu Nov 14 21:49:09 2019
@author: GRegAtom
"""
from primitives import * 

if __name__ == '__main__':  
    print('\n\n')  
    print("********* cg_lab2.py **************")
    print("Dimension of the canvas is 500x500")
    print()
    
    try:
        win = GraphWin("CG Lab1", 500, 500)
        print('Input Line AB: \n')
        L = Operations.getLineSegmentFromInput()
        L.draw(win)
        print(L,'\n')
        
        print("Input Test point P:")
        P = Operations.getPointFromInput()
        P.draw(win)
        print(P,'\n')

        area = Operations.Three_Point_Area(L.Point_A,L.Point_B,P)
        where = Operations.where_is_it(L,P)
        print('Area of Triangle, joining point P to end points of line segment AB, is :', area)
        print('Point P is',where,' to line AB')
        print('Point P is collinear: ',Operations.isCollinear(L,P))
        
        input("Terminating.....")
        win.close()
    except AttributeError as e:
        print("ERROR!!!!",sys.exc_info()[0],e)
        input("Terminating......")
        win.close()
