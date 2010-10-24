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
        self.definir_modo_ejecucion(ModoEjecucionNormal(self))
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
        self.ventana.Close()
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


class ModoEjecucion:

    def __init__(self, mundo):
        self.mundo = mundo


class ModoEjecucionNormal(ModoEjecucion):

    def esperar(self):
        time.sleep(0.01)

    def actualizar_simuladores(self):
        self.mundo.tweener.update(16)
        self.mundo.tasks.update(16)

    def actualizar_actores(self):
        for actor in actores.todos:
            actor.actualizar()

    def dibujar_actores(self):
        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        for actor in actores.todos:
            actor.dibujar(self.mundo.ventana)

    def emitir_evento_actualizar(self):
        self.mundo.control.actualizar()
        eventos.actualizar.send("bucle")

    def salir(self):
        pass

    def procesar_evento_teclado(self, event):
        eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

        if event.Key.Code == sf.Key.P:
            self.mundo.definir_modo_ejecucion(ModoEjecucionPausado(self.mundo))
        elif event.Key.Code == sf.Key.F12:
            self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracion(self.mundo))

    def analizar_colisiones(self):
        pilas.colisiones.verificar_colisiones()

class ModoEjecucionPausado(ModoEjecucionNormal):

    def __init__(self, m):
        ModoEjecucionNormal.__init__(self, m)
        self.icono = actores.Actor("icono_pausa.png")
        self.icono.z = -100

    def actualizar_simuladores(self):
        pass

    def actualizar_actores(self):
        pass

    def emitir_evento_actualizar(self):
        pass

    def procesar_evento_teclado(self, event):
        eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

        if event.Key.Code == sf.Key.P:
            self.mundo.definir_modo_ejecucion(ModoEjecucionNormal(self.mundo))
        elif event.Key.Code == sf.Key.F12:
            self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracionPausado(self.mundo))

    def salir(self):
        self.icono.eliminar()

class ModoEjecucionDepuracion(ModoEjecucionNormal):

    def __init__(self, m):
        ModoEjecucionNormal.__init__(self, m)
        self.eje = actores.Ejes()

    def salir(self):
        self.eje.eliminar()

    def dibujar_actores(self):
        ModoEjecucionNormal.dibujar_actores(self)

        color_de_colision = sf.Color(0, 255, 0, 160)
        color_de_punto_de_control = sf.Color(255, 0, 0, 160)
        color_borde = sf.Color(100, 100, 100, 100)

        for actor in actores.todos:
            if actor.radio_de_colision:
                self.pintar_radio_de_colision_del_actor(actor, color_de_colision, color_borde)

            self.pintar_punto_de_control_del_actor(actor, color_de_punto_de_control, color_borde)

            # intenta dibujar el numero de cuadro que usa el actor
            # si es que tiene una animacion asignada.

            try:
                cuadro = actor.animacion.obtener_cuadro()
                self.pintar_numero(cuadro, actor.x, actor.y)
            except AttributeError, e:
                pass


    def pintar_numero(self, numero, x, y):
        numero = pilas.actores.Texto(str(numero))
        numero.x = x
        numero.y = y

        self.mundo.ventana.Draw(numero)
        numero.eliminar()


    def pintar_radio_de_colision_del_actor(self, actor, color, color_borde):
        radio = actor.radio_de_colision *2
        delta = radio / 2
        circulo = sf.Shape.Circle(0, 0, delta, color, 2, color_borde)
        circulo.SetCenter(0, 0)
        circulo.SetPosition(actor.x, -actor.y)
        self.mundo.ventana.Draw(circulo)

    def pintar_punto_de_control_del_actor(self, actor, color, borde):
        circulo = sf.Shape.Circle(0, 0, 3, color)
        circulo.SetPosition(actor.x, -actor.y)
        self.mundo.ventana.Draw(circulo)

    def procesar_evento_teclado(self, event):
        eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

        if event.Key.Code == sf.Key.F12:
            self.mundo.definir_modo_ejecucion(ModoEjecucionNormal(self.mundo))
        if event.Key.Code == sf.Key.P:
            self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracionPausado(self.mundo))

    def salir(self):
        self.eje.eliminar()


        

class ModoEjecucionDepuracionPausado(ModoEjecucionPausado, ModoEjecucionDepuracion):

    def __init__(self, m):
        ModoEjecucionPausado.__init__(self, m)
        ModoEjecucionDepuracion.__init__(self, m)

    def procesar_evento_teclado(self, event):
        if event.Key.Code == sf.Key.F12:
            self.mundo.definir_modo_ejecucion(ModoEjecucionPausado(self.mundo))
        if event.Key.Code == sf.Key.P:
            self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracion(self.mundo))

    def dibujar_actores(self):
        ModoEjecucionDepuracion.dibujar_actores(self)

    def salir(self):
        ModoEjecucionPausado.salir(self)
        ModoEjecucionDepuracion.salir(self)
