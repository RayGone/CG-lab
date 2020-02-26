from geometry.shapes import *
import random

class ConvexHull:
    __pointList = []
    __ConvexHull = polygon()
    __point_count = 0

    def __init__(self,plist = []):
        if(len(plist)):
            if(type(plist[0]) == type(point)):
                self.__pointList = plist
            else:
                for p in plist:
                    self.addPoint(point(p[0],p[1]))
                     
    def __str__(self):
        return str(self.__ConvexHull)

    def getPointSpace(self):
        return self.__pointList

    def addPoint(self,p: point):
        self.__pointList.append(p)

    def giftwrap_algorithm(self,point_list):
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
        draw_line(complete_hull)

        # self.__ConvexHull.initialize(complete_hull)
        return
        # ref_turn = PLC_Types.RIGHT # extreme_points are at right turn of right part of the point space from the bisector line
        # right_hull = [en_pt]  # start from end point  of bisector_line for right hull        

    def ConvexHull(self):
        list_array = []
        for p in self.__pointList:
            list_array.append(p.getList())

        self.giftwrap_algorithm(list_array)
        return
        
    # num_pt = number of points to generate
    # x_range = max x-value to generate and similarly for y_range
    # naxis = negative axis, range of negative is according to x_range and y_range
    def generateRandomPoints(self,num_pt = 25,x_range=20,y_range=20,naxis = False):
        permutation = x_range * y_range
        if (3*permutation/4)<num_pt:
            raise ValueError('x_range={} and y_range={} is small to generate {} points'.format(x_range,y_range,num_pt))
        
        self.__pointList = []
        while num_pt!=0:
            x = random.randint(0,x_range)
            y = random.randint(0,y_range)
            p = point(x,y)
            if checkDuplicate(self.__pointList,p):
                # if the geerated point is already in list
                continue

            self.__pointList.append(p)
            num_pt -= 1
        pass
    

import matplotlib.pyplot as plt
def checkDuplicate(plist,p):
    for pt in plist:
        if(str(pt) == str(p)):
            return True

    return False 
    
def draw_multiple_points(pt_list):
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
    plt.scatter(x_number_list, y_number_list, s=35)

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
    plt.plot(x_number_list, y_number_list, linewidth=3)

    # Set chart title.
    plt.title("Point Space")

    # Set x, y label text.
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")

    # Set the x, y axis tick marks text size.
    plt.tick_params(axis='both', labelsize=9)


if __name__ == "__main__":
    ch = ConvexHull([[0, 32], [0, 7], [1, 34], [2, 16], [2, 43], [3, 26], [4, 17], [5, 3], [7, 48], [8, 33], [9, 28], [9, 24], [11, 44], [12, 39], [14, 12], [19, 4], [20, 19], [21, 42], [21, 46], [21, 16], [22, 25], [23, 12], [25, 2], [25, 47], [26, 16], [27, 10], [27, 31], [29, 2], [30, 32], [32, 25], [32, 6], [33, 12], [34, 22], [35, 6], [35, 19], [35, 13], [36, 27], [36, 9], [37, 1], [37, 7], [40, 2], [42, 34], [42, 12], [42, 41], [43, 39], [43, 29], [45, 1], [45, 15], [46, 15], [46, 12], [48, 30], [48, 31], [49, 24], [50, 41], [50, 50]])
    # draw_multiple_points(ch.getPointSpace())
    ch.generateRandomPoints(55,50,50)
    draw_multiple_points(ch.getPointSpace())
    ch.ConvexHull()
    plt.show()