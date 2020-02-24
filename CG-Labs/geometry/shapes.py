import math
from enum import Enum

# Type Enumerations
# ## --------------

# Point Polygon Classification
class PPC_Types(Enum):
    INSIDE=0
    BORDER=1
    OUTSIDE=-1

# Polygon Types
class PLG_Types(Enum):
    CONVEX = 0
    CONCAVE = 1
    NON = -1

class Intersect_Types(Enum):
    PROPER = 0
    IMPROPER = 1
    NON = -1
   
# Point Line Classification _ Types
class PLC_Types(Enum):
    # point line classification types
    COLLINEAR = 1
    LEFT = 2
    RIGHT = 3
    BEHIND = 5
    BEYOND = 6
    BETWEEN = 7
    START = 8
    END = 9
    NON_COLLINEAR = 0


# Geometries Classes
class point:
    _x = 0
    _y = 0

    def __init__(self,x=0,y=0):
        self._x = int(x)
        self._y = int(y)

    # Setter Methods
    def setXY(self,x: int ,y: int):        
        self._x = int(x)
        self._y = int(y)

    def setX(self,x):     
        self._x = int(x)

    def setY(self,y):
        self._y = int(y)

    def setPoint(self,pt):
        if(type(pt) == type(list()) or type(pt) == type(tuple())):
            self._x = pt[0]
            self._y = pt[1]
        
        if(type(pt) == type({})):
            self._x = pt['x']
            self._y = pt['y']


    # Getter Methods
    def getXY(self):
        return self._x,self._y
    def getX(self):
        return self._x 
    def getY(self):
        return self._y 
    def getList(self):
        return [self._x,self._y]
    def getDict(self):
        return {"x":self._x,"y":self._y}

    def __str__(self):
        return "({},{})".format(self._x,self._y)

# --------------------------------
class line:
    _start = point(0,0)
    _end = point(0,0)

    def __init__(self,p1 = point(0,0),p2 = point(0,0)):
        if(type(p1)==type(point()) and type(p2)==type(point())):
            self._start = p1
            self._end = p2
        

    # setter methods
    def setPointAB(self,start,end):
        self._start = start
        self._end = end
    def setXY(self,x1,y1,x2,y2):
        self.setStartXY(x1,y2)
        self.setEndXY(x2,y2)
    def setStartPoint(self,start):
        if(type(start) == type(point())):
            self._start = start
    def setEndPoint(self,end):
        if(type(end) == type(point())):
            self._end = end
    def setEndXY(self,x,y):
        self._end = point(x,y)
    def setStartXY(self,x,y):
        self._start = point(x,y)

    # getter methods
    def getStartPoint(self):
        return self._start
    def getStartXY(self):
        return self._start._x,self._start._y
    def getEndPoint(self):
        return self._end
    def getEndXY(self):
        return self._end._x,self._end._y
    def getList(self):
        return [[self._start._x,self._start._y],[self._end._x,self._end._y]]
    def getDict(self):
        return {"start":{"x":self._start._x,"y":self._start._y},"end":{"x":self._end._x,"y":self._end._y}}
    # others
    def reverse(self):
        return line(self._end,self._start)

    def __str__(self):
        return "[start{},end{}]".format(self._start,self._end)

