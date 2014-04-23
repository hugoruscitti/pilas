# -*- encoding: utf-8 -*-
from pilasengine.escenas.escena import Escena

class Error(Escena):
    """Representa la escena de errores de pilas.

    Esta escena muestra el tipo de error en la pantalla,
    junto con una descripción y el archivo que ocasionó
    el error.
    """

    def __init__(self, pilas, error):
        Escena.__init__(self, pilas)
        self._error = error

    def iniciar(self):
        self.fondo = self.pilas.fondos.Plano()
        self.actor_error = self.pilas.actores.MensajeError(self._error)

    def actualizar(self):
        pass

    def terminar(self):
        pass