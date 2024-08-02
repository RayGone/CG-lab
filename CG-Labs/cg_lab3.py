# -*- coding: utf-8 -*-
"""
cg_lab2.py
Created on Thu Dec 23 21:49:09 2019
@author: GRegAtom
"""
from primitives import *

#array is list of points and axis is 0=x-axis, 1= y-axis
def pointSort_linear(array,axis=0):
    if len(array)==0:
        return []

    if len(array) == 1:
        return array

    if len(array) == 2:
        if array[0][axis] <= array[1][axis] :
            return array
        else:
            return [array[1],array[0]] #swaping
    
    max_ax = array[0]
    for point in array:
        if(point[axis]>max_ax[axis]):
            max_ax = point

    center = max_ax[axis]/2
    left = []
    right = []
    for point in array:
        if point[axis]<=center:
            left.append(point)
        else:
            right.append(point)

    sorted_left = pointSort_linear(left,axis)
    sorted_right = pointSort_linear(right,axis)

    for point in sorted_right:
        sorted_left.append(point)

    return sorted_left


class polygon:
    vertex_list = []
    edge_list = []
    edge_vertex_maps = []
    vertex_list_size = 0
    _isConvex = False
    __curr_E_index = 0
    __curr_V_index = 0

    def __init__(self,vertex_list, edge_list=None):
        vertex_list_size = len(vertex_list)
        self.edge_vertex_maps = edge_list
        if vertex_list_size<3 :
                raise Exception('Not Enough Vertices in Vertex List. Only {} points given.'.format(vertex_list_size))
        
        self.vertex_list_size = vertex_list_size

        for x,y in vertex_list:
            self.vertex_list.append(Pointt(x,y))
            
        if edge_list!=None and len(edge_list) == vertex_list_size :
            for edge in edge_list:  
                self.edge_list.append(LineSegment(self.vertex_list[edge[0]],self.vertex_list[edge[1]]))
        else:
            self.sortCCW()
        
        self._isConvex = self.isConvex()

    def __str__(self):
        vl = []
        for point in self.vertex_list:
            vl.append([point.xc,point.yc])
        return "This is a Polygon with points: "+ vl.__str__()
    # ---------
    # doubly Linked list implementation
    # ---------
    def _next(self):
        self.curr_V_index = (self.curr_V_index+1)%self.vertex_list_size
        return self._current()

    def _prev(self):
        if(self.curr_V_index==0):
            self.curr_V_index = (self.vertex_list_size-1)%self.vertex_list_size
        else:
            self.curr_V_index = (self.curr_V_index-1)%self.vertex_list_size
        return self._current()

    def _nextEdge(self):
        self.curr_E_index = (self.curr_E_index+1)%self.vertex_list_size
        return self._currentEdge()

    def _prevEdge(self):
        if(self.curr_E_index==0):
            self.curr_E_index = (self.vertex_list_size-1)%self.vertex_list_size
        else:
            self.curr_E_index = (self.curr_E_index-1)%self.vertex_list_size
        return self._currentEdge()

    def _current(self):
        return self.vertex_list[self.curr_V_index]

    def _currentEdge(self):
        return self.edge_list[self.curr_E_index]


    # --------------------------

    def sortCCW(self):
        vl = []
        for point in self.vertex_list:
            vl.append([point.xc,point.yc])

        if not self.edge_vertex_maps or len(self.edge_vertex_maps) == 0:
            if True:
                center = vl[0]
                min_y = vl[0][1]
                # find the lowest y-axis point to mark it as divider
                for x,y in vl:
                    if  min_y>y:
                        min_y = y
                        center = [x,y]
                
                print(center)
                left = []
                right = []

                # separate vertices as left and right w.r.t the center point
                for x,y in vl:
                    if x < center[0]:
                        left.append([x,y])
                    if x > center[0]:
                        right.append([x,y])

                # sort left and right in ascending order
                left = pointSort_linear(left,1)
                left.reverse()
                right = pointSort_linear(right,1)
                # keep it in a linear array
                temp = []
                temp.append(Pointt(center[0],center[1]))
                for x,y in right:
                    temp.append(Pointt(x,y))
                for x,y in left:
                    temp.append(Pointt(x,y))

                self.vertex_list = temp

                #updating edge_list
                self.edge_list = []
                self.edge_vertex_maps = []
                for x in range(self.vertex_list_size):
                    self.edge_vertex_maps.append([x,(x+1)%self.vertex_list_size])
                    self.edge_list.append(LineSegment(self.vertex_list[x],self.vertex_list[((x+1)%self.vertex_list_size)]))

                return
            else:
                raise Exception('Edge List must be provided for non convex polygon.')
        else:
            pass

    def isConvex(self):
        previous = 'collinear'
        for x in range(self.vertex_list_size):
            # first point to be checked in third in the list
            vertex = self.vertex_list[(x+2)%self.vertex_list_size]
            edge = self.edge_list[x]

            status = Operations.turnTest(edge,vertex)

            if previous == 'collinear':
                previous = status
                continue

            if x==0:
                previous = status
                continue
            
            if status =='collinear':
                continue

            if previous != status:
                return False

        if previous == 'collinear':
            return False

        return True

    def PIT(self,point):
        if self._isConvex:
            if type(Pointt()) == type(point):
                prev_stat = Operations.turnTest(self.edge_list[0],point)

                if prev_stat == 'collinear':
                    return False

                for x in self.edge_list:
                    stat = Operations.turnTest(x,point)
                    if prev_stat != stat:
                        return False
                    
                return True
            
            return False
        else:
            # works for all polygons
            average_point = [0,0]
            for point in self.vertex_list:
                average_point[0] += point.xc
                average_point[1] += point.yc

            average_point = [average_point[0]/self.vertex_list_size,average_point[1]/self.vertex_list_size]

            angle = []
            for point in self.vertex_list:
                angle.append(math.atan2(point.xc-average_point[0],point.yc-average_point[1]),point)

            angle = sorted(angle,key=lambda a:a[0])
            

            raise Exception('Point Inclusion Test Cannot Be Performed on a Non-Convex Polygon')

    def RayCasting(self,point):
        hx_point = self.vertex_list[0]
        lx_point = self.vertex_list[0]

        for x in self.vertex_list:
            if x.xc>hx_point.xc:
                hx_point = x.clone()
            
            if x.xc<lx_point.xc:
                lx_point = x.clone()

        hx_point.xc += 20

        line = LineSegment(point,hx_point)
        # print('check point: ', line)
        # print(line)
        counter = 0
        for x in self.edge_list:
            stat = Operations.intersects(line,x)
            if stat == 'intersection':
                counter+=1

        print('number of intersections: ',counter)
        if counter == 0:
            return False

        if counter%2 == 0:
            return True
        
        return False




