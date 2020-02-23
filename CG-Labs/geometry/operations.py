from enum import Enum
from shapes import point,line

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
    # i.e. the reference point is 'c'.      
    A = a._x*(b._y-c._y)
    B = b._x*(c._y-a._y)
    C = c._x*(a._y-b._y)
     
    area = (A+B+C)/2
    return area

def Line_Point_Area(l: line,p: point):
    return Three_Point_Area(line._start,line._end)

def turnTest(line: line,point: point):
    if type(line)!=type(line()):
        raise ValueError('Objec of class line expected.')
    if type(point)!=type(point()):
        raise ValueError('Objec of class point expected.')
    
    area = Three_Point_Area(line.Point_A ,line.Point_B ,point)

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
    
    if (line.Point_A._x == point._x and line.Point_A._y == point._y) or (line.Point_B._x == point._x and line.Point_B._y == point._y):
        return 'end_point'

    area = Three_Point_Area(line.Point_A,line.Point_B,point)
    
    if area==0:
        if line.Point_A._x==line.Point_B._x:#if line is orthogonal line
            if line.Point_A._y>point._y and line.Point_B._y>point._y:
                return 'behind'
            elif line.Point_A._y<point._y and line.Point_B._y<point._y:
                return 'beyond'
            else:
                return 'between'
        else:#if line is not orthogonal
            if line.Point_A._x>point._x and line.Point_B._x>point._x:
                return 'behind'
            elif line.Point_A._x<point._x and line.Point_B._x<point._x:
                return 'beyond'
            else:
                return 'between'
    else:
        return False  

def intersection(line1: line,line2: line):
    test_a1 = turnTest(line1,line2.Point_A)
    if test_a1 == 'collinear':
        temp = isCollinear(line1,line2.Point_A)
        if (temp == 'between' or temp == 'end_point'):
            return True
        temp = isCollinear(line2,line1.Point_A)
        print(temp)
        if (temp == 'between' or temp == 'end_point'):
            return True

    test_b1 = turnTest(line1,line2.Point_B)
    if test_b1 == 'collinear':
        temp = isCollinear(line1,line2.Point_B)
        if (temp == 'between' or temp == 'end_point'):
            return True
        
        temp = isCollinear(line2,line1.Point_B)
        print(temp)
        if (temp == 'between' or temp == 'end_point'):
            return True


    if test_a1 == test_b1:
        return False

    test_a2 = turnTest(line1.reverse(),line2.Point_A)
    test_b2 = turnTest(line1.reverse(),line2.Point_B)

    if test_a1 != test_a2 and test_b1 != test_b2:
        return True

    return False


if __name__ == '__main__':
    print(__name__)
    print(point())
    print(line())
    print(PLC_Types.COLLINEAR)
    print(type(list()))
    print(type(line()))