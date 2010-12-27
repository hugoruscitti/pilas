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
import pygame
from pygame.locals import *

import tools

COLOR_HEX_BLUE1 = "6491a4"
COLOR_HEX_BLUE2 = "9ec9ff"

class MenuItem:   
    # padding [px]: left, top, right, bottom
    padding = (5, 2, 5, 2)
 
    def empty(self, *args):
        pass
        
    def __init__(self, title, pos, userData, parent=None, callback=None):
        self.title = title
        self.userData = userData
        self.parent = parent
        self.childs = []
        
        if self.parent:
            self.visible = False
        else:
            self.visible = True
        
        if callback:
            self.callback = callback
        else:
            self.callback = self.empty

        # Create Surface and Stuff :)
        self.font = pygame.font.Font(None, 32)
        text = self.font.render(title, 1, (255,255,255))

        rx, ry, rw, rh = rect = text.get_rect()
        pl, pt, pr, pb = self.padding
        
        s1 = pygame.Surface((rw+pl+pr, rh+pt+pb))
        s1.fill(tools.hex2rgb(COLOR_HEX_BLUE1))
        s1.blit(text, (pl, pt))

        s2 = pygame.Surface((rw+pl+pr, rh+pt+pb))
        s2.fill(tools.hex2rgb(COLOR_HEX_BLUE2))
        s2.blit(text, (pl, pt))
        
        self.rect = s1.get_rect().move(pos)

        self.surface_inactive = s1
        self.surface_active = s2
        
    def pos_inside(self, pos):
        if not self.visible:
            return False
            
        x,y,w,h = self.rect
        px, py = pos
        
        if px > x and px < x+w and py > y and py < y+h:
            return True
        else:
            return False
                
class MenuClass:
    """ Important: Never delete an Item, just overwrite it if deleting,
        else the menuitem id's get messed up
    """
    # current active menu point it
    focus = False
    
    # each item is stored as MenuItem
    items = []    

    # where to start drawing
    start_at = (0, 0)
   
    # menubar properties
    height = 0        # px
    width = 0         # px (set in set_width)
    setWidth = False  # if width was set by hand (if not, increase width by adding stuff)
    
    def __init__(self):
        self.draw_at = self.start_at
        
    def set_width(self, width):
        self.setWidth = True
        self.width = width
        
    def addItem(self, title, callback=None, userData='', parent=None):
        # Get position for the Item
        if parent: draw_at = (0,0)
        else: draw_at = self.draw_at
        
        # Create Items
        M = MenuItem(title=title, pos=draw_at, userData=userData, parent=parent, callback=callback)
        self.items.append(M)
                
        # Set a new position
        x,y,w,h = M.rect
        x, y = self.draw_at
        
        if parent:
            # Set the info that the item has a child to the parent item
            self.items[parent-1].childs.append(len(self.items)-1) 

        else:
            # New next drawing position
            self.draw_at = (x+w, y)

            # Adjust the width of the menu bar
            if not self.setWidth:
                self.width = x+w     

        # Adjust the height of the menu bar
        if h > self.height: self.height = h + 2

        # Return array id of this item
        return len(self.items)
        
    def click(self, pos):
        """ Checks a click for menuitems and starts the callback if found
            
            Return: True if a menu item was found or hit the MenuBar, and False if not
        """
        focus_in = self.focus
        
        found = False
        for i in xrange(len(self.items)):
            item = self.items[i]
            if item.pos_inside(pos):
                found = True
                item.callback(item.title, item.userData)
                
                # Expand the menu if necessary
                if len(item.childs) > 0:
                    self.focus = i+1
                    
        # Close any opened menu windows if clicked somewhere else 
        if self.focus == focus_in:
            self.focus = False
            self.subwin_rect = (0,0,0,0)
            for item in self.items:
                if item.parent:
                    item.visible = False
                 
        # Check if click is inside menubar
        x,y = pos
        mx, my = self.start_at
        
        if found:
            return True
        else: 
            return False
        
    def draw(self, surface):
        """ Draw the menu with pygame on a given surface
        """
        s = pygame.Surface((self.width, self.height))
        s.fill(tools.hex2rgb(COLOR_HEX_BLUE1))

        surface.blit(s, (0,0))
        
        for i in xrange(len(self.items)):
            item = self.items[i]
            if not item.parent: 
                x,y,w,h = item.rect
                if self.focus == i+1:
                    surface.blit(item.surface_active, (x,y))
                else:
                    surface.blit(item.surface_inactive, (x,y))

        # If a menu item is open, draw that
        if self.focus:
            width = 0
            height = 0

            i = []
            for j in self.items:
                if j.parent == self.focus:
                    i.append(j)
                    x, y, w, h = j.rect
                    if w > width: width = w
                    height += h

            if len(i) > 0:
                s = pygame.Surface((width, height))
                s.fill(tools.hex2rgb(COLOR_HEX_BLUE1))

                # Parent Coordinates    
                px, py, pw, ph = self.items[self.focus-1].rect
                
                # y Counter
                y = 0
                
                for item in i:
                    item.visible = True
                    s.blit(item.surface_inactive, (0, y))

                    ix, iy, iw, ih = item.rect                        
                    if (ix, iy) == (0, 0):
                        item.rect = item.rect.move((px, y+ph))
                        ix, iy, iw, ih = item.rect                        

                    if iw < width:
                        item.rect = (ix,iy,width,ih)

                    y += ih
                
                surface.blit(s, (px,py+ph))
                self.subwin_rect = s.get_rect().move(px, py+ph)

