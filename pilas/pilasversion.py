# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


'''
pilas.pilasverion
=================

Definición de la version actual de pilas y funciones para compararla.

'''


#: Contiene la versión actual de pilas.
VERSION = "0.84"


def compareactual(v):
    """Compara la versión actual de pilas con una que se pasa como parámetro

    Sus posibles retornos son:

    - **-1** si *versión actual de pilas* < ``v``.
    - **0** si *versión actual de pilas* == ``v``.
    - **1** si *versión actual de pilas* > ``v``.

    :param v: versión a comparar con la actual.
    :type v: str

    """
    return compare(VERSION, v)


def compare(v0, v1):
    """Compara dos versiones de pilas.

    Sus posibles retornos son

    - **-1** si ``v0`` < ``v1``.
    - **0** si ``v0`` == ``v1``.
    - **1** si ``v0`` > ``v1``.

    :param v0: primer versión a comparar.
    :type v0: str
    :param v1: segunda versión a comparar.
    :type v1: str

    """
    v0 = v0.split(".")
    v1 = v1.split(".")
    return -1 if v0 < v1 else 0 if v0 == 1 else 1

