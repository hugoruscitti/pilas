# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Pilas Activity.  Live interpreter to learn programming with games."""

import gtk
import logging

from gettext import gettext as _

from subprocess import Popen

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton

import os
import sys
import copy

base = os.environ['SUGAR_BUNDLE_PATH']
os.chdir(base)

qtlib = os.path.join(base, 'qt/lib/')
new_env = copy.copy(os.environ)
new_env['LD_LIBRARY_PATH'] = qtlib

class PilasActivity(activity.Activity):
    """Pilas class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the Pilas activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features,
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        socket = gtk.Socket()
        socket.connect("plug-added", self._on_plugged_event)
        socket.set_flags(gtk.CAN_FOCUS)
        self.set_canvas(socket)
        self.set_focus(socket)
        socket.show()

        screen_width = gtk.gdk.screen_width()
        screen_height = gtk.gdk.screen_height()

        Popen(["python", "pilas_plug.py", str(socket.get_id()),
               str(screen_width), str(screen_height)], env=new_env)

    def _on_plugged_event(self, widget):
        logging.info("Plug inserted")
