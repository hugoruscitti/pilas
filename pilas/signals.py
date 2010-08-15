# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import dispatch

mouse_move = dispatch.Signal(providing_args=['x', 'y'])
mouse_click = dispatch.Signal(providing_args=['button', 'x', 'y'])
mouse_wheel = dispatch.Signal(providing_args=['delta'])

