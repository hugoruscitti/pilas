# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
from pilas.escena.escena_base import EscenaBase
import pilas.colores
import pilas.fondos


class EscenaNormal(EscenaBase):
    """ Escena básica de pilas.
    Si no se define ninguna escena, cuando se ejecuta:

    >>> pilas.iniciar()
    >>> pilas.ejecutar()

    esta es la escena que se muestra en la pantalla.
    """

    def __init__(self):
        EscenaBase.__init__(self)

    def iniciar(self):
        fondo = pilas.fondos.Color(pilas.colores.grisclaro)
