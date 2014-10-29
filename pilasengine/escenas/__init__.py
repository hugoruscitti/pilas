# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.escenas.normal import Normal
from pilasengine.escenas.escena import Escena
from pilasengine.escenas.error import Error


class Escenas(object):
    """Representa la propiedad pilas.escenas

    Este objeto se encarga de hacer accesibles
    todas las escenas que incluye pilas.

    Por ejemplo, cuando un programador escribe
    "pilas.escenas.Normal()", en realidad está
    llamando a un método llamado Normal() que
    retorna un objeto escena listo para
    utilizar.
    """

    def __init__(self, pilas):
        self.pilas = pilas
        self.pila_de_escenas = []
        self.escena_actual = None
        self.iteraciones = 0

    def definir_escena(self, escena):
        if self.escena_actual:
            self.escena_actual.eliminar_el_motor_de_fisica()
            del self.escena_actual
            import gc
            gc.collect()

        self.pilas.log("Definiendo como activa la escena", escena)
        self.escena_actual = escena
        escena.iniciar()
        return escena

    def obtener_escena_actual(self):
        return self.escena_actual

    def realizar_actualizacion_logica(self):
        escena = self.obtener_escena_actual()

        # Resuelve un bug raro que activaba todos los callbacks de colisiones
        # cuando se usaba pilas desde un script. Resulta que en el instante
        # inicial de armar la escena todas las figuras fisicas están en la
        # coordenada (0, 0), y se necesita iterar al menos dos veces para
        # asegurarse que la fisica actualice las coordenadas y recién ahí
        # analizar colisiones.
        if self.iteraciones < 2:
            escena.colisiones.limpiar()
            self.iteraciones += 1
        else:
            escena.colisiones.actualizar()

        escena.cuando_actualiza.emitir()
        escena.actualizar_fisica()
        escena.actualizar_actores()
        escena.actualizar_interpolaciones()
        escena.tareas.actualizar(1/60.0)
        escena.actualizar()

    def realizar_actualizacion_logica_en_modo_pausa(self):
        escena = self.obtener_escena_actual()
        escena.actualizar_interpolaciones_en_modo_pause()

    def forzar_actualizacion_de_interpolaciones(self):
        escena = self.obtener_escena_actual()
        escena.forzar_actualizacion_de_interpolaciones()

    def simular_actualizacion_logica(self):
        escena = self.obtener_escena_actual()
        escena.cuando_actualiza.emitir()
        escena.actualizar_actores()
        escena.tareas.actualizar(1/60.0)
        escena.actualizar_interpolaciones(1/60.0)
        escena.actualizar()

    def realizar_dibujado(self, painter):
        escena = self.obtener_escena_actual()
        escena.dibujar_actores(painter)

    def Normal(self):
        import normal
        nueva_escena = normal.Normal(self.pilas)
        return self.definir_escena(nueva_escena)

    def Error(self, titulo, descripcion):
        import error
        nueva_escena = error.Error(self.pilas, titulo, descripcion)
        return self.definir_escena(nueva_escena)
