# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.tareas.tarea import Tarea


class TareaCondicional(Tarea):
    """Representa una tarea similar a Tarea, pero que solo se ejecuta si El
    retorno de la función a ejecutar devuelve True.
    """

    def ejecutar(self):
        """Ejecuta la tarea, y se detiene si no revuelve True."""
        retorno = Tarea.ejecutar(self)

        if not retorno:
            self.una_vez = True