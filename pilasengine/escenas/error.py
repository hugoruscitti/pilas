# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.escenas.escena import Escena


class Error(Escena):
    """Representa la escena de errores de pilas.

    Esta escena muestra el tipo de error en la pantalla,
    junto con una descripción y el archivo que ocasionó
    el error.
    """

    def iniciar(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fondo = self.pilas.fondos.Plano()
        self.actor_error = self.pilas.actores.MensajeError(self.titulo,
                                                           self.descripcion)

    def actualizar(self):
        pass

    def terminar(self):
        pass
