import math

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

    def setPoint(self,point):
        if(type(point) == type(list()) or type(point) == type(tuple())):
            self._x = point[0]
            self._y = point[1]
        
        if(type(point) == type({})):
            self._x = point['x']
            self._y = point['y']


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
    def __str__(self):
        return "[start{},end{}]".format(self._start,self._end)


class polygon:
    length = 0
    _edge = []
    _vertex = []
    isInitialized = False
    _isConvex = True 
    __curr_E_index = 0
    __curr_V_index = 0
    edge_vertex_maps = []

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
        
    def __initialize_with_vertex_list(self,vertex_list):
        for point in vertex_list:
            self._vertex.append(point)

        self.length = len(vertex_list)
        self.__updateEdgeTable()
        self.isInitialized = True

    def __initialize_with__edge(self,edge: line):
        for l in edge:
            self._vertex.append(l)
        self.__updateVertexTable()
        self.isInitialized = True

    def initialize(self,array,edge=False):
        # if edge is true then array contains edge list, else vertex list
        self._vertex = []
        self._edge = []
        if(edge):
            self.__initialize_with__edge(array)
        else:
            self.__initialize_with_vertex_list(array)
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
        return "This is a Polygon with points: {}".format(vl)+ "\nlines: {}".format(el)
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
            print(center,"center")
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
            print(left,right,"left-right--------\n")
            right.reverse()
                
            print(left,right,"left-right--------after reverse\n")
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
        previous = 'collinear'
        for x in range(self.length):
            # first point to be checked in third in the list
            vertex = self._vertex[(x+2)%self.length]
            edge = self._edge[x]

            status = TurnTest(edge,vertex)

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

    # Point Inclusion Test
    def PIT(self,pt):
        if self._isConvex:
            if type(point()) == type(pt):
                prev_stat = TurnTest(self._edge[0],pt)

                if prev_stat == 'collinear':
                    return False

                for x in self._edge:
                    stat = TurnTest(x,pt)
                    if prev_stat != stat:
                        return False
                    
                return True
            
            return False
        else:
            # works for all polygons
            average_point = [0,0]
            for point in self._vertex:
                average_point[0] += p._x
                average_point[1] += p._y

            average_point = [average_point[0]/self.length,average_point[1]/self.length]

            angle = []
            for point in self._vertex:
                angle.append(math.atan2(p._x-average_point[0],p._y-average_point[1]),point)

            angle = sorted(angle,key=lambda a:a[0])
            

            raise Exception('Point Inclusion Test Cannot Be Performed on a Non-Convex Polygon')

    def RayCasting(self,point):
        hx_point = self._vertex[0]
        lx_point = self._vertex[0]

        for x in self._vertex:
            if x._x>hx_p._x:
                hx_point = x.clone()
            
            if x._x<lx_p._x:
                lx_point = x.clone()

        hx_p._x += 20

        l = line(point,hx_point)
        # print('check point: ', line)
        # print(line)
        counter = 0
        for x in self._edge:
            stat = intersection(l,x)
            if stat == 'intersection':
                counter+=1

        print('number of intersections: ',counter)
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
from enum import Enum

class PLC_Types(Enum):
    # point line classification types
    COLLINEAR = 1
    LEFT = 2
    RIGHT = 3
    BEHIND = 5
    BEYOND = 6
    BETWEEN = 7
    NON_COLLINEAR = 0

def Three_Point_Area(a: point,b: point,c: point):   
    # calculating area of triangle formed by joining point c to end points of line ab.
    # i.e. the point in observation is point is 'c', and reference point is point 'b'.      
    A = b._x*(a._y-c._y)
    B = a._x*(c._y-b._y)
    C = c._x*(b._y-a._y)
     
    area = (A+B+C)/2
    return area

# here p is reference point
def Line_Point_Area(l: line,p: point):
    return Three_Point_Area(l._start,l._end,p)

def TurnTest(line: line,point: point):
    if type(line)!=type(line()):
        raise ValueError('Objec of class line expected.')
    if type(point)!=type(point()):
        raise ValueError('Objec of class point expected.')
    
    area = Three_Point_Area(l._start ,l._end ,point)

    if area<0:
        return PLC_Types.LEFT
    elif area>0:
        return PLC_Types.RIGHT
    else:
        return PLC_Types.COLLINEAR

def isCollinear(line: line,point: point):
    if type(line)!=type(line()):
        return False
    if type(point)!=type(point()):
        return False
    
    if (l._start._x == p._x and l._start._y == p._y) or (l._end._x == p._x and l._end._y == p._y):
        return 'end_point'

    area = Three_Point_Area(l._start,l._end,point)
    
    if area==0:
        if l._start._x==l._end._x:#if line is orthogonal line
            if l._start._y>p._y and l._end._y>p._y:
                return 'behind'
            elif l._start._y<p._y and l._end._y<p._y:
                return 'beyond'
            else:
                return 'between'
        else:#if line is not orthogonal
            if l._start._x>p._x and l._end._x>p._x:
                return 'behind'
            elif l._start._x<p._x and l._end._x<p._x:
                return 'beyond'
            else:
                return 'between'
    else:
        return False  

def intersection(line1: line,line2: line):
    test_a1 = TurnTest(line1,line2._start)
    if test_a1 == 'collinear':
        temp = isCollinear(line1,line2._start)
        if (temp == 'between' or temp == 'end_point'):
            return True
        temp = isCollinear(line2,line1._start)
        print(temp)
        if (temp == 'between' or temp == 'end_point'):
            return True

    test_b1 = TurnTest(line1,line2._end)
    if test_b1 == 'collinear':
        temp = isCollinear(line1,line2._end)
        if (temp == 'between' or temp == 'end_point'):
            return True
        
        temp = isCollinear(line2,line1._end)
        print(temp)
        if (temp == 'between' or temp == 'end_point'):
            return True


    if test_a1 == test_b1:
        return False

    test_a2 = TurnTest(line1.reverse(),line2._start)
    test_b2 = TurnTest(line1.reverse(),line2._end)

    if test_a1 != test_a2 and test_b1 != test_b2:
        return True

    return False

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
    for point in array:
        if(point[axis]>max_ax[axis]):
            max_ax = point

    center = math.ceil(max_ax[axis]/2)
    left = []
    right = []
    for p in array:
        if p[axis] < center:
            left.append(p)
        else:
            right.append(p)

    sorted_left = pointSort_linear(left,axis)
    sorted_right = pointSort_linear(right,axis)

    return sorted_left+sorted_right

if __name__ == '__main__':
    print(__name__)
    print(point())
    print(line())
    print(PLC_Types.COLLINEAR)
    print(type(list()))
    print(type(line()))
    
    vertex_table = [point(5,2),point(7,4),point(2,1),point(6,7),point(2,5),point(1,3)]
    plg = polygon()
    plg.initialize(vertex_table)
    print(plg)
    plg.sortCCW(0)
    print(plg)
    # # print(Three_Point_Area(point(5,2),point(2,1),point(1,3)))
    print(Line_Point_Area(line(point(5,2),point(7,4)),point(6,7)))
