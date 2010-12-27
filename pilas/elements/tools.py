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
# Some Hex Tools
def hex2dec(hex):
    """ Convert and hex value in a decimal number
    """ 
    return int(hex, 16)

def hex2rgb(hex): 
    """ Convert a hex color (#123abc) in RGB ((r), (g), (b))
    """
    if hex[0:1] == '#': hex = hex[1:]; 
    return (hex2dec(hex[:2]), hex2dec(hex[2:4]), hex2dec(hex[4:6]))

def rgb2floats(rgb):
    """Convert a color in the RGB (0..255,0..255,0..255) format to the
       (0..1, 0..1, 0..1) float format
    """
    ret = []
    for c in rgb:
        ret.append(float(c) / 255)
    return ret

def point_in_poly(point, poly):
    #print ">", point, poly
    x, y = point
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
    