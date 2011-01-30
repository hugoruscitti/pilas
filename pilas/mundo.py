# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import time
import sys

import ventana
import control
import camara
import escenas
import utils
import eventos
import tareas
import pytweener
import depurador
import pilas


class Mundo:
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.
    """

    def __init__(self, ancho, alto, titulo, fps=60, economico=True):
        self.ventana = ventana.iniciar(ancho, alto, titulo)
        self.fps = fps
        self.economico = economico
        ventana.ancho = ancho
        ventana.alto = alto

        self.control = control.Control()

        # todo: llevar a ventana.iniciar
        utils.hacer_flotante_la_ventana()
        pilas.motor.centrar_ventana()

        self.fps = pilas.fps.FPS(self.fps, self.economico)
        self.camara = camara.Camara(self.ventana)
        
        self.depurador = depurador.Depurador(self.fps)

        self.escena_actual = None

        # Genera los administradores de tareas e interpolaciones.
        self.tweener = pytweener.Tweener()
        self.tasks = tareas.Tareas() 
        
        # Genera el motor de fisica.
        self.fisica = pilas.fisica.Fisica()
        self.fisica.crear_suelo()
        
        self.pausa_habilitada = False
        self.depuracion_fisica_habilitada = False
        self.funciones_depuracion = []
        self.salir = False

    def terminar(self):
        self.salir = True

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."


        while not self.salir:

            # Invoca varias veces a la actualizacion si el equipo
            # es lento.
            for x in range(self.fps.actualizar()):
                # Mantiene el control de tiempo y lo reporta al sistema
                # de interpolaciones y tareas.

                pilas.motor.procesar_y_emitir_eventos()
                
                if not self.pausa_habilitada:
                    self._realizar_actualizacion_logica(ignorar_errores)

            self._realizar_actualizacion_grafica()

        self._cerrar_ventana()

    def _realizar_actualizacion_logica(self, ignorar_errores):
        self.actualizar_simuladores()

        # Emite el aviso de actualizacion a los receptores.
        self.emitir_evento_actualizar()

        # Analiza colisiones entre los actores
        if ignorar_errores:
            try:
                self.analizar_colisiones()
            except Exception, e:
                print e
        else:
            self.analizar_colisiones()

        # Dibuja la escena actual y a los actores
        if ignorar_errores:
            try:
                self.escena_actual.actualizar()
            except Exception, e:
                print e
        else:
            self.escena_actual.actualizar()
        
        if ignorar_errores:
            try:
                self.actualizar_actores()
            except Exception, e:
                print e
        else:
            self.actualizar_actores()

    def _realizar_actualizacion_grafica(self):
        self.escena_actual.dibujar(self.ventana)
        self.depurador.inicia_actualizacion_grafica()
        self.dibujar_actores()
        self.depurador.finaliza_actualizacion_grafica()
        pilas.motor.actualizar_pantalla()

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
        if self.pausa_habilitada:
            self.pausa_habilitada = False
            self.pausa.eliminar()
        else:
            self.pausa_habilitada = True
            self.pausa = pilas.actores.Actor("icono_pausa.png")
            self.pausa.z = -100
            
    def actualizar_simuladores(self):
        self.tweener.update(16)
        self.tasks.update(16/1000.0)
        self.fisica.actualizar()

    def actualizar_actores(self):
        for actor in pilas.actores.todos:
            actor.actualizar()
            actor.actualizar_comportamientos()
            actor.actualizar_habilidades()

    def dibujar_actores(self):
        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        
        for actor in pilas.actores.todos:
            actor.dibujar(self.ventana)
            self.depurador.dibuja_actor(actor)

    def emitir_evento_actualizar(self):
        self.control.actualizar()
        pilas.eventos.actualizar.send("bucle")

    def analizar_colisiones(self):
        pilas.colisiones.verificar_colisiones()
