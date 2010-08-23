# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os
import interpolaciones

def hacer_flotante_la_ventana():
    "Hace flotante la ventana para i3"
    try:
        os.system("i3-msg t >/dev/null")
    except:
        pass

def centrar_la_ventana(app):
    app.SetPosition(300, 100)

def es_interpolacion(an_object):
    return isinstance(an_object, interpolaciones.Interpolacion)
