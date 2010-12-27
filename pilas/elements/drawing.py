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
from math import pi
from math import cos
from math import sin
from math import sqrt

import tools

# Functions of a rendering class 
# mandatory:
#    __init__
#    start_drawing
#    after_drawing
#    draw_circle
#    draw_polygon
#    draw_lines
#    set_lineWidth
#
# renderer-specific mandatory functions:
# for pygame:
#    set_surface
# for cairo:
#    draw_text
# for opengl:
#    

# IMPORTANT
# The drawing functions get the coordinates in their screen coordinate system
# no need for translations anymore :)

class draw_pygame(object):
    """ This class handles the drawing with pygame, which is really
        simple since we only need draw_ellipse and draw_polygon.
    """
    lineWidth = 0
    
    def __init__(self):
        """ Load pygame.draw and pygame.Rect, and reference it for
            the drawing methods
            
            Parameters:
              surface .... pygame surface (default: None)
              lineWidth .. 

            Return: Class draw_pygame()
        """
        print "* Pygame selected as renderer"        
        from pygame import draw
        from pygame import Rect
        
        self.draw = draw
        self.Rect = Rect

    def set_lineWidth(self, lw):
        """
        """
        self.lineWidth = lw

    def set_surface(self, surface):
        """
        """
        self.surface = surface

    def get_surface(self):
        """
        """
        return self.surface

    def start_drawing(self):
        pass
        
    def after_drawing(self):
        pass

    def draw_circle(self, clr, pt, radius, angle):
        """ Draw a circle
        
            Parameters:
              pt ........ (x, y)
              clr ....... color in rgb ((r), (g), (b))
              radius .... circle radius 
              angle ..... rotation in radians
              
            Return: -
        """
        x, y = pt
        
        x1 = x - radius
        y1 = y - radius
        
        rect = self.Rect( [x1, y1, 2*radius, 2*radius] )
        self.draw.ellipse(self.surface, clr, rect, self.lineWidth)
                        
        # draw the orientation vector
        if radius > 10:
            rx = cos(angle) * radius
            ry = -sin(angle) * radius
            
            self.draw.line(self.surface, (255,255,255), pt, (x+rx, y+ry))

    def draw_polygon(self, clr, points):
        """ Draw a polygon
        
            Parameters:
              clr ....... color in rgb ((r), (g), (b))
              points .... polygon points in normal (x,y) positions
              
            Return: -
        """
        self.draw.polygon(self.surface, clr, points, self.lineWidth)
        #self.draw.lines(self.surface, clr, True, points)

    def draw_lines(self, clr, closed, points, width=None):
        """ Draw a polygon
        
            Parameters:
              clr ....... color in rgb ((r), (g), (b))
              points .... polygon points in normal (x,y) positions
              
            Return: -
        """
        if width == None:
            lw = self.lineWidth
        else: 
            lw = width
            
        self.draw.lines(self.surface, clr, closed, points, lw)

class draw_cairo(object):
    """ This class handles the drawing with cairo, which is really
        simple since we only need draw_ellipse and draw_polygon.
    """
    window = None
    da     = None
    circle_surface = None
    box_surface    = None

    def __init__(self, drawMethod="filled"):
        """ Load cairo.draw and cairo.Rect, and reference it for
            the drawing methods
            
            Return: Class draw_cairo()
        """
        print "* Cairo selected as renderer"
        import cairo
        self.cairo = cairo
        self.set_drawing_method(drawMethod)
        #self.draw_box = self.draw_box_image

    def set_lineWidth(self, lw): # unused
        self.lineWidth = lw 

    def set_drawing_area(self, da):
        """ Set the area for Cairo to draw to
        
            da ...... drawing area (gtk.DrawingArea)

            Return: -
        """
        self.da = da
        self.window = da.window
        print "* Cairo renderer drawing area set"

    def set_drawing_method(self, type):
        """ type = filled, image """
        self.draw_circle = getattr(self, "draw_circle_%s" % type)
        #self.draw_box    = getattr(self, "draw_box_%s" % type)

    def start_drawing(self):
        self.width, self.height = self.window.get_size()
        self.imagesurface = self.cairo.ImageSurface(self.cairo.FORMAT_ARGB32, self.width, self.height);
        self.ctx = ctx = self.cairo.Context(self.imagesurface)

        ctx.set_source_rgb(1, 1, 1) # background color
        ctx.paint()

        ctx.move_to(0, 0)
        ctx.set_source_rgb(0, 0, 0) # defaults for the rest of the drawing
        ctx.set_line_width(1)
        ctx.set_tolerance(0.1)

        ctx.set_line_join(self.cairo.LINE_CAP_BUTT)
        # LINE_CAP_BUTT, LINE_CAP_ROUND, LINE_CAP_SQUARE, LINE_JOIN_BEVEL, LINE_JOIN_MITER, LINE_JOIN_ROUND
        
        #ctx.set_dash([20/4.0, 20/4.0], 0)

    def after_drawing(self):
        dest_ctx = self.window.cairo_create()
        dest_ctx.set_source_surface(self.imagesurface)
        dest_ctx.paint()

    def set_circle_image(self, filename):
        self.circle_surface = self.cairo.ImageSurface.create_from_png(filename)
        self.draw_circle = self.draw_circle_image

