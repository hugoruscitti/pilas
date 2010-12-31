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
from locals import *
from elements import box2d

# Imports
from math import pi
from math import sqrt
from math import asin

import tools_poly

class Add:
    element_count = 0
    
    def __init__(self, parent):
        self.parent = parent
        
    def ground(self):
        """ Add a static ground to the scene
        
            Return: box2d.b2Body
        """
        return self._rect((-10.0, -2.4), 50.0, 0.1, dynamic=False)
            
    def triangle(self, pos, sidelength, dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        """ Add a triangle | pos & a in the current input unit system (meters or pixels)
        
            Parameters:
              pos .... position (x,y)
              sidelength ...... sidelength
              other .. see [physics parameters]
            
            Return: box2d.b2Body
        """
        vertices = [(-sidelength, 0.0), (sidelength, 0.0), (0.0, 2*sidelength)]
        return self.poly(pos, vertices, dynamic, density, restitution, friction, screenCoord)

    def ball(self, pos, radius, dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        """ Add a dynamic ball at pos after correcting the positions and legths to the internal
            meter system if neccessary (if INPUT_PIXELS), then call self._add_ball(...)
            
            Parameters:
              pos ..... position (x,y)
              radius .. circle radius
              other ... see [physics parameters]
              
            Return: box2d.b2Body
        """
        # Bring coordinates into the world coordinate system (flip, camera offset, ...)
        if screenCoord: x, y = self.parent.to_world(pos)
        else: x, y = pos


        if self.parent.input == INPUT_PIXELS:
            x /= self.parent.ppm
            y /= self.parent.ppm
            radius /= self.parent.ppm
            
        return self._ball((x,y), radius, dynamic, density, restitution, friction)

    def _ball(self, pos, radius, dynamic=True, density=1.0, restitution=0.16, friction=0.5):
        # Add a ball without correcting any settings
        # meaning, pos and vertices are in meters
        # Define the body
        x, y = pos
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        userData = { 'color' : self.parent.get_color() }
        bodyDef.userData = userData

        # Create the Body
        if not dynamic:
            density = 0

        body = self.parent.world.CreateBody(bodyDef)
                    
        self.parent.element_count += 1

        # Add a shape to the Body
        circleDef = box2d.b2CircleDef()
        circleDef.density = density
        circleDef.radius = radius
        circleDef.restitution = restitution
        circleDef.friction = friction

        body.CreateShape(circleDef)
        body.SetMassFromShapes()    
        
        return body    

    def rect(self, pos, width, height, angle=0, dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        """ Add a dynamic rectangle with input unit according to self.input (INPUT_PIXELS or INPUT_METERS)
            Correcting the positions to meters and calling self._add_rect()

            Parameters:
              pos ..... position (x,y)
              width ....... horizontal line
              height ....... vertical line
              angle ........ in degrees (0 .. 360)
              other ... see [physics parameters]

            Return: box2d.b2Body
        """
        # Bring coordinates into the world coordinate system (flip, camera offset, ...)
        if screenCoord: x, y = self.parent.to_world(pos)
        else: x, y = pos

        # If required, translate pixel -> meters
        if self.parent.input == INPUT_PIXELS:
            x /= self.parent.ppm
            y /= self.parent.ppm
            width /= self.parent.ppm
            height /= self.parent.ppm
        
        # grad -> radians
        angle = (angle * pi) / 180
        
        return self._rect((x,y), width, height, angle, dynamic, density, restitution, friction)


    def wall(self, pos1, pos2, width=5, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        """ Add a static rectangle between two arbitrary points with input unit according to self.input 
            (INPUT_PIXELS or INPUT_METERS) Correcting the positions to meters and calling self._add_rect()

            Return: box2d.b2Body
        """
        if width < 5: width = 5
        
        if (pos1[0] < pos2[0]):        
            x1, y1 = pos1
            x2, y2 = pos2
        else:
            x1, y1 = pos2
            x2, y2 = pos1          

        # Bring coordinates into the world coordinate system (flip, camera offset, ...)
        if screenCoord: 
           x1, y1 = self.parent.to_world((x1, y1))
           x2, y2 = self.parent.to_world((x2, y2))

        # If required, translate pixel -> meters
        if self.parent.input == INPUT_PIXELS:
            x1 /= self.parent.ppm
            y1 /= self.parent.ppm
            x2 /= self.parent.ppm
            y2 /= self.parent.ppm
            width /= self.parent.ppm
                           
        length = sqrt( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )*0.5

        if width > 0:
            halfX = x1 + (x2-x1)*0.5
            halfY = y1 + (y2-y1)*0.5

            angle = asin( (y2-halfY)/length )
            return self._rect((halfX, halfY), length, width, angle, False, density, restitution, friction)
                    
    def _rect(self, pos, width, height, angle=0, dynamic=True, density=1.0, restitution=0.16, friction=0.5):
        # Add a rect without correcting any settings
        # meaning, pos and vertices are in meters
        # angle is now in radians ((degrees * pi) / 180))
        x, y = pos
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        userData = { 'color' : self.parent.get_color() }
        bodyDef.userData = userData

        # Create the Body
        if not dynamic:
            density = 0

        body = self.parent.world.CreateBody(bodyDef)
                    
        self.parent.element_count += 1

        # Add a shape to the Body
        boxDef = box2d.b2PolygonDef()
        
        boxDef.SetAsBox(width, height, (0,0), angle)
        boxDef.density = density
        boxDef.restitution = restitution
        boxDef.friction = friction
        body.CreateShape(boxDef)
        
        body.SetMassFromShapes()
        
        return body

    def poly(self, pos, vertices, dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        """ Add a dynamic polygon, which has the vertices arranged around the poly's center at pos
            Correcting the positions to meters if INPUT_PIXELS, and calling self._add_poly()

            Parameters:
              pos ....... position (x,y)
              vertices .. vertices arranged around the center
              other ... see [physics parameters]

            Return: box2d.b2Body
        """        
        # Bring coordinates into the world coordinate system (flip, camera offset, ...)
        if screenCoord: x, y = self.parent.to_world(pos)
        else: x, y = pos
                    
        # If required, translate pixel -> meters
        if self.parent.input == INPUT_PIXELS:
            # translate pixel -> meters
            x /= self.parent.ppm
            y /= self.parent.ppm
            
            # Translate vertices from pixels to meters
            v_new = []
            for v in vertices:
                vx, vy = v
                v_new.append((vx/self.parent.ppm, vy/self.parent.ppm))
            vertices = v_new
        
        return self._poly((x,y), vertices, dynamic, density, restitution, friction)

    def _poly(self, pos, vertices, dynamic=True, density=1.0, restitution=0.16, friction=0.5):
        # add a centered poly at pos without correcting any settings
        # meaning, pos and vertices are in meters
        x, y = pos
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)
            
        userData = { 'color' : self.parent.get_color() }
        bodyDef.userData = userData

        # Create the Body
        if not dynamic:
            density = 0

        body = self.parent.world.CreateBody(bodyDef)
        
        self.parent.element_count += 1

        # Add a shape to the Body
        polyDef = box2d.b2PolygonDef()

        polyDef.setVertices(vertices)
        polyDef.density = density
        polyDef.restitution = restitution
        polyDef.friction = friction

        body.CreateShape(polyDef)
        body.SetMassFromShapes()
                
        return body
   
    def concavePoly(self, vertices, dynamic=True, density=1.0, restitution=0.16, friction=0.5, screenCoord=False):
        # 1. Step: Reduce        
        # Detect if the polygon is closed or open
        if vertices[0] != vertices[-1]:        
            is_closed = False
        else:
            is_closed = True
                            
        # Continue reducing the vertecs
        x, y = c = tools_poly.calc_center(vertices)
        vertices = tools_poly.poly_center_vertices(vertices)
        
        # Bring coordinates into the world coordinate system (flip, camera offset, ...)
        if screenCoord: x, y = self.parent.to_world(c)
        else: x, y = c

        # If required, translate pixel -> meters
        if self.parent.input == INPUT_PIXELS:
            # translate pixel -> meters
            x /= self.parent.ppm
            y /= self.parent.ppm
        
        # Let's add the body
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        userData = { 'color' : self.parent.get_color() }
        bodyDef.userData = userData

        # Create the Body
        if not dynamic:
            density = 0

        body = self.parent.world.CreateBody(bodyDef)
                    
        self.parent.element_count += 1

        # Create the reusable Box2D polygon and circle definitions
        polyDef = box2d.b2PolygonDef()
        polyDef.vertexCount = 4 # rectangle
        polyDef.density = density
        polyDef.restitution = restitution
        polyDef.friction = friction

        circleDef = box2d.b2CircleDef()
        circleDef.density = density
        circleDef.radius = 0.086
        circleDef.restitution = restitution
        circleDef.friction = friction

        # Set the scale factor 
        factor = 8.0

        v2 = box2d.b2Vec2(*vertices[0])
        for v in vertices[1:]:
            v1    = v2.copy()
            v2    = box2d.b2Vec2(*v)
             
            vdir = v2-v1 # (v2x-v1x, v2y-v1y)
            vdir.Normalize()
            
            # we need a little size for the end part
            vn = box2d.b2Vec2(-vdir.y*factor, vdir.x*factor)

            v = [ v1+vn, v1-vn, v2-vn, v2+vn ] 

            # Create a line (rect) for each part of the polygon, 
            # and attach it to the body                
            polyDef.setVertices( [vi / self.parent.ppm for vi in v] )

            try:
                polyDef.checkValues()
            except ValueError:
                print "concavePoly: Created an invalid polygon!"
                return None

            body.CreateShape(polyDef)

            # Now add a circle to the points between the rects
            # to avoid sharp edges and gaps
            if not is_closed and v2.tuple() == vertices[-1]:
                # Don't add a circle at the end
                break

            circleDef.localPosition = v2 / self.parent.ppm
            body.CreateShape(circleDef)            
                                 
        # Now, all shapes have been attached
        body.SetMassFromShapes()                
        
        # Return hard and soft reduced vertices
        return body

    def complexPoly(self, vertices, dynamic=True, density=1.0, restitution=0.16, friction=0.5):
        # 1. Step: Reduce
        # 2. Step: See if start and end are close, if so then close the polygon
        # 3. Step: Detect if convex or concave
        # 4. Step: Start self.convexPoly or self.concavePoly
        vertices, is_convex = tools_poly.reduce_poly_by_angle(vertices)            
        #print "->", is_convex

        # If start and endpoints are close to each other, close polygon
        x1, y1 = vertices[0]
        x2, y2 = vertices[-1]
        dx = x2 - x1
        dy = y2 - y1
        l = sqrt((dx*dx)+(dy*dy))

        if l < 50:
            vertices[-1] = vertices[0]
        else:
            # Never convex if open (we decide so :)
            is_convex = False

        if tools_poly.is_line(vertices):
            # Lines shall be drawn by self.concavePoly(...)
            print "is line"
            is_convex = False
                    
        if is_convex:
            print "convex"
            return self.convexPoly(vertices, dynamic, density, restitution, friction), vertices
        else:
            print "concave"
            return self.concavePoly(vertices, dynamic, density, restitution, friction), vertices        
        

    def convexPoly(self, vertices, dynamic=True, density=1.0, restitution=0.16, friction=0.5):
        """ Add a complex polygon with vertices in absolute positions (meters or pixels, according
            to INPUT_PIXELS or INPUT_METERS). This function does the reduction and convec hulling 
            of the poly, and calls add_poly(...) 

            Parameters:
              vertices .. absolute vertices positions
              other ..... see [physics parameters]

            Return: box2d.b2Body
        """
        # NOTE: Box2D has a maximum poly vertex count, defined in Common/box2d.b2Settings.h (box2d.b2_maxPolygonVertices)
        # We need to make sure, that we reach that by reducing the poly with increased tolerance
        # Reduce Polygon
        tolerance = 10 #5
        v_new = vertices
        while len(v_new) > box2d.b2_maxPolygonVertices:
            tolerance += 1    
            v_new = tools_poly.reduce_poly(vertices, tolerance)
            
        print "convexPoly: Polygon reduced from %i to %i vertices | tolerance: %i" % (len(vertices), len(v_new), tolerance)
        vertices = v_new
             
        # So poly should be alright now
        # Continue reducing the vertecs
        vertices_orig_reduced = vertices    
        vertices = tools_poly.poly_center_vertices(vertices)

        vertices = tools_poly.convex_hull(vertices)

        if len(vertices) < 3: 
            return 
        
        # Define the body
        x, y = c = tools_poly.calc_center(vertices_orig_reduced)
        return self.poly((x,y), vertices, dynamic, density, restitution, friction)

    def to_b2vec(self, pt):
    # Convert vector to a b2vect
        pt = self.parent.to_world(pt)
        ptx, pty = pt
        ptx /= self.parent.ppm
        pty /= self.parent.ppm
        pt = box2d.b2Vec2(ptx, pty)
        return pt

    def joint(self, *args):
        print "* Add Joint:", args

        if len(args) == 4:
            # Distance Joint
            b1, b2, p1, p2 = args

            p1 = self.to_b2vec(p1)
            p2 = self.to_b2vec(p2)            
           
            jointDef = box2d.b2DistanceJointDef()
            jointDef.Initialize(b1, b2, p1, p2)
            jointDef.collideConnected = True
            
            self.parent.world.CreateJoint(jointDef)           
             
        elif len(args) == 3:
            # Revolute Joint between two bodies (unimplemented)
            pass

        elif len(args) == 2:
            # Revolute Joint to the Background, at point 
            b1 = self.parent.world.GetGroundBody()
            b2 = args[0]
            p1 = self.to_b2vec(args[1])

            jointDef = box2d.b2RevoluteJointDef()
            jointDef.Initialize(b1, b2, p1)
            self.parent.world.CreateJoint(jointDef)

        elif len(args) == 1:
            # Revolute Joint to the Background, body center
            b1 = self.parent.world.GetGroundBody()
            b2 = args[0]
            p1 = b2.GetWorldCenter()
            
            jointDef = box2d.b2RevoluteJointDef()
            jointDef.Initialize(b1, b2, p1)
            
            self.parent.world.CreateJoint(jointDef)

    def motor(self, body, pt, torque=900, speed=-10):
        # Revolute joint to the background with motor torque applied
        b1 = self.parent.world.GetGroundBody()
        pt = self.to_b2vec(pt)

        jointDef = box2d.b2RevoluteJointDef()
        jointDef.Initialize(b1, body, pt)
        jointDef.maxMotorTorque = torque
        jointDef.motorSpeed = speed
        jointDef.enableMotor = True

        self.parent.world.CreateJoint(jointDef)

    def mouseJoint(self, body, pos, jointForce=100.0):
        pos = self.parent.to_world(pos)
        x, y = pos
        x /= self.parent.ppm
        y /= self.parent.ppm

        mj = box2d.b2MouseJointDef()
        mj.body1 = self.parent.world.GetGroundBody()
        mj.body2 = body
        mj.target = (x, y)
        mj.maxForce = jointForce * body.GetMass()
        self.parent.mouseJoint = self.parent.world.CreateJoint(mj).getAsType()
        body.WakeUp()
        
    def remove_mouseJoint(self):
        if self.parent.mouseJoint:
            self.parent.world.DestroyJoint(self.parent.mouseJoint)
            self.parent.mouseJoint = None

