# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


"""
Pilas engine - Un motor para realizar videojuegos.
==================================================

Este es el módulo principal de pilas. Desde aquí
puedes acceder a toda la funcionalidad del motor.

"""

import os
import sys
import time

from PySFML import sf

import actores
import imagenes
import sonidos
import tareas
import pytweener
import utils
import interpolaciones
import dispatch
import eventos
import habilidades
import ventana
import comportamientos
import escenas
from control import Control
from camara import Camara
import copy


tweener = pytweener.Tweener()

app = 1
event = 1
clock = 1
control = 1
camara = 1
escena = 0

path = os.path.dirname(os.path.abspath(__file__))
tasks = tareas.Tareas() 
 
def agregar_tarea(time_out, function, *params): 
    tasks.agregar(time_out, function, params)


def iniciar(*k, **kv):
    global app
    global control
    global camara

    app = ventana.iniciar()
    control = Control(app.GetInput())
    utils.hacer_flotante_la_ventana()
    utils.centrar_la_ventana(app)
    camara = Camara(app)
    escenas.Normal()


def ejecutar():
    "Pone en funcionamiento el ejecutar principal."
    global app

    if app == 1:
        print "Cuidado, no has llamado a pilas.iniciar(). Asi que se ejecutara sola..."
        iniciar()

    event = sf.Event()
    clock = sf.Clock()

    while True:
        time.sleep(0.01)

        tweener.update(16)
        tasks.update(app.GetFrameTime())

        # Emite el aviso de actualizacion a los receptores.
        control.actualizar()
        eventos.actualizar.send("bucle", input=app.GetInput())

        # Procesa todos los eventos.
        while app.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                eventos.pulsa_tecla.send("ejecutar", code=event.Key.Code)

                if event.Key.Code == sf.Key.Q:
                    app.Close()
                    sys.exit(0)
                elif event.Key.Code == sf.Key.F12:
                    ventana.alternar_modo_depuracion()
                        
            elif event.Type == sf.Event.MouseMoved:
                # Notifica el movimiento del mouse con una señal
                x, y = app.ConvertCoords(event.MouseMove.X, event.MouseMove.Y)
                eventos.mueve_mouse.send("ejecutar", x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonPressed:
                x, y = app.ConvertCoords(event.MouseButton.X, event.MouseButton.Y)
                eventos.click_de_mouse.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseButtonReleased:
                x, y = app.ConvertCoords(event.MouseButton.X, event.MouseMove.Y)
                eventos.termina_click.send("ejecutar", button=event.MouseButton.Button, x=x, y=-y)
            elif event.Type == sf.Event.MouseWheelMoved:
                eventos.mueve_rueda.send("ejecutar", delta=event.MouseWheel.Delta)

        # Dibuja la escena actual y a los actores
        escena.actualizar()
        escena.dibujar(app)

        for actor in actores.todos:
            actor.actualizar()

        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        for actor in actores.todos:
            actor.dibujar(app)

        # Muestra los cambios en pantalla.
        app.Display()


def ejecutar_en_segundo_plano():
    "Ejecuta el ejecutar de pilas en segundo plano."
    import threading

    bg = threading.Thread(target=ejecutar)
    bg.start()


def interpolar(*values, **kv):
    "Retorna un objeto de interlacion que se puede asignar a una propiedad."

    if 'duracion' in kv:
        duration = kv.pop('duracion')
    else:
        duration = 5

    if 'demora' in kv:
        delay = kv.pop('demora')
    else:
        delay = 0

    if 'tipo' in kv:
        tipo = kv.pop('tipo')
    else:
        tipo = 'lineal'

    if tipo == 'lineal':
        clase = interpolaciones.Lineal
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" %(tipo))

    return clase(values, duration, delay)

def ordenar_actores_por_valor_z():
    "Define el orden de impresion en pantalla."
    actores.todos.sort()


def cargar_autocompletado():
    "Carga los modulos de python para autocompletar desde la consola interactiva."
    import rlcompleter
    import readline

    readline.parse_and_bind("tab: complete")

def avisar(mensaje):
    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.izquierda = -320
    texto.abajo = -240

def definir_escena(escena_nueva):
    "Cambia la escena actual y elimina a todos los actores de la pantalla."
    global escena
    eliminar_actores = False

    if escena:
        eliminar_actores = True

    escena = escena_nueva

    if eliminar_actores:
        # Borra todos los actores de la escena.
        a_eliminar = list(actores.todos)

        for x in a_eliminar:
            x.eliminar()


# Detecta si la biblioteca se esta ejecutando
# desde el modo interactivo o desde un script.

# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.

if utils.esta_en_sesion_interactiva():
    cargar_autocompletado()
    ejecutar_en_segundo_plano()
else:
    pass