#    def set_box_image(self, filename):
#        self.box_surface = self.cairo.ImageSurface.create_from_png(filename)
#        self.draw_box = self.draw_box_image

    def draw_circle_filled(self, clr, pt, radius, angle=0):
        x, y = pt

        clr = tools.rgb2floats(clr)
        self.ctx.set_source_rgb(*clr)
        self.ctx.move_to(x, y)
        self.ctx.arc(x, y, radius, 0, 2*3.1415)
        self.ctx.fill()

    def draw_circle():
        pass

    def draw_circle_image(self, clr, pt, radius, angle=0, sf=None):
        if sf == None:
            sf = self.circle_surface
        x, y = pt
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.rotate(-angle)
        image_r = sf.get_width() / 2
        scale = float(radius) / image_r
        self.ctx.scale(scale, scale)
        self.ctx.translate(-0.5*sf.get_width(), -0.5*sf.get_height())
        self.ctx.set_source_surface(sf)
        self.ctx.paint()
        self.ctx.restore()

    def draw_image(self, source, pt, scale=1.0, rot=0, sourcepos=(0,0)):
        self.ctx.save()
        self.ctx.rotate(rot)
        self.ctx.scale(scale, scale)
        destx, desty = self.ctx.device_to_user_distance(pt[0], pt[1])
        self.ctx.set_source_surface(source, destx-sourcepos[0], desty-sourcepos[1])
        self.ctx.rectangle(destx, desty, source.get_width(), source.get_height())
        self.ctx.fill()
        self.ctx.restore()
                 
    def draw_polygon(self, clr, points):
        """ Draw a polygon
        
            Parameters:
              clr ....... color in rgb ((r), (g), (b))
              points .... polygon points in normal (x,y) positions
              
            Return: -
        """        
        clr = tools.rgb2floats(clr)
        self.ctx.set_source_rgb(clr[0], clr[1], clr[2])

        pt = points[0]
        self.ctx.move_to(pt[0], pt[1])
        for pt in points[1:]:
            self.ctx.line_to(pt[0], pt[1])
            
        self.ctx.fill()
   
    def draw_text(self, text, center, clr=(0,0,0), size=12, fontname="Georgia"):
        clr = tools.rgb2floats(clr)
        self.ctx.set_source_rgb(clr[0], clr[1], clr[2])

        self.ctx.select_font_face(fontname, self.cairo.FONT_SLANT_NORMAL, self.cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(size)
        x_bearing, y_bearing, width, height = self.ctx.text_extents(text)[:4]
        self.ctx.move_to(center[0] + 0.5 - width / 2 - x_bearing, center[1] + 0.5 - height / 2 - y_bearing)
        self.ctx.show_text(text)

    def draw_lines(self, clr, closed, points):
        """ Draw a polygon
        
            Parameters:
              clr ....... color in rgb ((r), (g), (b))
              closed .... whether or not to close the lines (as a polygon)
              points .... polygon points in normal (x,y) positions
            Return: -
        """        
        clr = tools.rgb2floats(clr)
        self.ctx.set_source_rgb(clr[0], clr[1], clr[2])

        pt = points[0]
        self.ctx.move_to(pt[0], pt[1])
        for pt in points[1:]:
            self.ctx.line_to(pt[0], pt[1])

        if closed:
            pt = points[0]
            self.ctx.line_to(pt[0], pt[1])

        self.ctx.stroke()

class draw_opengl_pyglet(object):
    """ This class handles the drawing with pyglet
    """
    lineWidth = 0
    def __init__(self):
        """ Load pyglet.gl, and reference it for the drawing methods
            
            Parameters:
              surface .... not used with pyglet
              lineWidth .. 
        """
        print "* OpenGL_Pyglet selected as renderer"

        from pyglet import gl
        self.gl = gl

    def set_lineWidth(self, lw):
        self.lineWidth = lw
    
    def draw_circle(self, clr, pt, radius, a=0):
        clr = tools.rgb2floats(clr)
    	self.gl.glColor3f(clr[0], clr[1], clr[2])

        x, y = pt
    	segs = 15
    	coef = 2.0*pi/segs;
    	
    	self.gl.glBegin(self.gl.GL_LINE_LOOP)
    	for n in range(segs):
    		rads = n*coef
    		self.gl.glVertex2f(radius*cos(rads + a) + x, radius*sin(rads + a) + y)
    	self.gl.glVertex2f(x,y)
    	self.gl.glEnd()

    def draw_polygon(self, clr, points):
        clr = tools.rgb2floats(clr)
    	self.gl.glColor3f(clr[0], clr[1], clr[2])
    	
        self.gl.glBegin(self.gl.GL_LINES)

        p1 = points[0]
        for p in points[1:]:
            x1, y1 = p1
            x2, y2 = p1 = p
            
            self.gl.glVertex2f(x1, y1)
            self.gl.glVertex2f(x2, y2)

        x1, y1 = points[0]
        
        self.gl.glVertex2f(x2, y2)
        self.gl.glVertex2f(x1, y1)

        self.gl.glEnd()
                
    def draw_lines(self, clr, closed, points):
        pass

    def start_drawing(self):
        pass
        
    def after_drawing(self):
        pass
