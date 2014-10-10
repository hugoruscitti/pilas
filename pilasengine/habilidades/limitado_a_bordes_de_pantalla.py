# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.habilidades import se_mantiene_en_pantalla


class LimitadoABordesDePantalla(se_mantiene_en_pantalla.SeMantieneEnPantalla):
    """Se asegura de que el actor no pueda salir por los bordes
    de la pantalla.
    """
    def iniciar(self, receptor):
        """
        :param receptor: El actor que aprenderá la habilidad.
        """
        super(LimitadoABordesDePantalla, self).iniciar(receptor, permitir_salida=False)