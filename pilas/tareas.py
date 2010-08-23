# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

class Tareas:
    """Contenedor de tareas a ejecutar por tiempo.

    El Tareas es un planificador de tareas, permite que
    podamos ejecutar funciones y métodos luego de transcurrido
    el tiempo que queramos.

    Por ejemplo, si se quiere que el planificardor ejecute
    una función dentro de dos segundos podemos escribir:

        pilas.add_task(2, hola)

    o bien, especificando argumentos para esa función:

        pilas.add_task(4, hola, 'persona')

    La función que se especifique como segundo argumento
    tiene que retornar True o False. Si retorna True será
    colocada nuevamente en la cola de tareas una vez que se
    ejecute (esto es útil para crear bucles).
    """

    def __init__(self):
        self.tasks = []
        self.time_counter = 0

    def update(self, dt):
        "Actualiza los contadores de tiempo y ejecuta las tareas pendientes."
        self.time_counter += dt
        to_remove = []

        for t, dt, function, params in self.tasks:
            if self.time_counter > t:
                must_continue = function(*params)
                to_remove.append((t, dt, function, params))

                if must_continue:
                    self.agregar(dt, function, params)

        # Elimina de la lista de trabajos los que ya han sido ejecutados.
        if to_remove:
            for x in to_remove:
                self.tasks.remove(x)

    def agregar(self, time_out, function, params):
        "Agrega una nueva tarea para ejecutarse luego."
        # El formato de la tarea es:
        #          (tiempo_absoluto, tiempo
        self.tasks.append((self.time_counter + time_out, time_out, function, params))

