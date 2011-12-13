# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

class Tarea(object):

    def __init__(self, planificador, time_out, dt, funcion, parametros, una_vez):
        """

        Parametros:

            - time_out: el tiempo absoluto para ejecutar la tarea.
            - dt: la frecuencia de ejecución.
            - funcion: la funcion a invocar.
            - parametros: una lista de argumentos para la funcion anterior.
            - una_vez: indica si la funcion se tiene que ejecutar una sola vez.
        """

        self.planificador = planificador
        self.time_out = time_out
        self.dt = dt
        self.funcion = funcion
        self.parametros = parametros
        self.una_vez = una_vez

    def ejecutar(self):
        return self.funcion(*self.parametros)

    def eliminar(self):
        self.planificador.eliminar_tarea(self)

    def terminar(self):
        self.eliminar()

class TareaCondicional(Tarea):

    def ejecutar(self):
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

        pilas.mundo.agregar_tarea(2, hola)

    o bien, especificando argumentos para esa función:

        pilas.mundo.agregar_tarea(4, hola, 'persona')

    La función que se especifique como segundo argumento
    tiene que retornar True o False. Si retorna True será
    colocada nuevamente en la cola de tareas una vez que se
    ejecute (esto es útil para crear bucles).
    """

    def __init__(self):
        self.tareas_planificadas = []
        self.contador_de_tiempo = 0

    def obtener_cantidad_de_tareas_planificadas(self):
        return len(self.tareas_planificadas)

    def actualizar(self, dt):
        "Actualiza los contadores de tiempo y ejecuta las tareas pendientes."
        self.contador_de_tiempo += dt
        to_remove = []
         
        for tarea in self.tareas_planificadas:
            if self.contador_de_tiempo > tarea.time_out:
                tarea.ejecutar()
            
                if tarea.una_vez:
                    self.tareas_planificadas.remove(tarea)
                else:
                    w = self.contador_de_tiempo - tarea.time_out
                    parte_entera = int((w)/float(tarea.dt))
                    resto = w - (parte_entera * tarea.dt)

                    for x in range(parte_entera):
                        tarea.ejecutar()

                    tarea.time_out += tarea.dt + (parte_entera * tarea.dt) - resto

    def _agregar(self, tarea):
        "Agrega una nueva tarea para ejecutarse luego."
        self.tareas_planificadas.append(tarea)

    def una_vez(self, time_out, function, params=[]):
        tarea = Tarea(self, self.contador_de_tiempo + time_out, time_out, function, params, True)
        self._agregar(tarea)
        return tarea

    def siempre(self, time_out, function, params=[]):
        tarea = Tarea(self, self.contador_de_tiempo + time_out, time_out, function, params, False)
        self._agregar(tarea)
        return tarea

    def condicional(self, time_out, function, params=[]):
        tarea = TareaCondicional(self, self.contador_de_tiempo + time_out, time_out, function, params, False)
        self._agregar(tarea)
        return tarea

    def eliminar_tarea(self, tarea):
        self.tareas_planificadas.remove(tarea)

    def eliminar_todas(self):
        self.tareas_planificadas = []