class polygon:
    length = 0
    _edge = []
    _vertex = []
    isInitialized = False
    _type = PLG_Types.NON
    _isSimple = False
    __curr_E_index = 0
    __curr_V_index = 0
    edge_vertex_maps = []
    _direction = False
    _ref_turn = PLC_Types.RIGHT # clockwise ordering of vertex and edge

    def __init__(self):
        self._edge = []
        self._vertex = []

    def __updateEdgeTable(self):
        self.__init_index()
        self._edge = [] # re-initialize
        # update _edge using _vertex
        counter = 0
        
        current_vertex = self._current()
        next_vertex = self._next()
        while(counter<self.length):
            l = line(current_vertex,next_vertex)
            self._edge.append(l)
            current_vertex = next_vertex
            next_vertex = self._next()
            # print(counter,self.__curr_V_index)
            counter += 1
        

    def __updateVertexTable(self):
        self._vertex = [] # re-initialize
        # update _vertex using _edge
        for edge in self._edge:
            self._vertex.append(edge._start)
        
    def __initialize_with_vertex_list(self,vertex_list,edge_vertex_map=[]):
        for pt in vertex_list:
            self._vertex.append(pt)
        self.length = len(vertex_list)
        self.sortCCW()
        if(self.isConvex()):
            self.__updateEdgeTable()
            self._isSimple = True
            self.isInitialized = True
            return
        else:
            if(len(edge_vertex_map)==0):
                self.__updateEdgeTable()
                self.isInitialized = True
                # if polygon is not convex
                # we have to determine if it is simple polygon or not

                self.__init_index()
                # first step to determine if it is simple polygon or not is to check for intersection
                counter = 0
                current = self._currentEdge()
                self._nextEdge()
                while(True):
                    test = self._nextEdge()
                    if(str(test) == str(current)):
                        current = self._nextEdge() 
                        self._nextEdge()
                        test = self._nextEdge()
                        # print(test,current)
                        counter += 1
                        if(counter == self.length):
                            # survived all the tests
                            self._isSimple = True
                            break
                    status = intersection(current,test)
                    if(status == Intersect_Types.PROPER):
                        self._isSimple = False
                        break
                # ------------------------
                # second step is to check for holes
                # ----
                ### don't know how to do that
                # ----
                if(self._isSimple):
                    self.SubConvexPolygonization()
                # return
            else:
                list_line = []
                # print('arr')
                for arr in edge_vertex_map:
                    list_line.append(line(vertex_list[arr[0]-1],vertex_list[arr[1]-1]))
                self.__initialize_with__edge(list_line)

    def __initialize_with__edge(self,edge: line):
        for l in edge:
            self._edge.append(l)
        self.__updateVertexTable()

        if(self.isConvex()):
            self._isSimple = True
        else:             
            # if polygon is not convex
            # we have to determine if it is simple polygon or not
            self.__init_index()
            # first step to determine if it is simple polygon or not is to check for intersection
            counter = 0
            current = self._currentEdge()
            self._nextEdge()
            while(True):
                test = self._nextEdge()
                if(str(test) == str(current)):
                    current = self._nextEdge() 
                    self._nextEdge()
                    test = self._nextEdge()
                    # print(test,current)
                    counter += 1
                    if(counter == self.length):
                        # survived all the tests
                        self._isSimple = True
                        break
                status = intersection(current,test)
                if(status == Intersect_Types.PROPER):
                    # print('this place')
                    self._isSimple = False
                    break
        self.isInitialized = True

    def initialize(self,array,edge=False,ve_map=[]):
        # if edge is true then array contains edge list, else vertex list
        self._vertex = []
        self._edge = []
        if(edge):
            self.__initialize_with__edge(array)
        else:
            # print('initializing with vertex')
            self.__initialize_with_vertex_list(array,ve_map)
        self.isInitialized = True

    def getVertex(self,i):
        return self._vertex[i]

    def __str__(self):
        vl = []
        for p in self._vertex:
            vl.append([p._x,p._y])
        el = []
        for l in self._edge:
            el.append(str(l))
        return "{}\"points\": {}".format('{',vl)+ ",\"lines\": {}{}".format(el,'}')
    # ---------
    # doubly Linked list implementation
    # ---------
    def _next(self):
        self.__curr_V_index = (self.__curr_V_index+1)%self.length
        return self._current()

    def _prev(self):
        if(self.__curr_V_index==0):
            self.__curr_V_index = (self.length-1)%self.length
        else:
            self.__curr_V_index = (self.__curr_V_index-1)%self.length
        return self._current()

    def _nextEdge(self):
        self.__curr_E_index = (self.__curr_E_index+1)%self.length
        return self._currentEdge()

    def _prevEdge(self):
        if(self.__curr_E_index==0):
            self.__curr_E_index = (self.length-1)%self.length
        else:
            self.__curr_E_index = (self.__curr_E_index-1)%self.length
        return self._currentEdge()

    def _current(self):
        return self._vertex[self.__curr_V_index]

    def _currentEdge(self):
        return self._edge[self.__curr_E_index]

    def __init_index(self):
        self.__curr_V_index = 0
        self.__curr_E_index = 0
        
    def __init_index_VtoE(self):
        self.__curr_V_index = self.__curr_E_index

    def __init_index_EtoV(self):
        self.__curr_E_index = self.__curr_V_index

    # --------------------------
    # if center_axis is 1, then center point is calculated as mid point of extreme x-axis
    # other_wise it is taken along y-axis
    # but for sorting purpose y-axis is used when center_axis =1, and vice-versa
    # The polygon is thus sorted along the center_axis such that, vertex_table of polygon
    # if printed sequentially will form a bounding box (edges from the vertex).
    def sortCCW(self,center_axis = 1):
        vl = []
        for p in self._vertex:
            vl.append(p.getList())

        if True:
            center = 0
            ext_up = 0
            ext_low = 0
            # find the lowest y-axis point to mark it as divider
            for x,y in vl:
                if  ext_low > y:
                    ext_low = y if center_axis == 0 else x
                if  ext_up < y:
                    ext_up = y if center_axis == 0 else x
            
            center = math.ceil((ext_up+ext_low)/2)
            # print(center,"center")
            left = []
            right = []
            # separate vertices as left and right w.r.t the center point
            for x,y in vl:
                if center_axis == 1:
                    if x < center:
                        left.append([x,y])
                    if x >= center: #because we use ceiling function for center
                        right.append([x,y])

                else:
                    if y < center:
                        left.append([x,y])
                    if y >= center: #because we use ceiling function for center
                        right.append([x,y])

            # print(left,right,"left-right--- before sorting")
            # sort left and right in ascending order
            left = pointSort_linear(left,center_axis)            
            right = pointSort_linear(right,center_axis)
            # print(left,right,"left-right--------\n")
            right.reverse()
                
            # print(left,right,"left-right--------after reverse\n")
            # keep it in a linear array
            temp = []
            for x,y in left:
                temp.append(point(x,y))
            for x,y in right:
                temp.append(point(x,y))

            self._vertex = temp
            self.__updateEdgeTable()
            return
        else:
            pass

    def isConvex(self):
        previous = PLC_Types.COLLINEAR
        for x in range(self.length):
            # first point to be checked in third in the list
            vertex = self._vertex[(x+2)%self.length]
            edge = self._edge[x]

            status = TurnTest(edge,vertex)

            # for the first point as we have pre-assumed previous to be COLLINEAR
            if previous == PLC_Types.COLLINEAR:
                previous = status
                continue
            
            # if the next point is COLLINEAR then it is still convex so just move ahead
            # and preserving the turn of previous to compare with next point because
            # we won't be able to decide if a polygon is convex by comparing turn of next point with COLLINEAR turn
            if status == PLC_Types.COLLINEAR:
                continue

            # if the previous NON-COLLINEAR turn doesn't match with current NON-COLLINEAR turn.
            # then we can simply conclude that the polygon is not convexs
            if previous != status:                
                self._type = PLG_Types.CONCAVE
                return False

        # previous remains unchanged, then it implies that the given point is rather a line
        if previous == PLC_Types.COLLINEAR:
            self._type = PLG_Types.NON
            return False

        # if the given set of points passes all the conditions then it is convex
        self._type = PLG_Types.CONVEX

        return True

    # Transforms Simple Concave Polygon to Multiple sub-convex polygons
    def SubConvexPolygonization(self):
        if(self._isSimple and self._type==PLG_Types.CONCAVE):
            self.__init_index()
            self._sub_polygons = []
            
            pts = []
            queue = self._edge.copy()
            #reference turn for condition
            while(len(queue)!=0):
                cline = queue.pop(0) # current line
                cpoint = None
                if(len(queue)==0):
                    cpoint = pts[0]._end
                else:
                    cpoint = queue[0]._end # current point; in turn test it is the end of next line
                
                turn = TurnTest(cline,cpoint)
                
                # print(cline,cpoint,self._ref_turn,turn)
                buffer = []
                # if turn is collinear, move to next untill turn other than collinear is found
                while(turn == PLC_Types.COLLINEAR):
                    buffer.append(cline)                    
                    cline = queue.pop(0)
                    cpoint = queue[0]._end
                    turn = TurnTest(cline,cpoint)

                if(self._ref_turn != turn):
                    # if turn doesn't match
                    if(len(pts) == 0):
                        # if there is no points in pts, then append the points in buffer back to queue
                        # it is because we can't use those points to make a convex sub-polygon                        
                        if len(buffer)>0:
                            queue.extend(buffer)
                        # if it is begining of next sub-polygon search
                        while True:
                            # untill self._ref_turn doesn't match, switch to next line and next point as current
                            queue.insert(-1,cline)
                            cline = queue.pop(0)
                            cpoint = queue[0]._end
                            turn = TurnTest(cline,cpoint)
                            if(self._ref_turn == turn):
                                # if turn matches break the loop
                                break
                    else:
                        # if there are edges in buffer , which were collinear, 
                        if len(buffer)>0:
                            pts.extend(buffer)

                        # Now we take turnTest of cline with starting point of each line in pts sequentially
                        ## We take turnTest untill turn is not equal to self._ref_turn
                        ## and break out of while loop when we find turn equal to self._ref_turn
                        while TurnTest(cline,pts[0]._start) != self._ref_turn:
                            ### if turnTest is not equal to self._ref_turn
                            ### pop the line out of pts and push it to queue
                            queue.append(pts.pop(0))
                            
                            #### if pts becomes empty break out of the loop
                            if len(pts) == 0:
                                break

                        # if pts is empty continue to start again  
                        if len(pts) == 0:
                            continue
                        # else:                        
                        # if pts is not empty, then cut out the convex sub-polygon from available line in pts.
                        new_line = line(cline._end,pts[0]._start) # make new line by joining point end of current line and start point of first line in pts
                        # print(new_line)
                        queue.append(new_line.reverse()) # append new_line to the queue
                        pts.extend([cline,new_line]) # add the lines to pts
                        temp_points = []
                        for ln in pts:
                            temp_points.append(ln._start)

                        tmp_plg = polygon()
                        tmp_plg.initialize(temp_points)
                        self._sub_polygons.append(tmp_plg) # make a polygon and add it to sub_polygons
                        # print(self._sub_polygons[-1],'sub-polygon')
                        pts = [] # re-initializing
                        # pass
                    
                if(self._ref_turn == turn):
                    if len(buffer)>0:
                        pts.extend(buffer)
                    pts.append(cline)

                    if(len(queue) == 0):
                        temp_points = []
                        for ln in pts:
                            temp_points.append(ln._start)
                            
                        tmp_plg = polygon()
                        tmp_plg.initialize(temp_points)
                        self._sub_polygons.append(tmp_plg) # make a polygon and add it to sub_polygons
                        
            # print(len(self._sub_polygons),"number of sub polygons")
            
        else:
            if(not self._isSimple):
                raise Exception('Can not perform sub convex polygonization of non-simple polygon')
            if(self._type==PLG_Types.CONVEX):
                self._sub_polygons = [polygon().initialize(self._vertex)]
    # ----------------------------------------------

    # Point Inclusion Test
    def PIT(self,pt):
        if self._isSimple:
            if self._type == PLG_Types.CONVEX:
                if type(point()) == type(pt):
                    for x in self._edge:
                        turn = TurnTest(x,pt)
                        print('turn',turn,x,pt)
                        if turn == PLC_Types.COLLINEAR:
                            return PPC_Types.BORDER
                        elif turn != self._ref_turn:
                            return PPC_Types.OUTSIDE
                        
                    return PPC_Types.INSIDE
                
                # here better raise an exception
                return PPC_Types.OUTSIDE
            else:
                # works for all polygons
                for sub_plg in self._sub_polygons:
                    print(sub_plg)
                    ppc = sub_plg.PIT(pt)
                    print(ppc)
                    if ppc != PPC_Types.OUTSIDE:
                        return ppc

                # since conditions didn't meet
                return PPC_Types.OUTSIDE
                

        else:
            raise Exception('Point Inclusion Test Cannot Be Performed on a Non-Simple Polygon')

    def RayCasting(self,p):
        hx_point = self._vertex[0]
        lx_point = self._vertex[0]

        for x in self._vertex:
            if x._x>hx_point._x:
                hx_point = x.clone()
            
            if x._x<hx_point._x:
                lx_point = x.clone()

        hx_point._x += 20

        l = line(point,hx_point)
        # print('check point: ', line)
        # print(line)
        counter = 0
        for x in self._edge:
            stat = intersection(l,x)
            if stat == 'intersection':
                counter+=1

        # print('number of intersections: ',counter)
        if counter == 0:
            return False

        if counter%2 == 0:
            return True
        
        return False


