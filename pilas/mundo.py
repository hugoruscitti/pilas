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

import actores
import ventana
import control
import camara
import escenas
import utils
import eventos
import tareas
import pytweener


class Mundo:
    """Representa un objeto unico que mantiene en funcionamiento al motor.

    Mundo tiene como responsabilidad iniciar los componentes del
    motor y mantener el bucle de juego.

    Este objeto tiene modos de ejecución que varían segun los objetos
    estado que se le vinculen, por ejemplo "ModoDepuracion", "ModoNormal" etc...
    """

    def __init__(self):
        self.ventana = ventana.iniciar()
        self.control = control.Control(self.ventana.GetInput())

        # todo: llevar a ventana.iniciar
        utils.hacer_flotante_la_ventana()
        utils.centrar_la_ventana(self.ventana)

        self.camara = camara.Camara(self.ventana)

        self.escena_actual = None

        # Genera los administradores de tareas e interpolaciones.
        self.tweener = pytweener.Tweener()
        self.tasks = tareas.Tareas() 

    def ejecutar_bucle_principal(self):
        "Mantiene en funcionamiento el motor completo."

        event = sf.Event()
        clock = sf.Clock()

        while True:

            # Mantiene el control de tiempo y lo reporta al sistema
            # de interpolaciones y tareas.
            time.sleep(0.01)
            self.tweener.update(16)
            self.tasks.update(self.ventana.GetFrameTime())

            # Emite el aviso de actualizacion a los receptores.
            self.control.actualizar()
            eventos.actualizar.send("bucle", input=self.ventana.GetInput())

            # Procesa todos los eventos.
            self.procesar_y_emitir_eventos(event)

            # Dibuja la escena actual y a los actores
            self.escena_actual.actualizar()
            self.escena_actual.dibujar(self.ventana)

            for actor in actores.todos:
                actor.actualizar()

            # Separo el dibujado de los actores porque la lista puede cambiar
            # dutante la actualizacion de actores (por ejemplo si uno se elimina).
            for actor in actores.todos:
                actor.dibujar(self.ventana)

            # Muestra los cambios en pantalla.
            self.ventana.Display()

    def procesar_y_emitir_eventos(self, event):
        "Procesa todos los eventos que la biblioteca SFML pone en una cola."

        while self.ventana.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

                if event.Key.Code == sf.Key.Q:
                    self.ventana.Close()
                    sys.exit(0)
                elif event.Key.Code == sf.Key.F12:
                    ventana.alternar_modo_depuracion()

            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal
                x, y = self.ventana.ConvertCoords(event.MouseMove.X, event.MouseMove.Y)
                eventos.mueve_mouse.send("ejecutar", x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonPressed:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonReleased:
                x, y = self.ventana.ConvertCoords(event.MouseButton.X, event.MouseMove.Y)
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)


    def definir_escena(self, escena_nueva):
        "Cambia la escena que se muestra en pantalla"

        if self.escena_actual:
            eliminar_actores = True
        else:
            eliminar_actores = False

        self.escena_actual = escena_nueva

        if eliminar_actores:
            actores.eliminar_a_todos()

    def agregar_tarea(self, time_out, function, *params): 
        self.tasks.agregar(time_out, function, params)
