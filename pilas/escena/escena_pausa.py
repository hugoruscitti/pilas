# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import pilas.actores
from pilas.escena import Base
import pilas.colores
import pilas.fondos


class Pausa(Base):
    """ Escena para pausar el juego.
    Por defecto crea un Actor llamado pausa en el centro de la pantalla.
    """

    def __init__(self):
        Base.__init__(self)
        self.escena_pausa = True

    def iniciar(self):
        pass

