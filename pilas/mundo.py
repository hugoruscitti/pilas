# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import time
import sys

from PySFML import sf

import ventana
import control
import camara
import escenas
import utils
import eventos
import tareas
import pytweener
import pilas
import modos_de_mundo


class Mundo:
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.

    Este objeto delega en otros el modo de ejecucion en un momento dado, 
    por ejemplo cuando inicia se usa el "ModoEjecucionNormal" y cuando el usuario
    pulsa F12 este modo cambia por "ModoEjecucionNormal".
    """

    def __init__(self, ancho, alto, titulo):
        self.ventana = ventana.iniciar(ancho, alto, titulo)
        ventana.ancho = ancho
        ventana.alto = alto

        self.control = control.Control()

        # todo: llevar a ventana.iniciar
        utils.hacer_flotante_la_ventana()
        pilas.motor.centrar_ventana()

        self.camara = camara.Camara(self.ventana)

        self.escena_actual = None

        # Genera los administradores de tareas e interpolaciones.
        self.tweener = pytweener.Tweener()
        self.tasks = tareas.Tareas() 

        self.modo_ejecucion = None
        self.definir_modo_ejecucion(modos_de_mundo.ModoEjecucionNormal(self))
        self.salir = False

    def definir_modo_ejecucion(self, nuevo_modo):
        if self.modo_ejecucion:
            self.modo_ejecucion.salir()

        self.modo_ejecucion = nuevo_modo

    def terminar(self):
        self.salir = True

    def ejecutar_bucle_principal(self):
        "Mantiene en funcionamiento el motor completo."


        while not self.salir:

            # Mantiene el control de tiempo y lo reporta al sistema
            # de interpolaciones y tareas.
            self.modo_ejecucion.esperar()
            self.modo_ejecucion.actualizar_simuladores()

            # Emite el aviso de actualizacion a los receptores.
            self.modo_ejecucion.emitir_evento_actualizar()

            # Procesa todos los eventos.
            pilas.motor.procesar_y_emitir_eventos()

            # Analiza colisiones entre los actores
            self.modo_ejecucion.analizar_colisiones()

            # Dibuja la escena actual y a los actores
            self.escena_actual.actualizar()
            self.escena_actual.dibujar(self.ventana)

            self.modo_ejecucion.actualizar_actores()
            self.modo_ejecucion.dibujar_actores()

            # Muestra los cambios en pantalla.
            pilas.motor.actualizar_pantalla()

        self._cerrar_ventana()

    def _cerrar_ventana(self):
        pilas.motor.cerrar_ventana()
        sys.exit(0)

    def definir_escena(self, escena_nueva):
        "Cambia la escena que se muestra en pantalla"

        if self.escena_actual:
            eliminar_actores = True
        else:
            eliminar_actores = False

        self.escena_actual = escena_nueva


    def agregar_tarea(self, time_out, function, *params): 
        self.tasks.agregar(time_out, function, params)

    def alternar_pausa(self):
        self.modo_ejecucion.alternar_pausa()

    def alternar_modo_depuracion(self):
        self.modo_ejecucion.alternar_modo_depuracion()



'''

    def cambiar_a_modo_pausa(self):
        self.definir_modo_ejecucion(ModoEjecucionPausado(self))

    def cambiar_a_modo_depuracion(self):
        pilas.mundo.definir_modo_ejecucion(ModoEjecucionDepuracion(self))
'''
