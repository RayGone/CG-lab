from geometry.shapes import *
import matplotlib.pyplot as plt,random

class STACK:
    __value = None
    length = 0
    
    def __init__(self):
        self.__value = []

    def initialize(self,value):
        if iter(value):
            if type(value) == type(list()):
                self.__value = value
                self.length = len(value)
            
            if type(value) == type(tuple()):
                tmp = []
                for v in value:
                    tmp.append(v)
                self.__value = tmp
                self.length = len(value)

    def push(self,value):
        self.length += 1
        self.__value.insert(0,value)

    def pop(self):
        if self.length > 0:
            self.length -= 1
            return self.__value.pop(0)

        return None

    def clear(self):

        self.length = 0
        self.__value = None

    def dump(self):
        return self.__value

    def getValueAt(self,index):
        return self.__value[index]

    def __str__(self):
        return str(self.__value)

class ConvexHull:
    __point_space = []
    __hull_pts = []
    __ConvexHull = polygon()
    __point_count = 0

    def __init__(self,plist = []):
        if(len(plist)):
            if(type(plist[0]) == type(point)):
                self.__point_space = plist
            else:
                for p in plist:
                    self.addPoint(point(p[0],p[1]))
                     
    def __str__(self):
        return str(self.__ConvexHull)

    def getPointSpace(self):
        return self.__point_space

    def addPoint(self,p: point):
        self.__point_space.append(p)

    def giftwrap_algorithm(self,point_list):
        # this implementation of giftwrap_algorithm is mixture of
        ## 1. GiftWrap algorithm -> Doing turn test for left-most or right-most point from reference point
        ###### is pretty much similar to looking for point with smallest slope to the reference point
        ## 2. Divide and Conquer -> We compute convex hull by dividing point space into two, left and right.
        ## 3. Quick Hull -> We use quick hull's approach to divide the point space i.e. by taking two extreme points,
        ####
        #### Instead of making traingles and performing Point Inclusion Test, we take GiftWrap approach.
        ##### Initially, point is sorted linearly across x-axis (y-axis can be done too). thus left half and right are also sorted, automatically.
        ###### Because of the sorted order of points, we can take advantage of this and take note of the index of the point last considered as hull
        ####### Thus we don't have to do turnTest for those point which are before that the point last considered as hull
        ########
        
        # sorting to get extreme x-axis point
        point_list = pointSort_linear(point_list)
        # print(point_list)
        points = [] # list of point objects
        for pl in point_list:
            points.append(point(pl[0],pl[1]))

        xtreme_low_x = points.pop(0)
        xtreme_high_x = points.pop(-1)
        # this is bisector_line in sense we will divide each points as per this line
        bisector_line = line(xtreme_low_x,xtreme_high_x)
        # the division is made to find at most two other points to form a rectangle which will be the basis to compute convex hull
        # otherwise a single to forma rectangle for the basis of convex hull
        left = []
        right = []
        for pl in points:
            # dividing points to left and right
            turn = TurnTest(bisector_line,pl)
            if turn == PLC_Types.LEFT:
                left.append(pl.getList())
            if turn == PLC_Types.RIGHT:
                right.append(pl.getList())
        # To match the direction with left we have to reverse the array ##########
        ## Note: point_sortLinear() sorts array in x_axis in ascending order
        ### left part of points are the upper half (not necessarily half) of the convex_hull as bisected by bisector line
        ### and right part of the points  are lower half of the convex hull
        
        # print(left,'left\n',right,'right\n')
        right.reverse()
        # print('\nreversed',right,'\n')
        st_pt = bisector_line._start # start from start point of bisector_line for points in left side
        en_pt = bisector_line._end # end at end point of bisector_line
        left_hull = []
        right_hull = []
        ref_turn = PLC_Types.LEFT # extreme_points are at left turn of left part of the point space from the bisector line
        # print('bisector line',bisector_line,'\n')  
        draw_line([st_pt,en_pt])
        """
            Computing convex hull of the left half
        """
        if True:
            # print('left_hull')
            temp = left.copy()
            temp.append(en_pt.getList())
            t_pt = point(temp[0][0],temp[0][1])
            t_ln = line(st_pt,t_pt)

            left_hull = [st_pt]
            # untill the hull point incorporates en_pt
            index = 0
            length = len(temp)

            while left_hull[-1] != en_pt and index < length :
                # index+=1 # incrementing to next index
                for i in range(index,length):
                    # print(i,temp[i],'for i temp[i]')
                    t_pt = point(temp[i][0],temp[i][1])
                    turn = TurnTest(t_ln,t_pt)
                    # print(turn,t_ln,t_pt)
                    if turn == ref_turn:
                        index = i
                        t_ln = line(st_pt,t_pt)
                    elif turn == PLC_Types.COLLINEAR:
                        if t_ln._end._x < t_pt._x or t_ln._end._y < t_pt._y:
                            index = 1
                            t_ln = line(st_pt,t_pt)
                    else: # PLC_Types.RIGHT

                        pass

                left_hull.append(t_ln._end)

                st_pt = t_ln._end # starting point for next iteration is the current test point
                index+=1 # incrementing to next index
                # print(index,'index')
                t_pt = point(temp[index%length][0],temp[index%length][1])
                
                if t_pt == en_pt:
                    left_hull.append(t_pt)

                t_ln = line(st_pt,t_pt)
   
        # print('left_hull')
        # for hp in left_hull:
        #     print(hp)
        # re-init st_pt and en_pt
        st_pt = bisector_line._end # start from start point of bisector_line for points in left side
        en_pt = bisector_line._start # end at end point of bisector_line
        # print('bisector line',bisector_line.reverse(),'\n')
        """
            Computing convex hull of the right half
        """
        if True:
            # print('right_hull')
            temp = right.copy()
            temp.append(en_pt.getList())
            t_pt = point(temp[0][0],temp[0][1])
            t_ln = line(st_pt,t_pt)
            # print(temp,'added end point')
            right_hull = [st_pt]
            # untill the hull point incorporates en_pt
            index = 0
            length = len(temp)
            
            while right_hull[-1] != en_pt and index < length :
                # index+=1
                for i in range(index,length):
                    t_pt = point(temp[i][0],temp[i][1])
                    turn = TurnTest(t_ln,t_pt)
                    # print(index,i,temp[i],t_pt,t_ln,'for i temp[i]',turn)
                    if turn == ref_turn:
                        # print('ref_turn matched')
                        index = i
                        t_ln = line(st_pt,t_pt)
                    
                    if turn == PLC_Types.COLLINEAR:
                        if t_ln._end._x > t_pt._x or t_ln._end._y > t_pt._y:
                            index = 1
                            t_ln = line(st_pt,t_pt)

                # print(t_ln._end,"accepted_hull\n\n")
                right_hull.append(t_ln._end)

                st_pt = t_ln._end # starting point for next iteration is the current test point
                
                index+=1 # incrementing to next index
                # print(index,'index')
                t_pt = point(temp[index%length][0],temp[index%length][1])

                if t_pt == en_pt:
                    right_hull.append(t_pt)

                t_ln = line(st_pt,t_pt)

        # print('right_hull')
        complete_hull = left_hull+right_hull
        complete_hull.append(left_hull[0])
        
        # for hp in complete_hull:
        #     print(hp)
        # hull = []

        self.__hull_pts = complete_hull
        # self.__ConvexHull.initialize(complete_hull)
        return
        # ref_turn = PLC_Types.RIGHT # extreme_points are at right turn of right part of the point space from the bisector line
        # right_hull = [en_pt]  # start from end point  of bisector_line for right hull        

    def GrahamScan_Algorithm(self,point_list):
        stk = STACK()
        stk.initialize(pointSort_Angular(point_list))
        # print(stk)
        hull = STACK()
        t_pt = stk.pop() # t_pt: temporary point
        hull.push(point(t_pt[0],t_pt[1]))
        t_pt = stk.pop()
        hull.push(point(t_pt[0],t_pt[1]))

        t_pt = stk.pop() # first check point
        t_pt = point(t_pt[0],t_pt[1])
        # print('first point to check',t_pt)
        t_ln = line(hull.getValueAt(1),hull.getValueAt(0)) # t_ln: temporary line
        
        while stk.length != 0:
            turn = TurnTest(t_ln,t_pt)
            if turn == PLC_Types.RIGHT:
                hull.push(t_pt)
                t_ln = line(t_ln.end(),t_pt)
                t_pt = stk.pop()
                t_pt = point(t_pt[0],t_pt[1])
            else:
                hull.pop()
                t_ln = line(hull.getValueAt(1),hull.getValueAt(0))
        
        self.__hull_pts = hull.dump()
        self.__hull_pts.reverse()
        self.__hull_pts.append(self.__hull_pts[0])

    def printConvexHull(self):

        # ps = []
        # for pt in self.__point_space:
        #     ps.append(pt.getList())
        # print('point space: ',ps,'\n')
        print(self.__ConvexHull)

    def ConvexHull(self,algorithm = 'giftwrap'):
        list_array = []
        for p in self.__point_space:
            list_array.append(p.getList())

        if(algorithm == 'giftwrap'):
            print("Using GiftWrap Algorithm")
            self.giftwrap_algorithm(list_array)
        
        elif(algorithm == 'grahamscan'):
            print("Using Graham Scan Algorithm")
            self.GrahamScan_Algorithm(list_array)

        else:
            return

        self.__ConvexHull.initialize(self.__hull_pts,sort=False)

        tmp = []
        for pt in self.__hull_pts:
            tmp.append(pt.getList())

        self.__hull_pts = tmp
        return

    def DrawExtremePointsWithPointSpace(self):        
        # self.printConvexHull()
        print(self.__ConvexHull._type,'type')
        draw_multiple_points(self.__point_space)
       
        draw_multiple_points(self.__hull_pts,p_size=45)
        plt.show()

    def DrawExtremeEdgesWithPointSpace(self):
        print(self.__ConvexHull._type,'type')
        draw_multiple_points(self.__point_space)
        # hull_pts = self.__ConvexHull._vertex    
        # hull_pts.append(hull_pts[0])
        draw_line(self.__hull_pts)
        plt.show()

    def Draw(self):
        self.printConvexHull()
        draw_multiple_points(self.__point_space)
      
        draw_multiple_points(self.__hull_pts,p_size=65)
        draw_line(self.__hull_pts)
        plt.show()
        pass

    # num_pt = number of points to generate
    # x_range = max x-value to generate and similarly for y_range
    # naxis = negative axis, range of negative is according to x_range and y_range
    def generateRandomPoints(self,num_pt = 25,x_range=20,y_range=20,naxis = False):
        permutation = x_range * y_range
        if (7*permutation/10)<num_pt:
            raise ValueError('x_range={} and y_range={} is small to generate {} points'.format(x_range,y_range,num_pt))
        
        self.__point_space = []
        while num_pt!=0:
            x = random.randint(0,x_range)
            y = random.randint(0,y_range)
            p = point(x,y)

            self.__point_space.append(p)
            num_pt -= 1
        pass
    
