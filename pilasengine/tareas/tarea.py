# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


class Tarea(object):

    def __init__(self, planificador, time_out, dt, funcion,
                 parametros, una_vez):
        """Representa una tarea que se puede ejecutar dentro del planificador.

        :param time_out: El tiempo absoluto para ejecutar la tarea.
        :param dt: La frecuencia de ejecución.
        :param funcion: La funcion a invocar.
        :param parametros: Una lista de argumentos para la funcion anterior.
        :param una_vez: Indica si la funcion se tiene que ejecutar una sola vez.
        """

        self.planificador = planificador
        self.time_out = time_out
        self.dt = dt
        self.funcion = funcion
        self.parametros = parametros
        self.una_vez = una_vez

    def ejecutar(self):
        "Ejecuta la tarea."
        return self.funcion(*self.parametros)

    def eliminar(self):
        "Quita la tarea del planificador para que no se vuelva a ejecutar."
        self.planificador.eliminar_tarea(self)

    def terminar(self):
        "Termina la tarea (alias de eliminar)."
        self.eliminar()