# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import subprocess

fabricar = pilas.actores.utils.fabricar

def crear_grupo(*k):
    return pilas.grupos.Grupo(k)

def definir_gravedad(x, y):
    pilas.escena_actual().fisica.definir_gravedad(x, y)

def leer(texto):
    # TODO: usar speak binding en lugar de subprocess.
    try:
        comando = subprocess.Popen(["espeak",  texto, "-v", "es-la"],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)
    except OSError:
        pass

def ocultar_puntero_del_mouse():
    pilas.mundo.motor.ocultar_puntero_del_mouse()

def mostrar_puntero_del_mouse():
    pilas.mundo.motor.mostrar_puntero_del_mouse()

def definir_modos(*k, **kv):
    pilas.mundo.motor.canvas.depurador.definir_modos(*k, **kv)
