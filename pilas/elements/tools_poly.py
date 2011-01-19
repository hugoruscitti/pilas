"""
This file is part of the 'Elements' Project
Elements is a 2D Physics API for Python (supporting Box2D2)

Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>

Home:  http://elements.linuxuser.at
IRC:   #elements on irc.freenode.org

Code:  http://www.assembla.com/wiki/show/elements
       svn co http://svn2.assembla.com/svn/elements                     

License:  GPLv3 | See LICENSE for the full text
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.              
"""
from functools import partial

from math import fabs
from math import sqrt
from math import atan2
from math import degrees
from math import acos

from locals import *
from elements import box2d

def calc_center(points):
    """ Calculate the center of a polygon
    
        Return: The center (x,y)
    """
    tot_x, tot_y = 0,0
    for p in points:
        tot_x += p[0]
        tot_y += p[1]
    n = len(points)
    return (tot_x/n, tot_y/n)
    
def poly_center_vertices(pointlist):
    """ Rearranges vectors around the center
    
        Return: pointlist ([(x, y), ...])
    """    
    poly_points_center = []
    center = cx, cy = calc_center(pointlist)
    
    for p in pointlist:
        x = p[0] - cx
        y = cy - p[1]
        poly_points_center.append((x, y))
    
    return poly_points_center
    
def is_line(vertices, tolerance=25.0):
    """ Check if passed vertices are a line. Done by comparing
        the angles of all vectors and check tolerance.
        
        Parameters:
          vertices ... a list of vertices (x, y)
          tolerance .. how many degrees should be allowed max to be a line
          
        Returns: True if line, False if no line
    """
    if len(vertices) <= 2:        
        return True

    # Step 1: Points -> Vectors
    p_old = vertices[0]
    alphas = []
    

    for p in vertices[1:]:
        x1, y1 = p_old
        x2, y2 = p
        p_old = p

        # Create Vector        
        vx, vy = (x2-x1, y2-y1)
        
        # Check Length
        l = sqrt((vx*vx) + (vy*vy))
        if l == 0.0: continue

        # Normalize vector
        vx /= l
        vy /= l
        
        # Append angle
        if fabs(vx) < 0.2: alpha = 90.0
        else: alpha = degrees(atan2(vy,vx))

        alphas.append(fabs(alpha))
        
    # Sort angles
    alphas.sort()
    
    # Get maximum difference
    alpha_diff = fabs(alphas[-1] - alphas[0])
    print "alpha difference:", alpha_diff
    
    if alpha_diff < tolerance:
        return True
    else:
        return False
    
def reduce_poly_by_angle(vertices, tolerance=10.0, minlen=20):
    """ This function reduces a poly by the angles of the vectors (detect lines)
        If the angle difference from one vector to the last > tolerance: use last point
        If the angle is quite the same, it's on the line
        
        Parameters:
          vertices ... a list of vertices (x, y)
          tolerance .. how many degrees should be allowed max
          
        Returns: (1) New Pointlist, (2) Soft reduced pointlist (reduce_poly())
    """
    v_last = vertices[-1]
    vertices = vxx = reduce_poly(vertices, minlen)
    
    p_new =  []
    p_new.append(vertices[0])
    
    dir = None 
    is_convex = True
    
    for i in xrange(len(vertices)-1):
        if i == 0:
            p_old = vertices[i]
            continue
        
        x1, y1 = p_old
        x2, y2 = vertices[i]
        x3, y3 = vertices[i+1]
        p_old = vertices[i]
        
        # Create Vectors
        v1x = (x2 - x1) * 1.0
        v1y = (y2 - y1) * 1.0
        
        v2x = (x3 - x2) * 1.0
        v2y = (y3 - y2) * 1.0

        # Calculate angle
        a = ((v1x * v2x) + (v1y * v2y))
        b = sqrt((v1x*v1x) + (v1y*v1y))
        c = sqrt((v2x*v2x) + (v2y*v2y))

        # No Division by 0 :)        
        if (b*c) == 0.0: continue
        
        # Get the current degrees
        # We have a bug here sometimes...
        try:
            angle = degrees(acos(a / (b*c)))
        except:
            # cos=1.0
            print "cos=", a/(b*c)
            continue
            
        # Check if inside tolerance
        if fabs(angle) > tolerance:
            p_new.append(vertices[i])        
            # print "x", 180-angle, is_left(vertices[i-1], vertices[i], vertices[i+1])
            
            # Check if convex:
            if dir == None:
                dir = is_left(vertices[i-1], vertices[i], vertices[i+1])
            else:
                if dir != is_left(vertices[i-1], vertices[i], vertices[i+1]):
                    is_convex = False
                    
    # We also want to append the last point :)
    p_new.append(v_last)
    
    # Returns: (1) New Pointlist, (2) Soft reduced pointlist (reduce_poly())
    return p_new, is_convex

    """ OLD FUNCTION: """    
    # Wipe all points too close to each other
    vxx = vertices = reduce_poly(vertices, minlen)
    
    # Create Output List
    p_new = []
    p_new.append(vertices[0])
    
    # Set the starting vertice
    p_old = vertices[0]
    alpha_old = None

    # For each vector, compare the angle difference to the last one
    for i in range(1, len(vertices)):
        x1, y1 = p_old
        x2, y2 = vertices[i]
        p_old = (x2, y2)

        # Make Vector
        vx, vy = (x2-x1, y2-y1)
    
        # Vector length
        l = sqrt((vx*vx) + (vy*vy))
        
        # normalize
        vx /= l
        vy /= l
        
        # Get Angle
        if fabs(vx) < 0.2:
            alpha = 90
        else: 
            alpha = degrees(atan2(vy,vx))

        if alpha_old == None:
            alpha_old = alpha
            continue
        
        # Get difference to previous angle
        alpha_diff = fabs(alpha - alpha_old)        
        alpha_old = alpha
        
        # If the new vector differs from the old one, we add the old point
        # to the output list, as the line changed it's way :)
        if alpha_diff > tolerance:
            #print ">",alpha_diff, "\t", vx, vy, l
            p_new.append(vertices[i-1])

    # We also want to append the last point :)
    p_new.append(vertices[-1])
    
    # Returns: (1) New Pointlist, (2) Soft reduced pointlist (reduce_poly())
    return p_new, vxx
    
        
