# -*- coding: utf-8 -*-
"""
cg_lab2.py
Created on Thu Nov 14 21:49:09 2019
@author: GRegAtom
"""
from primitives import *

if __name__ == '__main__':  
    print('\n\n')  
    print("\t\t********* cg_lab2.py **************")
    print("Dimension of the canvas is 500x500")
    print()
    
    try:
        # win = Grid("CG Lab1", 500, 500)
        while True:
            print('What do you want to do: ')
            print('\tInsert 1 to do turn test.\n\tInsert 2 to check intersection test.')
            print('\tInsert 0 to exit.\n')

            insert = input('insert: ')
            if insert == '1':
                print('\n\t\t*******Turn Test***********\n')
                print('Input Line AB: \n')
                L = Operations.getLineSegmentFromInput()
                # L.draw(win)
                print(L,'\n')
                
                while True:
                    print("Input Test point P:")
                    P = Operations.getPointFromInput()
                    # P.draw(win)
                    print(P,'\n')   

                    L2 = LineSegment(L.Point_B,P)
                    # L2.drawDashedLine(10,win)
                    # L.Point_A.draw(win)
                    # L.Point_B.draw(win)

                    area = Operations.Three_Point_Area(L.Point_A,L.Point_B,P)
                    where = Operations.turnTest(L,P)
                    print('Area of Triangle, joining point P to end points of line segment AB, is :', area)
                    print('Point P is',where,' to line AB')
                    print('Point P is collinear: ',Operations.isCollinear(L,P))
                    if input('\n\nDo you want to test with another: ') != 'y':
                        print('\n\n')
                        break
            
            elif insert == '2':
                print('\n\t\t*******Line Intersection Test***********\n')
                print('Input Line 1: \n')
                L1 = Operations.getLineSegmentFromInput()
                print(L1,'\n')

                while True:
                    print('Input Line 2: \n')
                    L2 = Operations.getLineSegmentFromInput()
                    print(L1,'\n')

                    print('Line 1 and Line 2: ', Operations.intersection_check(L1,L2), '\n\n')
                    if input('\n\nDo you want to check intersection of another line with line 1: ') != 'y':
                        print('\n\n')
                        break

            else:            
                print("Terminating.....")
                break
        # win.close()
    except AttributeError as e:
        print("ERROR!!!!",sys.exc_info()[0],e)
        input("Terminating......")
        win.close()
