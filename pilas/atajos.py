# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

fabricar = pilas.actores.utils.fabricar

def crear_grupo(*k):
    return pilas.grupos.Grupo(k)

def definir_gravedad(x=0, y=-900):
    pilas.fisica.fisica.definir_gravedad(x, y)
