# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os

def float_child_window():
    "Hace flotante la ventana para i3"
    try:
        os.system("i3-msg t >/dev/null")
    except:
        pass

def center_window(app):
    app.SetPosition(300, 100)