def draw_multiple_points(pt_list,p_size = 20):
    # x axis value list.
    x_number_list = []

    # y axis value list.
    y_number_list = []

    if len(pt_list)>0:
        if(type(pt_list[0])  == type([])):
            for pt in pt_list:
                x_number_list.append(pt[0])
                y_number_list.append(pt[1])
        
        if(type(pt_list[0])  == type(point())):
            for pt in pt_list:
                x_number_list.append(pt.getX())
                y_number_list.append(pt.getY())

    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, s=p_size)

    # Set chart title.
    plt.title("Point Space")

    # Set x, y label text.
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")

def draw_line(pt_list):

    # x axis value list.
    x_number_list = []

    # y axis value list.
    y_number_list = []

    if len(pt_list)>0:
        if(type(pt_list[0])  == type([])):
            for pt in pt_list:
                x_number_list.append(pt[0])
                y_number_list.append(pt[1])
        
        if(type(pt_list[0])  == type(point())):
            for pt in pt_list:
                x_number_list.append(pt.getX())
                y_number_list.append(pt.getY())

    # Plot the number in the list and set the line thickness.
    plt.plot(x_number_list, y_number_list, linewidth=3,color='green')

    # Set chart title.
    plt.title("Point Space")

    # Set x, y label text.
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")

    # Set the x, y axis tick marks text size.
    plt.tick_params(axis='both', labelsize=9)