class Reader:
    pass


"""
    Functions
"""

def Three_Point_Area(a: point,b: point,c: point):   
    # calculating area of triangle formed by joining point c to end points of line ab.
    # i.e. the point in observation is point is 'c', and reference point is point 'b'.      
    A = b._x*(a._y-c._y)
    B = a._x*(c._y-b._y)
    C = c._x*(b._y-a._y)
     
    area = (A+B+C)/2
    return area

def Line_Point_Area(l: line,p: point):
    return Three_Point_Area(l._start,l._end,p)


# Point Line Classification
def PLC(l: line,p: point):    
    if (l._start._x == p._x and l._start._y == p._y): 
        return PLC_Types.START

    if (l._end._x == p._x and l._end._y == p._y):
        return PLC_Types.END

    area = Line_Point_Area(l,p)
    
    if area==0:
        if l._start._x == l._end._x:#if line is orthogonal line
            if l._start._y > p._y and l._end._y > p._y:
                return PLC_Types.BEHIND
            elif l._start._y < p._y and l._end._y < p._y:
                return PLC_Types.BEYOND
            else:
                return PLC_Types.BETWEEN
        else:#if line is not orthogonal
            if l._start._x > p._x and l._end._x > p._x:
                return PLC_Types.BEHIND
            elif l._start._x < p._x and l._end._x < p._x:
                return PLC_Types.BEYOND
            else:
                return PLC_Types.BETWEEN

