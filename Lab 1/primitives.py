# -*- coding: utf-8 -*-
"""
primitives.py
Created on Mon Nov 11 15:42:40 2019

@author: GRegAtom
"""
from graphics import *
import math

# =============================================================================
# class Pointt and LineSegment is build as part of Lab1:
# =============================================================================
    
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
        return {"Point_A":repr(self.Point_A),"Point_B":repr(self.Point_B)}
    
    @classmethod
    def get_linesegment_with(cls,p1,p2):
        cls.Point_A = p1
        cls.Point_B = p2
        return cls
    
    def BresenhamLine(self):   
        point_list = []
        
        dx = self.Point_A.xc - self.Point_B.xc
        dy = self.Point_A.yc - self.Point_B.yc
        stepx = 0
        stepy = 0
        xc = self.Point_A.xc
        yc = self.Point_A.yc
        point_list.append([xc,yc])
        if dy<0:
            dy = -dy
            stepy = 1
        else:
            stepy = -1
        
        if dx<0:
            dx = -dx
            stepx = 1
        else:
            stepx = -1

        dy = 2*dy
        dx = 2*dx

        if dx>dy:
            fraction = dy-math.ceil(dx/2)
            for x in range(int(abs(dx/2))):
                xc = xc + stepx
                if fraction>=0:
                    yc = stepy+yc
                    fraction = fraction - dx
                fraction = fraction + dy
                x
                point_list.append([xc,yc])
        else:
            # print('else')
            fraction = dx-math.ceil(dy/2)
            for y in range(int(abs(dy/2))):
                if fraction>=0:
                    xc = stepx+xc
                    fraction = fraction - dy
                yc = yc+stepy
                fraction = fraction + dx
                y
                point_list.append([xc,yc])
        return point_list

    def dashedLine(self,spacing=5):
        #----creating list of lines to 
        point_list = self.BresenhamLine()
        list_of_lines = []
        if len(point_list) > (2*spacing):
            number_of_points = len(point_list)
            number_of_breakpoints = math.floor(number_of_points/spacing)                
            if number_of_breakpoints%2 == 0:#if even number of breakpoints
                # print('even')
                for x in range(number_of_breakpoints):
                    if x%2==0:
                        line = LineSegment(Pointt(point_list[0][0],point_list[0][1]),Pointt(point_list[2][0],point_list[2][1]))
                        list_of_lines.append(line)
                        continue
                    start_point = x*spacing
                    end_point = (x+1)*spacing
                    p1 = Pointt(point_list[start_point][0],point_list[start_point][1])
                    if x==number_of_breakpoints-1:                        
                        p2 = Pointt(point_list[len(point_list)-1][0],point_list[len(point_list)-1][1])
                    else:
                        p2 = Pointt(point_list[end_point][0],point_list[end_point][1])
                    line = LineSegment(p1,p2)
                    list_of_lines.append(line)

            else:#if odd number of breakpoints
                # print('odd')
                for x in range(number_of_breakpoints):
                    if x%2!=0: 
                        continue
                    start_point = x*spacing
                    end_point = (x+1)*spacing
                    p1 = Pointt(point_list[start_point][0],point_list[start_point][1])
                    if x==number_of_breakpoints-1:                        
                        p2 = Pointt(point_list[len(point_list)-1][0],point_list[len(point_list)-1][1])
                    else:
                        p2 = Pointt(point_list[end_point][0],point_list[end_point][1])
                    line = LineSegment(p1,p2)
                    list_of_lines.append(line)
            
            return list_of_lines
        else:
            return [self]

    def drawDashedLine(self,spacing,window):
        line_list = self.dashedLine(spacing)

        line_list[0].Point_A.draw(window)
        line_list[len(line_list)-1].Point_B.draw(window)

        for x in range(len(line_list)):
            line_list[x].draw(window)    


    def draw(self,window,color='black'):
        c = Line(Point(self.Point_A.xc,self.Point_A.yc), Point(self.Point_B.xc,self.Point_B.yc))
        c.draw(window)

    def where_does_this_point_lie(self,x,y):        
        if(self.Point_A.xc==self.Point_B.xc):#x-co-ordinate is same
            if(self.Point_A.yc==self.Point_B.yc):#if both ends, point A and point B, is same point
                return "A==B"
            else:#if line is vertical line
                if x==self.Point_A.xc:#if given point is part of the line
                    if y>self.Point_A.yc and y>self.Point_B.yc:
                        return 'beyond'
                    elif y<self.Point_A.yc and y<self.Point_B.yc:
                        return 'behind'
                    else:
                        return 'between'  
                else:
                    return 'unknown 0'
        elif x==self.Point_A.xc and y==self.Point_A.yc:#checking if the point is Point_A of linesegment
            return 'start'
        elif x==self.Point_B.xc and y==self.Point_B.yc:#checking if the point is Point_B of linesegment
            return 'terminal'
        else:#checking if the point lies in the line of the given linesegment
            self.slope = (self.Point_B.yc-self.Point_A.yc)/(self.Point_B.xc-self.Point_A.xc)
            m = 0
            #calculating slope of linesegment of Point_A and given point
            if x < self.Point_A.xc:
                m = (self.Point_A.yc-y)/(self.Point_A.xc-x)
            else :
                m = (y-self.Point_A.yc)/(x-self.Point_A.xc)
                
            #checking if slope matches with error 0.01    
            if abs(self.slope-m) <= 0.01:
                #checking if point lies within the lineseggment
                if (self.Point_A.xc <= self.Point_B.xc and x>self.Point_A.xc and x<self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x<self.Point_A.xc and x>self.Point_B.xc):
                    return 'between'
                #checking if point lies beyond the linesegment
                elif (self.Point_A.xc <= self.Point_B.xc and x > self.Point_A.xc and x > self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x < self.Point_A.xc and x < self.Point_B.xc):
                    return 'beyond' 
                #checking if point lies behind the linesegment
                elif (self.Point_A.xc <= self.Point_B.xc and x < self.Point_A.xc and x < self.Point_B.xc) or (self.Point_A.xc > self.Point_B.xc and x > self.Point_A.xc and x > self.Point_B.xc):
                    return 'behind'
                else:
                    return 'unknown A'
            else:
                return 'unknown B'
   
