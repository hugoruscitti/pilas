# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

class Tarea(object):

    def __init__(self, planificador, time_out, dt, funcion, parametros, una_vez):
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

class TareaCondicional(Tarea):
    """Representa una tarea similar a Tarea, pero que solo se ejecuta si El
    retorno de la función a ejecutar devuelve True.
    """

    def ejecutar(self):
        """Ejecuta la tarea, y se detiene si no revuelve True."""
        retorno = Tarea.ejecutar(self)

        if not retorno:
            self.una_vez = True

class Tareas(object):
    """Contenedor de tareas a ejecutar por tiempo.

    El Tareas es un planificador de tareas, permite que
    podamos ejecutar funciones y métodos luego de transcurrido
    el tiempo que queramos.

    Por ejemplo, si se quiere que el planificardor ejecute
    una función dentro de dos segundos podemos escribir:

        >>> pilas.mundo.agregar_tarea(2, hola)

    o bien, especificando argumentos para esa función:

        >>> pilas.mundo.agregar_tarea(4, hola, 'persona')

    La función que se especifique como segundo argumento
    tiene que retornar True o False. Si retorna True será
    colocada nuevamente en la cola de tareas una vez que se
    ejecute (esto es útil para crear bucles).
    """

    def __init__(self):
        "Inicializa el gestor de tareas."
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
                    w = self.contador_de_tiempo - tarea.time_out
                    parte_entera = int((w)/float(tarea.dt))
                    resto = w - (parte_entera * tarea.dt)

                    for x in range(parte_entera):
                        tarea.ejecutar()

                    tarea.time_out += tarea.dt + (parte_entera * tarea.dt) - resto

        for x in tareas_a_eliminar:
            if x in self.tareas_planificadas:
                self.tareas_planificadas.remove(x)

    def _agregar(self, tarea):
        """Agrega una nueva tarea para ejecutarse luego.

        :param tarea: Referencia a la tarea que se debe agregar.
        """
        self.tareas_planificadas.append(tarea)

    def una_vez(self, time_out, function, params=[]):
        """Genera una tarea que se ejecutará usan sola vez.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        :param params: Parámetros que tiene que recibir la función a ejecutar.
        """
        tarea = Tarea(self, self.contador_de_tiempo + time_out, time_out, function, params, True)
        self._agregar(tarea)
        return tarea

    def siempre(self, time_out, function, params=[]):
        """Genera una tarea para ejecutar todo el tiempo, sin expiración.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        :param params: Parámetros que tiene que recibir la función a ejecutar.
        """
        tarea = Tarea(self, self.contador_de_tiempo + time_out, time_out, function, params, False)
        self._agregar(tarea)
        return tarea

    def condicional(self, time_out, function, params=[]):
        """Genera una tarea que se puede ejecutar una vez o mas, pero que tiene una condición.

        La tarea se ejecutará hasta que la función a ejecutar revuelva False.

        :param time_out: Cantidad se segundos que deben transcurrir para ejecutar la tarea.
        :param function: Función a ejecutar para lanzar la tarea.
        :param params: Parámetros que tiene que recibir la función a ejecutar.
        """
        tarea = TareaCondicional(self, self.contador_de_tiempo + time_out, time_out, function, params, False)
        self._agregar(tarea)
        return tarea

    def eliminar_tarea(self, tarea):
        """Elimina una tarea de la lista de tareas planificadas.

        :param tarea: Referencia a la tarea que se tiene que eliminar.
        """
        self.tareas_planificadas.remove(tarea)

    def eliminar_todas(self):
        """Elimina todas las tareas de la lista de planificadas."""
        self.tareas_planificadas = []
