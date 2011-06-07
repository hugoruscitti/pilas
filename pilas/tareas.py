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

    def actualizar(self, dt):
        "Actualiza los contadores de tiempo y ejecuta las tareas pendientes."
        self.time_counter += dt
        to_remove = []
         

        for t, dt, function, params, ejecutar_una_sola_vez in self.tasks:
            if self.time_counter > t:


                if ejecutar_una_sola_vez == "condicional":
                    ejecutar_una_sola_vez = not function(*params)
                    to_remove.append((t, dt, function, params, ejecutar_una_sola_vez))
                elif ejecutar_una_sola_vez:
                    function(*params)
                    to_remove.append((t, dt, function, params, ejecutar_una_sola_vez))
                else:
                    w = self.time_counter - t
                    parte_entera = int((w)/float(dt))
                    resto = w - (parte_entera * dt)

                    for x in range(parte_entera + 1):
                        function(*params)

                    to_remove.append((t, dt, function, params, ejecutar_una_sola_vez))

                    self._agregar(self.time_counter + (1 - resto) * dt, dt, function, params)

        # Elimina de la lista de trabajos los que ya han sido ejecutados.
        if to_remove:
            for x in to_remove:
                self.tasks.remove(x)

    def _agregar(self, proxima_ejecucion, periodo, function, params, invocar_una_vez=False):
        "Agrega una nueva tarea para ejecutarse luego."
        self.tasks.append((proxima_ejecucion, periodo, function, params, invocar_una_vez))

    def una_vez(self, time_out, function, params=[]):
        self._agregar(self.time_counter + time_out, time_out, function, params, True)

    def siempre(self, time_out, function, params=[]):
        self._agregar(self.time_counter + time_out, time_out, function, params, False)

    def condicional(self, time_out, function, params=[]):
        self._agregar(self.time_counter + time_out, time_out, function, params, "Condicional")
