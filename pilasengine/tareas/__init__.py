# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.tareas.tarea import Tarea
from pilasengine.tareas.tarea_condicional import TareaCondicional


class Tareas(object):
    """Contenedor de tareas a ejecutar por tiempo.

    El Tareas es un planificador de tareas, permite que
    podamos ejecutar funciones y métodos luego de transcurrido
    el tiempo que queramos.

    Por ejemplo, si se quiere que el planificardor ejecute
    una función dentro de dos segundos podemos escribir:

        >>> pilas.tareas.agregar_tarea(2, hola)

    o bien, especificando argumentos para esa función:

        >>> pilas.tareas.agregar_tarea(4, hola, 'persona')

    La función que se especifique como segundo argumento
    tiene que retornar True o False. Si retorna True será
    colocada nuevamente en la cola de tareas una vez que se
    ejecute (esto es útil para crear bucles).
    """

    def __init__(self, escena, pilas):
        "Inicializa el gestor de tareas."
        self.escena = escena
        self.pilas = pilas
        self.tareas_planificadas = []
        self.contador_de_tiempo = 0

    def obtener_cantidad_de_tareas_planificadas(self):
        """Retora la cantidad de tareas planificadas."""
        return len(self.tareas_planificadas)

    def actualizar(self, dt):
        """Actualiza los contadores de tiempo y ejecuta las tareas pendientes.

        :param dt: Tiempo transcurrido desde la anterior llamada.
        """
        self.contador_de_tiempo += dt
        tareas_a_eliminar = []

        for tarea in self.tareas_planificadas:
            if self.contador_de_tiempo > tarea.time_out:
                tarea.ejecutar()

                if tarea.una_vez:
                    tareas_a_eliminar.append(tarea)
                else:
                    tarea.time_out += tarea.dt

        for x in tareas_a_eliminar:
            if x in self.tareas_planificadas:
                self.tareas_planificadas.remove(x)

    def _agregar(self, tarea):
        """Agrega una nueva tarea para ejecutarse luego.

        :param tarea: Referencia a la tarea que se debe agregar.
        """
        self.tareas_planificadas.append(tarea)

    def una_vez(self, time_out, function, *args, **kwargs):
        """Genera una tarea que se ejecutará usan sola vez.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        :param params: Parámetros que tiene que recibir la función a ejecutar.
        """
        tarea = Tarea(self, self.pilas, True, self.contador_de_tiempo + time_out, time_out,
                      function, *args, **kwargs)
        self._agregar(tarea)
        return tarea

    def siempre(self, time_out, function, *args, **kwargs):
        """Genera una tarea para ejecutar todo el tiempo, sin expiración.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        """
        tarea = Tarea(self, self.pilas, False, self.contador_de_tiempo+time_out, time_out,
                      function, *args, **kwargs)
        self._agregar(tarea)
        return tarea

    def condicional(self, time_out, function, *args, **kwargs):
        """Genera una tarea que se puede ejecutar una vez o mas, pero que tiene una condición.

        La tarea se ejecutará hasta que la función a ejecutar devuelva False.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        """
        tarea = TareaCondicional(self, self.pilas, False, self.contador_de_tiempo+time_out,
                                 time_out, function, *args, **kwargs)
        self._agregar(tarea)
        return tarea

    def agregar(self, *k, **kw):
        return self.condicional(*k, **kw)

    def eliminar_tarea(self, tarea):
        """Elimina una tarea de la lista de tareas planificadas.

        :param tarea: Referencia a la tarea que se tiene que eliminar.
        """
        self.tareas_planificadas.remove(tarea)

    def eliminar_todas(self):
        """Elimina todas las tareas de la lista de planificadas."""
        self.tareas_planificadas = []