if __name__ == "__main__":
    ch = ConvexHull([[152, 2], [52, 21], [23, 64], [27, 370], [47, 387], [284, 396], [421, 397], [465, 390], [476, 368], [498, 270], [496, 76], [345, 9], [328, 7]])
    # draw_multiple_points(ch.getPointSpace())
    ch.generateRandomPoints(150,500,400)
    # draw_multiple_points(ch.getPointSpace())
    ch.ConvexHull('grahamscan')
    # ch.GrahamScan_Algorithm([[0, 32], [0, 7], [1, 34], [2, 16], [2, 43], [3, 26], [4, 17], [5, 3], [7, 48], [8, 33], [9, 28], [9, 24], [11, 44], [12, 39], [14, 12], [19, 4], [20, 19], [21, 42], [21, 46], [21, 16], [22, 25], [23, 12], [25, 2], [25, 47], [26, 16], [27, 10], [27, 31], [29, 2], [30, 32], [32, 25], [32, 6], [33, 12], [34, 22], [35, 6], [35, 19], [35, 13], [36, 27], [36, 9], [37, 1], [37, 7], [40, 2], [42, 34], [42, 12], [42, 41], [43, 39], [43, 29], [45, 1], [45, 15], [46, 15], [46, 12], [48, 30], [48, 31], [49, 24], [50, 41], [50, 50]])
    # ch.DrawExtremePointsWithPointSpace()
    # ch.DrawExtremeEdgesWithPointSpace()
    ch.Draw()