# =============================================================================
# class Operations and its functions:
# getPointFromInput ,Three_Point_Area, isCollinear and where_is_it 
# are build as part of lab2:
# =============================================================================
    
class Operations:
    @staticmethod
    def getPointFromInput():
        val = input("point(x,y): ")
        if val.find(','):
            coords = val.split(',')
            if len(coords)==2:
                if coords[0].isdigit() and coords[1].isdigit():
                    p = Pointt(coords[0],coords[1])
                    return p
                else:
                    print('co-ordinates must be integers')
                    return Operations.getPointFromInput()    
            else:
                print("Input x and y co-ordinate of the point in the form x,y: ")
                return Operations.getPointFromInput()               
        else:            
            print("Input x and y co-ordinate of the point in the form x,y: ")
            return Operations.getPointFromInput()            
        # print(val,type(val))
        
    @staticmethod
    def getLineSegmentFromInput():
        print("Input start point of the line, A:")
        p1 = Operations.getPointFromInput()
        print()
        print("Input terminal point of the line, B:")
        p2 = Operations.getPointFromInput()
        print()
        return LineSegment(p1,p2)
        
        
    @staticmethod
    def Three_Point_Area(a: Pointt,c: Pointt,b: Pointt):   
        #calculating area of triangle formed by joining point b to end points of line ac     
        A = a.xc*(b.yc-c.yc)
        B = b.xc*(c.yc-a.yc)
        C = c.xc*(a.yc-b.yc)
        
        area = (A+B+C)/2
        return area
    
    @staticmethod
    def isCollinear(line: LineSegment,point: Pointt):
        if type(line)!=type(LineSegment()):
            return 'notlinesegment'
        if type(point)!=type(Pointt()):
            return 'notpointt'
        
        area = Operations.Three_Point_Area(line.Point_A,line.Point_B,point)
        
        if area==0:
            if line.Point_A.xc==line.Point_B.xc:#if line is vertical line
                if line.Point_A.yc>point.yc and line.Point_B.yc>point.yc:
                    return 'behind'
                elif line.Point_A.yc<point.yc and line.Point_B.yc<point.yc:
                    return 'beyond'
                else:
                    return 'between'
            else:#if line is not vertical
                if line.Point_A.xc>point.xc and line.Point_B.xc>point.xc:
                    return 'behind'
                elif line.Point_A.xc<point.xc and line.Point_B.xc<point.xc:
                    return 'beyond'
                else:
                    return 'between'
        else:
            return False  
        
    @staticmethod
    def where_is_it(line: LineSegment,point: Pointt):
        if type(line)!=type(LineSegment()):
            return 'notlinesegment'
        if type(point)!=type(Pointt()):
            return 'notpointt'
        
        area = Operations.Three_Point_Area(line.Point_A ,line.Point_B ,point)
        # =============================================================================
        # here the logic is opposite to actual co-ordinate geometry
        # and it is because in co-ordinate geometry, y-axis goes-up-increasing
        # where in computer-graphics, y-axis goes-down-increasing
        # =============================================================================
        if area<0:
            return 'right'
        elif area>0:
            return 'left'
        else:
            return 'collinear'
        


if __name__ == '__main__':
    print("********* primitives.py **************")
    print("Dimension of the canvas is 500x500")
    print()
    try:
        pass
        win = GraphWin("graph primitives", 500, 500)
        line = LineSegment(Pointt(200,20),Pointt(250,250))
        line.draw(win)
        line.Point_A.draw(win)
        line.Point_B.draw(win)

        point = Pointt(0,100)
        point.draw(win)

        line2 = LineSegment(line.Point_B,point)
        line2.drawDashedLine(5,win)
        # line2.draw(win)

        line2.Point_A.draw(win)
        line2.Point_B.draw(win)
        stat = Operations.where_is_it(line,point)  
        print(stat) 
        input()
        win.close()
    except GraphicsError as e:
        print("ERROR!!!!",sys.exc_info()[0],e)
        win.close()