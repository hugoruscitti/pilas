# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.actores.actor import ActorEliminadoException


class Tarea(object):

    def __init__(self, planificador, pilas, una_vez, time_out, dt, funcion,
                 *args, **kwargs):
        """Representa una tarea que se puede ejecutar dentro del planificador.

        :param time_out: El tiempo absoluto para ejecutar la tarea.
        :param dt: La frecuencia de ejecución.
        :param funcion: La funcion a invocar.
        :param parametros: Una lista de argumentos para la funcion anterior.
        :param una_vez: Indica si la funcion se tiene que ejecutar una sola vez.
        """

        self.planificador = planificador
        self.una_vez = una_vez
        self.time_out = time_out
        self.dt = dt
        self.funcion = funcion
        self.args, self.kwargs = args, kwargs
        self.pilas = pilas

    def ejecutar(self):
        "Ejecuta la tarea."
        try:
            return self.funcion(*self.args, **self.kwargs)
        except ActorEliminadoException:
            self.pilas.log("Se evitó ejecutar la tarea sobre un actor eliminado...")


    def eliminar(self):
        "Quita la tarea del planificador para que no se vuelva a ejecutar."
        self.planificador.eliminar_tarea(self)

    def terminar(self):
        "Termina la tarea (alias de eliminar)."
        self.eliminar()