# The following functions is_left, reduce_poly and convex_hull are 
# from the pymunk project (http://code.google.com/p/pymunk/)
def is_left(p0, p1, p2):
    """Test if p2 is left, on or right of the (infinite) line (p0,p1).
    
    :return: > 0 for p2 left of the line through p0 and p1
        = 0 for p2 on the line
        < 0 for p2 right of the line
    """
    sorting = (p1[0] - p0[0])*(p2[1]-p0[1]) - (p2[0]-p0[0])*(p1[1]-p0[1])
    if sorting > 0: return 1
    elif sorting < 0: return -1 
    else: return 0

def is_convex(points):
    """Test if a polygon (list of (x,y)) is strictly convex or not.
    
    :return: True if the polygon is convex, False otherwise
    """
    #assert len(points) > 2, "not enough points to form a polygon"
    
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]

    xc, yc = 0, 0
    is_same_winding = is_left(p0, p1, p2)
    for p2 in points[2:] + [p0] + [p1]:
        if is_same_winding != is_left(p0, p1, p2): 
            return False
        a = p1[0] - p0[0], p1[1] - p0[1] # p1-p0
        b = p2[0] - p1[0], p2[1] - p1[1] # p2-p1
        if sign(a[0]) != sign(b[0]): xc +=1
        if sign(a[1]) != sign(b[1]): yc +=1
        p0, p1 = p1, p2
   
    return xc <= 2 and yc <= 2

def sign(x): 
    if x < 0: return -1 
    else: return 1


def reduce_poly(points, tolerance=50):
    """Remove close points to simplify a polyline
    tolerance is the min distance between two points squared.
    
    :return: The reduced polygon as a list of (x,y)
    """
    curr_p = points[0]
    reduced_ps = [points[0]]
    
    for p in points[1:]:
        x1, y1 = curr_p
        x2, y2 = p
        dx = fabs(x2 - x1)
        dy = fabs(y2 - y1)
        l = sqrt((dx*dx) + (dy*dy))
        if l > tolerance:
            curr_p = p
            reduced_ps.append(p)
            
    return reduced_ps

def convex_hull(points):
    """Create a convex hull from a list of points.
    This function uses the Graham Scan Algorithm.
    
    :return: Convex hull as a list of (x,y)
    """
    ### Find lowest rightmost point
    p0 = points[0]
    for p in points[1:]:
        if p[1] < p0[1]:
            p0 = p
        elif p[1] == p0[1] and p[0] > p0[0]:
            p0 = p
    points.remove(p0)
    
    ### Sort the points angularly about p0 as center
    f = partial(is_left, p0)
    points.sort(cmp = f)
    points.reverse()
    points.insert(0, p0)
    
    ### Find the hull points
    hull = [p0, points[1]]
    
    for p in points[2:]:
        
        pt1 = hull[-1]
        pt2 = hull[-2]
        l = is_left(pt2, pt1, p) 
        if l > 0:
            hull.append(p)
        else:
            while l <= 0 and len(hull) > 2:
                hull.pop()
                pt1 = hull[-1]
                pt2 = hull[-2]
                l = is_left(pt2, pt1, p)
            hull.append(p)
    return hull     
    
