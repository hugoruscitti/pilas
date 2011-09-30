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

def definir_gravedad(x=0, y=-900):
    pilas.mundo.fisica.definir_gravedad(x, y)


def leer(texto):
    # TODO: usar speak binding en lugar de subprocess.
    try:
        comando = subprocess.Popen(["espeak",  texto, "-v", "es-la"], 
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)
    except OSError:
        pass

