# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


"""Pilas engine - Un motor para realizar videojuegos.


Este es el módulo principal de pilas. Desde aquí
puedes acceder a toda la funcionalidad del motor.


"""

import os
import sys
import time

from PySFML import sf

import actores
import imagen
import sonidos
import tareas
import pytweener
import utils
import interpolaciones
import dispatch
import eventos
import habilidades
import ventana


tweener = pytweener.Tweener()

app = 1
event = 1
clock = 1

path = os.path.dirname(os.path.abspath(__file__))
tasks = tareas.Tareas() 
 
def agregar_tarea(time_out, function, *params): 
    tasks.agregar(time_out, function, params)


def iniciar(*k, **kv):
    global app

    app = ventana.iniciar()
    utils.hacer_flotante_la_ventana()
    utils.centrar_la_ventana(app)


def ejecutar():
    "Pone en funcionamiento el ejecutar principal."
    global app

    if app == 1:
        print "Cuidado, no has llamado a pilas.iniciar(). Asi que se ejecutara sola..."
        iniciar()

    event = sf.Event()
    clock = sf.Clock()
    bg_color = sf.Color(200, 200, 200)

    while True:
        time.sleep(0.01)

        tweener.update(16)
        tasks.update(app.GetFrameTime())
        app.Clear(bg_color)

        # Procesa todos los eventos.
        while app.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

                if event.Key.Code == sf.Key.Escape:
                    app.Close()
                    sys.exit(0)
            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal
                eventos.mueve_mouse.send("ejecutar", x=event.MouseMove.X, y=event.MouseMove.Y)
            elif event.Type == sf.Event.MouseButtonPressed:
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=event.MouseButton.X, y=event.MouseButton.Y)
            elif event.Type == sf.Event.MouseButtonReleased:
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=event.MouseButton.X, y=event.MouseButton.Y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)

        for actor in actores.todos:
            actor.update()
            app.Draw(actor)

        app.Display()


def ejecutar_en_segundo_plano():
    "Ejecuta el ejecutar de pilas en segundo plano."
    import threading

    bg = threading.Thread(target=ejecutar)
    bg.start()


def interpolar(*values, **kv):
    "Retorna un objeto de interlacion que se puede asignar a una propiedad."

    if 'duration' in kv:
        duration = kv.pop('duration')
    else:
        duration = 5

    if 'delay' in kv:
        delay = kv.pop('delay')
    else:
        delay = 0

    return interpolaciones.Lineal(values, duration, delay)

def cargar_autocompletado():
    "Carga los modulos de python para autocompletar desde la consola interactiva."
    import rlcompleter
    import readline

    readline.parse_and_bind("tab: complete")


# Detecta si la biblioteca se esta ejecutando
# desde el modo interactivo o desde un script.

# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.

if utils.esta_en_sesion_interactiva():
    cargar_autocompletado()
    ejecutar_en_segundo_plano()
    print "Esta en consola interactiva"
else:
    pass

print 'ejecutando normalmente.'
#app = ventana.iniciar()
#utils.hacer_flotante_la_ventana()
