# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os
import interpolaciones
import pilas
from PySFML import sf
import sys

def hacer_flotante_la_ventana():
    "Hace flotante la ventana para i3 (el manejador de ventanas que utiliza hugo...)"

    try:
        os.system("i3-msg t >/dev/null")
    except:
        pass

def centrar_la_ventana(app):
    "Coloca la ventana principal en el centro del escritorio."

    vm = sf.VideoMode(100, 100)

    # Obtiene la resolución del escritorio y la ventana.
    desktop_mode = vm.GetDesktopMode()
    w, h = app.GetWidth(), app.GetHeight()

    # Calcula cual debería la coordenada para centrar la ventana.
    to_x = desktop_mode.Width/2 - w/2
    to_y = desktop_mode.Height/2 - h/2

    app.SetPosition(300, 100)

def es_interpolacion(an_object):
    "Indica si un objeto se comporta como una colisión."

    return isinstance(an_object, interpolaciones.Interpolacion)


def obtener_ruta_al_recurso(ruta):
    """Busca la ruta a un archivo de recursos.

    Los archivos de recursos (como las imagenes) se buscan en varios
    directorios (ver docstring de image.load), así que esta
    función intentará dar con el archivo en cuestión.
    """

    dirs = ['./', 'data', pilas.path, pilas.path + '/data']

    for x in dirs:
        full_path = os.path.join(x, ruta)
        #DEBUG: print "buscando en: '%s'" %(full_path)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." %(ruta))


def esta_en_sesion_interactiva():
    "Indica si pilas se ha ejecutado desde una consola interactiva de python."
    try:
        cursor = sys.ps1
        return True
    except AttributeError:
        return False