# here start point of line is observation point, end point of line is reference point
# input point p is the point that is observed.
def TurnTest(l: line,p: point):
    if type(l)!=type(line()):
        raise ValueError('Object of class line expected.')
    if type(p)!=type(point()):
        raise ValueError('Object of class point expected.')
    
    area = Line_Point_Area(l ,p)

    if area<0:
        return PLC_Types.LEFT
    elif area>0:
        return PLC_Types.RIGHT
    else:
        return PLC_Types.COLLINEAR

# -------------------------------
def isCollinear(l: line,p: point):
    if type(l)!=type(line()):
        return PLC_Types.NON_COLLINEAR
    if type(p)!=type(point()):
        return PLC_Types.NON_COLLINEAR
    
    area = Line_Point_Area(l,p)    
    if area==0:
        return PLC_Types.COLLINEAR
        
    return PLC_Types.NON_COLLINEAR 
 
# ---------------------------------------
def intersection(line1: line,line2: line):
    test_a1 = TurnTest(line1,line2._start)
    # if collinear 
    if test_a1 == PLC_Types.COLLINEAR:
        temp = PLC(line1,line2._start)
        if (temp == PLC_Types.BETWEEN):
            return Intersect_Types.PROPER
        # and end-point then intersection is improper
        if (temp == PLC_Types.END or temp == PLC_Types.START):
            return Intersect_Types.IMPROPER

        temp = PLC(line2,line1._start)
        if (temp == PLC_Types.BETWEEN):
            return Intersect_Types.PROPER
        if (temp == PLC_Types.END or temp == PLC_Types.START):
            return Intersect_Types.IMPROPER

    test_b1 = TurnTest(line1,line2._end)
    # if collinear 
    if test_b1 == PLC_Types.COLLINEAR:
        temp = PLC(line1,line2._end)
        if (temp == PLC_Types.BETWEEN):
            return Intersect_Types.PROPER
        # and end-point then intersection is improper
        if (temp == PLC_Types.END or temp == PLC_Types.START):
            return Intersect_Types.IMPROPER
        
        temp = isCollinear(line2,line1._end)
        # print(temp)
        if (temp == PLC_Types.BETWEEN):
            return Intersect_Types.PROPER
        if (temp == PLC_Types.END or temp == PLC_Types.START):
            return Intersect_Types.IMPROPER

    # not collinear but same so no intersection
    if test_a1 == test_b1:
        return Intersect_Types.NON

    test_a2 = TurnTest(line2,line1._start)
    test_b2 = TurnTest(line2,line1._end)

    # if the turn test doesn't match with change in reference point for observation then there is a proper intersection
    if test_a1 != test_a2 and test_b1 != test_b2:
        return Intersect_Types.PROPER

    return Intersect_Types.NON

