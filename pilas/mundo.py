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

        self.camara = camara.Camara(self.ventana)

        self.escena_actual = None

        # Genera los administradores de tareas e interpolaciones.
        self.tweener = pytweener.Tweener()
        self.tasks = tareas.Tareas() 
        self.pausa_habilitada = False
        self.pizarra_depuracion = None
        self.funciones_depuracion = []
        self.salir = False

    def terminar(self):
        self.salir = True

    def ejecutar_bucle_principal(self, ignorar_errores=False):
        "Mantiene en funcionamiento el motor completo."

        fps = pilas.fps.FPS(self.fps, self.economico)

        while not self.salir:

            # Invoca varias veces a la actualizacion si el equipo
            # es lento.
            for x in range(fps.actualizar()):
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
        self.dibujar_actores()
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
        pilas.fisica.fisica.actualizar()

    def actualizar_actores(self):
        for actor in pilas.actores.todos:
            actor.actualizar_comportamientos()
            actor.actualizar_habilidades()
            actor.actualizar()

    def dibujar_actores(self):
        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        if self.pizarra_depuracion:
            self.pizarra_depuracion.limpiar()
            self._imprimir_nombres_de_funciones_depuracion()
            
        for actor in pilas.actores.todos:
            actor.dibujar(self.ventana)
            
            for f in self.funciones_depuracion:
                f(actor)

        if self.pizarra_depuracion:
            self.pizarra_depuracion.actualizar()

    def emitir_evento_actualizar(self):
        self.control.actualizar()
        pilas.eventos.actualizar.send("bucle")

    def salir(self):
        pass

    def analizar_colisiones(self):
        pilas.colisiones.verificar_colisiones()
        
        
        

    def alternar_ver_eje_coordenadas(self):
        habilita = self.alternar_funcion_depuracion(self.imprimir_posicion)
        
        if habilita:
            self.eje_de_coordenadas = pilas.actores.Ejes()
        else:
            self.eje_de_coordenadas.eliminar()
            del(self.eje_de_coordenadas)
        
        
    def alternar_puntos_de_control(self):
        self.alternar_funcion_depuracion(self.imprimir_puntos_de_control)
            
    def alternar_areas(self):
        self.alternar_funcion_depuracion(self.imprimir_area)
            
    def alternar_radios_de_colision(self):
        self.alternar_funcion_depuracion(self.imprimir_radio_de_colision)
        
    def alternar_funcion_depuracion(self, funcion):
        if funcion in self.funciones_depuracion:
            self.desconectar_funcion_depuracion(funcion)
            return False
        else:
            self.conectar_funcion_depuracion(funcion)
            return True

    def imprimir_puntos_de_control(self, actor):
        self.pizarra_depuracion.pintar_cruz(actor.x, actor.y, 6, pilas.colores.rojo)

    def imprimir_area(self, actor):
        (x, y) = pilas.utils.hacer_coordenada_mundo(actor.izquierda, actor.arriba)
        self.pizarra_depuracion.definir_color(pilas.colores.azul)
        self.pizarra_depuracion.dibujar_rectangulo(x, y, actor.ancho, actor.alto, False)

    def imprimir_radio_de_colision(self, actor):
        self.pizarra_depuracion.definir_color(pilas.colores.verde)
        self.pizarra_depuracion.dibujar_circulo(actor.x, actor.y, actor.radio_de_colision, False)

    def imprimir_posicion(self, actor):
        posicion = "(%d, %d)" %(actor.x, actor.y)
        self.pizarra_depuracion.definir_color(pilas.colores.violeta)
        (x, y) = pilas.utils.hacer_coordenada_mundo(actor.x, actor.y)
        self.pizarra_depuracion.escribir(posicion, x + 20, y + 20, tamano=14)

    def desconectar_funcion_depuracion(self, funcion):
        self.funciones_depuracion.remove(funcion)
        if not self.funciones_depuracion:
            self.pizarra_depuracion.eliminar()
            self.pizarra_depuracion = None

    def conectar_funcion_depuracion(self, funcion):            
        self.funciones_depuracion.append(funcion)
    
        if not self.pizarra_depuracion:
            self.pizarra_depuracion = pilas.actores.Pizarra()

    def _imprimir_nombres_de_funciones_depuracion(self):
        dy = 20
        for funcion in self.funciones_depuracion:
            self.pizarra_depuracion.escribir(funcion.__name__.replace('_', ' '), 10, dy, tamano=14)
            dy += 20