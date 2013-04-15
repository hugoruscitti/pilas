# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


'''
pilas.pilasverion -- Definición de la version actual de pilas y funciones
para compararla.

'''

VERSION = "0.78"


def compareactual(v1):
    """Compara la versión actual de pilas con una que se pasa como parámetro
    
    Sus posibles retornos son:
    
    - **-1** si *versión actual de pilas* < ``v1``.
    - **0** si *versión actual de pilas* == ``v1``.
    - **1** si *versión actual de pilas* > ``v1``.
    
    """
    return compare(VERSION, v1)


def compare(v0, v1):
    """Compara dos versiones de pilas.
    
    Sus posibles retornos son
    
    - **-1** si ``v0`` < ``v1``.
    - **0** si ``v0`` == ``v1``.
    - **1** si ``v0`` > ``v1``.
    
    """
    v0 = v0.split(".")
    v1 = v1.split(".")
    return -1 if v0 < v1 else 0 if v0 == 1 else 1

