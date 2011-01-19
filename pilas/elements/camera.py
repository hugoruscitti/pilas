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

class Camera:
    """ The Camera class. We will see :)
        Please also see: http://www.assembla.com/spaces/elements/tickets/31
        
        This class currently handles:
        - Scaling factor
        - Screen Offset from the World Coordinate System
        
        Inputs from the user have to be checked for them.
        - Places to check for it: elements.py, drawing.py, add_objects.py
        
    """
    scale_factor = 1.0          # All coords to the renderer are multiplied with the scale factor in elements.draw()
    track_body = None           # Body which means to be tracked. Offset is set at each elements.draw()
    
    def __init__(self, parent):
        self.parent = parent
            
    def track(self, body):
        """ Start tracking a specific body
        """
        self.track_body = body

    def track_stop(self):
        """ Stop tracking a body
        """
        self.track_body = None
            
    def center(self, pos, screenCoord=True, stopTrack=True):
        """ Centers the camera at given screen coordinates -- in pixel
            Typical call: world.camera.center(event.pos)
            
            Problem: Works ONLY WITH screenCoord now!
        """        
        x, y = pos

        x -= self.parent.display_width / 2
        y -= self.parent.display_height  / 2

        if screenCoord:
            x /= self.scale_factor
            y /= self.scale_factor

        # Set the offset
        self.inc_offset((x, y), screenCoord, stopTrack)
        
    def set_offset(self, offset, screenCoord=True, stopTrack=True):
        """ Set an offset from the screen to the world cs 
            -- in screen (or world) coordinates and in pixel
        """
        # Stop tracking of an object
        if stopTrack: self.track_stop()

        # If screenCoords, we have to bring them to the world cs
        if screenCoord: x, y = self.parent.to_world(offset)
        else: x, y = offset

        self._set_offset((x/self.parent.ppm, y/self.parent.ppm))

    def inc_offset(self, offset, screenCoord=True, stopTrack=True):
        """ Increment an offset from the screen to the world cs -- in world coordinates and in pixel
        """
        # Stop tracking of an object
        if stopTrack: self.track_stop()

        # Get Current Offset
        x, y = self.parent.screen_offset_pixel
        dx, dy = offset

        # Bring the directions into the world coordinate system
        if screenCoord:
            if self.parent.inputAxis_x_left: dx *= -1
            if self.parent.inputAxis_y_down: dy *= -1
                
        # Set New Offset
        self._set_offset(((x+dx)/self.parent.ppm, (y+dy)/self.parent.ppm))
                
    def _set_offset(self, offset):
        """ Set the screen offset to the world coordinate system
            (using meters and the world coordinate system's orientation)
        """
        x, y = offset            
        self.parent.screen_offset = (x, y)
        self.parent.screen_offset_pixel = (x*self.parent.ppm, y*self.parent.ppm)
        
    def set_scale_factor(self, factor=1.0):
        """ Zoom factor for the renderer 1.0 = 1:1 (original)
        """
        self.scale_factor = factor
        
    def inc_scale_factor(self, factor=0.0):
        """ Increases the zooms for the renderer a given factor
        """
        self.scale_factor += factor
        
        