# for polygon; array = vertex_list
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
    min_ax = array[0]
    for pt in array:
        if(pt[axis]>max_ax[axis]):
            max_ax = pt
        if(pt[axis]<min_ax[axis]):
            min_ax = pt

    center = math.ceil((max_ax[axis]+min_ax[axis])/2)
    left = []
    right = []
    for pt in array:
        if pt[axis] < center:
            left.append(pt)
        else:
            right.append(pt)

    sorted_left = []
    # print(right)
    if len(left)>0:
        sorted_left = pointSort_linear(left,axis)

    sorted_right = []
    if len(right)>0:
        sorted_right = pointSort_linear(right,axis) 

    return sorted_left+sorted_right

if __name__ == '__main__':
    # print(__name__)
    # print(point())
    # print(line())
    # print(PLC_Types.COLLINEAR)
    # print(type(list()))
    # print(type(line()))
    
    vertex_table = [point(7,4),point(5,1),point(2,1),point(5,5),point(6,7),point(1,3),point(2,5)] # concave-simple
    # vertex_table = [point(7,4),point(5,2),point(2,1),point(6,7),point(1,3),point(2,5)] # convex-simple
    
    # edge_vertex_mapping = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
    plg = polygon()
    plg.initialize(vertex_table)
    print(plg)
    print(plg._isSimple,plg._type)
    print(plg.PIT(point(3,1)))
    # print(plg.SubConvexPolygonization())
    # print(intersection(line(point(6,7),point(5,5)),line(point(5,2),point(2,1))))
    # print(TurnTest(line(point(6,7),point(5,5)),point(5,2)))
    # # print(Three_Point_Area(point(5,2),point(2,1),point(1,3)))
    # print(Line_Point_Area(line(point(5,2),point(7,4)),point(6,7)))