if __name__ == '__main__':  
    print('\n\n')  
    print("\t\t*********CG_ Lab3.py **************")
    print()
    
    try:
        # win = Grid("CG Lab1", 500, 500)
        while True:
            print('What do you want to do: ')
            print('\tInsert 1 to do turn test.\n\tInsert 2 to check intersection test.')
            print('\tInsert 3 for Polygon.\n\tInsert 0 to exit.\n')
            #\tInsert 3 to do Point Inclusion Test.\n\tInsert 4 to do Ray Casting Test.\n
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
                    print(L2,'\n')

                    print('Line 1 and Line 2: ', Operations.intersects(L1,L2), '\n\n')
                    if input('\n\nDo you want to check intersection of another line with line 1: ') != 'y':
                        print('\n\n')
                        break
            
            elif insert == '3':                
                print('\n\t\t*******Polygon Operations***********\n')
                strv = input('Insert Vertex List: ')
                import json
                Pn = polygon(json.loads(strv))
                print(Pn)    
                # print(Pn.vertex_list_size,len(Pn.vertex_list))            
                print('is the given polygon convex? ',Pn.isConvex(),'\n\n')
                P = Operations.getPointFromInput()
                
                while True:
                    print('\n\tinsert 1 for Point Inclusion Test.\n\tinsert 2 for ray casting.')
                    insert = input('insert: ')
                    if insert=='1':
                        stat = Pn.PIT(P)
                        if stat:
                            print('inside')
                        else:
                            print('outside')
                    elif insert=='2':
                        stat = Pn.RayCasting(P)
                        if stat:
                            print('given point is inside the polygon')
                        else:
                            print('given point is outside the polygon')
                    else:
                        break
                    if input('\n\nDo you want to do another test with same point: ') != 'y':
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

# p = polygon([[10,10],[50,20],[35,60],[15,40],[5,25]])
# print(p)
# print('is the given polygon convex? ',p.isConvex())
# if(p.isConvex()):
#     print(Pointt(20,35),'\nis the given point inside the polygon: ',p.PIT(Pointt(20,35)))

# print('Point Inclusion - Ray Casting: ',p.RayCasting(Pointt(20,35)))